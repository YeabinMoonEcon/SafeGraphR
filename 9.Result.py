#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 20:47:25 2020

@author: yeabinmoon
"""

import pandas as pd



week_list = ['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
             '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17',
             '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16',
             '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
             '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
             '2020-05-18', '2020-05-25', '2020-06-01', '2020-06-08',
             '2020-06-15']

visit_total_zip1 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/visit_total_zip1.csv',
                               dtype = {'ZIP':str})

visit_large_zip1 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/visit_large_zip1.csv',
                               dtype = {'ZIP':str})


zipcode = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx', 
                        dtype = {'ZIP':str, 'TRACT':str},
                        usecols = ['ZIP', 'TRACT', 'RES_RATIO'])
zipcode.set_index('ZIP',inplace = True)
zipcode = zipcode.groupby('TRACT')['RES_RATIO'].idxmax()
zipcode = zipcode.reset_index()
zipcode.rename(columns = {'RES_RATIO':'ZIP'}, inplace = True)

total_device = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/device_total.csv',
                           index_col = 0, dtype = {'origin_census_block_group':str})


total_device.loc[:,'TRACT'] =  total_device.origin_census_block_group.str[:-1]

total_device.drop(columns = {'origin_census_block_group'}, inplace = True)
list_dates = total_device.columns
total_device_tract = total_device.groupby('TRACT')[list_dates[:-1]].sum()
total_device_tract.reset_index(inplace = True)
total_device_zip = total_device_tract.merge(zipcode, how = 'left' , on = 'TRACT')
total_device_zip = total_device_zip.groupby('ZIP')[list_dates[:-1]].sum()

base_zip = total_device_zip.iloc[:,:54]

temp_df = base_zip.iloc[:,:5].mean(axis = 1)
temp_df = temp_df.reset_index()
temp_df.rename(columns = {0:week_list[0]}, inplace = True)
for i in range(7):
    temp = base_zip.iloc[:,5+7*i:12+7*i].mean(axis = 1)
    temp = temp.reset_index()
    temp.rename(columns = {0:week_list[i+1]}, inplace = True)
    temp_df = temp_df.merge(temp, how = 'outer', on = 'ZIP')

base_visit = visit_total_zip1.iloc[:,0:9]

test = temp_df.merge(base_visit, how = 'left', on = 'ZIP')
test.fillna(0,inplace = True)
test.set_index('ZIP', inplace = True)

ini_df = test.iloc[:,8]/ test.iloc[:,0]
ini_df = ini_df.reset_index()
ini_df.rename(columns = {0:week_list[0]}, inplace = True)
for i in range(7):
    temp = test.iloc[:,9+i]/ test.iloc[:,1+i]
    temp = temp.reset_index()
    temp.rename(columns = {0:week_list[i+1]}, inplace = True)
    ini_df = ini_df.merge(temp, how = 'outer', on = 'ZIP')
ini_df.loc[:,'ind'] = ini_df.iloc[:,1:].mean(axis = 1)

ini_df = ini_df.loc[ini_df.loc[:,'ind']>= 0.05,:]

baseline_zipcode = ini_df.loc[:,['ZIP']]
baseline_total_visitor = baseline_zipcode.copy()
baseline_total_visitor = baseline_total_visitor.merge(visit_total_zip1, how = 'left', on = 'ZIP')
baseline_total_visitor.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/baseline_total_visitor.csv')

baseline_large_visitor = baseline_zipcode.copy()
baseline_large_visitor = baseline_large_visitor.merge(visit_large_zip1, how = 'left', on = 'ZIP')
baseline_large_visitor.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/baseline_large_visitor.csv')

baseline_total_device = baseline_zipcode.copy()

base_zip = total_device_zip.iloc[:,:173]

temp_df = base_zip.iloc[:,:5].mean(axis = 1)
temp_df = temp_df.reset_index()
temp_df.rename(columns = {0:week_list[0]}, inplace = True)
for i in range(24):
    temp = base_zip.iloc[:,5+7*i:12+7*i].mean(axis = 1)
    temp = temp.reset_index()
    temp.rename(columns = {0:week_list[i+1]}, inplace = True)
    temp_df = temp_df.merge(temp, how = 'outer', on = 'ZIP')
baseline_total_device = baseline_total_device.merge(temp_df, how = 'left', on = 'ZIP')
baseline_total_device.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/baseline_total_device.csv')
