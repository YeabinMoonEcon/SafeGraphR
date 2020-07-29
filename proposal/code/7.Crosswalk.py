#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:57:12 2020

@author: yeabinmoon
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


zipcode = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx', 
                        dtype = {'ZIP':str, 'TRACT':str},
                        usecols = ['ZIP', 'TRACT', 'RES_RATIO'])
zipcode.set_index('ZIP',inplace = True)
zipcode = zipcode.groupby('TRACT')['RES_RATIO'].idxmax()
zipcode = zipcode.reset_index()
zipcode.rename(columns = {'RES_RATIO':'ZIP'}, inplace = True)

visit_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visist_total.csv',
                          dtype = {'cbg':str})
visit_total.loc[:,'TRACT'] =  visit_total.cbg.str[:-1] 
visit_total = visit_total.iloc[:,1:]
list_dates = visit_total.columns
visit_total_tract = visit_total.groupby('TRACT')[list_dates[:-1]].sum()
visit_total_tract.reset_index(inplace = True)
visit_total_zip = visit_total_tract.merge(zipcode, how = 'left' , on = 'TRACT')
visit_total_zip = visit_total_zip.groupby('ZIP')[list_dates[:-1]].sum()
visit_total_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visit_total_zip.csv')


visit_large = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visist_large.csv',
                          dtype = {'cbg':str})
visit_large.loc[:,'TRACT'] =  visit_large.cbg.str[0:-1] 
visit_large = visit_large.iloc[:,1:]
list_dates = visit_large.columns
visit_large_tract = visit_large.groupby('TRACT')[list_dates[:-1]].sum()
visit_large_tract.reset_index(inplace = True)
visit_large_zip = visit_large_tract.merge(zipcode, how = 'left' , on = 'TRACT')
visit_large_zip = visit_large_zip.groupby('ZIP')[list_dates[:-1]].sum()
visit_large_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visit_large_zip.csv')



visit_small = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visist_small.csv',
                          dtype = {'cbg':str})
visit_small.loc[:,'TRACT'] =  visit_small.cbg.str[0:-1] 
visit_small = visit_small.iloc[:,1:]
list_dates = visit_small.columns
visit_small_tract = visit_small.groupby('TRACT')[list_dates[:-1]].sum()
visit_small_tract.reset_index(inplace = True)
visit_small_zip = visit_small_tract.merge(zipcode, how = 'left' , on = 'TRACT')
visit_small_zip = visit_small_zip.groupby('ZIP')[list_dates[:-1]].sum()
visit_small_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visit_small_zip.csv')






device_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/total_device.csv',
                           index_col = 0, dtype = {'origin_census_block_group':str})
device_total.loc[:,'TRACT'] =  device_total.origin_census_block_group.str[0:-1] 
device_total = device_total.iloc[:,1:]
device_total.fillna(0, inplace = True)
list_dates = device_total.columns
device_total_tract = device_total.groupby('TRACT')[list_dates[:-1]].sum()
device_total_tract.reset_index(inplace = True)
device_total_zip = device_total_tract.merge(zipcode, how = 'left' , on = 'TRACT')
device_total_zip = device_total_zip.groupby('ZIP')[list_dates[:-1]].sum()
device_total_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/device_total_zip.csv')

device_home = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/home_device.csv',
                          index_col = 0, dtype = {'origin_census_block_group':str})
device_home.loc[:,'TRACT'] =  device_home.origin_census_block_group.str[0:-1] 
device_home = device_home.iloc[:,1:]
device_home.fillna(0, inplace = True)
list_dates = device_home.columns
device_home_tract = device_home.groupby('TRACT')[list_dates[:-1]].sum()
device_home_tract.reset_index(inplace = True)
device_home_zip = device_home_tract.merge(zipcode, how = 'left' , on = 'TRACT')
device_home_zip = device_home_zip.groupby('ZIP')[list_dates[:-1]].sum()
device_home_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/device_home_zip.csv')

device_distancing = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/social_distancing.csv',
                                index_col = 0, dtype = {'origin_census_block_group':str})
device_distancing.loc[:,'TRACT'] =  device_distancing.origin_census_block_group.str[0:-1] 
device_distancing = device_distancing.iloc[:,1:]
device_distancing.fillna(0, inplace = True)
list_dates = device_distancing.columns
device_distancing_tract = device_distancing.groupby('TRACT')[list_dates[:-1]].sum()
device_distancing_tract.reset_index(inplace = True)
device_distancing_zip = device_distancing_tract.merge(zipcode, how = 'left' , on = 'TRACT')
device_distancing_zip = device_distancing_zip.groupby('ZIP')[list_dates[:-1]].sum()
device_distancing_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/device_distancing_zip.csv')






a = np.array([0,1])
b = np.array([5,6,7,8])
for i in range(25):
    c = b + 7 * i
    a = np.append(a,c)

device_total_zip_weekdays = device_total_zip.iloc[:,list(a)]
device_home_zip_weekdays  = device_home_zip.iloc[:,list(a)]
device_distancing_zip_weekdays = device_distancing_zip.iloc[:,list(a)]



a = np.array([2,3,4])
b = np.array([2,3,4])
for i in range(25):
    c = b + 7 *(i+1)
    a = np.append(a,c)
device_total_zip_weekends = device_total_zip.iloc[:,list(a)]
device_home_zip_weekends = device_home_zip.iloc[:,list(a)]
device_distancing_zip_weekends = device_distancing_zip.iloc[:,list(a)]

df_temp = visit_total_zip.copy()
df_temp.loc[:,'outcome'] = df_temp.iloc[:,9:13].mean(axis = 1)
df_temp.loc[:,'preperiod'] = df_temp.iloc[:,0:8].mean(axis = 1)
df = df_temp[['outcome','preperiod']]
df.reset_index(inplace = True)

df_temp = visit_large_zip / visit_total_zip
df_temp.fillna(0, inplace = True)
df_temp.loc[:,'large'] =  df_temp.iloc[:,0:8].mean(axis = 1)
df_temp = df_temp[['large']]
df_temp.reset_index(inplace = True)

df = df.merge(df_temp, how = 'left', on = 'ZIP')

df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/stata/df.csv')

visit_large_zip.mean(axis = 0).plot(label = 'large')
visit_small_zip.mean(axis = 0).plot(label = 'small')
#visit_total_zip.mean(axis = 0).plot(label = 'total')
plt.legend(loc='upper right')
plt.show()




visit_total_zip.mean(axis = 0).plot()

visit_large_zip.sum(axis = 0).plot()
visit_small_zip.mean(axis = 0).plot()
visit_small_zip.sum(axis = 0).plot()
