#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 23:50:04 2020

@author: yeabinmoon
"""

import pandas as pd

total_device = pd.read_csv('/Volumes/LaCie/cg-data/working_data/total_device.csv',
                           index_col = 0, dtype = {'ZIP':str})
home_device = pd.read_csv('/Volumes/LaCie/cg-data/working_data/home_device.csv',
                          index_col = 0, dtype = {'ZIP':str})
social_distancing = pd.read_csv('/Volumes/LaCie/cg-data/working_data/social_distancing.csv',
                                index_col = 0, dtype = {'ZIP':str})



Y = home_device[['ZIP','03-02','03-03','03-04','03-05','03-06',
                 '03-09','03-10','03-11','03-12','03-13',
                 '03-16','03-17','03-18','03-19','03-20',
                 '03-23','03-24','03-25','03-26','03-27',
                 '03-30','03-31','04-01','04-02','04-03',
                 '04-06','04-07','04-08','04-09','04-10',
                 '04-11','04-12','04-13']]
Y = Y.mean(axis = 1)


X1 = total_device[['ZIP','03-02','03-03','03-04','03-05','03-06',
                   '03-09','03-10','03-11','03-12','03-13',
                   '03-16','03-17','03-18','03-19','03-20',
                   '03-23','03-24','03-25','03-26','03-27',
                   '03-30','03-31','04-01','04-02','04-03',
                   '04-06','04-07','04-08','04-09','04-10',
                   '04-11','04-12','04-13']]












week_list = ['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
             '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17', 
             '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16', 
             '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
             '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
             '2020-05-18', '2020-05-25']
temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/2020-02-17-weekly-patterns.csv', 
                      index_col = 0, dtype = {'cbg':str,'year':str},nrows = 10)
