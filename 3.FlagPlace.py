#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 15:28:30 2020

@author: yeabinmoon
"""

import pandas as pd
import json
import time

def sum_dict(inline_data):
    return sum(inline_data.values())


raw_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/df_CA_Reli_raw.csv',
                     index_col = 0, dtype ={'postal_code':str, 'stateFIPS':str,
                                            'countyFIPS':str, 'poi_cbg':str})

WorshipPlace = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/WorshipPlace.csv'
                           , index_col=0)

WorshipPlace = WorshipPlace.merge(raw_df, how = 'left', on = 'safegraph_place_id')


week_list = ['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
             '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17',
             '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16',
             '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
             '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
             '2020-05-18', '2020-05-25', '2020-06-01', '2020-06-08',
             '2020-06-15']



data_uni_visits = WorshipPlace.copy()
data_dict_total = WorshipPlace.copy()
data_rate = WorshipPlace.copy()
data_flag_info = WorshipPlace.copy()

for week in week_list:     
    start_time = time.time()
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+week+'-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','raw_visitor_counts', 'visitor_home_cbgs'])
    temp_df['raw_visitor_counts'] = temp_df['raw_visitor_counts'].astype(int)
    temp_df['raw_visitor_counts'] = pd.to_numeric(temp_df['raw_visitor_counts'], downcast = 'integer')
    temp_df.loc[:,'visitor_home_cbgs'] = temp_df.loc[:,'visitor_home_cbgs'].apply(json.loads)
    temp_df = temp_df.loc[temp_df.loc[:,'visitor_home_cbgs'].apply(len) != 0, :]
    temp_df.loc[:,'sum_dict'] = temp_df.loc[:,'visitor_home_cbgs'].apply(sum_dict)
    temp_df.loc[:,'rate'] = temp_df.loc[:,'sum_dict'] / temp_df.loc[:,'raw_visitor_counts']
    temp_df.loc[:,'flag'] = 0    
    temp = temp_df.loc[:,'rate'] > 1
    temp_df.loc[temp,'flag'] = 1
    
    data_uni_visits = data_uni_visits.merge(temp_df[['safegraph_place_id','raw_visitor_counts']],
                                            how = 'left', on = 'safegraph_place_id')
    data_uni_visits.rename(columns = {'raw_visitor_counts':week}, inplace = True)
    data_dict_total = data_dict_total.merge(temp_df[['safegraph_place_id','sum_dict']],
                                            how = 'left', on = 'safegraph_place_id')
    data_dict_total.rename(columns = {'sum_dict':week}, inplace = True)
    data_rate = data_rate.merge(temp_df[['safegraph_place_id','rate']],
                                            how = 'left', on = 'safegraph_place_id')
    data_rate.rename(columns = {'rate':week}, inplace = True)
    data_flag_info = data_flag_info.merge(temp_df[['safegraph_place_id','flag']],
                                            how = 'left', on = 'safegraph_place_id')
    data_flag_info.rename(columns = {'flag':week}, inplace = True)      
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))

    
data_uni_visits.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/data_uni_visits.csv')
data_dict_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/data_dict_total.csv') 
data_rate.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/data_rate.csv') 
data_flag_info.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/data_flag_info.csv')
