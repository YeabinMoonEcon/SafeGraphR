#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 18:15:10 2020

Census tract (or block) is usually the smallest block of the regions, 
but even within the same POI there could be multiple ZIPCODE. 
Here, as a temporary, use the smallest zipcode (number). 

@author: yeabinmoon
"""


import pandas as pd

zipcode = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx',
                     dtype = {'ZIP':str,'TRACT':str}, usecols = ['ZIP','TRACT'])

zip_unique = zipcode.loc[~zipcode.TRACT.duplicated(),:]





df = pd.read_csv('/Volumes/LaCie/cg-data/working_data/RegionDist.csv',
                 index_col = 0, dtype = {'cbg':str,'year':str})
df.loc[:,'TRACT'] = df.loc[:,'cbg'].str[:-1]
df.loc[:,'FIPS']  = df.loc[:,'cbg'].str[0:5]
df.loc[:,'date']  = df.loc[:,'year'] +'-'+ df.loc[:,'week']

AlamedaCounty = df.loc[df.FIPS == '06001',:]
AlamedaCounty = AlamedaCounty.merge(zip_unique, how = 'left', on = 'TRACT')
AlamedaCounty = AlamedaCounty[['date','ZIP','safegraph_place_id','large','shutdown','visits']]

total = AlamedaCounty.groupby(['date', 'ZIP'])['visits'].sum()
total = total.reset_index()
total = total.pivot(index= 'ZIP', columns = 'date', values = 'visits')
total.fillna(0, inplace = True)

shutdown = AlamedaCounty.loc[AlamedaCounty.shutdown == 1,:]
shutdown = shutdown.groupby(['date', 'ZIP'])['visits'].sum()
shutdown = shutdown.reset_index()
shutdown = shutdown.pivot(index= 'ZIP', columns = 'date', values = 'visits')
shutdown.fillna(0, inplace = True)

Open = AlamedaCounty.loc[AlamedaCounty.shutdown == 0,:]
Open = Open.groupby(['date', 'ZIP'])['visits'].sum()
Open = Open.reset_index()
Open = Open.pivot(index= 'ZIP', columns = 'date', values = 'visits')
Open.fillna(0, inplace = True)

large = AlamedaCounty.loc[AlamedaCounty.large == 1,:]
large = large.groupby(['date', 'ZIP'])['visits'].sum()
large = large.reset_index()
large = large.pivot(index= 'ZIP', columns = 'date', values = 'visits')
large.fillna(0, inplace = True)

total.loc[:,'before'] = total.iloc[:,0:8].mean(axis = 1)
total.loc[:,'after'] = total.iloc[:,9:15].min(axis = 1)
total.loc[:,'instrument'] = (large.iloc[:,0:8] / total.iloc[:,0:8]).mean(axis = 1)

total.iloc[:, 0:8]

df_reg = total[['before','after','instrument']]
df_reg.reset_index(inplace = True)
df_reg.fillna(0, inplace = True)
df_reg.to_csv('/Volumes/LaCie/cg-data/working_data/df_reg.csv')


total.reset_index(inplace = True)
