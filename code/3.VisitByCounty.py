#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 22:02:33 2020

@author: yeabinmoon
"""

import pandas as pd
import time
import json

WorshipPlace = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/WorshipPlace.csv', index_col = 0)

HolyPois = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/HolyPois.csv',
                       usecols=['safegraph_place_id', 'location_name','poi_cbg',
                                'region', 'city', 'countyName'],
                       dtype = {'poi_cbg':str})

WorshipPlace = WorshipPlace.merge(HolyPois, how = 'left', on = 'safegraph_place_id')

temp = WorshipPlace.groupby('region')['safegraph_place_id'].count()
temp = temp.reset_index()

temp.mean()

week_list = ['2019-11-25', '2019-12-02', '2019-12-09', '2019-12-16', '2019-12-23',
              '2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
              '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17',
              '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16',
              '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
              '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
              '2020-05-18', '2020-05-25', '2020-06-01', '2020-06-08',
              '2020-06-15']


# week_list = ['2019-11-25', '2019-12-02', '2019-12-09', '2019-12-16', '2019-12-23',
             # '2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20']


for week in week_list:
    start_time = time.time()
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+week+'-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','raw_visitor_counts'])
    WorshipPlace = WorshipPlace.merge(temp_df, how = 'left', on = 'safegraph_place_id')
    WorshipPlace.rename(columns = {'raw_visitor_counts':week}, inplace = True)
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))
    
WorshipPlace.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/WeekVisitors_2.csv')

"""
German Church Shops: sg:2c68989832e14f9ebfe60f8215f652ca needs to be omitted?
"""

# temp_df = WorshipPlace.copy()
# temp_df.fillna(0, inplace = True)
# temp_df = temp_df.loc[temp_df.loc[:,'safegraph_place_id'] != 'sg:2c68989832e14f9ebfe60f8215f652ca',:]
# temp_df.loc[:,'baseline'] = (temp_df.iloc[:,6:15].sum(axis = 1) - temp_df.iloc[:,6:15].max(axis = 1) - temp_df.iloc[:,6:15].min(axis = 1))/7


# temp = temp_df[['safegraph_place_id', 'baseline']]
# temp.loc[:,'size'] = 0
# temp.loc[temp.loc[:,'baseline'] > 44, 'size'] = 1
# temp.groupby('size')['baseline'].sum()

# temp_df2 = WorshipPlace.copy()


############################################

"""
4 largest number of POIs states: TX, CA, FL, IL
"""

temp_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/WeekVisitors.csv',index_col = 0)
temp = (temp_df.loc[:,'region'] == 'TX') | (temp_df.loc[:,'region'] == 'CA') | (temp_df.loc[:,'region'] == 'FL') | (temp_df.loc[:,'region'] == 'IL')

temp_df = temp_df.loc[temp,:]
temp_df.fillna(0, inplace = True)
temp_df.loc[:,'baseline'] = (temp_df.iloc[:,6:15].sum(axis = 1) - temp_df.iloc[:,6:15].max(axis = 1) - temp_df.iloc[:,6:15].min(axis = 1))/7
temp_df.loc[:,'size'] = 0
temp_df.loc[temp_df.loc[:,'baseline'] > 44, 'size'] = 1

temp_list = temp_df[['safegraph_place_id','size']]

(temp_list['size'] == 1).sum()
(temp_list['size'] == 0).sum()

temp_list.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/temp_list.csv')


##############################################
BaseList = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/temp_list.csv',
                       index_col = 0)
                        


####????
home_df = BaseList.copy()    # typo?
for week in week_list:  
    start_time = time.time()
    home_df = BaseList.copy()
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+ week + '-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','visitor_home_cbgs'])
    temp_df.rename(columns = {'visitor_home_cbgs': week}, inplace = True)
    home_df = home_df.merge(temp_df, how = 'left', on = 'safegraph_place_id')
    home_df.dropna(inplace = True)
    home_df.loc[:,week] = home_df.loc[:,week].apply(json.loads)
    home_df = home_df.loc[home_df.loc[:,week].apply(len) != 0,:]
    df = pd.DataFrame()
    for i in range(len(home_df)):      
        temp_df = pd.DataFrame.from_dict(home_df.iloc[i,2], orient = 'index')
        temp_df = temp_df.reset_index()
        temp_df.loc[:,'safegraph_place_id'] = home_df.iloc[i,0]
        temp_df.loc[:,'size'] = home_df.iloc[i,1]
        temp_df.loc[:,'date'] = week
        temp_df.rename(columns = {0:'visits','index':'cbg'}, inplace = True)
        #temp_df.loc[:,'year'] = temp_df.loc[:,'date'].str[0:4]
        #temp_df.loc[:,'week'] = temp_df.loc[:,'date'].str[5:]        
        temp_df = temp_df[['safegraph_place_id', 'cbg', 'date', 'visits', 'size']]
        df = pd.concat([df, temp_df], axis = 0, ignore_index = True)
    df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/monthly/'+week+'_cbg2.csv')
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))

df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/monthly/2019-11-25_cbg.csv',
                 index_col = 0, dtype = {'cbg':str})

for week in week_list[1:]:
    temp_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/monthly/'+week+'_cbg.csv', 
                          index_col = 0, dtype = {'cbg':str})
    df = pd.concat([df, temp_df], axis = 0, ignore_index = True)
df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/cbg_visitors.csv')


df = df[['date','cbg','safegraph_place_id','size','visits']]

visits_total = df.groupby(['date', 'cbg'])['visits'].sum()
visits_total = visits_total.reset_index()
visits_total = visits_total.pivot(index= 'cbg', columns = 'date', values = 'visits')

visits_total.fillna(0, inplace = True)
visits_total.reset_index(inplace = True)
visits_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/visits_total.csv')



visits_large = df.loc[df.loc[:,'size'] == 1,:]
visits_large = visits_large.groupby(['date', 'cbg'])['visits'].sum()
visits_large = visits_large.reset_index()
visits_large = visits_large.pivot(index= 'cbg', columns = 'date', values = 'visits')
visits_large.fillna(0, inplace = True)
visits_large.reset_index(inplace = True)
visits_large.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/visits_large.csv')

##############################################
"""
County level
"""
visits_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/visits_total.csv', 
                           index_col = 0, dtype = {'cbg':str})

visits_total.loc[:,'FIPS'] =  visits_total.cbg.str[0:5]
visits_total.drop(columns = {'cbg'}, inplace = True)
list_dates = visits_total.columns
visits_total_county = visits_total.groupby('FIPS')[list_dates[:-1]].sum()
visits_total_county.reset_index(inplace = True)
visits_total_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/visits_total_county.csv')

visits_large = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/visits_large.csv', 
                           index_col = 0, dtype = {'cbg':str})

visits_large.loc[:,'FIPS'] =  visits_large.cbg.str[0:5]
visits_large.drop(columns = {'cbg'}, inplace = True)
list_dates = visits_large.columns
visits_large_county = visits_large.groupby('FIPS')[list_dates[:-1]].sum()
visits_large_county.reset_index(inplace = True)

temp = visits_total_county[['FIPS']]
temp = temp.merge(visits_large_county, how = 'outer', on = 'FIPS')
temp.fillna(0, inplace = True)
temp.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/visits_large_county.csv')



visits_total_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/visits_total_county.csv', 
                                  index_col = 0, dtype = {'FIPS':str})
visits_large_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/visits_large_county.csv',
                                  index_col = 0, dtype = {'FIPS':str})


temp_df = visits_total_county.merge(visits_large_county, how = 'outer', on = 'FIPS')


temp_df.fillna(0, inplace = True)
temp_df.set_index('FIPS', inplace = True)

for i in range(30):
    temp_df.loc[:,week_list[i]] = temp_df.iloc[:,30+i] / temp_df.iloc[:,0+i]
large_share_county = temp_df.iloc[:,60:]
large_share_county.reset_index(inplace = True)
large_share_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/large_share_county.csv')


device_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/device_total.csv', 
                           index_col = 0, dtype = {'origin_census_block_group':str})
device_total.loc[:,'FIPS'] = device_total.loc[:,'origin_census_block_group'].str[0:5]
device_total.drop(columns = {'origin_census_block_group'}, inplace = True)
list_dates = device_total.columns
device_total_county = device_total.groupby('FIPS')[list_dates[:-1]].sum()
device_total_county.reset_index(inplace = True)
device_total_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/device_total_county.csv')
