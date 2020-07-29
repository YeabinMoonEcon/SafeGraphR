#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 18:20:21 2020

@author: yeabinmoon
"""

import pandas as pd

df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/RegionDist1.csv',
                 index_col = 0, dtype = {'cbg':str})

df = df[['date','cbg','safegraph_place_id','size','visits']]

visits_total1 = df.groupby(['date', 'cbg'])['visits'].sum()
visits_total1 = visits_total1.reset_index()
visits_total1 = visits_total1.pivot(index= 'cbg', columns = 'date', values = 'visits')
visits_total1.fillna(0, inplace = True)
visits_total1.reset_index(inplace = True)
visits_total1.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/visits_total1.csv')


visits_large1 = df.loc[df.loc[:,'size'] == 1,:]
visits_large1 = visits_large1.groupby(['date', 'cbg'])['visits'].sum()
visits_large1 = visits_large1.reset_index()
visits_large1 = visits_large1.pivot(index= 'cbg', columns = 'date', values = 'visits')
visits_large1.fillna(0, inplace = True)
visits_large1.reset_index(inplace = True)
visits_large1.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/visits_large1.csv')


visits_small1 = df.loc[df.loc[:,'size'] == 0,:]
visits_small1 = visits_small1.groupby(['date', 'cbg'])['visits'].sum()
visits_small1 = visits_small1.reset_index()
visits_small1 = visits_small1.pivot(index= 'cbg', columns = 'date', values = 'visits')
visits_small1.fillna(0, inplace = True)
visits_small1.reset_index(inplace = True)
visits_small1.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/visits_small1.csv')


df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/RegionDist2.csv',
                 index_col = 0, dtype = {'cbg':str})

df = df[['date','cbg','safegraph_place_id','size','visits']]

visits_total2 = df.groupby(['date', 'cbg'])['visits'].sum()
visits_total2 = visits_total2.reset_index()
visits_total2 = visits_total2.pivot(index= 'cbg', columns = 'date', values = 'visits')
visits_total2.fillna(0, inplace = True)
visits_total2.reset_index(inplace = True)
visits_total2.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/visits_total2.csv')


visits_large2 = df.loc[df.loc[:,'size'] == 1,:]
visits_large2 = visits_large2.groupby(['date', 'cbg'])['visits'].sum()
visits_large2 = visits_large2.reset_index()
visits_large2 = visits_large2.pivot(index= 'cbg', columns = 'date', values = 'visits')
visits_large2.fillna(0, inplace = True)
visits_large2.reset_index(inplace = True)
visits_large2.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/visits_large2.csv')


visits_small2 = df.loc[df.loc[:,'size'] == 0,:]
visits_small2 = visits_small2.groupby(['date', 'cbg'])['visits'].sum()
visits_small2 = visits_small2.reset_index()
visits_small2 = visits_small2.pivot(index= 'cbg', columns = 'date', values = 'visits')
visits_small2.fillna(0, inplace = True)
visits_small2.reset_index(inplace = True)
visits_small2.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/visits_small2.csv')