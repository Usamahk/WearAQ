#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 12:48:51 2018

@author: Usamahk
"""

import os
import pandas as pd
import numpy as np
import folium
from pyKriging import kriging

from scipy.spatial import KDTree

# =============================================================================
# Locations
# =============================================================================

os.chdir("/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/data")

# Read airbeam data

w_airbeam = pd.read_csv("WearAQ_workshop_1.xlsx - PM10.csv")
w_airbeam = w_airbeam.drop(['Timestamp'], axis = 1)

# Extract Lon/lat in array

coords = np.array([w_airbeam['geo:lat'],w_airbeam['geo:long']]).T

# Initialize workshop locations

locations = np.array([[-0.004744, 51.509824],
                      [-0.003672, 51.510358],
                      [-0.002685, 51.511079],
                      [-0.003586, 51.511400],
                      [-0.004272, 51.510899],
                      [-0.005056, 51.510445]])

# Find closest readings  to locations

tree = KDTree(coords)

nearest_neighbour = np.empty((0,3), int)

for i in range(len(locations)):
    idx = tree.query([locations[i,0], locations[i,1]], k = 2)
    temp = w_airbeam.iloc[idx[1]]
    temp = np.array(temp.head(1))
    
    nearest_neighbour = np.append(nearest_neighbour, temp, axis = 0).astype(None)

# Compile in array

closest = pd.DataFrame(nearest_neighbour)
closest = closest.rename(columns = {0:'lat',1:'lon', 2:'Value'})

X_init = np.array([closest['lat'],closest['lon']]).T
y = np.array(closest['Value'])

# clean

offset_lon1 = -0.000003
offset_lat1 = -0.000001

X=X_init

for i in range(len(X_init)):
    lon1 = X_init[i,0] + offset_lon1
    
    lat1 = X_init[i,1] + offset_lat1
    
    loc1 = np.array([lon1,lat1])
    
    X = np.append(X,[loc1], axis=0)
    y = np.append(y,[y[i]])
   

# Run through kriging

optimizer = 'ga'

print('Setting up the Kriging Model')
k = kriging(X, y)

k.train(optimizer = optimizer)
k.plot()

new_loc = []

# infill points to improve models accuracy

for i in range(3):
    newpoints = k.infill(1, method='error')
    for point in newpoints:
        print('Adding point {}'.format(point))
        k.addPoint(point, y[0])
    k.train(optimizer=optimizer)
    new_loc.append({'lon':point[0],'lat':point[1]})

new_loc = pd.DataFrame(new_loc)
#########

print('Now plotting final results...')
k.plot() # plot with new points




#plot to check

closest = pd.DataFrame(nearest_neighbour)
closest = closest.rename(columns = {0:'lat',1:'lon', 2:'Value'})

map_osm = folium.Map(location = [51.509824,-0.004744])
closest.apply(lambda row:folium.CircleMarker(location=[row['lon'], row['lat']])
                                             .add_to(map_osm), axis=1)
map_osm.save('w1_air.html')