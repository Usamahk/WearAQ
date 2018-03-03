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
blackwall = pd.read_csv("Blackwall.csv")
millwall_park = pd.read_csv("Millwall Park.csv")
wren_close = pd.read_csv("Wren Close.csv")
cam_road = pd.read_csv("Cam Road.csv")

frames = [blackwall, millwall_park, wren_close, cam_road]

df_learn = pd.concat(frames)

# datetime = pd.to_datetime(df_learn["ReadingDateTime"]) # use if datetime not saved
# datetime.to_csv('datetime.csv')

datetime = pd.read_csv('datetime.csv')

df_learn['Month'] = datetime.apply(lambda x: x.month)
df_learn['Day'] = datetime.apply(lambda x: x.day)
df_learn['Hour'] = datetime.apply(lambda x: x.hour)

df_learn1 = df_learn.reset_index(drop=True)

df_analyze = df_learn1.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

datetime2 = pd.to_datetime(blackwall['ReadingDateTime'])

df_b = blackwall

df_b['Month'] = datetime2.apply(lambda x: x.month)
df_b['Day'] = datetime2.apply(lambda x: x.day)
df_b['Hour'] = datetime2.apply(lambda x: x.hour)

df_analyze =  df_b.pivot(index=['Hour','Day','Month'],
                            columns='Species',
                            values='Value')
