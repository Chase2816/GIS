import arcpy
from arcgis.gis import GIS


wrks = "F:/无人机数据/1/slpk/"
# outslpk = "测试定安03.slpk"
outslpk = "B01.slpk"
outputslpkpath = wrks + outslpk

osgb_path = r"F:\无人机数据\1\台山terra_osgbs"
# osgb_path = r"F:\无人机数据\1\定安terra_osgbs"
osgb_xml = ""
# 将osgb转成slpk
# 函数说明：https://pro.arcgis.com/zh-cn/pro-app/latest/tool-reference/data-management/create-integrated-mesh-scene-layer-package.htm
# arcpy.CreateIntegratedMeshSceneLayerPackage_management(osgb_path+"/Block", outputslpkpath,
#                                                        osgb_path+"/metadata.xml", "OSGB",
#                                                        arcpy.SpatialReference(4326))

# 将multipatch转成slpk
# arcpy.management.Create3DObjectSceneLayerPackage(r'D:\myarcgispro\pro3d\dataToLayerFile.lyrx', outputslpkpath,
#                                                  arcpy.SpatialReference(4326), None, 'DESKTOP')

print("打包成功")


# 发布三维服务
portalUrl = "https://arcgis.ygwl.com/arcgis"
portalUsername = "gisgis"
portalpassword = "1qazxsw2"

arcpy.GetActivePortalURL()
print(arcpy.GetPortalInfo(portal_URL=arcpy.GetActivePortalURL()))

# 登录 portal
arcpy.SignInToPortal(portalUrl, portalUsername, portalpassword)
print("登录成功")

# 上传
# 场景图层 (.slpk)包，portal用户名，密码，摘要，标签，包的制作者，权限范围
# arcpy.SharePackage_management(outputslpkpath, portalUsername, portalpassword,"测试定安05", "测试定安05","YGWL","EVERYBODY")
# # 发布
# gis = GIS(portalUrl, portalUsername, portalpassword, verify_cert=False)
# slpkitem = gis.content.add({}, data=outputslpkpath, folder='ygwl')
# slpkscenelayer = slpkitem.publish()
# print("slpk publish success")


# 上传并发布图层包
# 函数说明：https://desktop.arcgis.com/zh-cn/arcmap/latest/tools/data-management-toolbox/share-package.htm
arcpy.SharePackage_management(outputslpkpath, portalUsername, portalpassword,
                              "B01", "B01", "abb",
                              "MYGROUPS"
                              , None, "MYORGANIZATION", "TRUE",None)

print("成功上传并发布slpk")
