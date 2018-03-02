#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 12:53:16 2018

@author: Usamahk
"""

import pandas as pd

blackwell = pd.read_csv("/Users/Usamahk/Admin/Work/Umbrellium/WearAQ 2.0/data/Tower Hamlets - Blackwell.csv")

blackwell = blackwell.pivot(index='ReadingDateTime',
                            columns='Species',
                            values='Value')

