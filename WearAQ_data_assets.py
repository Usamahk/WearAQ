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

# =============================================================================
# Tower Hamlets information
# 
# Bounding box:
# North Latitude: 51.544686 South Latitude: 51.484503 East Longitude: 0.009864 West Longitude: -0.080190
# 
# geo_lat = 51.523325
# geo_long = -0.013044
# =============================================================================

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

### Assets from Thingful - Tower Hamlets AQ index

lat = 51.5203
lon = 0.0293

url = "https://thingful-pipes.herokuapp.com/api/run/token"
headers = {'Authorization': 'token'}

resp = requests.get(url, headers=headers)

## save response
data_th = resp.json()

## extract coords

num_sensors = len(data_th)

df_th = []

for i in range(num_sensors):
    lon = data_th[i]["longitude"]
    lat = data_th[i]["latitude"]
    ID = data_th[i]["id"]
    df_th.append({'Lon':lon, 'Lat':lat, 'ID':ID})

df_th = pd.DataFrame(df_th)

### Assets from Thingful - London AQ index

url = "https://thingful-pipes.herokuapp.com/api/run/token"
headers = {'Authorization': 'token'}

resp = requests.get(url, headers=headers)

## save response
data_london = resp.json()

## extract coords

num_sensors = len(data_london)

df_london = []

for i in range(num_sensors):
    lon = data_london[i]["longitude"]
    lat = data_london[i]["latitude"]
    AQ = data_london[i]["id"]
    df_london.append({'Lon':lon, 'Lat':lat, 'ID':ID})

df_london = pd.DataFrame(df_london)

### Plot all sensors

data_all = []

data_all = pd.concat([df,df_th,df_london])

map_osm = folium.Map(location = [51.5203,0.0293])
data_all.apply(lambda row:folium.CircleMarker(location=[row["Lat"], row["Lon"]])
                                             .add_to(map_osm), axis=1)

map_osm.save('/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/map_all.html')

### Traffic data from developer.here.com

### AQ from World Air Quality Index

WAQI_token = "31f916780446867bcaae2261eee8f654a01d07cc"

url2 = "https://api.waqi.info/feed/london/?token=31f916780446867bcaae2261eee8f654a01d07cc"
url3 = "https://api.waqi.info/feed/geo:51.523325;-0.013044/?token=31f916780446867bcaae2261eee8f654a01d07cc"
url4 = "https://api.waqi.info/map/bounds/?latlng=51.484503,-0.080190,51.544686,0.009864&token=31f916780446867bcaae2261eee8f654a01d07cc"

# North Latitude: 51.544686 South Latitude: 51.484503 East Longitude: 0.009864 West Longitude: -0.080190

r2 = requests.get(url2)
r3 = requests.get(url3)
r4 = requests.get(url4)

WAQI_data_2 = r2.json()
WAQI_data_3 = r3.json()
WAQI_data_4 = r4.json()