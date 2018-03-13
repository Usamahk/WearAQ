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
X = np.array([[ -0.008356,  51.515017],
       [ -0.042199,  51.522501],
       [ -0.019934,  51.510117],
       [ -0.033470,  51.540364],
       [ -0.013044,  51.523325]])


## Need to normalize the data - maybe on a 1-5 scale or not
y = np.array([4,8,6,2,7])

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


# =============================================================================
# new testing ground
# 
# =============================================================================

from __future__ import print_function
__author__ = 'cpaulson'
import pyKriging
from pyKriging.krige import kriging
from pyKriging.samplingplan import samplingplan

# The Kriging model starts by defining a sampling plan, we use an optimal Latin Hypercube here
sp = samplingplan(2)
X = sp.optimallhc(15)

# Next, we define the problem we would like to solve
testfun = pyKriging.testfunctions().paulson1
y = testfun(X)

# We can choose between a ga and a pso here
optimizer = 'ga'

# Now that we have our initial data, we can create an instance of a kriging model
print('Setting up the Kriging Model')
k = kriging(X, y, testfunction=testfun, name='simple_ei', testPoints=300)
k.train(optimizer=optimizer)
k.snapshot()
k.plot()

# Add 10 points based on model error reduction
for i in range(1):
    newpoints = k.infill(1, method='error')
    for point in newpoints:
        print('Adding point {}'.format(point))
        k.addPoint(point, testfun(point)[0])
    k.train(optimizer=optimizer)
    k.snapshot()

# Infill ten points based on the expected improvement criterion
for i in range(5):
    newpoints = k.infill(1, method='ei')
    for point in newpoints:
        print('Adding point {}'.format(point))
        k.addPoint(point, testfun(point)[0])
    k.train(optimizer=optimizer)
    k.snapshot()

# And plot the results
print('Now plotting final results...')
k.plot()

# =============================================================================
# new testing ground
# 
# =============================================================================

from __future__ import print_function
__author__ = 'cpaulson'
import pyKriging
from pyKriging.krige import kriging
from pyKriging.samplingplan import samplingplan

# The Kriging model starts by defining a sampling plan, we use an optimal Latin Hypercube here
sp = samplingplan(2)
X = sp.optimallhc(15)

# Next, we define the problem we would like to solve
testfun = pyKriging.testfunctions().branin

# We generate our observed values based on our sampling plan and the test function
y = testfun(X)

print('Setting up the Kriging Model')

# Now that we have our initial data, we can create an instance of a kriging model
k = kriging(X, y, testfunction=testfun, name='simple', testPoints=250)
k.train(optimizer='ga')
k.snapshot()
k.plot()

for i in range(5):
    newpoints = k.infill(1, method='ei')
    for point in newpoints:
        print('Adding point {}'.format(point))
        k.addPoint(point, testfun(point)[0])
    k.train(optimizer=optimizer)
    k.snapshot()

# #And plot the model

print('Now plotting final results...')
k.plot()

# =============================================================================
# MORE TESTING TESTING TESTING
# =============================================================================

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

from pyKriging import kriging
X = np.array([[ -0.008356,  51.515017],
       [ -0.042199,  51.522501],
       [ -0.019934,  51.510117],
       [ -0.033470,  51.540364],
       [ -0.013044,  51.523325]])

#y = np.array([10,8,10,2,10,5,4]) <- this gives a good result for demo    
    

## Need to normalize the data - maybe on a 1-5 scale or not
y = np.array([4,8,6,6,7])

optimizer = 'ga'

print('Setting up the Kriging Model')

# We can choose between a ga and a pso here
k = kriging(X, y, testPoints=100)

k.train()
k.plot()

for i in range(5):
    newpoints = k.infill(1, method='ei')
    for point in newpoints:
        print('Adding point {}'.format(point))
        k.addPoint(point, y[0])
    k.train(optimizer=optimizer)
    k.snapshot()

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












