#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 20:16:51 2020

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


week_list = ['2019-11-25', '2019-12-02', '2019-12-09', '2019-12-16', '2019-12-23',
             '2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20']
             # '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17',
             # '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16',
             # '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
             # '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
             # '2020-05-18', '2020-05-25', '2020-06-01', '2020-06-08',
             # '2020-06-15']

for week in week_list:
    start_time = time.time()
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+week+'-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','raw_visitor_counts'])
    RelList = RelList.merge(temp_df, how = 'left', on = 'safegraph_place_id')
    RelList.rename(columns = {'raw_visitor_counts':week}, inplace = True)
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))

RelList.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/temp1.csv')

#df_list = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/weekly.csv',index_col = 0)
RelList.fillna(0,inplace = True)

RelList.loc[:,'baseline'] = (RelList.iloc[:,1:10].sum(axis = 1) - RelList.iloc[:,1:10].max(axis = 1) - RelList.iloc[:,1:10].min(axis = 1))/7

temp_df = RelList.loc[RelList.loc[:,'baseline'] >= 15,:]

temp_df = temp_df[['safegraph_place_id']]

temp_df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/temp_df.csv')

#########################################################################

temp_list = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/temp_df.csv',index_col = 0)

month = '01'

df_total = pd.DataFrame()    
start_time = time.time()
df = pd.DataFrame()
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2020/' + month +'/' + file,
                          usecols = ['safegraph_place_id', 'popularity_by_day'])
    temp_df.rename(columns = {'popularity_by_day': '2020-'+month}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
temp_df = temp_list.merge(df, how = 'left', on = 'safegraph_place_id')
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
    df_total = pd.DataFrame()    
    start_time = time.time()
    df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2019/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'popularity_by_day'])
        temp_df.rename(columns = {'popularity_by_day': '2019-'+month}, inplace = True)
        df = pd.concat([df,temp_df], axis = 0)
    temp_df =  temp_list.merge(df, how = 'left', on = 'safegraph_place_id')
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
    

##################################

temp_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/monthly/202001.csv',
                      index_col = 0)