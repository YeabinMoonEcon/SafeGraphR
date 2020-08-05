#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 22:51:52 2020

@author: yeabinmoon

output: HolyPois.csv

"""

import pandas as pd

cols_list = ['safegraph_place_id','location_name', 'safegraph_brand_ids', 
             'brands', 'naics_code', 'latitude', 'longitude', 'city', 'region', 
             'postal_code']

list_of_files = ['core_poi-part1.csv', 'core_poi-part2.csv', 'core_poi-part3.csv', 'core_poi-part4.csv','core_poi-part5.csv']

df_POI_NAICS = pd.DataFrame()


for file in list_of_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/CorePlaceUS/2020/07/Core-USA-July2020-Release-CORE_POI-2020_06-2020-07-13/'+file+'.gz',
                          compression = 'gzip',
                          usecols = cols_list,
                          dtype = {'naics_code':str, 'postal_code':str})
    df_POI_NAICS = pd.concat([df_POI_NAICS,temp_df], axis = 0, ignore_index = True)

HolyPois = df_POI_NAICS.loc[df_POI_NAICS.loc[:,'naics_code'] == '813110',:]

temp = HolyPois.iloc[0:11]

temp_df = pd.read_csv('/Volumes/LaCie/cg-data/placeToCBGMay/placeCountyCBG.csv',
                      dtype = {'CBGFIPS':str, 'stateFIPS':str, 'countyFIPS':str},
                      usecols = ['safegraph_place_id','stateFIPS', 'countyFIPS', 'countyName', 'CBGFIPS'])
temp_df.rename(columns = {'CBGFIPS':'poi_cbg'}, inplace = True)

HolyPois = HolyPois.merge(temp_df, how = 'left', on = 'safegraph_place_id')
HolyPois.drop(columns = 'naics_code', inplace = True)

HolyPois.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/HolyPois.csv')
