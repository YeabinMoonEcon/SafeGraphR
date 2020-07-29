#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 18:42:22 2020

@author: yeabinmoon
"""

import pandas as pd

data_uni_visits = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/data_uni_visits.csv',
                              index_col = 0, dtype = {'postal_code':str,
                                                      'stateFIPS':str,
                                                      'countyFIPS':str,
                                                      'poi_cbg':str})
data_dict_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/data_dict_total.csv',
                              index_col = 0, dtype = {'postal_code':str, 'stateFIPS':str,
                                                      'countyFIPS':str, 'poi_cbg':str})
                                                      
data_rate = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/data_rate.csv',
                        index_col = 0, dtype = {'postal_code':str, 'stateFIPS':str,
                                                'countyFIPS':str, 'poi_cbg':str})
                                               
data_flag_info = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/data_flag_info.csv',
                             index_col = 0, dtype = {'postal_code':str, 'stateFIPS':str,
                                                     'countyFIPS':str, 'poi_cbg':str})

temp_df = data_rate.copy()
temp_df.fillna(0, inplace = True)
temp_df.loc[:,'ind'] = temp_df.iloc[:,11:19].mean(axis= 1)

temp_df = temp_df.loc[(temp_df.loc[:,'ind'] >= .7) ,:]

temp_df1 = temp_df.loc[temp_df.iloc[:,11:19].mean(axis= 1) <= 1, :]
temp_df2 = temp_df.loc[temp_df.iloc[:,11:19].min(axis= 1) <= 1, :]

temp_df1 = temp_df1.iloc[:,:11]
temp_df2 = temp_df2.iloc[:,:11]

data_uni_visits.drop(columns = {'location_name', 'latitude', 'longitude', 'city',
                                'region', 'postal_code', 'stateFIPS', 'countyFIPS', 
                                'countyName','poi_cbg'}, inplace = True)
       

temp_df1 = temp_df1.merge(data_uni_visits, how = 'left', on = 'safegraph_place_id')
