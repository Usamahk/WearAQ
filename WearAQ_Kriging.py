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

# New Locations - Teviot Center - 51.518800, -0.013402

loc_lon = -0.013402
loc_lat = 51.518800

location = np.array([loc_lon, loc_lat])

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

offset_lon1 = -0.00003
offset_lon2 =  0.00003

offset_lat1 = -0.0001
offset_lat2 = -0.0001

X=X_init
y = np.array(data_all['NO']) # saved in env - from WearAQ_LAQN_data

for i in range(len(X_init)):
    lon1 = X_init[i,0] + offset_lon1
    lon2 = X_init[i,0] + offset_lon2
    lat1 = X_init[i,1] + offset_lat1
    lat2 = X_init[i,1] + offset_lat2
    
    loc1 = np.array([lon1,lat1])
    loc2 = np.array([lon2,lat2])
    
    X = np.append(X,[loc1,loc2], axis=0)
    y = np.append(y,[y[i],y[i]])
   

# =============================================================================
# First pass through model
# =============================================================================

# We can choose between a ga and a pso here

optimizer = 'ga'

print('Setting up the Kriging Model')
k = kriging(X, y)

k.train(optimizer = optimizer)
k.plot()

# new locations
# 51.514691, -0.008711
# 51.513681, -0.014376
# 51.518531, -0.016505
# 51.520406, -0.010749

X1 = [ -0.008711, 51.514691]
X2 = [ -0.014376, 51.513681]
X3 = [ -0.016505, 51.518531]
X4 = [ -0.010749, 51.520406]

ypred1 = k.predict(X1)
ypred2 = k.predict(X2)
ypred3 = k.predict(X3)
ypred4 = k.predict(X4)


X_new = np.array([X1,X2,X3,X4])

y_new = np.array([ypred1,ypred2,ypred3,ypred4])

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

walk_loc = pd.DataFrame(walk_loc)
walk_loc.columns = ['lon','lat']

import folium


map_osm = folium.Map(location = [loc_lat,loc_lon])
walk_loc.apply(lambda row:folium.CircleMarker(location=[row["lon"], row["lat"]])
                                             .add_to(map_osm), axis=1)

map_osm.save('/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/map_workshop4.html')




