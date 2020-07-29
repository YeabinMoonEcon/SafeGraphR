#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 23:23:11 2020

@author: yeabinmoon
"""

import pandas as pd
import time
import json

BaseList = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/monthly/ClassificationCA.csv',
                       usecols = ['safegraph_place_id','size'])



list_files = ['patterns-part1.csv', 'patterns-part2.csv','patterns-part3.csv',
              'patterns-part4.csv']

home_df = BaseList.copy()
df = pd.DataFrame()
month = '12'
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2019/' + month +'/' + file,
                          usecols = ['safegraph_place_id', 'visitor_home_cbgs'])
    temp_df.rename(columns = {'visitor_home_cbgs': '2019-'+month}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
home_df = home_df.merge(df, how = 'left', on = 'safegraph_place_id')
home_df.dropna(inplace = True)
home_df.loc[:,'2019-'+month] = home_df.loc[:,'2019-'+month].apply(json.loads)
home_df = home_df.loc[home_df.loc[:,'2019-'+month].apply(len) != 0,:]
df = pd.DataFrame()
for i in range(len(home_df)):        
    temp_df = pd.DataFrame.from_dict(home_df.iloc[i,2], orient = 'index')
    temp_df = temp_df.reset_index()
    temp_df.loc[:,'safegraph_place_id'] = home_df.iloc[i,0]
    temp_df.loc[:,'size'] = home_df.iloc[i,1]
    temp_df.loc[:,'date'] = '2019-'+month
    temp_df.rename(columns = {0:'visits','index':'cbg'}, inplace = True)
    #temp_df.loc[:,'year'] = temp_df.loc[:,'date'].str[0:4]
    #temp_df.loc[:,'week'] = temp_df.loc[:,'date'].str[5:]        
    temp_df = temp_df[['safegraph_place_id', 'cbg', 'date', 'visits', 'size']]
    df = pd.concat([df, temp_df], axis = 0, ignore_index = True)    
df = df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/monthly/temp/2019-'+month+'.csv')




month_list = ['01','02','03','04']
for month in month_list:
    home_df = BaseList.copy()
    start_time = time.time()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2020/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'visitor_home_cbgs'])
        temp_df.rename(columns = {'visitor_home_cbgs': '2020-'+month}, inplace = True)   
        df = pd.concat([df,temp_df], axis = 0)
    home_df = home_df.merge(df, how = 'left', on = 'safegraph_place_id')
    home_df.dropna(inplace = True)
    home_df.loc[:,'2020-'+month] = home_df.loc[:,'2020-'+month].apply(json.loads)
    home_df = home_df.loc[home_df.loc[:,'2020-'+month].apply(len) != 0,:]
    df = pd.DataFrame()
    for i in range(len(home_df)):        
        temp_df = pd.DataFrame.from_dict(home_df.iloc[i,2], orient = 'index')
        temp_df = temp_df.reset_index()
        temp_df.loc[:,'safegraph_place_id'] = home_df.iloc[i,0]
        temp_df.loc[:,'size'] = home_df.iloc[i,1]
        temp_df.loc[:,'date'] = '2020-'+month
        temp_df.rename(columns = {0:'visits','index':'cbg'}, inplace = True)
        #temp_df.loc[:,'year'] = temp_df.loc[:,'date'].str[0:4]
        #temp_df.loc[:,'week'] = temp_df.loc[:,'date'].str[5:]        
        temp_df = temp_df[['safegraph_place_id', 'cbg', 'date', 'visits', 'size']]
        df = pd.concat([df, temp_df], axis = 0, ignore_index = True)    
    df = df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/monthly/temp/2020-'+month+'.csv')
    print("Done", month,'!')
    print("%f seconds" % (time.time() - start_time))
    
home_df = BaseList.copy()
df = pd.DataFrame()
month = '05'
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern_after/2020/06/05/06/'+ file +'.gz',
                          usecols = ['safegraph_place_id', 'visitor_home_cbgs'],
                          compression = 'gzip')
    temp_df.rename(columns = {'visitor_home_cbgs': '2020-'+month}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
home_df = home_df.merge(df, how = 'left', on = 'safegraph_place_id')
home_df.dropna(inplace = True)
home_df.loc[:,'2020-'+month] = home_df.loc[:,'2020-'+month].apply(json.loads)
home_df = home_df.loc[home_df.loc[:,'2020-'+month].apply(len) != 0,:]
df = pd.DataFrame()
for i in range(len(home_df)):        
    temp_df = pd.DataFrame.from_dict(home_df.iloc[i,2], orient = 'index')
    temp_df = temp_df.reset_index()
    temp_df.loc[:,'safegraph_place_id'] = home_df.iloc[i,0]
    temp_df.loc[:,'size'] = home_df.iloc[i,1]
    temp_df.loc[:,'date'] = '2020-'+month
    temp_df.rename(columns = {0:'visits','index':'cbg'}, inplace = True)
    #temp_df.loc[:,'year'] = temp_df.loc[:,'date'].str[0:4]
    #temp_df.loc[:,'week'] = temp_df.loc[:,'date'].str[5:]        
    temp_df = temp_df[['safegraph_place_id', 'cbg', 'date', 'visits', 'size']]
    df = pd.concat([df, temp_df], axis = 0, ignore_index = True)    
df = df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/monthly/temp/2020-'+month+'.csv')

home_df = BaseList.copy()
df = pd.DataFrame()
month = '06'
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern_after/2020/07/06/06/'+ file +'.gz',
                          usecols = ['safegraph_place_id', 'visitor_home_cbgs'],
                          compression = 'gzip')
    temp_df.rename(columns = {'visitor_home_cbgs': '2020-'+month}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
home_df = home_df.merge(df, how = 'left', on = 'safegraph_place_id')
home_df.dropna(inplace = True)
home_df.loc[:,'2020-'+month] = home_df.loc[:,'2020-'+month].apply(json.loads)
home_df = home_df.loc[home_df.loc[:,'2020-'+month].apply(len) != 0,:]
df = pd.DataFrame()
for i in range(len(home_df)):        
    temp_df = pd.DataFrame.from_dict(home_df.iloc[i,2], orient = 'index')
    temp_df = temp_df.reset_index()
    temp_df.loc[:,'safegraph_place_id'] = home_df.iloc[i,0]
    temp_df.loc[:,'size'] = home_df.iloc[i,1]
    temp_df.loc[:,'date'] = '2020-'+month
    temp_df.rename(columns = {0:'visits','index':'cbg'}, inplace = True)
    #temp_df.loc[:,'year'] = temp_df.loc[:,'date'].str[0:4]
    #temp_df.loc[:,'week'] = temp_df.loc[:,'date'].str[5:]        
    temp_df = temp_df[['safegraph_place_id', 'cbg', 'date', 'visits', 'size']]
    df = pd.concat([df, temp_df], axis = 0, ignore_index = True)    
df = df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/monthly/temp/2020-'+month+'.csv')


df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/monthly/temp/2019-12.csv',
                 index_col = 0, dtype = {'cbg':str})
month_list = ['01','02','03','04','05','06']
for month in month_list:
    temp_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/monthly/temp/2020-'+ month +'.csv',
                          index_col = 0, dtype = {'cbg':str})
    df = pd.concat([df,temp_df], axis = 0, ignore_index = True)
df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/monthly/RegionDist.csv')