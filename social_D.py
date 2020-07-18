#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:40:29 2020

@author: yeabinmoon
"""

import pandas as pd

zipcode = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx',
                     dtype = {'ZIP':str,'TRACT':str}, usecols = ['ZIP','TRACT'])


dtypes = {'origin_census_block_group':str}
cols = ['origin_census_block_group', 'device_count', 'distance_traveled_from_home',
        'completely_home_device_count','median_home_dwell_time',
        'part_time_work_behavior_devices','full_time_work_behavior_devices',
        'median_non_home_dwell_time','candidate_device_count',
        'median_percentage_time_home', ]


temp_df = pd.read_csv('/Volumes/LaCie/cg-data/SocialDistMetric/2020/01/01/2020-01-01-social-distancing.csv.gz',
                      compression = 'gzip', 
                      dtype = dtypes,
                      usecols = cols,
                      nrows = 1000)
temp_df['TRACT'] = temp_df.origin_census_block_group.str[:-1]
temp_df['FIPS'] = temp_df.origin_census_block_group.str[0:5]

temp_df_Alameda = temp_df.loc[temp_df.FIPS == '06001',:]


df = temp_df_Alameda.merge(zipcode, how = 'left', on = 'TRACT')
temp_df_Alameda.duplicated()


test = zipcode.iloc[0:10]
zipcode.loc[zipcode.TRACT == '06001407500',:]

zipcode.loc[zipcode.ZIP == '94601',:]
