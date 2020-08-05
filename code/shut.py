#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 15:18:43 2020

@author: yeabinmoon
"""
import time
import pandas as pd

BaseList = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/temp_list2.csv',
                       index_col = 0)

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
    BaseList = BaseList.merge(temp_df, how = 'left', on = 'safegraph_place_id')
    BaseList.rename(columns = {'raw_visitor_counts':week}, inplace = True)
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))
