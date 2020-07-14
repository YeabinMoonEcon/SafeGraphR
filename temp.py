#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 13:19:33 2020

@author: yeabinmoon
"""


import pandas as pd

zipcode = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx',
                     dtype = {'ZIP':str,'TRACT':str}, usecols = ['ZIP','TRACT'])
BaseList = pd.read_csv('/Volumes/LaCie/cg-data/working_data/ClassificationCA.csv',
                       usecols = ['safegraph_place_id','shutdown', 'large'])



df = pd.read_csv('/Volumes/LaCie/cg-data/working_data/RegionDist.csv',
                 index_col = 0, dtype = {'cbg':str,'year':str})
df.loc[:,'TRACT'] = df.loc[:,'cbg'].str[:-1]
df.loc[:,'FIPS']  = df.loc[:,'cbg'].str[0:5]
df.loc[:,'date']  = df.loc[:,'year'] +'-'+ df.loc[:,'week']

AlamedaCounty = df.loc[df.FIPS == '06001',:]
AlamedaCounty = AlamedaCounty.merge(zipcode, how = 'left', on = 'TRACT')
AlamedaCounty = AlamedaCounty[['date','ZIP','safegraph_place_id','large','shutdown','visits']]
