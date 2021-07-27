# import os
# import arcpy
# # Set environment settings
# arcpy.env.overwriteOutput = True
# # arcpy.env.workspace = "C:/Tilepackages"
# # Loop through the project, find all the maps, and
# #   create a map tile package for each map,
# #   using the same name as the map
# p = arcpy.mp.ArcGISProject(r"E:\pycharm_project\tfservingconvert\gis\Yosemite_updated.aprx")
# m = p.listMaps()[0]
# print(m.listLayers())
# print(m)
# print(m.listLayers()[0])
# arcpy.CreateMapTilePackage_management(m.listLayers()[0], "ONLINE", "{1}.tpk","PNG8", "10")
# # arcpy.CreateVectorTilePackage_management(map, 'Example.vtpk', "ONLINE", "", "INDEXED", 295828763.795777, 564.248588)

import arcpy

import requests
import json

token_url = "https://arcgis.ygwl.com/arcgis/sharing/rest/generateToken"
token_payload = {"username": "gisgis", "password": "1qazxsw2", "referer": "ygwl", "f": "pjson", "client": "referer",
                 "expiration": "60"}
token_result = requests.post(token_url, data=token_payload, verify=False)
print token_result.content.decode('utf-8')
print json.loads(token_result.content.decode('utf-8'))['token']
token = json.loads(token_result.content.decode('utf-8'))['token']

search_url = "https://arcgis.ygwl.com/arcgis/sharing/rest/search"
# search_payload = {"q": "title:%s AND type:'Map Service'" % 'B02',
search_payload = {"q": "title:%s AND type:'Scene Service'" % 'p5',
                  "token": token,
                  "f": "pjson", "referer": "ygwl"}
search_result = requests.post(search_url, data=search_payload, verify=False)
print search_result.content.decode('utf-8')
id_results = json.loads(search_result.content.decode('utf-8'))['results'][0]['id']
print id_results

share_url = "https://arcgis.ygwl.com/arcgis/sharing/rest/content/users/gisgis/shareItems"
share_payload = {"everyone": "true", "items": id_results,
                 "token": token,
                 "f": "pjson", "referer": "ygwl"}
share_result = requests.post(share_url, share_payload, verify=False)
print(share_result.content.decode('utf-8'))
