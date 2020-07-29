#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 00:11:38 2020

@author: yeabinmoon
"""

import pandas as pd

df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/monthly/RegionDist.csv',
                 index_col = 0, dtype = {'cbg':str},
                 nrows = 10)

                 
                 