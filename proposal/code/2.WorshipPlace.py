#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 09:06:22 2020

@author: yeabinmoon

Data created:
    1. pop_day.csv: For each religious POI, counts the number of visists by date
    2. WorshipPlace.csv: the list of religious organization having the most crowded days are either Friday, Saturday, or Sunday.

the List is constructed by counting the pattern of 2019.
"""


import pandas as pd
import time
import json


raw_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/df_CA_Reli_raw.csv',
                     index_col = 0, dtype ={'postal_code':str, 'stateFIPS':str,
                                            'countyFIPS':str, 'poi_cbg':str})
list_files = ['patterns-part1.csv', 'patterns-part2.csv','patterns-part3.csv',
              'patterns-part4.csv']
month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
list_col = ['safegraph_place_id', 'raw_visitor_counts',
            'visitor_home_cbgs',  'popularity_by_day']

month_CA_pop_day = raw_df.copy()

"""
Following block takes a lot of computing power and time.
Go to line 62!
"""

df_total = pd.DataFrame()
for month in month_list:
    start_time = time.time()
    df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2019/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'popularity_by_day'])
        temp_df.rename(columns = {'popularity_by_day': '2019-'+month}, inplace = True)
        df = pd.concat([df,temp_df], axis = 0)
    month_CA_pop_day = month_CA_pop_day.merge(df, how = 'left',
                                      on = 'safegraph_place_id')
    test = month_CA_pop_day.copy()
    test = test[['safegraph_place_id', '2019-'+ month]]
    test.dropna(inplace = True)
    test.loc[:,'2019-'+ month] = test.loc[:,'2019-'+ month].apply(json.loads)
    test.reset_index(inplace = True)
    test.drop(columns = 'index', inplace = True)
    for i in range(len(test)):
        temp_df = pd.DataFrame.from_dict(test.iloc[i,1], orient = 'index')
        temp_df = temp_df.reset_index()
        temp_df['safegraph_place_id'] = test.iloc[i,0]
        temp_df['month'] = month
        temp_df.rename(columns = {0:'visits','index':'date'}, inplace = True)
        temp_df = temp_df[['safegraph_place_id','month','date','visits']]
        df_total = pd.concat([df_total,temp_df], axis = 0, ignore_index = True)
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))

df_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/pop_day.csv')
# pop_day.csv


df_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/pop_day.csv',
                       index_col = 0)
# Find the most crowded day
temp_df = df_total.groupby(['safegraph_place_id','date'])['visits'].sum()
temp_df = temp_df.reset_index()
temp_df = temp_df.set_index('date')
temp_df = temp_df.groupby(['safegraph_place_id'])['visits'].idxmax()

temp_df = temp_df.reset_index()
temp_df.groupby('visits').count()

temp_ind = (temp_df.visits == 'Friday') | (temp_df.visits == 'Saturday') | (temp_df.visits == 'Sunday')
temp_lists = temp_df.loc[temp_ind,:]

WorshipPlace = temp_lists.loc[:,['safegraph_place_id']]
WorshipPlace.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/WorshipPlace.csv')
