#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 15:01:49 2018

@author: Usamahk
"""
from __future__ import print_function
import numpy as np
from pyKriging import kriging
from pyKriging.samplingplan import samplingplan
from sklearn.preprocessing import normalize

norm1 = y / np.linalg.norm(y)
norm1 = norm1*10
############

X = np.array([[ -0.008356,  51.515017],
       [ -0.042199,  51.522501],
       [ -0.019934,  51.510117],
       [ -0.033470,  51.540364],
       [ -0.013047,  51.488903],
       [  0.014595,  51.514581],
       [ -0.002081,  51.537683]])

y = np.array([10,8,10,2,10,5,4])
#y = np.array([51,35,50,30,50,60,42])
#y = np.array(data_all['NO2'])


# We can choose between a ga and a pso here

optimizer = 'ga'

print('Setting up the Kriging Model')
k = kriging(X, norm1)

k.train(optimizer = optimizer)
k.plot()



# infill points to improve models accuracy
for i in range(3):
    newpoints = k.infill(1, method='error')
    for point in newpoints:
        print('Adding point {}'.format(point))
        k.addPoint(point, y[0])
    k.train(optimizer=optimizer)


print('Now plotting final results...')
k.plot() # plot with new points

# First workshop location - Lon: 0.006186, Lat: 51.514209


