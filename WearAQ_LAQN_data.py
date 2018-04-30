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
import timeit

os.chdir("/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/data/LAQN data") # set directory

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
start = timeit.default_timer()

df_1 = blackwall.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_1

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

#df_1_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
#                       df['times'].dt.month,df['times'].dt.weekday]).mean()

df_1_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

stop = timeit.default_timer()
print(stop-start)
# =============================================================================
# Mile End
# =============================================================================
start = timeit.default_timer()

df_2 = mile_end.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_2

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

#df_2_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
#                       df['times'].dt.month,df['times'].dt.weekday]).mean()

df_2_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

stop = timeit.default_timer()
print(stop-start)
# =============================================================================
# Poplar
# =============================================================================
start = timeit.default_timer()

df_3 = poplar.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_3

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

#df_3_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
#                       df['times'].dt.month,df['times'].dt.weekday]).mean()

df_3_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

stop = timeit.default_timer()
print(stop-start)
# =============================================================================
# Victoria Park
# =============================================================================
start = timeit.default_timer()

df_4 = victoria_park.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_4

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

#df_4_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
#                       df['times'].dt.month,df['times'].dt.weekday]).mean()

df_4_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

stop = timeit.default_timer()
print(stop-start)
# =============================================================================
# Millwall Park
# =============================================================================
start = timeit.default_timer()

df_5 = millwall_park.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_5

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

#df_5_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
#                       df['times'].dt.month,df['times'].dt.weekday]).mean()

df_5_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

stop = timeit.default_timer()
print(stop-start)
# =============================================================================
# Wren Close
# =============================================================================
start = timeit.default_timer()

df_6 = wren_close.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_6

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

#df_6_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
#                       df['times'].dt.month,df['times'].dt.weekday]).mean()

df_6_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

stop = timeit.default_timer()
print(stop-start)
# =============================================================================
# Cam Road
# =============================================================================
start = timeit.default_timer()

df_7 = cam_road.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df_7

df['times'] = pd.DatetimeIndex(df.index)
df = df.reset_index(drop=True)

#df_7_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
#                       df['times'].dt.month,df['times'].dt.weekday]).mean()

df_7_avg = df.groupby([df['times'].dt.hour,df['times'].dt.day, 
                       df['times'].dt.month]).mean()

stop = timeit.default_timer()
print(stop-start)

# =============================================================================
# Impute Missing data for each of the sensors
# =============================================================================

df_1_avg.describe() # check data

df_1_avg.isnull().sum() # look at how many missing values there are

# =============================================================================
# Do regression so that we can get PM10 For everything
# =============================================================================

## 4 datasets with PM10 df_1,5,6,7

frames = [blackwall, millwall_park, wren_close, cam_road]

df_learn = pd.concat(frames)

datetime = pd.to_datetime(df_learn["ReadingDateTime"])
# datetime.to_csv('datetime.csv')

datetime = pd.read_csv('datetime.csv')

df_learn['Month'] = datetime.apply(lambda x: x.month)
df_learn['Day'] = datetime.apply(lambda x: x.day)
df_learn['Hour'] = datetime.apply(lambda x: x.hour)



# =============================================================================
# Get data for day in question
# =============================================================================

all = [df_1_avg, df_2_avg, df_3_avg, df_4_avg, df_5_avg, df_6_avg, df_7_avg ]

hour = 10 # Set hour
day = 20 # Set day
month = 4 # Set month
#weekday = 4 # Set weekday

df_all = []

for i in range(7):
    df_all.append(all[i].loc[(hour,day,month)])
    
data_all = pd.DataFrame(df_all)

# =============================================================================
# Tests and analysis of data
# =============================================================================

blackwall_analysis = blackwall.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df_analysis = blackwall_analysis.dropna(how='any')

#blackwell_['times'] = pd.DatetimeIndex(blackwell_.index)
# blackwall_analysis = blackwall_analysis.reset_index(drop=True)

l = sns.pairplot(df_analysis, vars=['NO','NO2','NOX','PM10','PM2.5'])

test = df.groupby([df['times'].dt.hour,df['times'].dt.day,df['times'].dt.month]).mean()

test.loc[(0,5)]


