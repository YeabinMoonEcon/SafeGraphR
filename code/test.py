#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 17:50:31 2020

@author: yeabinmoon
"""


import pandas as pd
import time
import json



def MaxKey(dict_list):
    return max(dict_list, key = dict_list.get)


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

df_total = RelList.copy()

for month in month_list:    
    start_time = time.time()
    df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2019/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'popularity_by_day'])
        temp_df.rename(columns = {'raw_visitor_counts': '2019-'+month}, inplace = True)
        df = pd.concat([df,temp_df], axis = 0)
    temp_df = RelList.merge(df, how = 'left', on = 'safegraph_place_id')
    temp_df.dropna(inplace = True)
    temp_df.iloc[:,1] = temp_df.iloc[:,1].apply(json.loads)     
    temp_df.loc[:,'2019-'+month] = temp_df.iloc[:,1].apply(MaxKey)
    df_total = df_total.merge(temp_df[['safegraph_place_id','2019-'+month]],
                              how = 'left', on = 'safegraph_place_id')
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))

month = '01'
start_time = time.time()
df = pd.DataFrame()
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2020/' + month +'/' + file,
                          usecols = ['safegraph_place_id', 'popularity_by_day'])
    temp_df.rename(columns = {'raw_visitor_counts': '2020-'+month}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
temp_df = RelList.merge(df, how = 'left', on = 'safegraph_place_id')
temp_df.dropna(inplace = True)
temp_df.iloc[:,1] = temp_df.iloc[:,1].apply(json.loads)     
temp_df.loc[:,'2020-'+month] = temp_df.iloc[:,1].apply(MaxKey)
df_total = df_total.merge(temp_df[['safegraph_place_id','2020-'+month]],
                          how = 'left', on = 'safegraph_place_id')
print("Done",month,'!')
print("%f seconds" % (time.time() - start_time))

df_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/df_total.csv')


##################
df_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/df_total.csv',
                       index_col = 0)

for month in list(df_total.columns)[1:]:
    df_total.loc[:,month] = df_total.loc[:,month].replace({'Monday':1,'Tuesday':1,
                                                           'Wednesday':1,'Thursday':1,
                                                           'Friday':0,'Saturday':0,
                                                           'Sunday':0})
df_total.fillna(0, inplace = True)
df_total.loc[:,'ind'] = df_total.iloc[:,1:].sum(axis = 1 )

df_list = df_total.loc[df_total.loc[:,'ind'] <= 4,['safegraph_place_id']]

df_list_copy = df_list.copy()


for month in month_list:    
    start_time = time.time()
    df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2019/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'raw_visitor_counts'])
        temp_df.rename(columns = {'raw_visitor_counts': '2019-'+month}, inplace = True)
        df = pd.concat([df,temp_df], axis = 0)
    df_list_copy = df_list_copy.merge(df, how = 'left', on = 'safegraph_place_id')
    df_list_copy.rename(columns = {'raw_visitor_counts':'2019-'+month}, inplace = True)
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))

month = '01'
start_time = time.time()
df = pd.DataFrame()
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2020/' + month +'/' + file,
                          usecols = ['safegraph_place_id', 'raw_visitor_counts'])
    temp_df.rename(columns = {'raw_visitor_counts': '2020-'+month}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
df_list_copy = df_list_copy.merge(df, how = 'left', on = 'safegraph_place_id')
df_list_copy.rename(columns = {'raw_visitor_counts':'2020-'+month}, inplace = True)
print("Done",month,'!')
print("%f seconds" % (time.time() - start_time))

df_list_copy.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/df_list_copy.csv')

df_temp = df_list_copy.copy()
    
df_temp.fillna(0, inplace = True)
df_temp.loc[:,'num'] = (df_temp.iloc[:,1:].sum(axis = 1) - df_temp.iloc[:,1:].max(axis = 1) - df_temp.iloc[:,1:].min(axis = 1))/11
df = df_temp.loc[df_temp.loc[:,'num'] >= 15,:]

df = df[['safegraph_place_id', 'num']]

df.loc[:,'size'] = 0
df.loc[df.loc[:,'num'] > 79,'size'] =  1
df.groupby('size')['num'].sum()

df = df[['safegraph_place_id','size']]
df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/init_list.csv')

################

df_list = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/df_list_copy.csv',
                      index_col = 0)

#df_list = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/init_list.csv',
#                      index_col = 0)

df_list = df_list[['safegraph_place_id']]

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
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+week+'-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','raw_visitor_counts'])
    df_list = df_list.merge(temp_df, how = 'left', on = 'safegraph_place_id')
    df_list.rename(columns = {'raw_visitor_counts':week}, inplace = True)
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))

df_list.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/weekly.csv')

df_list = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/weekly.csv',index_col = 0)
df_list.fillna(0,inplace = True)

df_list.loc[:,'baseline'] = (df_list.iloc[:,2:11].sum(axis = 1) - df_list.iloc[:,2:11].max(axis = 1) - df_list.iloc[:,2:11].min(axis = 1))/7

temp = df_list.loc[df_list.loc[:,'baseline'] >= 15,:]

temp = temp[['safegraph_place_id','baseline']]

temp['size'] = 0
temp.loc[temp.loc[:,'baseline'] >= 45,'size'] = 1
temp.groupby('size')['baseline'].sum()

temp = temp[['safegraph_place_id','size']]
temp['size'].sum()

temp.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/temp.csv')

temp_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/temp.csv')

