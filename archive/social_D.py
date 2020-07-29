#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:40:29 2020

@author: yeabinmoon
"""

import pandas as pd

zipcode = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx',
                     dtype = {'ZIP':str,'TRACT':str}, usecols = ['ZIP','TRACT'])

zip_unique = zipcode.loc[~zipcode.TRACT.duplicated(),:]


dtypes = {'origin_census_block_group':str}
cols = ['origin_census_block_group', 'device_count', 'distance_traveled_from_home',
        'completely_home_device_count','median_home_dwell_time',
        'part_time_work_behavior_devices','full_time_work_behavior_devices',
        'median_non_home_dwell_time','candidate_device_count',
        'median_percentage_time_home', ]


temp_df = pd.read_csv('/Volumes/LaCie/cg-data/SocialDistMetric/2020/01/01/2020-01-01-social-distancing.csv.gz',
                      compression = 'gzip', 
                      dtype = dtypes,
                      usecols = cols)
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
total_device = df_Alameda[['ZIP','device_count']]
home_device  = df_Alameda[['ZIP','completely_home_device_count']]
social_distancing = df_Alameda[['ZIP','distancing']]

total_device.rename(columns = {'device_count':'01-01'}, inplace = True)
home_device.rename(columns = {'completely_home_device_count':'01-01'}, inplace = True)
social_distancing.rename(columns = {'distancing':'01-01'}, inplace = True)




days = pd.date_range(start='1/1/2020', end='1/31/2020')
days = list(days.strftime('%d'))

for day in days[1:]:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/SocialDistMetric/2020/01/'+day+'/2020-01-'+ day +'-social-distancing.csv.gz',
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
    total_device.rename(columns = {'device_count':'01-'+day}, inplace = True)
    home_device.rename(columns = {'completely_home_device_count':'01-'+day}, inplace = True)
    social_distancing.rename(columns = {'distancing':'01-'+day}, inplace = True)
    