#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 16:53:26 2020

@author: yeabinmoon
"""

import pandas as pd
import time
import json

BaseList1 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/listwithsize1.csv',
                        usecols = ['safegraph_place_id','size'])


week_list = ['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
             '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17',
             '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16',
             '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
             '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
             '2020-05-18', '2020-05-25', '2020-06-01', '2020-06-08',
             '2020-06-15']

home_df = BaseList1.copy()

for week in week_list:  
    start_time = time.time()
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
    df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/list1/'+week+'.csv')
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))
    

df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/list1/2019-12-30.csv', 
                 index_col = 0, dtype = {'cbg':str})
for week in week_list[1:]:
    temp_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/list1/'+week+'.csv', 
                          index_col = 0, dtype = {'cbg':str})
    df = pd.concat([df, temp_df], axis = 0, ignore_index = True)
df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/RegionDist1.csv')





BaseList2 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/listwithsize2.csv',
                        usecols = ['safegraph_place_id','size'])
home_df = BaseList2.copy()

for week in week_list:  
    start_time = time.time()
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
    df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/list2/'+week+'.csv')
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))
    

df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/list2/2019-12-30.csv', 
                 index_col = 0, dtype = {'cbg':str})
for week in week_list[1:]:
    temp_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/list2/'+week+'.csv', 
                          index_col = 0, dtype = {'cbg':str})
    df = pd.concat([df, temp_df], axis = 0, ignore_index = True)
df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/RegionDist2.csv')
