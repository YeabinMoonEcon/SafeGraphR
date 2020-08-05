#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 16:24:16 2020

@author: yeabinmoon
"""

import pandas as pd
import time
import json

HolyPois = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/HolyPois.csv',
                       usecols=['safegraph_place_id', 'location_name','poi_cbg',
                                'region', 'city', 'countyName'],
                       dtype = {'poi_cbg':str})

RelList = HolyPois[['safegraph_place_id']]

list_files = ['patterns-part1.csv', 'patterns-part2.csv','patterns-part3.csv',
              'patterns-part4.csv']
month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
list_col = ['safegraph_place_id', 'raw_visitor_counts',
            'visitor_home_cbgs',  'popularity_by_day']


for month in month_list:
    start_time = time.time()
    df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2019/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'raw_visitor_counts'])
        temp_df.rename(columns = {'raw_visitor_counts': '2019-'+month}, inplace = True)
        df = pd.concat([df,temp_df], axis = 0)
    RelList =  RelList.merge(df, how = 'left', on = 'safegraph_place_id')
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))
    
month = '01'
df = pd.DataFrame()
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2020/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'raw_visitor_counts'])
    temp_df.rename(columns = {'raw_visitor_counts': '2020-'+month}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
RelList =  RelList.merge(df, how = 'left', on = 'safegraph_place_id')
RelList.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/RelList.csv')


RelList = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/RelList.csv',
                      index_col = 0)

RelList.fillna(0, inplace = True)
RelList.loc[:,'avg'] = (RelList.iloc[:,1:].sum(axis = 1) - RelList.iloc[:,1:].max(axis = 1) - RelList.iloc[:,1:].min(axis = 1))/11

Filtered = RelList.loc[RelList.loc[:,'avg'] >= 15, :]
Filtered = Filtered[['safegraph_place_id']]

start_time = time.time()
month = '01'
df_total = pd.DataFrame()    
df = pd.DataFrame()
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2020/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'popularity_by_day'])
    temp_df.rename(columns = {'popularity_by_day': '2020-'+month}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
temp_df = Filtered.merge(df, how = 'left', on = 'safegraph_place_id')
temp_df.dropna(inplace = True)
temp_df.iloc[:,1] = temp_df.iloc[:,1].apply(json.loads) 
for i in range(len(temp_df)):
    temp = pd.DataFrame.from_dict(temp_df.iloc[i,1], orient = 'index')
    temp.reset_index(inplace = True)
    temp['safegraph_place_id'] = temp_df.iloc[i,0]
    temp['date'] = '2020-'+month
    temp.rename(columns = {0:'visit'}, inplace = True)
    temp = temp[['safegraph_place_id', 'date', 'index','visit']]
    df_total = pd.concat([df_total, temp], axis = 0, ignore_index= True)
df_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/monthly/2020'+month+'.csv')
print("Done",month,'!')
print("%f seconds" % (time.time() - start_time))
    
    
    
for month in month_list:
    
    month = '01'
    
    df_total = pd.DataFrame()    
    start_time = time.time()
    df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2019/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'popularity_by_day'])
        temp_df.rename(columns = {'raw_visitor_counts': '2019-'+month}, inplace = True)
        df = pd.concat([df,temp_df], axis = 0)
    temp_df =  RelList.merge(df, how = 'left', on = 'safegraph_place_id')
    
    
    
    
    
    temp_df.dropna(inplace = True)
    temp_df.iloc[:,1] = temp_df.iloc[:,1].apply(json.loads) 
    for i in range(len(temp_df)):
        temp = pd.DataFrame.from_dict(temp_df.iloc[i,1], orient = 'index')
        temp.reset_index(inplace = True)
        temp['safegraph_place_id'] = temp_df.iloc[i,0]
        temp['date'] = '2019-'+month
        temp.rename(columns = {0:'visit'}, inplace = True)
        temp = temp[['safegraph_place_id', 'date', 'index','visit']]
        df_total = pd.concat([df_total, temp], axis = 0, ignore_index= True)
    df_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/monthly/2019'+month+'.csv')
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))
    


df = pd.read_csv()