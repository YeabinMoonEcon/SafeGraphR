#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 09:06:22 2020

@author: yeabinmoon

Data created:
    WorshipPlace.csv: the list of religious organization having the most crowded days are either Friday, Saturday, or Sunday.

the List is constructed by counting the pattern before March 2020.
"""


import pandas as pd
import time
import json


raw_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/df_CA_Reli_raw.csv',
                     index_col = 0, dtype ={'postal_code':str, 'stateFIPS':str,
                                            'countyFIPS':str, 'poi_cbg':str})
list_files = ['patterns-part1.csv', 'patterns-part2.csv','patterns-part3.csv',
              'patterns-part4.csv']
month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
list_col = ['safegraph_place_id', 'raw_visitor_counts',
            'visitor_home_cbgs',  'popularity_by_day']

month_CA_pop_day = raw_df.copy()
month_CA_pop_day = month_CA_pop_day.loc[:,['safegraph_place_id']]
"""
Following block takes a lot of computing power and time.
Go to line 62!
"""


for month in month_list:
    df_total = pd.DataFrame()    
    start_time = time.time()
    df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2019/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'popularity_by_day'])
        temp_df.rename(columns = {'popularity_by_day': '2019-'+month}, inplace = True)
        df = pd.concat([df,temp_df], axis = 0)
    temp_df =  month_CA_pop_day.merge(df, how = 'left', on = 'safegraph_place_id')
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
    df_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/2019'+month+'.csv')
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))

for month in month_list[0:2]:
    df_total = pd.DataFrame()    
    start_time = time.time()
    df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2020/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'popularity_by_day'])
        temp_df.rename(columns = {'popularity_by_day': '2020-'+month}, inplace = True)
        df = pd.concat([df,temp_df], axis = 0)
    temp_df =  month_CA_pop_day.merge(df, how = 'left', on = 'safegraph_place_id')
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
    df_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/2020'+month+'.csv')
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))




        

df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/201901.csv',
                 index_col = 0)

for month in month_list[1:]:
    df_temp = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/2019'+month+'.csv',
                          index_col = 0)
    df = pd.concat([df,df_temp], axis= 0)
for month in month_list[0:2]:
    df_temp = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/2020'+month+'.csv',
                          index_col = 0)
    df = pd.concat([df,df_temp], axis= 0)

# Find the most crowded day
temp_df = df.groupby(['safegraph_place_id','index'])['visit'].sum()
temp_df = temp_df.reset_index()
temp_df = temp_df.set_index('index')
temp_df = temp_df.groupby(['safegraph_place_id'])['visit'].idxmax()
temp_df = temp_df.reset_index()
temp_df.groupby('visit').count()

temp_ind = (temp_df.loc[:,'visit'] == 'Friday') | (temp_df.loc[:,'visit'] == 'Saturday') | (temp_df.loc[:,'visit'] == 'Sunday')
temp_lists = temp_df.loc[temp_ind,:]

WorshipPlace = temp_lists.loc[:,['safegraph_place_id']]
WorshipPlace.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/WorshipPlace.csv')



