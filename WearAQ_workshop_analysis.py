#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 10:10:59 2018

@author: Usamahk
"""

import pandas as pd
import numpy as np
import seaborn as sns
import folium
import os
import glob
from pymc.Matplot import plot as mcplot
from matplotlib import pyplot as plt
import matplotlib as mpl
from IPython.core.pylabtools import figsize

import matplotlib.dates as md
import datetime as dt
import time


os.chdir("/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/") # set directory


workshop_1 = pd.read_csv("data/Workshop data/Workshop_1.csv", float_precision = 'round_trip')

map_osm = folium.Map(location = [51.510727, -0.006155])
workshop_1.apply(lambda row:folium.CircleMarker(location=[row["lat"], row["lon"]])
                                             .add_to(map_osm), axis=1)

map_osm.save('data/Workshop data/map_w1.html')

w1_clean = pd.read_csv("Workshop data/Workshop 1 - Perceptions - FINAL - Clean.csv",float_precision = 'high')
w1 = pd.DataFrame(w1_clean)

with pd.option_context('display.precision',10): # check precision
    print(w1)

"""Locations

1 51.509841, -0.004725
2 51.510383, -0.003696
3 51.511037, -0.002661
4 51.511411, -0.003664
5 51.510954, -0.004286
6 51.510426, -0.005086
"""

w1_loc = np.array([[ 51.509841, -0.0047257],
       [ 51.510383, -0.003696],
       [ 51.511037, -0.002661],
       [ 51.511411, -0.003664],
       [ 51.510954, -0.004286],
       [ 51.510426, -0.005086]])


w1_loc = pd.DataFrame(w1_loc)
w1_loc.columns = ['lat','lon']
w1_loc.index += 1

w1.loc[w1['lon'].isnull(),'lon'] = w1['Location'].map(w1_loc.lon)
w1.loc[w1['lat'].isnull(),'lat'] = w1['Location'].map(w1_loc.lat)

# =============================================================================
# Plot for funsies
# =============================================================================

map_osm = folium.Map(location = [51.510727, -0.006155])
w1_map = w1
w1_map['color']=pd.cut(w1_map['Location'],bins=6,labels=['yellow','green','blue','red','orange','purple'])
w1_map['color']=pd.cut(w1_map['gesture'],bins=5,labels=['#0571b0','#92c5de','#f7f7f7','#f4a582','#ca0020'])


w1.apply(lambda row:folium.CircleMarker(location=[row["lat"], row["lon"]],
                                        color=row['color'],
                                        zoom = 1)
                                             .add_to(map_osm), axis=1)

map_osm.save('/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/map_workshop3.html')

['#fef0d9','#fdcc8a','#fc8d59','#e34a33','#b30000']


# =============================================================================
# Compare to prediction
# =============================================================================

w1_loc['pred'] = np.nan

for i in range(len(w1_loc)):
    X_loc = [w1_loc.iloc[i,1],w1_loc.iloc[i,0]]
    w1_loc.iloc[i,2] = k.predict(X_loc) 

w1_loc = np.array(w1_loc)
 
w1['pred'] = np.nan
w1['loc_pred'] = np.nan

for i in range(len(w1)):
    X_loc = [w1.iloc[i,3],w1.iloc[i,4]]
    w1.iloc[i,5] = k.predict(X_loc)
    w1.iloc[i,7] = w1_loc[(w1.iloc[i,1])-1,2]

w1.to_csv("workshop_1.csv")


# =============================================================================
# Workshop 1
# =============================================================================


os.chdir("/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0")

filenames = os.listdir("data/Workshop Data/Workshop 1")

for i in range(len(filenames)):
    filenames[i] = "data/Workshop Data/Workshop 1/" + filenames[i]

w1 = [pd.read_csv(filename, header = 2) for filename in filenames]

for i in range(len(filenames)):
    w1[i]["Timestamp"] = pd.to_datetime(w1[i].Timestamp)

w1_temp = w1[0]

w1_temp["Timestamp"].min()
w1_temp["Timestamp"].max()

x = np.linspace(0, len(w1_temp), len(w1_temp))

plt.plot(w1[0].Timestamp[::20],((w1[0].Value[::20]-32)*5)/9, label = "Temperature")
plt.plot(w1[1].Timestamp[::20],w1[1].Value[::20], label = "PM 2.5")
plt.plot(w1[2].Timestamp[::20],w1[2].Value[::20], label = "Humidity")
plt.legend(title="Pollutant", loc="upper right")
plt.yscale('linear')
axes = plt.gca()
axes.set_ylim([0,100])
plt.show()

n=20
timestamps=np.linspace(w1_temp["Timestamp"].min(), w1_temp["Timestamp"].max(), 20)
dates=[dt.datetime.fromtimestamp(ts) for ts in timestamps]

n=20
duration = 1000

now=time.mktime(time.localtime())
timestamps=np.linspace(now,now+duration,n)

for i in range(len(w1_temp)):
    w1_temp.Timestamp[i] = time.mktime(w1_temp.Timestamp[i].timetuple())

time.mktime(test.timetuple())

values = w1_temp.Value

plt.subplots_adjust(bottom=0.2)
plt.xticks( rotation=25 )

ax=plt.gca()

xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
plt.plot(dates,values)
plt.show()

x = np.linspace(w1_temp["Timestamp"].min(), w1_temp["Timestamp"].max(), 100)

plt.plot(x)

# =============================================================================
# Workshop 2
# =============================================================================

filenames = os.listdir("data/Workshop Data/Workshop 2")
print(filenames)

for i in range(len(filenames)):
    filenames[i] = "data/Workshop Data/Workshop 2/" + filenames[i]

w2 = [pd.read_csv(filename, header = 2) for filename in filenames]

for i in range(len(filenames)):
    w2[i]["Timestamp"] = pd.to_datetime(w2[i].Timestamp)

w2_percep = pd.read_csv("data/Workshop data/Perception/W2_perception.csv",float_precision = 'high')

w2_percep["timestamp"] = pd.to_datetime(w2_percep.timestamp)







