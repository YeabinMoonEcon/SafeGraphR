#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 10:12:08 2020

@author: yeabinmoon

Assume that the residents in Alameda County attends the church in California

Data created:
    RegionDist.csv: summarize regional distribution
"""

import pandas as pd
import time
import json

BaseList = pd.read_csv('/Volumes/LaCie/cg-data/working_data/ClassificationCA.csv',
                       usecols = ['safegraph_place_id','shutdown', 'large'])

week_list = ['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
             '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17', 
             '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16', 
             '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
             '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
             '2020-05-18', '2020-05-25']

home_df = BaseList.copy()

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
        temp_df = pd.DataFrame.from_dict(home_df.iloc[i,3], orient = 'index')
        temp_df = temp_df.reset_index()
        temp_df.loc[:,'safegraph_place_id'] = home_df.iloc[i,0]
        temp_df.loc[:,'shutdown'] = home_df.iloc[i,1]
        temp_df.loc[:,'large']    = home_df.iloc[i,2]
        temp_df.loc[:,'date']     = week
        temp_df.rename(columns = {0:'visits','index':'cbg'}, inplace = True)
        temp_df.loc[:,'year'] = temp_df.loc[:,'date'].str[0:4]
        temp_df.loc[:,'week'] = temp_df.loc[:,'date'].str[5:]        
        temp_df = temp_df[['safegraph_place_id', 'cbg', 'year','week','visits', 'shutdown','large']]
        df = pd.concat([df, temp_df], axis = 0, ignore_index = True)
    df.to_csv('/Volumes/LaCie/cg-data/working_data/temp/'+week+'.csv')
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))


df = pd.read_csv('/Volumes/LaCie/cg-data/working_data/temp/2019-12-30.csv', 
                 index_col = 0, dtype = {'cbg':str})
for week in week_list[1:]:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/working_data/temp/'+week+'.csv', 
                          index_col = 0, dtype = {'cbg':str})
    df = pd.concat([df, temp_df], axis = 0, ignore_index = True)
df.to_csv('/Volumes/LaCie/cg-data/working_data/RegionDist.csv')

