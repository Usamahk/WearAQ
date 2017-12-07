#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 23:09:42 2017

@author: Usamahk
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

os.chdir("/Users/Usamahk/Admin/Work/Thingful/WearAQ 2.0")

"Read a data frame in to python

nba = pd.read_csv("nba_2013.csv")

"To see the dimensions of the data frame and see the first few rows

nba.shape
nba.head(10)

"find the mean of the all the values

nba.mean()

"plot a pairwise graph
sns.set_style("dark")
sns.pairplot(nba[["ast","fg","trb"]])

plt.show()