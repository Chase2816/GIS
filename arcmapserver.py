# coding:utf-8

import json
from wsgiref.simple_server import make_server

import arcpy, os, time
import requests, json
import shutil


def PublishAll(folder, name, con, serviceFolder):
    print "检查文件夹路径……"
    if os.path.isdir(folder) == False:
        print "输入的文件夹路径无效！"
        return ["error: 输入的文件夹路径无效！"]

    print "遍历文件夹……"
    files = os.listdir(folder)
    for f in files:
        if f.endswith(".mxd"):
            mxdPath = os.path.join(folder, f)
            print "publishing: " + f
            PublishMxd(f, mxdPath, name, con, serviceFolder)
        else:
            continue


# 将mxd文档发布为服务：1.将mxd转为msd；2.分析msd；3.发布msd
def PublishMxd(mxdName, mxdPath, name, con, serviceFolder):
    # 检查mxd文件是否存在
    print "检查文件路径……"
    if os.path.exists(mxdPath) == False:
        print "指定路径的mxd文档不存在！"
        return ["error: 指定路径的mxd文档不存在！"]

    # 打开mxd文档
    try:
        print "正在打开mxd文档……"
        mxd = arcpy.mapping.MapDocument(mxdPath)
    except Exception, e:
        print "open mxd error: ", e
        return ["open mxd error ！"]
    else:
        print "mxd文档打开成功……"

    # 获取默认的数据框
    # 构造sddraft文档名称
    sddraft = mxdPath.replace(".mxd", ".sddraft")
    service = mxdName.replace(".mxd", "")
    sd = mxdPath.replace(".mxd", ".sd")
    copy_data_to_server = True
    # 将mxd文档转换为sddraft文档……"
    arcpy.mapping.CreateMapSDDraft(mxd, sddraft, service, 'ARCGIS_SERVER', con, copy_data_to_server, serviceFolder)
    print arcpy.GetMessages()
    analysis = arcpy.mapping.AnalyzeForSD(sddraft)
    print arcpy.GetMessages()

    print "The following information was returned during analysis of the MXD:"
    for key in ('messages', 'warnings', 'errors'):
        print '----' + key.upper() + '---'
        vars = analysis[key]
        for ((message, code), layerlist) in vars.iteritems():
            print '    ', message, ' (CODE %i)' % code
            print '       applies to:',
            for layer in layerlist:
                print layer.name,
            print "smwy......"

    if analysis['errors'] == {}:
        arcpy.StageService_server(sddraft, sd)
        # 函数说明：https://desktop.arcgis.com/zh-cn/arcmap/10.3/tools/server-toolbox/upload-service-definition.htm
        # arcpy.UploadServiceDefinition_server(sd, con)
        arcpy.UploadServiceDefinition_server(sd, con, name)
        print "Service successfully published"
    else:
        print "Service could not be published because errors were found during analysis."
        return ["error ：Service could not be published because errors were found during analysis."]

    print arcpy.GetMessages()


# demoMXDPath：包含mxd文档名称
# folder：包含新建的mxd文档以及tiff文件的文件夹路径
def createMxdDocument(demoMXDPath, folder, serviceDir):
    if os.path.exists(demoMXDPath) == False:
        print "mxd document it's not exist!"
        return ["error : mxd document it's not exist!"]
    else:
        try:
            print "opening mxd document……"
            mxd = arcpy.mapping.MapDocument(demoMXDPath)
            print "repair layer source"
            if os.path.isdir(folder) == False:
                print "invalid document path!"
                return ["error : invalid document path!"]
            print "reading layer document one by one......"
            files = os.listdir(folder)
            i = 0
            layerName = ""
            for f in files:
                if f.endswith(".tif"):
                    if layerName == "":
                        name1 = f.replace("nasa-worldview-", "")
                        layerName = name1[0:9]
                    if i > 3:
                        continue
                    if f.index(layerName) >= 0:
                        print folder
                        # 构建金字塔处理tif
                        # tifflist = arcpy.ListRasters("", "TIF")
                        # for tiff in tifflist:
                        #     arcpy.BuildPyramids_management(tiff)

                        # arcpy.env.pyramid = "PYRAMIDS -1 BILINEAR DEFAULT"
                        # arcpy.BuildPyramids_management(os.path.join(folder,f))
                        arcpy.BuildPyramids_management(
                            os.path.join(folder, f), "-1", "NONE", "BILINEAR", "DEFAULT")
                        # os.path.join(folder,f), "-1", "NONE",
                        # "BILINEAR", "JPEG", "100", "SKIP_EXISTING")

                        print layerName + ";" + f
                        # 获取图层
                        # df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
                        print mxd
                        # df = arcpy.mapping.ListDataFrames(mxd, "Layers")
                        df = arcpy.mapping.ListDataFrames(mxd)[0]
                        print df
                        print "3-" * 10

                        print arcpy.mapping.ListLayers(mxd, "", df)[i].name
                        print "@" * 20
                        # 对图层进行修改
                        lyr = arcpy.mapping.ListLayers(mxd, "", df)[i]
                        # 设置数据源
                        lyr.replaceDataSource(folder, "RASTER_WORKSPACE", f)
                        lyr.name = f.replace(".tif", "")
                        i = i + 1
                else:
                    continue

            mxdName = time.strftime("%Y_%m_%d", time.localtime()) + "_1_" + files[0].split(".")[
                0] + ".mxd"  # 2015_11_24样式文件名
            newMXD = folder + "\\" + mxdName
            mxd.saveACopy(newMXD)
            del mxd

        except Exception, e:
            print "open mxd error: ", e
            return ["open mxd error ！"]


