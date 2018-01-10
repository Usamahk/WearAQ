#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 12:44:54 2018

@author: Usamahk
"""


import pandas as pd
import numpy as np
from scipy.interpolate import Rbf

import matplotlib.pyplot as plt

#Creating some data, with each coordinate and the values stored in separated lists
x = [-0.008356,-0.042199,-0.019934,-0.033470,-0.013044]
y = [51.515017,51.522501,51.510117,51.540364,51.523325]
values = [225.18199114,168.51785582,58.64423091,56.18785729,96.00000000]

#Creating the output grid (100x100, in the example)
# np.linspace(start, stop, n)
ti = np.linspace(-0.05, 0, 5)
XI, YI = np.meshgrid(ti, ti)


#Creating the interpolation function and populating the output matrix value
rbf = Rbf(x, y, values, function='inverse')
ZI = rbf(XI, YI)

# Plotting the result
n = plt.Normalize(0, 100.0)
plt.subplot(1, 1, 1)
plt.pcolor(XI, YI, ZI)
plt.scatter(x, y, 100, values)
plt.title('RBF interpolation')
plt.xlim(-0.1, 0.1)
plt.ylim(-0.1, 0.1)
plt.colorbar()

plt.show() 

example = pd.DataFrame(ZI)
#
#     latitude longitude          NOX
# 34  51.515017 -0.008356 225.18199114
# 341 51.522501 -0.042199 168.51785582
# 342 51.510117 -0.019934  58.64423091
# 343 51.540364 -0.033470  56.18785729
# 5   51.523325 -0.013044  96.00000000