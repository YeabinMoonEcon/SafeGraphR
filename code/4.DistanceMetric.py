#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 15:36:51 2020

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
#temp_df['TRACT'] = temp_df.origin_census_block_group.str[:-1]
temp_df['STATE'] = temp_df.origin_census_block_group.str[0:2]


state_ind = (temp_df.loc[:,'STATE'] == '48') | (temp_df.loc[:,'STATE'] == '06') \
        | (temp_df.loc[:,'STATE'] == '17') | (temp_df.loc[:,'STATE'] == '12') \

temp4states = temp_df.loc[state_ind , :]

temp = temp4states.groupby('origin_census_block_group')['device_count'].sum()
temp = temp.reset_index()
temp = temp.loc[:,['origin_census_block_group']]

device_total = temp.copy()
device_home  = temp.copy()
device_rate  = temp.copy()
device_part  = temp.copy()
device_full  = temp.copy()

months = ['11', '12']
day1 = pd.date_range(start='11/25/2019', end='11/30/2019')
day1 = list(day1.strftime('%d'))
day2 = pd.date_range(start='12/1/2019', end='12/31/2019')
day2 = list(day2.strftime('%d'))
days = [day1, day2]

i = 0
for month in months:
    start_time = time.time()
    
    for day in days[i]:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/SocialDistMetric/2019/'+month+'/'+day+'/2019-' +month + '-' + day +'-social-distancing.csv.gz',
                              compression = 'gzip', dtype = dtypes, usecols = cols)
        temp_df['STATE'] = temp_df.origin_census_block_group.str[0:2]
        state_ind = (temp_df.loc[:,'STATE'] == '48') | (temp_df.loc[:,'STATE'] == '06') \
                    | (temp_df.loc[:,'STATE'] == '17') | (temp_df.loc[:,'STATE'] == '12') 
        temp4states = temp_df.loc[state_ind , :]
        temp4states = temp4states[['origin_census_block_group', 'device_count', 'completely_home_device_count',
                                   'part_time_work_behavior_devices', 'full_time_work_behavior_devices',
                                   'candidate_device_count']]
        temp4states = temp4states.groupby('origin_census_block_group')['device_count', 'completely_home_device_count',
                                                                       'part_time_work_behavior_devices', 'full_time_work_behavior_devices',
                                                                       'candidate_device_count'].sum()
        temp4states.reset_index(inplace = True)
        temp4states.loc[:,'distancing'] = temp4states.loc[:,'completely_home_device_count'] / temp4states.loc[:,'device_count']

        temp_total_device = temp4states[['origin_census_block_group','device_count']]
        temp_home_device  = temp4states[['origin_census_block_group','completely_home_device_count']]
        temp_social_distancing = temp4states[['origin_census_block_group','distancing']]
        
        temp_parttime = temp4states[['origin_census_block_group','part_time_work_behavior_devices']]
        temp_fulltime = temp4states[['origin_census_block_group','full_time_work_behavior_devices']]
        
        device_total = device_total.merge(temp_total_device, how = 'outer', on = 'origin_census_block_group')
        device_home  = device_home.merge(temp_home_device, how = 'outer', on = 'origin_census_block_group')
        device_rate = device_rate.merge(temp_social_distancing, how = 'outer', on = 'origin_census_block_group')
        device_part = device_part.merge(temp_parttime, how = 'outer', on = 'origin_census_block_group')
        device_full = device_full.merge(temp_fulltime, how = 'outer', on = 'origin_census_block_group')
        
        device_total.rename(columns = {'device_count': '2019-'+month+'-'+day}, inplace = True)
        device_home.rename(columns = {'completely_home_device_count':'2019-'+month+'-'+day}, inplace = True)
        device_rate.rename(columns = {'distancing':'2019-'+month+'-'+day}, inplace = True)
        device_part.rename(columns = {'part_time_work_behavior_devices':'2019-'+month+'-'+day}, inplace = True)
        device_full.rename(columns = {'full_time_work_behavior_devices':'2019-'+month+'-'+day}, inplace = True)
    i += 1
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))





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
        temp_df['STATE'] = temp_df.origin_census_block_group.str[0:2]
        state_ind = (temp_df.loc[:,'STATE'] == '48') | (temp_df.loc[:,'STATE'] == '06') \
                    | (temp_df.loc[:,'STATE'] == '17') | (temp_df.loc[:,'STATE'] == '12') 
        temp4states = temp_df.loc[state_ind , :]
        temp4states = temp4states[['origin_census_block_group', 'device_count', 'completely_home_device_count',
                                   'part_time_work_behavior_devices', 'full_time_work_behavior_devices',
                                   'candidate_device_count']]
        temp4states = temp4states.groupby('origin_census_block_group')['device_count', 'completely_home_device_count',
                                                                       'part_time_work_behavior_devices', 'full_time_work_behavior_devices',
                                                                       'candidate_device_count'].sum()
        temp4states.reset_index(inplace = True)
        temp4states.loc[:,'distancing'] = temp4states.loc[:,'completely_home_device_count'] / temp4states.loc[:,'device_count']

        temp_total_device = temp4states[['origin_census_block_group','device_count']]
        temp_home_device  = temp4states[['origin_census_block_group','completely_home_device_count']]
        temp_social_distancing = temp4states[['origin_census_block_group','distancing']]
        
        temp_parttime = temp4states[['origin_census_block_group','part_time_work_behavior_devices']]
        temp_fulltime = temp4states[['origin_census_block_group','full_time_work_behavior_devices']]
        
        device_total = device_total.merge(temp_total_device, how = 'outer', on = 'origin_census_block_group')
        device_home  = device_home.merge(temp_home_device, how = 'outer', on = 'origin_census_block_group')
        device_rate = device_rate.merge(temp_social_distancing, how = 'outer', on = 'origin_census_block_group')
        device_part = device_part.merge(temp_parttime, how = 'outer', on = 'origin_census_block_group')
        device_full = device_full.merge(temp_fulltime, how = 'outer', on = 'origin_census_block_group')
        
        device_total.rename(columns = {'device_count': '2020-'+month+'-'+day}, inplace = True)
        device_home.rename(columns = {'completely_home_device_count':'2020-'+month+'-'+day}, inplace = True)
        device_rate.rename(columns = {'distancing':'2020-'+month+'-'+day}, inplace = True)
        device_part.rename(columns = {'part_time_work_behavior_devices':'2020-'+month+'-'+day}, inplace = True)
        device_full.rename(columns = {'full_time_work_behavior_devices':'2020-'+month+'-'+day}, inplace = True)
    i += 1
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))
    
device_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/device_total.csv')
device_home.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/device_home.csv')
device_rate.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/device_rate.csv')
device_part.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/device_part.csv')
device_full.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/device_full.csv')