def Permission_handle(folderPath, service_name, Map_Service="Map Service"):
    """
    servicr_name:服务名
    Map_Service:Scene Service or Map Service
    """
    # folderPath = r"E:\pycharm_project\tfservingconvert\gis\gis\DAtif"
    print len(os.listdir(folderPath))
    folderfiles = os.listdir(folderPath)
    if len(folderfiles) > 1:
        for file in folderfiles:
            flag = file.split(".")[-1]
            print flag
            if flag != "tif":
                os.remove(os.path.join(folderPath, file))

    serviceDir = "https://arcgis.ygwl.com/arcgis"
    # con = r'C:\Users\pc\AppData\Roaming\Esri\Desktop10.5\ArcCatalog\arcgis on arcgis.ygwl.com_6080 (发布者) (2).ags'
    # createMxdDocument(r"E:\pycharm_project\tfservingconvert\gis\gis\dingan.mxd", folderPath, serviceDir)

    con = r'C:\Users\ygwl\AppData\Roaming\Esri\Desktop10.5\ArcCatalog\arcgis on arcgis.ygwl.com_6080 (发布者).ags'
    createMxdDocument(r"C:\ArcGIS_H20T\dingan.mxd", folderPath, serviceDir)

    # PublishAll(folderPath, "https://arcgis.ygwl.com/arcgis", "ygwl")
    # service_name = "C07"
    PublishAll(folderPath, service_name, con, "")
    # print "上传成功！！！服务名：%s" % service_name

    print "=" * 30
    print "获取token........"
    token_url = "https://arcgis.ygwl.com/arcgis/sharing/rest/generateToken"
    token_payload = {"username": "gisgis", "password": "1qazxsw2", "referer": "ygwl", "f": "pjson", "client": "referer",
                     "expiration": "60"}
    token_result = requests.post(token_url, data=token_payload, verify=False)
    print token_result.content.decode('utf-8')
    print json.loads(token_result.content.decode('utf-8'))['token']
    token = json.loads(token_result.content.decode('utf-8'))['token']
    print "获取token成功！！！"

    print "搜索服务名id.........."
    search_url = "https://arcgis.ygwl.com/arcgis/sharing/rest/search"
    # 搜索Map Service
    search_payload = {"q": "title:%s AND type:%s" % (service_name, Map_Service), "token": token, "f": "pjson",
                      "referer": "ygwl"}
    # 搜索Scene Service
    # search_payload = {"q": "title:%s AND type:'Scene Service'" % service_name, "token": token, "f": "pjson",
    #                   "referer": "ygwl"}

    search_result = requests.post(search_url, data=search_payload, verify=False)
    print search_result.content.decode('utf-8')
    id_results = json.loads(search_result.content.decode('utf-8'))['results'][0]['id']
    print "搜索服务名成功！！！"

    print "修改服务查看权限........."
    share_url = "https://arcgis.ygwl.com/arcgis/sharing/rest/content/users/gisgis/shareItems"
    share_payload = {"everyone": "true", "items": id_results,
                     "token": token,
                     "f": "pjson", "referer": "ygwl"}
    share_result = requests.post(share_url, share_payload, verify=False)
    print share_result.content.decode('utf-8')
    print "服务查看权限修改成功！！！"

    service_resturl = "https://arcgis.ygwl.com/arcgis/rest/services/%s/MapServer" % service_name
    # print "服务:%s : url：%s" % (service_name, service_resturl)
    return service_resturl, id_results


# 定义函数，参数是函数的两个参数，都是python本身定义的，默认就行了。
def application(environ, start_response):
    # 定义文件请求的类型和当前请求成功的code
    # start_response('200 OK', [('Content-Type', 'application/json')])
    # environ是当前请求的所有数据，包括Header和URL，body

    # start_response  如下调用就会发送HTTP响应的Header，注意只能调用一次start_response()函数发送Header。
    # start_response  函数两个参数，一是HTTP响应码，一是一组list表示的HTTP Header，每个Header用一个包含两个str的数组表示
    status = '200 OK'
    # response_headers  中添加请求头部 ，解决跨域问题
    response_headers = [('Content-type', 'application/json'),
                        ('Access-Control-Allow-Origin', '*'),
                        ('Access-Control-Allow-Methods', 'POST'),
                        ('Access-Control-Allow-Headers', 'x-requested-with,content-type'),
                        ]  # json
    start_response(status, response_headers)

    # request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0)))
    request_body = environ["wsgi.input"]
    print request_body
    request_body = request_body.read(int(environ.get("CONTENT_LENGTH", 0)))
    request_body = json.loads(request_body)
    print request_body

    name = request_body["name"]
    file = request_body["file"]
    print name
    print "*" * 30 + file

    # file = "//172.20.153.193/upload/" + file
    file = "//172.20.154.83/upload/" + file
    print "*" * 20 + file

    # newfolder = os.path.dirname(os.path.abspath(file)) + "/" + os.path.basename(file).split('.')[0]
    newfolder = "C:/ArcGIS_H20T/" + os.path.basename(file).split('.')[0]
    # newfolder = "E:/pycharm_project/tfservingconvert/gis/protest/arcgis/" + os.path.basename(file).split('.')[0]

    if not os.path.exists(newfolder):
        os.mkdir(newfolder)

    filename = os.path.basename(file)
    dst = os.path.join(newfolder, filename)
    shutil.copyfile(file, dst)

    service_resturl, id_results = Permission_handle(newfolder, name)

    shutil.rmtree(newfolder)

    print service_resturl
    print id_results
    print name

    return [json.dumps({"url": service_resturl, "id": str(id_results), "name": name})]


if __name__ == "__main__":
    port = 6088
    httpd = make_server("0.0.0.0", port, application)
    print "serving http on port {0}...".format(str(port))
    httpd.serve_forever()
