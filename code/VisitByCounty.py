#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 23:57:47 2020

@author: yeabinmoon
"""


import pandas as pd
import time
import json

WorshipPlace = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/WorshipPlace.csv', index_col = 0)

HolyPois = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/HolyPois.csv',
                       usecols=['safegraph_place_id', 'location_name','poi_cbg',
                                'region', 'city', 'countyName'],
                       dtype = {'poi_cbg':str})

WorshipPlace = WorshipPlace.merge(HolyPois, how = 'left', on = 'safegraph_place_id')

temp = WorshipPlace.groupby('region')['safegraph_place_id'].count()
temp = temp.reset_index()

temp.mean()




week_list = ['2019-11-25', '2019-12-02', '2019-12-09', '2019-12-16', '2019-12-23',
             '2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20']


for week in week_list:
    start_time = time.time()
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+week+'-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','raw_visitor_counts'])
    WorshipPlace = WorshipPlace.merge(temp_df, how = 'left', on = 'safegraph_place_id')
    WorshipPlace.rename(columns = {'raw_visitor_counts':week}, inplace = True)
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))
    
WorshipPlace.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/WeekVisitors_2.csv')


temp_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/WeekVisitors_2.csv',index_col = 0)
temp_df.fillna(0, inplace = True)
temp_df.loc[:,'baseline'] = (temp_df.iloc[:,6:15].sum(axis = 1) - temp_df.iloc[:,6:15].max(axis = 1) - temp_df.iloc[:,6:15].min(axis = 1))/7

temp_df.loc[:,'size'] = 0
temp_df.loc[temp_df.loc[:,'baseline'] > 31, 'size'] = 1

temp_list = temp_df[['safegraph_place_id','size']]

(temp_list['size'] == 1).sum()
(temp_list['size'] == 0).sum()

temp_list.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/temp_list2.csv')


##############################################
BaseList = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/temp_list2.csv',
                       index_col = 0)

week_list = ['2019-11-25', '2019-12-02', '2019-12-09', '2019-12-16', '2019-12-23',
              '2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
              '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17',
              '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16',
              '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
              '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
              '2020-05-18', '2020-05-25', '2020-06-01', '2020-06-08',
              '2020-06-15']




for week in week_list:     
    start_time = time.time()
    home_df = BaseList.copy()
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+ week + '-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','visitor_home_cbgs'])
    temp_df.rename(columns = {'visitor_home_cbgs': week}, inplace = True)
    home_df = home_df.merge(temp_df, how = 'left', on = 'safegraph_place_id')
    home_df.dropna(inplace = True)
    home_df.loc[:,week] = home_df.loc[:,week].apply(json.loads)
    home_df = home_df.loc[home_df.loc[:,week].apply(len) != 0,:]
    df = pd.DataFrame()
    for i in range(len(home_df)):      
        temp_df = pd.DataFrame.from_dict(home_df.iloc[i,2], orient = 'index')
        temp_df = temp_df.reset_index()
        temp_df.loc[:,'safegraph_place_id'] = home_df.iloc[i,0]
        temp_df.loc[:,'size'] = home_df.iloc[i,1]
        temp_df.loc[:,'date'] = week
        temp_df.rename(columns = {0:'visits','index':'cbg'}, inplace = True)
        #temp_df.loc[:,'year'] = temp_df.loc[:,'date'].str[0:4]
        #temp_df.loc[:,'week'] = temp_df.loc[:,'date'].str[5:]        
        temp_df = temp_df[['safegraph_place_id', 'cbg', 'date', 'visits', 'size']]
        df = pd.concat([df, temp_df], axis = 0, ignore_index = True)
    df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/month/'+week+'_cbg.csv')
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))