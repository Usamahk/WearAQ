#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 21:14:51 2017

@author: Usamahk
"""

"""
Start by calling libraries, and setting workspace directory
"""

import os
import numpy as np
import pandas as pd
import folium
import seaborn as sns
import matplotlib.pyplot as plt
import random

os.chdir("/Users/Usamahk/Admin/Work/Umbrellium/Sandbox/WearAQ 2.0")

print(os.listdir())

"""
Rebuilding the code from WearAQ phase 1. Look at some of the analysis at Marner
Primary School
The location of the school is
"""

geo_lat = 51.523325
geo_long = -0.013044

"""
Want to see the current spread of the sensors right now. Manually defining
variables and then will plot them
"""

site = ['Blackwell', "Mile End", "Poplar", "Victoria Park"]
latitude = [51.515017,51.522501,51.510117,51.540364]
longitude = [-0.008356,-0.042199,-0.019934,-0.033470]

locations = pd.DataFrame({"site" :site,
                          "longitude": longitude,
                          "latitude" : latitude
                          })

m = folium.Map(location=[45.5236, -122.6750])
m.save("test_map.html")

"""m2 = folium.Map(location)"""

blackwell = pd.read_csv("Tower Hamlets - Blackwell.csv")
mile_end = pd.read_csv("Tower Hamlets - Mile End.csv")
poplar = pd.read_csv("Tower Hamlets - Poplar.csv")
victoria_park = pd.read_csv("Tower Hamlets - Victoria Park.csv")

"""
change from long to wide format
"""

blackwell = blackwell.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = blackwell.dropna(how='any')

"""
Experimenting with different pairwise plots
"""

l = sns.pairplot(df, vars=['NO','NO2','NOX','O3','PM10','PM2.5'])
g =  sns.pairplot(df.head(500), diag_kind='kde', kind = 'reg', 
                  vars=['NOX','O3','PM2.5'])

h =  sns.pairplot(df.head(500), diag_kind='kde', vars=['NOX','O3','PM2.5'])

plt.show()

"""
Try a machine learning algorithm
"""

df1 = df.head(500)

maxs = df1.max()
mins = df1.min()

from sklearn import preprocessing

df_scaled = preprocessing.scale(df1)

df_s = pd.DataFrame(df_scaled)

col = df.columns
df_s.columns = col

""""Use Kmeans clustering to determine a relative AQ band"""

from sklearn.cluster import KMeans

km = KMeans(n_clusters=5, random_state=1)
new = df_s._get_numeric_data().dropna(axis=1)
km.fit(new)
predict=km.predict(new)

"""Fill dataframe with clusters"""

df_s['Class'] = pd.Series(predict, index=df_s.index)

"""Try with df1"""

km = KMeans(n_clusters=5, random_state=1)
new = df1._get_numeric_data().dropna(axis=1)
km.fit(new)
predict=km.predict(new)

df1['Class'] = pd.Series(predict, index=df1.index)

"""
Now see if we can apply some models to accurately predict aq band from data
"""

X = df1.drop('Class',axis=1)
y = df1.loc[:,'Class'].values

from sklearn.cross_validation import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, 
                                                    random_state = 0)

"""
Transform the data once more - standardize
"""

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

"""
Use a neural network for classification
"""

from sklearn.linear_model import Perceptron

ppn = Perceptron(n_iter=100, eta0=0.1, random_state=0)
ppn.fit(X_train_std, y_train)

"""
Check accuracy of model
"""

y_pred = ppn.predict(X_test_std)
print('Misclassified sample : %d' % (y_test != y_pred).sum())

from sklearn.metrics import accuracy_score
print('Accuracy : %.2f' % accuracy_score(y_test, y_pred))

"""
from sklearn.neural_network import MLPClassifier

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5,2), random_state =1)
clf.fit(df_s, 'NOX')
"""


from __future__ import division
import math

lat = 51.523325
long = -0.013044

radius = 20

"""
Use the Haversine formula
"""

lng_min = long - radius / abs(math.cos(math.radians(lat)) * 69)
lng_max = long + radius / abs(math.cos(math.radians(lat)) * 69)
lat_min = lat - (radius / 69)
lat_max = lat + (radius / 69)

print ('lng (min/max): %f %f' % (lng_min, lng_max))
print ('lat (min/max): %f %f' % (lat_min, lat_max))

dist_lng = lng_max-lng_min
dist_lat = lat_max-lat_min

lats = np.random.rand(3)
longs = np.random.rand(3)

lat_out = (lats*dist_lat)+lat_min
long_out = (longs*dist_lng)+lng_min

import proximityhash

"""
Working on some plotting
"""

import gmplot

gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)

latitudes = 37.428
longitudes = -122.145

gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
gmap.heatmap(heat_lats, heat_lngs)

gmap.draw("mymap.html")

import math

def makeGrid(maxLat, maxLon, minLat, minLon, resX, resY):
	"""
	makeGrid generates a grid of <resX> x <resY> resolution
	mapped on a boundig box described by <maxLat>, <maxLon>, <minLat>, <minLon>
	"""

	# TO VALIDATE!
	# latitude ranages from -90 to +90
	# latitude ranages from -180 to +180

	# the grid array
	grid = []

	# find lat absolute distance
	totolLat = abs(maxLat - minLat)
	
	# find lon absolute distance
	totolLon = abs(maxLon - minLon)

	# divide distances by gurd resolution
	gridBlockWidth = totolLat/resX
	gridBlockHeight = totolLon/resY

	# get grid blocks coordinates
	for i in range(resY):
		for j in range(resX):
			x1 = minLat + (gridBlockWidth * j)
			x2 = minLat + (gridBlockWidth * (j+1))

			y1 = maxLon - (gridBlockHeight * i)
			y2 = maxLon - (gridBlockHeight * (i+1))

			currentBlock = { 'minX': roundTo3DecimalP(x1), 'minY': roundTo3DecimalP(y1), 'maxX': roundTo3DecimalP(x2), 'maxY': roundTo3DecimalP(y2) }

			grid.append(currentBlock)


	return grid

def roundTo3DecimalP(c):

	return math.ceil(c*1000)/1000

