#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 23:16:49 2020

@author: yeabinmoon
"""

import pandas as pd
import time

week_list = ['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
             '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17',
             '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16',
             '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
             '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
             '2020-05-18', '2020-05-25', '2020-06-01', '2020-06-08',
             '2020-06-15']

used = ['safegraph_place_id', 'location_name', 'city', 'region']

HolyPois = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/HolyPois.csv',
                       usecols = used)

for week in week_list:
    start_time = time.time()
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+week+'-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','raw_visitor_counts'])
    temp_df['raw_visitor_counts'] = temp_df['raw_visitor_counts'].astype(int)
    temp_df['raw_visitor_counts'] = pd.to_numeric(temp_df['raw_visitor_counts'], downcast = 'integer')
    temp_df.rename(columns = {'raw_visitor_counts': week}, inplace = True)
    HolyPois = HolyPois.merge(temp_df, how = 'left', on = 'safegraph_place_id')
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))
HolyPois.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/HolyPois.csv')


test = HolyPois[HolyPois.region == 'WA']
