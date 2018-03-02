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


############

X = np.array([[ -0.008356,  51.515017],
       [ -0.042199,  51.522501],
       [ -0.019934,  51.510117],
       [ -0.033470,  51.540364],
       [ -0.013047,  51.488903],
       [  0.014595,  51.514581],
       [ -0.002081,  51.537683]])

y = np.array(data_all['NO'])

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

X1 = [ -0.007241,  51.511574]
X2 = [ 0.000278, 51.513042]

Xa = X[0]

ypred1 = k.predict(X1)
ypred2 = k.predict(X2)

ya = y[0]

X_new = np.array([[ -0.007241,  51.511574],
                  [ 0.000278, 51.513042],
                  [ -0.008356,  51.515017]])

y_new = np.array([ypred1,ypred2,ya])

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

walk_loc = np.array([[ -8.35600000e-03,   5.15140558e+01],
[ -2.41605182e-03,   5.15131937e+01],
[ -4.29542164e-03,   5.15122197e+01],
[ -5.76185580e-03,   5.15125515e+01],
[ -1.07227840e-03,   5.15115740e+01],
[ -3.35547465e-03,   5.15124322e+01],
[ -6.50219595e-03,   5.15143960e+01],
[ -5.02930972e-03,   5.15127430e+01]])
    
walk_loc = pd.DataFrame(walk_loc)
walk_loc.columns = ['lon','lat']

import folium

# First workshop location - Lon: 0.006186, Lat: 51.514209

map_osm = folium.Map(location = [51.514209,0.006186])
walk_loc.apply(lambda row:folium.CircleMarker(location=[row["lat"], row["lon"]])
                                             .add_to(map_osm), axis=1)

map_osm.save('/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/map_workshop1.html')



