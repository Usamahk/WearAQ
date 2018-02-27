#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 17:13:03 2018

@author: Usamahk
"""

import os
import numpy as np
import pandas as pd
import folium
import seaborn as sns
import matplotlib.pyplot as plt
import random

os.chdir("/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/data")

print(os.listdir())

## read in training data
blackwell = pd.read_csv("Tower Hamlets - Blackwell.csv")
mile_end = pd.read_csv("Tower Hamlets - Mile End.csv")
poplar = pd.read_csv("Tower Hamlets - Poplar.csv")
victoria_park = pd.read_csv("Tower Hamlets - Victoria Park.csv")

## combine training data
## df = pd.concat([blackwell,mile_end,poplar,victoria_park])


df = blackwell.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

df = df.dropna(how = 'any')

num = len(df)

df2 = df

for i in range(num):
    if df2.iloc[i,0] < 



