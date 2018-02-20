#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 15:01:49 2018

@author: Usamahk
"""
from __future__ import print_function
__author__ = 'cpaulson'
import pyKriging
import numpy as np
from pyKriging import kriging
from pyKriging.samplingplan import samplingplan

# The Kriging model starts by defining a sampling plan, we use an optimal Latin Hypercube here

X = np.array([[-0.008356,-0.042199,-0.019934,-0.033470,-0.013044],
               [51.515017,51.522501,51.510117,51.540364,51.523325]])

X = X.T

# Next, we define the problem we would like to solve
y = np.array([225.18199114,168.51785582,58.64423091,56.18785729,96.00000000]

############
import numpy as np 
from pyKriging import kriging
X = np.array([[ -0.008356,  51.515017],
       [ -0.042199,  51.522501],
       [ -0.019934,  51.510117],
       [ -0.033470,  51.540364],
       [ -0.013044,  51.523325]])


## Need to normalize the data - maybe on a 1-5 scale or not
y = np.array([4,8,6,6,7])

optimizer = 'ga'

print('Setting up the Kriging Model')

# We can choose between a ga and a pso here
k = kriging(X, y)

k.train()
k.plot()

for i in range(10):
    newpoints = k.infill(1, method='error')
    for point in newpoints:
        print('Adding point {}'.format(point))
        k.addPoint(point, y[0])
    k.train(optimizer=optimizer)

print('Now plotting final results...')
k.plot()

##########


# We can choose between a ga and a pso here
optimizer = 'ga'

# Now that we have our initial data, we can create an instance of a kriging model
print('Setting up the Kriging Model')
k = kriging(X, y, testfunction=testfun, name='simple_ei', testPoints=300)
k.train(optimizer=optimizer)
k.snapshot()


# Add 10 points based on model error reduction
for i in range(10):
    newpoints = k.infill(1, method='error')
    for point in newpoints:
        print('Adding point {}'.format(point))
        k.addPoint(point, testfun(point)[0])
    k.train(optimizer=optimizer)
    k.snapshot()

## Infill ten points based on the expected improvement criterion
#for i in range(5):
#    newpoints = k.infill(1, method='ei')
#    for point in newpoints:
#        print('Adding point {}'.format(point))
#        k.addPoint(point, testfun(point)[0])
#    k.train(optimizer=optimizer)
#    k.snapshot()

# And plot the results
print('Now plotting final results...')
k.plot()
