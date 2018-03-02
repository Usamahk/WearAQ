#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 12:53:16 2018

@author: Usamahk
"""

import pandas as pd
import numpy as np
import seaborn as sns
import folium
import os

os.chdir("/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/data") # set directory

# =============================================================================
# Important sites in and around Tower Hamlets
# =============================================================================

site = ['Blackwell', "Mile End", "Poplar", "Victoria Park", "Millwall Park", "Wren Close", "Cam Road"]
latitude = [51.515017,51.522501,51.510117,51.540364, 51.488903, 51.514581, 51.537683]
longitude = [-0.008356,-0.042199,-0.019934,-0.033470, -0.013047, 0.014595, -0.002081]

locations = pd.DataFrame({"site" :site,
                          "longitude": longitude,
                          "latitude" : latitude
                          })

map_osm = folium.Map(location = [51.5203,0.0293])
locations.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]])
                                             .add_to(map_osm), axis=1)


map_osm.save('map_th.html')

# =============================================================================
# Read in all data - stored locally in folder labelled "data"
# =============================================================================

blackwall = pd.read_csv("Blackwall.csv")
mile_end = pd.read_csv("Mile End Road.csv")
poplar = pd.read_csv("Poplar.csv")
victoria_park = pd.read_csv("Victoria Park.csv")
millwall_park = pd.read_csv("Millwall Park.csv")
wren_close = pd.read_csv("Wren Close.csv")
cam_road = pd.read_csv("Cam Road.csv")

# =============================================================================
# Blackwall
# =============================================================================

df_1 = blackwall.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_1

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

df_1_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

# =============================================================================
# Mile End
# =============================================================================

df_2 = mile_end.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_2

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

df_2_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

# =============================================================================
# Poplar
# =============================================================================

df_3 = poplar.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_3

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

df_3_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

# =============================================================================
# Victoria Park
# =============================================================================

df_4 = victoria_park.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_4

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

df_4_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

# =============================================================================
# Millwall Park
# =============================================================================

df_5 = millwall_park.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_5

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

df_5_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

# =============================================================================
# Wren Close
# =============================================================================

df_6 = wren_close.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_6

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

df_6_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

# =============================================================================
# Cam Road
# =============================================================================

df_7 = cam_road.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_7

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

df_7_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()


# =============================================================================
# Do regression so that we can get PM10 For everything
# =============================================================================

## 4 datasets with PM10 df_1,5,6,7

frames = [blackwall, millwall_park, wren_close, cam_road]

df_learn = pd.concat(frames)

datetime = pd.to_datetime(df_learn["ReadingDateTime"])

df_learn['Month'] = datetime.apply(lambda x: x.month)

# =============================================================================
# Get data for day in question
# =============================================================================

all = [df_1_avg, df_2_avg, df_3_avg, df_4_avg, df_5_avg, df_6_avg, df_7_avg ]

df_all = []

for i in range(7):
    df_all.append(all[i].loc[(12,7,3)])
    
data_all = pd.DataFrame(df_all)



latitude = [51.515017,51.522501,51.510117,51.540364, 51.488903, 51.514581, 51.537683]
longitude = [-0.008356,-0.042199,-0.019934,-0.033470, -0.013047, 0.014595, -0.002081]


blackwell_ = blackwell.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = blackwell_.dropna(how='any')

blackwell_['times'] = pd.DatetimeIndex(blackwell_.index)
blackwell_ = blackwell_.reset_index(drop=True)

l = sns.pairplot(df, vars=['NO','NO2','NOX','O3','PM10','PM2.5'])

test = df.groupby([df['times'].dt.hour,df['times'].dt.day,df['times'].dt.month]).mean()

test.loc[(0,5)]




site = ['Blackwell', "Mile End", "Poplar", "Victoria Park", "Millwall Park", "Wren Close", "Cam Road"]
latitude = [51.515017,51.522501,51.510117,51.540364, 51.488903, 51.514581, 51.537683]
longitude = [-0.008356,-0.042199,-0.019934,-0.033470, -0.013047, 0.014595, -0.002081]

locations = pd.DataFrame({"site" :site,
                          "longitude": longitude,
                          "latitude" : latitude
                          })

map_osm = folium.Map(location = [51.5203,0.0293])
locations.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]])
                                             .add_to(map_osm), axis=1)


map_osm.save('/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/map_th.html')
