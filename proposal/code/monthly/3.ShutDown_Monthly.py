#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 22:45:14 2020

@author: yeabinmoon
"""

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt


raw_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/df_CA_Reli_raw.csv',
                     index_col = 0, dtype ={'postal_code':str, 'stateFIPS':str,
                                            'countyFIPS':str, 'poi_cbg':str})

WorshipPlace = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/WorshipPlace.csv'
                           , index_col=0)

WorshipPlace = WorshipPlace.merge(raw_df, how = 'left', on = 'safegraph_place_id')

list_files = ['patterns-part1.csv', 'patterns-part2.csv','patterns-part3.csv',
              'patterns-part4.csv']
month_list = ['01','02','03','04']

df = pd.DataFrame()
month = '12'
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2019/' + month +'/' + file,
                          usecols = ['safegraph_place_id', 'raw_visitor_counts'])
    temp_df.rename(columns = {'raw_visitor_counts': '2019-'+month}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
WorshipPlace = WorshipPlace.merge(df, how = 'left', on = 'safegraph_place_id')



for month in month_list:
    start_time = time.time()
    df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2020/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'raw_visitor_counts'])
        temp_df.rename(columns = {'raw_visitor_counts': '2020-'+month}, inplace = True)
        df = pd.concat([df,temp_df], axis = 0)
    WorshipPlace = WorshipPlace.merge(df, how = 'left', on = 'safegraph_place_id')
    print("Done", month,'!')
    print("%f seconds" % (time.time() - start_time))
  
df = pd.DataFrame()
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern_after/2020/06/05/06/'+ file+ '.gz',
                          usecols = ['safegraph_place_id', 'raw_visitor_counts'])
    temp_df.rename(columns = {'raw_visitor_counts': '2020-05'}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
WorshipPlace = WorshipPlace.merge(df, how = 'left', on = 'safegraph_place_id')

df = pd.DataFrame()
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern_after/2020/07/06/06/'+ file+ '.gz',
                          usecols = ['safegraph_place_id', 'raw_visitor_counts'])
    temp_df.rename(columns = {'raw_visitor_counts': '2020-06'}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
WorshipPlace = WorshipPlace.merge(df, how = 'left', on = 'safegraph_place_id')


temp_df = WorshipPlace.copy()
temp_df.fillna(0, inplace = True)

BaseVisitsMonthly = temp_df.copy()

BaseVisitsMonthly.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/monthly/BaseVisitsMonthly.csv')

###################################################

BaseVisitsMonthly = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/monthly/BaseVisitsMonthly.csv',
                                index_col = 0, dtype = {'postal_code':str,'stateFIPS':str,
                                                        'countyFIPS':str, 'poi_cbg':str})
BaseVisitsMonthly.loc[:,'base'] = BaseVisitsMonthly.iloc[:,12:14].mean(axis = 1)
BaseVisitsMonthly.loc[:,'base'].quantile([.25,.5,.75,.9])

temp0 = (BaseVisitsMonthly.loc[:,'base'] >= 100) 
temp0.sum()
BaseVisitsMonthly.loc[temp0,'base'].sum()

temp1 = (BaseVisitsMonthly.loc[:,'base'] >= 50) & (BaseVisitsMonthly.loc[:,'base'] < 100)
temp1.sum()
BaseVisitsMonthly.loc[temp1,'base'].sum()

temp2 = (BaseVisitsMonthly.loc[:,'base'] >= 30) & (BaseVisitsMonthly.loc[:,'base'] < 50)
temp2.sum()
BaseVisitsMonthly.loc[temp2,'base'].sum()

temp3 = (BaseVisitsMonthly.loc[:,'base'] >= 20) & (BaseVisitsMonthly.loc[:,'base'] < 30)
temp3.sum()
BaseVisitsMonthly.loc[temp3,'base'].sum()

temp4 = (BaseVisitsMonthly.loc[:,'base'] >= 10) & (BaseVisitsMonthly.loc[:,'base'] < 20)
temp4.sum()
BaseVisitsMonthly.loc[temp4,'base'].sum()

temp5 = BaseVisitsMonthly.loc[:,'base'] < 10
temp5.sum()
BaseVisitsMonthly.loc[temp5,'base'].sum()



BaseVisitsMonthly.loc[temp5, 'size'] = 0
BaseVisitsMonthly.loc[temp4, 'size'] = 1
BaseVisitsMonthly.loc[temp3, 'size'] = 2
BaseVisitsMonthly.loc[temp2, 'size'] = 3
BaseVisitsMonthly.loc[temp1, 'size'] = 4
BaseVisitsMonthly.loc[temp0, 'size'] = 5

BaseVisitsMonthly.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/monthly/ClassificationCA.csv')
