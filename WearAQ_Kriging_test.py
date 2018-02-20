#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import pyKriging
import numpy as np
from pyKriging import kriging
from pyKriging.samplingplan import samplingplan


def calcuatemeanMSE(self, p2s=200, points=None):
#        This function calculates the mean MSE metric of the model by evaluating MSE at a number of points.
#        :param p2s: Points to Sample, the number of points to sample the mean squared error at. Ignored if the points argument is specified
#        :param points: an array of points to sample the model at
#        :return: the mean value of MSE and the standard deviation of the MSE points     
        if points is None:
            points = self.sp.rlh(p2s)
        values = np.zeros(len(points))
        for enu, point in enumerate(points):
            values[enu] = self.predict_var(point)
        return np.mean(values), np.std(values)

# The Kriging model starts by defining a sampling plan

# Next, we define the problem we would like to solve
# y = np.array([225.18199114,168.51785582,58.64423091,56.18785729,96.00000000]

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

# We can choose between a ga and a pso here
optimizer = 'ga'

print('Setting up the Kriging Model')

k = kriging(X, y)
k.train()
k.plot()
print(k.calcuatemeanMSE())

for i in range(10):
    newpoints = k.infill(1, method='error')
    for point in newpoints:
        print('Adding point {}'.format(point))
        k.addPoint(point, y[0])
    k.train(optimizer=optimizer)

print('Now plotting final results...')
k.plot()

print(k.calcuatemeanMSE())


