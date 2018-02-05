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

url = "http://discovery.organicity.eu/v0/assets/geo/search?lat=51.5203&lon=0.0293&radius=1000"

r = requests.get(url)

data = r.json()

num_sensors = len(data[1]["features"])

for i in range(num_sensors):
    lon = data[1]["features"][i]["geometry"]["coordinates"][0]
    lat = data[1]["features"][i]["geometry"]["coordinates"][1]
    ID = data[1]["features"][i]["properties"]["id"]
    print(lat,lon,ID)


### Assets from Thingful

lat = 51.5203
lon = 0.0293

url2 = "https://datapipes.thingful.net/api/run/4e9ce2e7-50b9-4fdb-a491-ff4d6da72700"
## payload = open("request.json")
headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
r = requests.get("https://datapipes.thingful.net/api/run/4e9ce2e7-50b9-4fdb-a491-ff4d6da72700")

os.path.expanduser(path)
