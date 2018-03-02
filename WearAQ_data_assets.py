#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 15:42:46 2018

@author: Usamahk
"""

import requests
import pandas as pd
import numpy as np

# =============================================================================
# Tower Hamlets information
# 
# Coordinates making a Bounding box:
# North Latitude: 51.544686 South Latitude: 51.484503 East Longitude: 0.009864 
# West Longitude: -0.080190
# 
# Center of zone:
# geo_lat = 51.523325
# geo_long = -0.013044
# =============================================================================

## Assets from Organicity

## All Assests for tower hamlets

baseurl = "http://discovery.organicity.eu/v0/assets/"
url = "http://discovery.organicity.eu/v0/assets/geo/search?lat=51.5203&lon=0.0293&radius=1000"

r = requests.get(url)

data = r.json()

## Organicity - AQ data 

num_sensors = len(data[1]["features"])

df = []

for i in range(num_sensors):
    lon = data[1]["features"][i]["geometry"]["coordinates"][0]
    lat = data[1]["features"][i]["geometry"]["coordinates"][1]
    ID = data[1]["features"][i]["properties"]["id"]
    df.append({'Lon':lon, 'Lat':lat, 'ID':ID})

df = pd.DataFrame(df)

## Pull the data from Organicity, each AQ sensor

df_val = []

for i in range(num_sensors):
    requesturl = baseurl+df.iloc[i,0]
    
    r = requests.get(requesturl)
    data = r.json()
    
    try:
        PM10 = data["data"]["attributes"]["data"]["chemicalAgentAtmosphericConcentration:airParticlesPM10"]["value"]
    except KeyError:
        PM10 = np.nan
        
    try:
        PM25 = data["data"]["attributes"]["data"]["chemicalAgentAtmosphericConcentration:airParticlesPM25"]["value"]
    except KeyError:
        PM25 = np.nan
    
    try:
        NO = data["data"]["attributes"]["data"]["chemicalAgentAtmosphericConcentration:NO"]["value"]
    except KeyError:
        NO = np.nan
        
    df_val.append({'PM10':PM10, 'PM2.5':PM25, 'NO':NO})
    print(i)

df_val = pd.DataFrame(df_val)
df_val= df_val.apply(pd.to_numeric)

aq_organicity_result = pd.concat([df,df_val], axis = 1)

# =============================================================================
# Get data from thingful
# =============================================================================

### Assets from Thingful - London AQ index

url = "https://thingful-pipes.herokuapp.com/api/run/3042858c-284c-4d8e-b62b-62db014def87"
headers = {'Thingful-Authorization': 'Bearer 2f67bce7-4454-4a6d-a44d-245a68a8d2b9'} # add token

resp = requests.get(url, headers=headers)

## save response
data_london = resp.json()

## extract coords

num_sensors = len(data_london)

df_london = []

for i in range(num_sensors):
    lon = data_london[i]["longitude"]
    lat = data_london[i]["latitude"]
    ID = data_london[i]["id"]
    AQ = data_london[i]["airQualityQuantityKind"]
    df_london.append({'Lon':lon, 'Lat':lat,'AQ Index':AQ, 'ID':ID})

df_london = pd.DataFrame(df_london)

# =============================================================================
# ### Combine all data
# =============================================================================

data_all = []

data_all = pd.concat([df_london,aq_organicity_result]).reset_index(drop=True)

for i in range(8, 32):
    if data_all.iloc[i,5]<15:
        data_all.iloc[i,0] = 1
    else:
        data_all.iloc[i,0] = 2

data_all = data_all.apply(pd.to_numeric, errors = 'coerce')

## Subset Tower Hamlets data

data_th = data_all[(data_all.Lat < 51.544686) & (data_all.Lat >51.484503) & 
         (data_all.Lon > -0.080190) & (data_all.Lon < 0.009864)].reset_index(drop=True)

data_th = data_th.drop_duplicates(subset = 'Lat')

import folium

map_osm = folium.Map(location = [51.5203,0.0293])
data_th.apply(lambda row:folium.CircleMarker(location=[row["Lat"], row["Lon"]])
                                             .add_to(map_osm), axis=1)

map_osm.save('/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/map_all.html')