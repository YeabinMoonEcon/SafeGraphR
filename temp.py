#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 13:19:33 2020

@author: yeabinmoon

Data created:
    df_shutdown_percent.csv

"""


import pandas as pd

zipcode = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx',
                     dtype = {'ZIP':str,'TRACT':str}, usecols = ['ZIP','TRACT'])
BaseList = pd.read_csv('/Volumes/LaCie/cg-data/working_data/ClassificationCA.csv',
                       usecols = ['safegraph_place_id','shutdown', 'large'])



week_list = ['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
             '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17', 
             '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16', 
             '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
             '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
             '2020-05-18', '2020-05-25']


temp_df = pd.read_csv('/Volumes/LaCie/cg-data/working_data/temp/2019-12-30.csv', 
                      index_col = 0, dtype = {'cbg':str,'year':str})
temp_df.loc[:,'TRACT'] = temp_df.loc[:,'cbg'].str[:-1]
temp_df.loc[:,'FIPS']  = temp_df.loc[:,'cbg'].str[0:5]
temp_df.loc[:,'date']  = temp_df.loc[:,'year'] +'-'+ temp_df.loc[:,'week']
temp_df = temp_df.loc[temp_df.FIPS == '06001',:]
temp_df = temp_df.merge(zipcode, how = 'left', on = 'TRACT')
temp_df = temp_df[['date','ZIP','safegraph_place_id','large','shutdown','visits']]

temp_df_total = temp_df[['date','ZIP','safegraph_place_id','visits']]
temp_df_total = temp_df_total.groupby('ZIP')['visits'].sum()
temp_df_total = temp_df_total.reset_index()
temp_df_total.rename(columns = {'visits':'total'}, inplace = True)

temp_df_shutdown = temp_df.loc[temp_df.shutdown == 1,['date','ZIP','safegraph_place_id','visits']]
temp_df_shutdown = temp_df_shutdown.groupby('ZIP')['visits'].sum()
temp_df_shutdown = temp_df_shutdown.reset_index()
temp_df_shutdown.rename(columns = {'visits':'shutdown'}, inplace = True)

temp_df_total = temp_df_total.merge(temp_df_shutdown, how = 'left', on = 'ZIP')
temp_df_total.fillna(0,inplace = True)
temp_df_total['2019-12-30'] = temp_df_total['shutdown'] / temp_df_total['total'] * 100

df = temp_df_total[['ZIP', '2019-12-30']]

for wk in week_list[1:]:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/working_data/temp/'+ wk + '.csv',
                          index_col = 0, dtype = {'cbg':str,'year':str})
    temp_df.loc[:,'TRACT'] = temp_df.loc[:,'cbg'].str[:-1]
    temp_df.loc[:,'FIPS']  = temp_df.loc[:,'cbg'].str[0:5]
    temp_df.loc[:,'date']  = temp_df.loc[:,'year'] +'-'+ temp_df.loc[:,'week']
    temp_df = temp_df.loc[temp_df.FIPS == '06001',:]
    temp_df = temp_df.merge(zipcode, how = 'left', on = 'TRACT')
    temp_df = temp_df[['date','ZIP','safegraph_place_id','large','shutdown','visits']]

    temp_df_total = temp_df[['date','ZIP','safegraph_place_id','visits']]
    temp_df_total = temp_df_total.groupby('ZIP')['visits'].sum()
    temp_df_total = temp_df_total.reset_index()
    temp_df_total.rename(columns = {'visits':'total'}, inplace = True)
    
    temp_df_shutdown = temp_df.loc[temp_df.shutdown == 1,['date','ZIP','safegraph_place_id','visits']]
    temp_df_shutdown = temp_df_shutdown.groupby('ZIP')['visits'].sum()
    temp_df_shutdown = temp_df_shutdown.reset_index()
    temp_df_shutdown.rename(columns = {'visits':'shutdown'}, inplace = True)
    
    temp_df_total = temp_df_total.merge(temp_df_shutdown, how = 'left', on = 'ZIP')
    temp_df_total.fillna(0,inplace = True)
    temp_df_total[wk] = temp_df_total['shutdown'] / temp_df_total['total'] * 100
    temp = temp_df_total[['ZIP', wk]]
    
    df = df.merge(temp, how = 'outer', on = 'ZIP')
df.fillna(0, inplace = True)
df_shutdown_percent = df.copy()
df_shutdown_percent.to_csv('/Volumes/LaCie/cg-data/working_data/df_shutdown_percent.csv')






df = pd.read_csv('/Volumes/LaCie/cg-data/working_data/RegionDist.csv',
                 index_col = 0, dtype = {'cbg':str,'year':str})
df.loc[:,'TRACT'] = df.loc[:,'cbg'].str[:-1]
df.loc[:,'FIPS']  = df.loc[:,'cbg'].str[0:5]
df.loc[:,'date']  = df.loc[:,'year'] +'-'+ df.loc[:,'week']

AlamedaCounty = df.loc[df.FIPS == '06001',:]
AlamedaCounty = AlamedaCounty.merge(zipcode, how = 'left', on = 'TRACT')
AlamedaCounty = AlamedaCounty[['date','ZIP','safegraph_place_id','large','shutdown','visits']]

total = AlamedaCounty.groupby(['date', 'ZIP'])['visits'].sum()
total = total.reset_index()
total = total.pivot(index= 'ZIP', columns = 'date', values = 'visits')
total.to_csv('/Volumes/LaCie/cg-data/working_data/total.csv')

shutdown = AlamedaCounty.loc[AlamedaCounty.shutdown == 1,:]
shutdown = shutdown.groupby(['date', 'ZIP'])['visits'].sum()
shutdown = shutdown.reset_index()
shutdown = shutdown.pivot(index= 'ZIP', columns = 'date', values = 'visits')
shutdown.fillna(0, inplace = True)
shutdown.to_csv('/Volumes/LaCie/cg-data/working_data/shutdown.csv')

Open = AlamedaCounty.loc[AlamedaCounty.shutdown == 0,:]
Open = Open.groupby(['date', 'ZIP'])['visits'].sum()
Open = Open.reset_index()
Open = Open.pivot(index= 'ZIP', columns = 'date', values = 'visits')
Open.fillna(0, inplace = True)
Open.to_csv('/Volumes/LaCie/cg-data/working_data/Open.csv')
