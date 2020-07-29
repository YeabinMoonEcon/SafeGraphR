#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 20:24:47 2020

@author: yeabinmoon
"""

import pandas as pd
import time

dtypes = {'origin_census_block_group':str}
cols = ['origin_census_block_group', 'device_count', 'distance_traveled_from_home',
        'completely_home_device_count','median_home_dwell_time',
        'part_time_work_behavior_devices','full_time_work_behavior_devices',
        'median_non_home_dwell_time','candidate_device_count',
        'median_percentage_time_home']


temp_df = pd.read_csv('/Volumes/LaCie/cg-data/SocialDistMetric/2020/01/01/2020-01-01-social-distancing.csv.gz',
                      compression = 'gzip',
                      dtype = dtypes,
                      usecols = cols)
temp_df['TRACT'] = temp_df.origin_census_block_group.str[:-1]
temp_df['FIPS'] = temp_df.origin_census_block_group.str[0:5]

temp = (temp_df.FIPS == '06001') | (temp_df.FIPS == '06075')

temp_df_ALSF = temp_df.loc[temp , :]

temp = temp_df_ALSF.groupby('origin_census_block_group')['device_count'].sum()
temp = temp.reset_index()
temp = temp.loc[:,['origin_census_block_group']]

total_device = temp.copy()
home_device  = temp.copy()
social_distancing = temp.copy()

months = ['01', '02', '03', '04', '05', '06']

day1 = pd.date_range(start='1/1/2020', end='1/31/2020')
day1 = list(day1.strftime('%d'))
day2 = pd.date_range(start='2/1/2020', end='2/29/2020')
day2 = list(day2.strftime('%d'))
day3 = pd.date_range(start='3/1/2020', end='3/31/2020')
day3 = list(day3.strftime('%d'))
day4 = pd.date_range(start='4/1/2020', end='4/30/2020')
day4 = list(day4.strftime('%d'))
day5 = pd.date_range(start='5/1/2020', end='5/31/2020')
day5 = list(day5.strftime('%d'))
day6 = pd.date_range(start='6/1/2020', end='6/30/2020')
day6 = list(day6.strftime('%d'))
days = [day1, day2, day3, day4, day5, day6]


i = 0
for month in months:
    
    start_time = time.time()
    for day in days[i]:
                       
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/SocialDistMetric/2020/'+month+'/'+day+'/2020-' +month + '-' + day +'-social-distancing.csv.gz',
                              compression = 'gzip', dtype = dtypes, usecols = cols)
        temp_df['FIPS'] = temp_df.origin_census_block_group.str[0:5]
        temp = (temp_df.FIPS == '06001') | (temp_df.FIPS == '06075')
        temp_df_ALSF = temp_df.loc[temp , :]
        temp_df_ALSF = temp_df_ALSF[['origin_census_block_group', 'device_count', 'completely_home_device_count',
                                     'part_time_work_behavior_devices', 'full_time_work_behavior_devices',
                                     'candidate_device_count']]
        temp_df_ALSF = temp_df_ALSF.groupby('origin_census_block_group')['device_count', 'completely_home_device_count',
                                                                         'part_time_work_behavior_devices', 'full_time_work_behavior_devices',
                                                                         'candidate_device_count'].sum()
        temp_df_ALSF.reset_index(inplace = True)
        temp_df_ALSF.loc[:,'distancing'] = temp_df_ALSF.loc[:,'completely_home_device_count'] / temp_df_ALSF.loc[:,'device_count']
        
        temp_total_device = temp_df_ALSF[['origin_census_block_group','device_count']]
        temp_home_device  = temp_df_ALSF[['origin_census_block_group','completely_home_device_count']]
        temp_social_distancing = temp_df_ALSF[['origin_census_block_group','distancing']]
        
        total_device = total_device.merge(temp_total_device, how = 'outer', on = 'origin_census_block_group')
        home_device  = home_device.merge(temp_home_device, how = 'outer', on = 'origin_census_block_group')
        social_distancing = social_distancing.merge(temp_social_distancing, how = 'outer', on = 'origin_census_block_group')
        total_device.rename(columns = {'device_count': month+'-'+day}, inplace = True)
        home_device.rename(columns = {'completely_home_device_count':month+'-'+day}, inplace = True)
        social_distancing.rename(columns = {'distancing':month+'-'+day}, inplace = True)
    i += 1
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))
    
total_device.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/total_device.csv')
home_device.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/home_device.csv')
social_distancing.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/social_distancing.csv')
