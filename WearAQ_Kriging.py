#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 15:01:49 2018

@author: Usamahk
"""
from __future__ import print_function
import pyKriging
import numpy as np
from pyKriging import kriging
from pyKriging.samplingplan import samplingplan

############

X = np.array(data_all[['Lon','Lat']])
y = np.array(data_all['AQ Index'])

# We can choose between a ga and a pso here

optimizer = 'ga'

print('Setting up the Kriging Model')
k = kriging(X, y)

k.train()
k.plot()

# infill points to improve models accuracy
for i in range(5):
    newpoints = k.infill(1, method='erro')
    for point in newpoints:
        print('Adding point {}'.format(point))
        k.addPoint(point, y[0])
    k.train(optimizer=optimizer)
    

print('Now plotting final results...')
k.plot() # plot with new points



