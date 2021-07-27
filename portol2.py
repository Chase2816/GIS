# import arcpy
# from arcgis.gis import GIS
#
# wrks = "F:/无人机数据/1/slpk/"
# outslpk = "测试定安03.slpk"
# outputslpkpath = wrks + outslpk
#
# # 将osgb转成slpk
# # arcpy.CreateIntegratedMeshSceneLayerPackage_management(r"F:\无人机数据\1\定安terra_osgbs\Block", outputslpkpath,r"F:\无人机数据\1\定安terra_osgbs\metadata.xml", "OSGB",arcpy.SpatialReference(4326))
#
# # 将multipatch转成slpk
# # arcpy.management.Create3DObjectSceneLayerPackage(r'D:\myarcgispro\pro3d\dataToLayerFile.lyrx', outputslpkpath,arcpy.SpatialReference(4326), None, 'DESKTOP')
# print("打包成功")
#
# # 发布三维服务
# portalUrl = "https://arcgis.ygwl.com/arcgis"
# portalUsername = "gisgis"
# portalpassword = "1qazxsw2"
#
# # 返回活动门户的 URL
# arcpy.GetActivePortalURL()
# print(arcpy.GetPortalInfo(portal_URL=arcpy.GetActivePortalURL()))
#
# # 登录 portal
# arcpy.SignInToPortal(portalUrl, portalUsername, portalpassword)
# print("登录成功")
#
# # 场景图层 (.slpk)包，portal用户名，密码，摘要，标签，包的制作者，权限范围
# # arcpy.SharePackage_management(outputslpkpath, portalUsername, portalpassword,"测试定安02", "测试定安02","YGWL","EVERYBODY")
# arcpy.SharePackage_management(outputslpkpath, "gisgis", "1qazxsw2","summary", "test","Credits")
# print("成功上传slpk")
#
# gis = GIS(portalUrl, portalUsername, portalpassword, verify_cert=False)
# slpkitem = gis.content.add({}, data=outputslpkpath, folder='ygwl')
# slpkscenelayer = slpkitem.publish()
# print("slpk publish success")

# -*- coding: utf-8 -*-
import arcpy
import os
import datetime
import arcgis
from arcgis.gis import GIS

wrks = "F:/无人机数据/1/slpk/"
outslpk = "测试定安03.slpk"
outputslpkpath = wrks + outslpk
# 将multipatch转成slpk
# arcpy.management.Create3DObjectSceneLayerPackage(r'D:\myarcgispro\pro3d\dataToLayerFile.lyrx', outputslpkpath,
#                                                  arcpy.SpatialReference(4326), None, 'DESKTOP')
# arcpy.CreateIntegratedMeshSceneLayerPackage_management(r"F:\无人机数据\1\定安terra_osgbs\Block", outputslpkpath,r"F:\无人机数据\1\定安terra_osgbs\metadata.xml", "OSGB",arcpy.SpatialReference(4326))

print("打包成功")

# 发布三维服务
portalUrl = "https://arcgis.ygwl.com/arcgis"
portalUsername = "gisgis"
portalpassword = "1qazxsw2"
# 返回活动门户的 URL
arcpy.GetActivePortalURL()
print(arcpy.GetPortalInfo(portal_URL=arcpy.GetActivePortalURL()))
# 登录 portal
arcpy.SignInToPortal(portalUrl, portalUsername, portalpassword)
# arcpy.SharePackage_management(outputslpkpath, portalUsername, portalpassword,
#                               "summary", "test",
#                               "Credits")
arcpy.SharePackage_management(outputslpkpath, portalUsername, portalpassword,"测试定安02", "测试定安02","YGWL","EVERYBODY")

print("成功上传slpk")
# gis = GIS(portalUrl, portalUsername, portalpassword, verify_cert=False)
# slpkitem = gis.content.add({}, data=outputslpkpath, folder='ygwl')
# slpkscenelayer = slpkitem.publish()
# print("slpk publish success")
