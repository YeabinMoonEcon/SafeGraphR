#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 21:41:17 2020

@author: yeabinmoon

Data created:
    total_device.csv: total number of device by zipcode
    home_device.csv:  total number of device staying at home by zipcode
    social_distancing.csv: proportion of device staying at home by zipcode
    

"""


import pandas as pd
import time

zipcode = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx',
                     dtype = {'ZIP':str,'TRACT':str}, usecols = ['ZIP','TRACT'])

zip_unique = zipcode.loc[~zipcode.TRACT.duplicated(),:]


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

temp_df_Alameda = temp_df.loc[temp_df.FIPS == '06001',:]
temp_df_Alameda = temp_df_Alameda.merge(zip_unique, how = 'left', on = 'TRACT')

temp = temp_df_Alameda.groupby('ZIP')['device_count'].sum()
temp = temp.reset_index()
temp = temp.loc[:,['ZIP']]

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
        temp_df['TRACT'] = temp_df.origin_census_block_group.str[:-1]
        temp_df['FIPS'] = temp_df.origin_census_block_group.str[0:5]

        temp_df_Alameda = temp_df.loc[temp_df.FIPS == '06001',:]
        temp_df_Alameda = temp_df_Alameda.merge(zip_unique, how = 'left', on = 'TRACT')
        df_Alameda = temp_df_Alameda[['ZIP', 'device_count', 'completely_home_device_count',
                                      'part_time_work_behavior_devices', 'full_time_work_behavior_devices',
                                      'candidate_device_count']]
        df_Alameda = df_Alameda.groupby('ZIP')['device_count', 'completely_home_device_count',
                                               'part_time_work_behavior_devices', 'full_time_work_behavior_devices',
                                               'candidate_device_count'].sum()
        df_Alameda.reset_index(inplace = True)
        df_Alameda.loc[:,'distancing'] = df_Alameda.loc[:,'completely_home_device_count'] / df_Alameda.loc[:,'device_count']
        temp_total_device = df_Alameda[['ZIP','device_count']]
        temp_home_device  = df_Alameda[['ZIP','completely_home_device_count']]
        temp_social_distancing = df_Alameda[['ZIP','distancing']]

        total_device = total_device.merge(temp_total_device, how = 'outer', on = 'ZIP')
        home_device  = home_device.merge(temp_home_device, how = 'outer', on = 'ZIP')
        social_distancing = social_distancing.merge(temp_social_distancing, how = 'outer', on = 'ZIP')
        total_device.rename(columns = {'device_count': month+'-'+day}, inplace = True)
        home_device.rename(columns = {'completely_home_device_count':month+'-'+day}, inplace = True)
        social_distancing.rename(columns = {'distancing':month+'-'+day}, inplace = True)
    i += 1
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))

total_device.to_csv('/Volumes/LaCie/cg-data/working_data/total_device.csv')
home_device.to_csv('/Volumes/LaCie/cg-data/working_data/home_device.csv')
social_distancing.to_csv('/Volumes/LaCie/cg-data/working_data/social_distancing.csv')
