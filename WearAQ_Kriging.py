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

# New Locations - Teviot Center - 51.492642, -0.007476

loc_lon = -0.007476
loc_lat = 51.492642

location = np.array([loc_lon, loc_lat])



X_init = np.array([[ -0.008356,  51.515017],
       [ -0.042199,  51.522501],
       [ -0.019934,  51.510117],
       [ -0.033470,  51.540364],
       [ -0.013047,  51.488903],
       [  0.014595,  51.514581],
       [ -0.002081,  51.537683]])

# For the addition of the City of London sensor
#X_init = np.array([[ -0.008356,  51.515017],
#       [ -0.042199,  51.522501],
#       [ -0.019934,  51.510117],
#       [ -0.033470,  51.540364],
#       [ -0.013047,  51.488903],
#       [  0.014595,  51.514581],
#       [ -0.002081,  51.537683],
#       [ -0.077670,  51.513533]])

# =============================================================================
# Add dummy inputs
# =============================================================================

offset_lon1 = -0.00003
offset_lon2 =  0.00003

offset_lat1 = -0.0001
offset_lat2 = -0.0001

X=X_init
y = np.array(data_all['NO']) # saved in env - from WearAQ_LAQN_data
#y = np.append(y, 38.8) - City of London sensor

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
# 51.494148, -0.008185
# 51.494416, -0.005447
# 51.490444, -0.008367
# 51.490532, -0.003583
#
#corner 1 - 51.509133, -0.006260
#corner 2 - 51.511024, -0.000543
#corner 3 - 51.511431, -0.006752

X1 = [ -0.006260, 51.509133]
X2 = [ -0.000543, 51.511024]
X3 = [ -0.006752, 51.511431]


ypred1 = k.predict(X1)
ypred2 = k.predict(X2)
ypred3 = k.predict(X3)


X_new = np.array([X1,X2,X3])

y_new = np.array([ypred1,ypred2,ypred3])

# =============================================================================
# Second pass through model
# =============================================================================

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

# =============================================================================
# Predictions for locations
# Run this section to get the output of the model to compare and contrast
# =============================================================================

X=X_init
y = np.array(data_all['NO2']) # saved in env - from WearAQ_LAQN_data

for i in range(len(X_init)):
    lon1 = X_init[i,0] + offset_lon1
    lon2 = X_init[i,0] + offset_lon2
    lat1 = X_init[i,1] + offset_lat1
    lat2 = X_init[i,1] + offset_lat2
    
    loc1 = np.array([lon1,lat1])
    loc2 = np.array([lon2,lat2])
    
    X = np.append(X,[loc1,loc2], axis=0)
    y = np.append(y,[y[i],y[i]])


# Run kriging
    
optimizer = 'ga'

print('Setting up the Kriging Model')
k = kriging(X, y)

k.train(optimizer = optimizer)
k.plot()

# Locations - set this according to the locations you wish to output.

X1 = [51.513165, -0.071385]
X2 = [51.512873, -0.072538]
X3 = [51.511493, -0.072265]
X4 = [51.511957, -0.069203]
X5 = [51.512866, -0.068837]
X6 = [51.513313, -0.070054]
X7 = [51.513576, -0.071512]
X8 = [51.512856, -0.071320]

perm = [1,0]

ypred1 = k.predict([X1[i] for i in perm ])
ypred2 = k.predict([X2[i] for i in perm ])
ypred3 = k.predict([X3[i] for i in perm ])
ypred4 = k.predict([X4[i] for i in perm ])
ypred5 = k.predict([X5[i] for i in perm ])
ypred6 = k.predict([X6[i] for i in perm ])
ypred7 = k.predict([X7[i] for i in perm ])
ypred8 = k.predict([X8[i] for i in perm ])

ypred = [ypred1,ypred2,ypred3,ypred4,ypred5,ypred6,ypred7,ypred8]

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




