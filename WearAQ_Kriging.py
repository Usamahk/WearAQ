#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 15:01:49 2018

@author: Usamahk
"""
from __future__ import print_function
import numpy as np
import pandas as pd
from pyKriging import kriging

# =============================================================================
# Set up the locations of the intial sensors from Tower Hamlets and Newham
# =============================================================================

## Locations of the sensors in question

# New location - Tower Hamlets Council - 51.510727, -0.006155
# corner 1 - 51.509133, -0.006260
# corner 2 - 51.511024, -0.000543
# corner 3 - 51.511431, -0.006752

location = np.array([-0.006155,51.510727])

X_init = np.array([[ -0.008356,  51.515017],
       [ -0.042199,  51.522501],
       [ -0.019934,  51.510117],
       [ -0.033470,  51.540364],
       [ -0.013047,  51.488903],
       [  0.014595,  51.514581],
       [ -0.002081,  51.537683]])

# =============================================================================
# Add dummy inputs
# =============================================================================

#offset_lon1 = -0.000028
#offset_lon2 =  0.000382
# Values that were manually picked
#offset_lat1 = -0.000491
#offset_lat2 = -0.000109

offset_lon1 = -0.00003
offset_lon2 =  0.00003

offset_lat1 = -0.0001
offset_lat2 = -0.0001

X=X_init
y = np.array([ 50.6125, 54.2125, 9.95, 13.1, 3.2, 8.8, 19.45])

for i in range(len(X_init)):
    lon1 = X_init[i,0] + offset_lon1
    lon2 = X_init[i,0] + offset_lon2
    lat1 = X_init[i,1] + offset_lat1
    lat2 = X_init[i,1] + offset_lat2
    
#    loc1 = np.array([X_init[i,0],X_init[i,1]])
    loc1 = np.array([lon1,lat1])
    loc2 = np.array([lon2,lat2])
    
    X = np.append(X,[loc1,loc2], axis=0)
    y = np.append(y,[y[i],y[i]])
   

y = np.array(data_all['NO']) # saved in env - from WearAQ_LAQN_data

y = np.array([ 50.6125, 54.2125, 9.95, 13.1, 3.2, 8.8, 19.45])

# =============================================================================
# First pass through model
# =============================================================================

# We can choose between a ga and a pso here

optimizer = 'ga'

print('Setting up the Kriging Model')
k = kriging(X, y)

k.train(optimizer = optimizer)
k.plot()

# Select 2 locations based on corners of zone  

# corner 1 - 51.509133, -0.006260
# corner 2 - 51.511024, -0.000543
# corner 3 - 51.511431, -0.006752

# X1 = [ -0.006260, 51.509133]
X1 = [ -0.003602, 51.509599]
X2 = [ -0.000543, 51.511024]
X3 = [ -0.006752, 51.511431]

# Xa = X[0]

ypred1 = k.predict(X1)
ypred2 = k.predict(X2)
ypred3 = k.predict(X3)

# ya = y[0]

X_new = np.array([X1,X2,X3])

y_new = np.array([ypred1,ypred2,ypred3])

# =============================================================================
# Second pass through model
# =============================================================================

optimizer = 'ga'

print('Setting up the Kriging Model')
k = kriging(X_new, y_new)

k.train(optimizer = optimizer)
k.plot()

new_loc = []

# infill points to improve models accuracy
for i in range(8):
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

# =============================================================================
# ## Results returned from a first pass
# =============================================================================

walk_loc = new_loc

# Workshop 2
#      lat       lon
#  51.510362 -0.006752
#  51.509133 -0.001958
#  51.509668 -0.004848
#  51.509133 -0.004088
#  51.510016 -0.000543
#  51.510702 -0.006752
#  51.509402 -0.000543
#  51.510520 -0.003343
#
# Workshop 1
#walk_loc = np.array([[ -8.35600000e-03,   5.15140558e+01],
#[ -2.41605182e-03,   5.15131937e+01],
#[ -4.29542164e-03,   5.15122197e+01],
#[ -5.76185580e-03,   5.15125515e+01],
#[ -1.07227840e-03,   5.15115740e+01],
#[ -3.35547465e-03,   5.15124322e+01],
#[ -6.50219595e-03,   5.15143960e+01],
#[ -5.02930972e-03,   5.15127430e+01]])
#    
walk_loc = pd.DataFrame(walk_loc)
walk_loc.columns = ['lon','lat']

import folium

# First workshop location - Lon: 0.006186, Lat: 51.514209

map_osm = folium.Map(location = [51.514209,0.006186])
walk_loc.apply(lambda row:folium.CircleMarker(location=[row["lat"], row["lon"]])
                                             .add_to(map_osm), axis=1)

map_osm.save('/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/map_workshop2.html')



