#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 21:33:21 2020

@author: yeabinmoon
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def state_filter(indata):
    temp = (indata.loc[:,'state'] == '06') | (indata.loc[:,'state'] == '12') | (indata.loc[:,'state'] == '17') | (indata.loc[:,'state'] == '48')
    return indata.loc[temp,:]




visits_total_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/visits_total_county.csv', 
                                  index_col = 0, dtype = {'FIPS':str})
visits_large_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/visits_large_county.csv',
                                  index_col = 0, dtype = {'FIPS':str})
large_share_county  = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/large_share_county.csv',
                                  index_col = 0, dtype = {'FIPS':str})


visits_total_county.loc[:,'state'] = visits_total_county.loc[:,'FIPS'].str[0:2]
visits_large_county.loc[:,'state'] = visits_large_county.loc[:,'FIPS'].str[0:2]
large_share_county.loc[:,'state']  = large_share_county.loc[:,'FIPS'].str[0:2]

large_share_county.columns[1:31]


visits_total_county = state_filter(visits_total_county)
visits_large_county = state_filter(visits_large_county)
large_share_county = state_filter(large_share_county)



url = 'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv'
temp_df = pd.read_csv(url, dtype = {'STATE':str,'COUNTY':str}, usecols = ['STATE','COUNTY','POPESTIMATE2019'])
temp_df.loc[:,'FIPS'] = temp_df.loc[:,'STATE'] + temp_df.loc[:,'COUNTY']

county_pop = pd.DataFrame()
temp = large_share_county['FIPS']

for i in temp:
    temp_list = temp_df.loc[temp_df.loc[:,'FIPS'] == i,:]
    county_pop = pd.concat([county_pop,temp_list], axis = 0)
    
device_total_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/device_total_county.csv',
                                  index_col = 0, dtype = {'FIPS':str})
device_total_county.loc[:,'base_device']= device_total_county.iloc[:,1:32].mean(axis = 1)
base_device = device_total_county[['FIPS', 'base_device']]

county_pop = county_pop[['FIPS', 'POPESTIMATE2019']]
county_pop = county_pop.merge(base_device, how = 'left', on = 'FIPS')
teat = county_pop.set_index('FIPS')
teat.corr()


teat.loc[:,'rate'] = teat.loc[:,'POPESTIMATE2019'] / teat.loc[:,'base_device']  


temp_df = visits_total_county.merge(base_device, how = 'left', on = 'FIPS')

for i in range(30):
    temp_df.iloc[:,i+1] = temp_df.iloc[:,i+1] / temp_df.iloc[:,-1] * 100


temp_df.loc[:,'base_exposure'] = temp_df.iloc[:,1:10].mean(axis = 1)
temp_df.set_index('FIPS', inplace = True)

exposure = temp_df.iloc[:,9:]

for i in range(21):
    exposure.iloc[:,i] = exposure.iloc[:,-1] - exposure.iloc[:,i]

list_up = list(exposure.columns[:-3])
lists = ['state']
for i in list_up:
    lists.append(i)
exposure_diff = exposure[lists]
exposure_diff.reset_index(inplace = True)

large_share_county.loc[:,'avg_share_Z'] = large_share_county.iloc[:,1:10].mean(axis = 1)

shares = large_share_county[['FIPS', 'avg_share_Z']]

exposure_diff = exposure_diff.merge(shares, how = 'left', on = 'FIPS')
exposure_diff = exposure_diff.merge(base_device, how = 'left', on = 'FIPS')
visits_total_county.loc[:,'base_visits'] = visits_total_county.iloc[:,1:10].mean(axis = 1)
temp = visits_total_county[['FIPS', 'base_visits']]
exposure_diff = exposure_diff.merge(temp, how = 'left', on = 'FIPS')

exposure_diff.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/test.csv')
# temp = exposure.iloc[:,:-2]
# temp = temp.groupby('state').mean()

# fig, ax = plt.subplots()
# ax.plot(temp.columns, temp.loc['06'], linewidth=2, label='CA', alpha=0.6)
# ax.plot(temp.columns, temp.loc['48'], linewidth=2, label='TX', alpha=0.6)
# ax.plot(temp.columns, temp.loc['17'], linewidth=2, label='IL', alpha=0.6)
# ax.plot(temp.columns, temp.loc['12'], linewidth=2, label='FL', alpha=0.6)
# ax.legend()
# plt.xticks(rotation=90)
# plt.show()



confirmed = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/confirmed.csv', 
                        index_col = 0, dtype = {'FIPS':str})
death  = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/death.csv', 
                     index_col = 0, dtype = {'FIPS':str})


confirmed_county = pd.DataFrame()
temp = large_share_county['FIPS']

for i in temp:
    temp_list = confirmed.loc[confirmed.loc[:,'FIPS'] == i,:]
    confirmed_county = pd.concat([confirmed_county,temp_list], axis = 0)

death_county = pd.DataFrame()
temp = large_share_county['FIPS']

for i in temp:
    temp_list = death.loc[death.loc[:,'FIPS'] == i,:]
    death_county = pd.concat([death_county,temp_list], axis = 0)
