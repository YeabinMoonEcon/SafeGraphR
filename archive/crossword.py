#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 14:39:55 2020

@author: yeabinmoon
"""

import pandas as pd



zipcode = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx', 
                        dtype = {'ZIP':str, 'TRACT':str})
                        
device_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/total_device.csv',
                           index_col = 0, dtype = {'origin_census_block_group':str})
device_total.loc[:,'TRACT'] =  device_total.origin_census_block_group.str[0:-1] 
device_total = device_total.iloc[:,1:]
device_total.fillna(0, inplace = True)
list_dates = device_total.columns
device_total_tract = device_total.groupby('TRACT')[list_dates[:-1]].sum()
device_total_tract.reset_index(inplace = True)


visit_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visist_total.csv',
                          dtype = {'cbg':str})
visit_total.loc[:,'TRACT'] =  visit_total.cbg.str[0:-1] 
visit_total = visit_total.iloc[:,1:]
list_dates = visit_total.columns
visit_total_tract = visit_total.groupby('TRACT')[list_dates[:-1]].sum()
visit_total_tract.reset_index(inplace = True)

visit_large = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visist_large.csv',
                          dtype = {'cbg':str})
visit_large.loc[:,'TRACT'] =  visit_large.cbg.str[0:-1] 
visit_large = visit_large.iloc[:,1:]
list_dates = visit_large.columns
visit_large_tract = visit_large.groupby('TRACT')[list_dates[:-1]].sum()
visit_large_tract.reset_index(inplace = True)


test_cross = device_total_tract[['TRACT']]
test_cross = test_cross.merge(zipcode, how = 'left', on = 'TRACT')
test_cross.set_index('ZIP',inplace = True)

temp = test_cross.groupby('TRACT')['RES_RATIO'].idxmax()
temp = temp.reset_index()
temp.rename(columns = {'RES_RATIO':'ZIP'}, inplace = True)

test = device_total_tract.merge(temp, how = 'left', on = 'TRACT')

visit_total_tract = visit_total_tract.merge(temp, how = 'left', on = "TRACT")


large_list = visit_total_tract.loc[:,['TRACT']]
large_list = large_list.merge(visit_large_tract, how = 'left', on = 'TRACT')
large_list.fillna(0, inplace = True)


visit_total_tract.loc[:,'before'] = visit_total_tract.iloc[:,1:9].mean(axis = 1)
visit_total_tract.loc[:,'after'] = visit_total_tract.iloc[:,10:14].min(axis = 1)
visit_total_tract.loc[:,'instrument'] = (large_list.iloc[:,1:9] / visit_total_tract.iloc[:,1:9]).mean(axis = 1)


df_reg = visit_total_tract[['before','after','instrument']]
#df_reg.reset_index(inplace = True)
df_reg.fillna(0, inplace = True)
df_reg.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/df_reg4.csv')
