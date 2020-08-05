#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 15:49:09 2020

@author: yeabinmoon
"""

import pandas as pd


visits_total_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/visits_total_county.csv',
                                  index_col = 0, dtype = {'FIPS':str})
visits_large_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/visits_large_county.csv',
                                  index_col = 0, dtype = {'FIPS':str})
large_share_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/large_share_county.csv',
                                 index_col = 0, dtype = {'FIPS':str})
device_total_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/device_total_county.csv',
                                  index_col = 0, dtype = {'FIPS':str})
device_rate_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/device_rate_county.csv',
                                  index_col = 0, dtype = {'FIPS':str})


week_list = ['2019-11-25', '2019-12-02', '2019-12-09', '2019-12-16', '2019-12-23',
              '2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
              '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17',
              '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16',
              '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
              '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
              '2020-05-18', '2020-05-25', '2020-06-01', '2020-06-08',
              '2020-06-15']
temp = device_total_county.set_index('FIPS')
temp = temp.iloc[:,::7]
temp = temp.iloc[:,:-2]
device_total_county = temp.reset_index()

temp = device_rate_county.set_index('FIPS')
temp = temp.iloc[:,::7]
temp = temp.iloc[:,:-2]
device_rate_whole_county = temp.reset_index()


temp = device_rate_county.set_index('FIPS')
for i in range(30):
    temp.loc[:,str(i)] = temp.iloc[:,0+7*i:4+7*i].mean(axis = 1)
temp = temp.iloc[:,219:]
temp.columns = week_list
device_rate_wk_county = temp.copy()
device_rate_wk_county.reset_index(inplace = True)

visits_total_county = visits_total_county.iloc[:,:-1]
visits_large_county = visits_large_county.iloc[:,:-1]
large_share_county  = large_share_county.iloc[:,:-1]

visit_temp = visits_total_county.set_index('FIPS')
total_temp = device_total_county.set_index('FIPS')
exposure = visit_temp / total_temp * 100
exposure.reset_index(inplace = True)


confirmed_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/confirmed_county.csv', index_col = 0,
                               dtype = {'FIPS':str})
death_county     = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/death_county.csv', index_col = 0,
                               dtype = {'FIPS':str})

temp = confirmed_county.set_index('FIPS')
temp = temp.iloc[:,2:]
temp = temp.iloc[:,5::7]
temp = temp.iloc[:,:-6]
confirmed_county = temp.reset_index()

temp = confirmed_county[['FIPS']]
for i in range(9):
    temp.loc[:,week_list[i]] = 0
confirmed_county = temp.merge(confirmed_county, how = 'left', on = 'FIPS')
confirmed_county.set_index('FIPS', inplace = True)
confirmed_county.columns = week_list
confirmed_county.reset_index(inplace = True)


temp = death_county.set_index('FIPS')
temp = temp.iloc[:,3:]
temp = temp.iloc[:,5::7]
temp = temp.iloc[:,:-6]
death_county = temp.reset_index()

temp = death_county[['FIPS']]
for i in range(9):
    temp.loc[:,week_list[i]] = 0
death_county = temp.merge(death_county, how = 'left', on = 'FIPS')
death_county.set_index('FIPS', inplace = True)
death_county.columns = week_list
death_county.reset_index(inplace = True)

#exposure.loc[:,'var'] = exposure.iloc[:,:9].var(axis = 1)
#a = exposure.reset_index()


"""
1. device_total_county
2. visits_total_county
3. visits_large_county
4. large_share_county
5. exposure
6. confirmed_county
7. death_county
"""
temp = device_total_county.copy()
temp.loc[:,'avg'] = temp.iloc[:,1:10].mean(axis = 1)
temp.loc[:,'avg'].quantile([.1])


list_up = temp.loc[temp.loc[:,'avg'] > 320, ['FIPS']]

device_reg = list_up.merge(device_total_county, how = 'left', on = 'FIPS')
visit_total_reg = list_up.merge(visits_total_county, how = 'left', on = 'FIPS')
visit_large_reg = list_up.merge(visits_large_county, how = 'left', on = 'FIPS')
large_share_reg = list_up.merge(large_share_county, how = 'left', on = 'FIPS')
exposure_reg = list_up.merge(exposure, how = 'left', on = 'FIPS')
confiremd_reg = list_up.merge(confirmed_county, how = 'left', on = 'FIPS')
death_reg = list_up.merge(death_county, how = 'left', on = 'FIPS')
sd_reg = list_up.merge(device_rate_whole_county, how = 'left', on = 'FIPS')
sd_wk_reg = list_up.merge(device_rate_wk_county, how = 'left', on = 'FIPS')


temp = device_reg.set_index('FIPS')
device_reg_T = temp.T
temp = visit_total_reg.set_index('FIPS')
visit_total_reg_T = temp.T
temp = visit_large_reg.set_index('FIPS')
visit_large_reg_T = temp.T
temp = large_share_reg.set_index('FIPS')
large_share_reg_T = temp.T
temp = exposure_reg.set_index('FIPS')
exposure_reg_T = temp.T

temp = sd_reg.set_index('FIPS')
sd_reg_T = temp.T
temp = sd_wk_reg.set_index('FIPS')
sd_wk_reg_T = temp.T

temp = confiremd_reg.set_index('FIPS')
confiremd_reg_T = temp.T
temp = death_reg.set_index('FIPS')
death_reg_T = temp.T


df = pd.DataFrame()

col_name = ['t', 'date', 'num_device', 'num_visitors',
            'num_large_vis','large_share','exposure',
            'confirmed','death','SD','SD_wk']

# temp_df = pd.concat([device_reg_T.iloc[:,0], visit_total_reg_T.iloc[:,0],
#                       visit_large_reg_T.iloc[:,0], large_share_reg_T.iloc[:,0],
#                       exposure_reg_T.iloc[:,0], confiremd_reg_T.iloc[:,0],
#                       death_reg_T.iloc[:,0], sd_reg_T.iloc[:,0],
#                       sd_wk_reg_T.iloc[:,0]],
#                     axis = 1, ignore_index = True)

# temp_df.reset_index(inplace = True)
# temp_df.reset_index(inplace = True)
# temp_df.columns = col_name
# temp_df.loc[:,'pre_share'] = (temp_df.iloc[0:9,5].sum() - temp_df.iloc[0:9,5].max() - temp_df.iloc[0:9,5].min())/7
# temp_df.loc[:,'pre_exposure'] = (temp_df.iloc[0:9,6].sum() - temp_df.iloc[0:9,6].max() - temp_df.iloc[0:9,6].min())/7
# temp = temp_df.loc[:,['confirmed', 'death']] - temp_df.loc[:,['confirmed', 'death']].shift(periods = 1,fill_value = 0)
# temp.columns = ['confirmed_new', 'death_new']
# temp_df = pd.concat([temp_df,temp],axis = 1)
# temp_df.loc[:,'FIPS'] = device_reg_T.iloc[:,0].name
# df = pd.concat([df, temp_df], axis = 0)

# temp_a = (temp_df.loc[0,'pre_exposure'] - temp_df.iloc[14:18,6].min())
# temp_b = temp_df.loc[0,'pre_share']
# temp_c = temp_df.iloc[:9,3].mean()
# temp_d = temp_df.loc[0,]
for i in range(len(device_reg_T.columns)):
    temp_df = pd.concat([device_reg_T.iloc[:,i], visit_total_reg_T.iloc[:,i],
                         visit_large_reg_T.iloc[:,i], large_share_reg_T.iloc[:,i],
                         exposure_reg_T.iloc[:,i], confiremd_reg_T.iloc[:,i],
                         death_reg_T.iloc[:,i], sd_reg_T.iloc[:,i],
                         sd_wk_reg_T.iloc[:,i]],
                        axis = 1, ignore_index = True)
    
    temp_df.reset_index(inplace = True)
    temp_df.reset_index(inplace = True)
    temp_df.columns = col_name
    temp_df.loc[:,'pre_share'] = (temp_df.iloc[0:9,5].sum() - temp_df.iloc[0:9,5].max() - temp_df.iloc[0:9,5].min())/7
    temp_df.loc[:,'pre_exposure'] = (temp_df.iloc[0:9,6].sum() - temp_df.iloc[0:9,6].max() - temp_df.iloc[0:9,6].min())/7
    temp = temp_df.loc[:,['confirmed', 'death']] - temp_df.loc[:,['confirmed', 'death']].shift(periods = 1,fill_value = 0)
    temp.columns = ['confirmed_new', 'death_new']
    temp_df = pd.concat([temp_df,temp],axis = 1)
    
    temp_df.loc[:,'FIPS'] = device_reg_T.iloc[:,i].name
    df = pd.concat([df, temp_df], axis = 0, ignore_index= True)

df.loc[:,'state'] = df.loc[:,'FIPS'].str[:2]
df.loc[:,'county'] = df.loc[:,'FIPS'].str[2:]

county_pop = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/county_pop.csv', index_col = 0,
                         dtype = {'FIPS':str})

temp = df.merge(county_pop, how = 'left', on = 'FIPS')
temp.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/panel2.csv')
df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/panel.csv')


# temp_df.loc[0,'pre_exposure']
# (temp_df.loc[0,'pre_exposure'] - temp_df.iloc[14:18,6].min())

# temp_a = temp.loc[0,'pre_exposure'] - temp.loc[14:18,'exposure'].min()
# temp_b = temp_a / temp.loc[0,'pre_exposure']
# temp_c = temp.loc[0,'pre_share']
# temp_d = temp.loc[:9,'num_visitors'].mean()
# temp_e = temp.loc[0,'FIPS']

# tempp = [temp_a,temp_b,temp_c,temp_d,temp_e]
# pd.DataFrame(tempp)
ddd = pd.DataFrame()
for i in range(433):
    temp_a = temp.loc[0+30*i,'pre_exposure'] - temp.loc[14+30*i:18+30*i,'exposure'].min()
    temp_b = temp_a / temp.loc[0+30*i,'pre_exposure']
    temp_c = temp.loc[0+30*i,'pre_share']
    temp_d = temp.loc[0+30*i:9+30*i,'num_visitors'].mean()
    temp_e = temp.loc[0+30*i,'FIPS']
    tempp = [temp_a,temp_b,temp_c,temp_d,temp_e]
    tempp = pd.DataFrame(tempp)
    tempp = tempp.T
    ddd=pd.concat([ddd,tempp],axis = 0, ignore_index = True)    

ddd.columns = ['D','D_pro','preshare','pre_visi','FIPS']
ddd.loc[:,'state'] = ddd.loc[:,'FIPS'].str[:2]
ddd.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/panel3.csv')
