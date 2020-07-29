#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 16:33:48 2020

@author: yeabinmoon

Data created:
    listwithsize1.csv: size with larger num of POIS
    listwithsize2.csv: size with smaller num of POIS
    Dividing line is 40

"""

import pandas as pd


raw_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/df_CA_Reli_raw.csv',
                     index_col = 0, dtype ={'postal_code':str, 'stateFIPS':str,
                                            'countyFIPS':str, 'poi_cbg':str})


data_uni_visits = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/data_uni_visits.csv',
                              index_col = 0)
selected_POIs1 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/selected_POIs.csv',
                             index_col = 0, dtype = {'postal_code':str, 'poi_cbg':str})
selected_POIs1 = selected_POIs1[['safegraph_place_id']]
selected_POIs1 = selected_POIs1.merge(data_uni_visits, how = 'left', on = 'safegraph_place_id')

selected_POIs2 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/selected_POIs_2.csv',
                              index_col = 0, dtype = {'postal_code':str, 'poi_cbg':str})
selected_POIs2 = selected_POIs2[['safegraph_place_id']]
selected_POIs2 = selected_POIs2.merge(data_uni_visits, how = 'left', on = 'safegraph_place_id')


selected_POIs1.fillna(0,inplace = True)
selected_POIs1.loc[:,'base'] = selected_POIs1.iloc[:,1:].mean(axis = 1)
selected_POIs1.loc[:,'base'].quantile([.1,.25, .5, .75, .9])
selected_POIs1.loc[:,'base'].mean()
selected_POIs1.loc[:,'base'].max()
selected_POIs1.loc[:,'size'] = 0
selected_POIs1.loc[selected_POIs1.loc[:,'base'] >= 40, 'size'] = 1
selected_POIs1.groupby('size')['base'].sum()
selected_POIs1 = selected_POIs1[['safegraph_place_id', 'size']]
selected_POIs1 = selected_POIs1.merge(raw_df, how = 'left', on = 'safegraph_place_id')
selected_POIs1.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/listwithsize1.csv')

selected_POIs2.fillna(0,inplace = True)
selected_POIs2.loc[:,'base'] = selected_POIs2.iloc[:,1:].mean(axis = 1)
selected_POIs2.loc[:,'base'].quantile([.1,.25, .5, .75, .9])
selected_POIs2.loc[:,'base'].mean()
selected_POIs2.loc[:,'base'].max()
selected_POIs2.loc[:,'size'] = 0
selected_POIs2.loc[selected_POIs2.loc[:,'base'] >= 40, 'size'] = 1
selected_POIs2.groupby('size')['base'].sum()
selected_POIs2 = selected_POIs2[['safegraph_place_id', 'size']]
selected_POIs2 = selected_POIs2.merge(raw_df, how = 'left', on = 'safegraph_place_id')
selected_POIs2.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/listwithsize2.csv')
