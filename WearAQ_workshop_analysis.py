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

workshop_1 = pd.read_csv("data/Workshop data/Workshop_1.csv", float_precision = 'round_trip')
(51.510727, -0.006155)

map_osm = folium.Map(location = [51.510727, -0.006155])
workshop_1.apply(lambda row:folium.CircleMarker(location=[row["lat"], row["lon"]])
                                             .add_to(map_osm), axis=1)

map_osm.save('data/Workshop data/map_w1.html')

w1_clean = pd.read_csv("Workshop 1 - Perceptions - FINAL - Clean.csv",float_precision = 'high')
w1 = pd.DataFrame(w1_clean)

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

map_osm = folium.Map(location = [51.510727, -0.006155])
w1.apply(lambda row:folium.CircleMarker(location=[row["lat"], row["lon"]])
                                             .add_to(map_osm), axis=1)

with pd.option_context('display.precision',10):
    print(w1)

