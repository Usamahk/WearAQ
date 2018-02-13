#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 15:42:46 2018

@author: Usamahk
"""

import requests
import pandas as pd
import os
import json

## Assets from Organicity

request1 = requests.get("https://discovery.organicity.eu/v0/assets/geo/search?city=Towerhamlets&type=urn:oc:entityType:iotdevice")
request2 = requests.get("http://discovery.organicity.eu/v0/assets/urn:oc:entity:london:aqn:TH4")
request3 = requests.get("http://discovery.organicity.eu/v0/assets/urn:oc:entity:london:districtProfile:uk.gov.london:E09000030")

## All Assests for tower hamlets

url3 = "https://discovery.organicity.eu/v0/assets/geo/search?lat=51.5203&lon=0.0293&radius=0&km=true&service=aqn"

url = "http://discovery.organicity.eu/v0/assets/geo/search?lat=51.5203&lon=0.0293&radius=1000"

r = requests.get(url)

data = r.json()

## AQ data 

num_sensors = len(data[1]["features"])

df = []

for i in range(num_sensors):
    lon = data[1]["features"][i]["geometry"]["coordinates"][0]
    lat = data[1]["features"][i]["geometry"]["coordinates"][1]
    ID = data[1]["features"][i]["properties"]["id"]
    df.append({'Lon':lon, 'Lat':lat, 'ID':ID})

df = pd.DataFrame(df)

## Traffic data

num_sensors2 = len(data[0]["features"])

df2 = []

for i in range(num_sensors2):
    lon = data[0]['features'][i]['geometry']['coordinates'][0]
    lat = data[0]['features'][i]['geometry']['coordinates'][1]
    ID = data[0]['features'][i]['properties']['id']
    df2.append({'Lon':lon, 'Lat':lat, 'ID':ID})
    
df2 = pd.DataFrame(df2)


## df contains list of all sensors in London - including Tower Hamlets
## Plot on map

import folium

map_osm = folium.Map(location = [51.5203,0.0293])
df.apply(lambda row:folium.CircleMarker(location=[row["Lat"], row["Lon"]])
                                             .add_to(map_osm), axis=1)

map_osm.save('/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/map.html')

map_osm = folium.Map(location = [51.5203,0.0293])
df2.apply(lambda row:folium.CircleMarker(location=[row["Lat"], row["Lon"]])
                                             .add_to(map_osm), axis=1)

map_osm.save('/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/map_traffic.html')

## Pull the data from Organicity, each sensor

request2 = requests.get("http://discovery.organicity.eu/v0/assets/urn:oc:entity:london:aqn:TH4")
request3 = requests.get("http://discovery.organicity.eu/v0/assets/urn:oc:entity:london:aqn:TH2")
request4 = requests.get("http://discovery.organicity.eu/v0/assets/urn:oc:entity:london:aqn:TH5")
request5 = requests.get("http://discovery.organicity.eu/v0/assets/urn:oc:entity:london:aqn:TH6")

data_2 = request2.json()

names = data_2["data"]["attributes"]["data"]
names.keys()

key_vars=[]

for key in names.keys(): 
    key_vars.append({"key":key})

key_vars.sort()

key_vars = pd.DataFrame(key_vars)

dPM25 = key_vars.iloc[4,0]
dPM10 = key_vars.iloc[6,0]
dNO =key_vars.iloc[7,0]

### Assets from Thingful

lat = 51.5203
lon = 0.0293

url2 = "https://datapipes.thingful.net/api/run/4e9ce2e7-50b9-4fdb-a491-ff4d6da72700"

## payload = open("request.json")

headers = {"Authorization": "2f67bce7-4454-4a6d-a44d-245a68a8d2b9"}
r = requests.get("https://datapipes.thingful.net/api/run/4e9ce2e7-50b9-4fdb-a491-ff4d6da72700", params = headers)

url = "https://datapipes.thingful.net/api/run/4e9ce2e7-50b9-4fdb-a491-ff4d6da72700"
headers = {'Authorization': 'Bearer 2f67bce7-4454-4a6d-a44d-245a68a8d2b9'}
r = requests.post(url, headers=headers)

thing_data = r.json()

os.path.expanduser(path)

