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


os.chdir("/Users/Usamahk/Admin/Work/Thingful/WearAQ 2.0")

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



