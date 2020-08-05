#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 22:14:22 2020

@author: yeabinmoon
"""

import pandas as pd
import time
import json

list_files = ['patterns-part1.csv', 'patterns-part2.csv','patterns-part3.csv',
              'patterns-part4.csv']
month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']



HolyPois = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/HolyPois.csv',
                       usecols=['safegraph_place_id', 'location_name','poi_cbg',
                                'region', 'city', 'countyName'],
                       dtype = {'poi_cbg':str})
temp = (HolyPois.loc[:,'region'] == 'TX') | (HolyPois.loc[:,'region'] == 'IL') | (HolyPois.loc[:,'region'] == 'CA') | (HolyPois.loc[:,'region'] == 'FL')
states_POIs = HolyPois.loc[temp,:]





temp_list = states_POIs[['safegraph_place_id']]
month = '01'

df_total = pd.DataFrame()    
start_time = time.time()
df = pd.DataFrame()
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2020/' + month +'/' + file,
                          usecols = ['safegraph_place_id', 'popularity_by_day'])
    temp_df.rename(columns = {'popularity_by_day': '2020-'+month}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
temp_df = temp_list.merge(df, how = 'left', on = 'safegraph_place_id')
temp_df.dropna(inplace = True)
temp_df.iloc[:,1] = temp_df.iloc[:,1].apply(json.loads) 
for i in range(len(temp_df)):
    temp = pd.DataFrame.from_dict(temp_df.iloc[i,1], orient = 'index')
    temp.reset_index(inplace = True)
    temp['safegraph_place_id'] = temp_df.iloc[i,0]
    temp['date'] = '2020-'+month
    temp.rename(columns = {0:'visit'}, inplace = True)
    temp = temp[['safegraph_place_id', 'date', 'index','visit']]
    df_total = pd.concat([df_total, temp], axis = 0, ignore_index= True)
df_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/month/2020'+month+'.csv')
print("Done",month,'!')
print("%f seconds" % (time.time() - start_time))



for month in month_list:
    df_total = pd.DataFrame()    
    start_time = time.time()
    df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2019/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'popularity_by_day'])
        temp_df.rename(columns = {'popularity_by_day': '2019-'+month}, inplace = True)
        df = pd.concat([df,temp_df], axis = 0)
    temp_df =  temp_list.merge(df, how = 'left', on = 'safegraph_place_id')
    temp_df.dropna(inplace = True)
    temp_df.iloc[:,1] = temp_df.iloc[:,1].apply(json.loads) 
    for i in range(len(temp_df)):
        temp = pd.DataFrame.from_dict(temp_df.iloc[i,1], orient = 'index')
        temp.reset_index(inplace = True)
        temp['safegraph_place_id'] = temp_df.iloc[i,0]
        temp['date'] = '2019-'+month
        temp.rename(columns = {0:'visit'}, inplace = True)
        temp = temp[['safegraph_place_id', 'date', 'index','visit']]
        df_total = pd.concat([df_total, temp], axis = 0, ignore_index= True)
    df_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/month/2019'+month+'.csv')
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))


##################################################################################

# worship place

df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/month/202001.csv',
                 index_col = 0)
for month in month_list:
    df_temp = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/month/2019'+month+'.csv',
                          index_col = 0)
    df = pd.concat([df,df_temp], axis= 0)

temp_df = df.groupby(['safegraph_place_id','index'])['visit'].sum()
temp_df = temp_df.reset_index()
temp_df = temp_df.set_index('index')
temp_df = temp_df.groupby(['safegraph_place_id'])['visit'].idxmax()
temp_df = temp_df.reset_index()
temp_df.groupby('visit').count()

temp_ind = (temp_df.loc[:,'visit'] == 'Friday') | (temp_df.loc[:,'visit'] == 'Saturday') | (temp_df.loc[:,'visit'] == 'Sunday')
temp_lists = temp_df.loc[temp_ind,:]

WorshipPlace = temp_lists.loc[:,['safegraph_place_id']]
WorshipPlace.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/WorshipPlace.csv')




# attachment (monthly)

df_temp = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/WorshipPlace.csv',index_col = 0)

month_list = ['08','09','10','11','12']
for month in month_list:
    start_time = time.time()
    df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2019/' + month +'/' + file,
                              usecols = ['safegraph_place_id', 'raw_visitor_counts'])
        temp_df.rename(columns = {'raw_visitor_counts': '2019-'+month}, inplace = True)
        df = pd.concat([df,temp_df], axis = 0)
    df_temp =  df_temp.merge(df, how = 'left', on = 'safegraph_place_id')
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))

month = '01'
df = pd.DataFrame()
for file in list_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2020/' + month +'/' + file,
                          usecols = ['safegraph_place_id', 'raw_visitor_counts'])
    temp_df.rename(columns = {'raw_visitor_counts': '2020-'+month}, inplace = True)
    df = pd.concat([df,temp_df], axis = 0)
df_temp =  df_temp.merge(df, how = 'left', on = 'safegraph_place_id')


df_temp.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/temp_list.csv')


# attachment (weekly) and determine size

df_temp = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/temp_list.csv', index_col = 0)
temp =  df_temp.dropna()
temp = temp[['safegraph_place_id']]


week_list = ['2019-11-25', '2019-12-02', '2019-12-09', '2019-12-16', '2019-12-23',
             '2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20']


for week in week_list:
    start_time = time.time()
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+week+'-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','raw_visitor_counts'])
    temp = temp.merge(temp_df, how = 'left', on = 'safegraph_place_id')
    temp.rename(columns = {'raw_visitor_counts':week}, inplace = True)
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))
    
temp.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/temp_list_base.csv')

temp_list_base = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/temp_list_base.csv', index_col = 0)
temp_list_base = temp_list_base.dropna()

temp_list_base.loc[:,'baseline'] = (temp_list_base.iloc[:,1:10].sum(axis = 1) - temp_list_base.iloc[:,1:10].max(axis = 1) - temp_list_base.iloc[:,1:10].min(axis = 1))/7
temp_list_base.loc[:,'size'] = 0
temp_list_base.loc[temp_list_base.loc[:,'baseline'] > 31, 'size'] = 1

temp_list = temp_list_base[['safegraph_place_id','size']]
(temp_list['size'] == 1).sum()
(temp_list['size'] == 0).sum()

temp_list.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/temp_list2.csv')


##############################################
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
    df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/monthly/'+week+'_cbg.csv')
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))
    

df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/monthly/2019-11-25_cbg.csv',
                 index_col = 0, dtype = {'cbg':str})
for week in week_list[1:]:
    temp_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/monthly/'+week+'_cbg.csv', 
                          index_col = 0, dtype = {'cbg':str})
    df = pd.concat([df, temp_df], axis = 0, ignore_index = True)
df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/cbg_visitors.csv')

df = df[['date','cbg','safegraph_place_id','size','visits']]

visits_total = df.groupby(['date', 'cbg'])['visits'].sum()
visits_total = visits_total.reset_index()
visits_total = visits_total.pivot(index= 'cbg', columns = 'date', values = 'visits')

visits_total.fillna(0, inplace = True)
visits_total.reset_index(inplace = True)
visits_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/visits_total.csv')



visits_large = df.loc[df.loc[:,'size'] == 1,:]
visits_large = visits_large.groupby(['date', 'cbg'])['visits'].sum()
visits_large = visits_large.reset_index()
visits_large = visits_large.pivot(index= 'cbg', columns = 'date', values = 'visits')
visits_large.fillna(0, inplace = True)
visits_large.reset_index(inplace = True)
visits_large.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/visits_large.csv')


##############################################
"""
County level
"""
visits_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/visits_total.csv', 
                           index_col = 0, dtype = {'cbg':str})

visits_total.loc[:,'FIPS'] =  visits_total.cbg.str[0:5]
visits_total.drop(columns = {'cbg'}, inplace = True)
list_dates = visits_total.columns
visits_total_county = visits_total.groupby('FIPS')[list_dates[:-1]].sum()
visits_total_county.reset_index(inplace = True)
visits_total_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/visits_total_county.csv')

visits_large = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/visits_large.csv', 
                           index_col = 0, dtype = {'cbg':str})

visits_large.loc[:,'FIPS'] =  visits_large.cbg.str[0:5]
visits_large.drop(columns = {'cbg'}, inplace = True)
list_dates = visits_large.columns
visits_large_county = visits_large.groupby('FIPS')[list_dates[:-1]].sum()
visits_large_county.reset_index(inplace = True)

temp = visits_total_county[['FIPS']]
temp = temp.merge(visits_large_county, how = 'outer', on = 'FIPS')
temp.fillna(0, inplace = True)
temp.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/visits_large_county.csv')    





visits_total_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/visits_total_county.csv', 
                                  index_col = 0, dtype = {'FIPS':str})
visits_large_county = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/visits_large_county.csv',
                                  index_col = 0, dtype = {'FIPS':str})


temp_df = visits_total_county.merge(visits_large_county, how = 'outer', on = 'FIPS')


temp_df.fillna(0, inplace = True)
temp_df.set_index('FIPS', inplace = True)

for i in range(30):
    temp_df.loc[:,week_list[i]] = temp_df.iloc[:,30+i] / temp_df.iloc[:,0+i]
large_share_county = temp_df.iloc[:,60:]
large_share_county.reset_index(inplace = True)
large_share_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp2/large_share_county.csv')



visits_total_county.loc[:,'STATE'] = visits_total_county.loc[:,'FIPS'].str[0:2]
state_ind = (visits_total_county.loc[:,'STATE'] == '48') | (visits_total_county.loc[:,'STATE'] == '06') \
                    | (visits_total_county.loc[:,'STATE'] == '17') | (visits_total_county.loc[:,'STATE'] == '12') 
visits_total_county = visits_total_county.loc[state_ind,:]

visits_large_county.loc[:,'STATE'] = visits_large_county.loc[:,'FIPS'].str[0:2]
state_ind = (visits_large_county.loc[:,'STATE'] == '48') | (visits_large_county.loc[:,'STATE'] == '06') \
                    | (visits_large_county.loc[:,'STATE'] == '17') | (visits_large_county.loc[:,'STATE'] == '12') 
visits_large_county = visits_large_county.loc[state_ind,:]


large_share_county.loc[:,'STATE'] = large_share_county.loc[:,'FIPS'].str[0:2]
state_ind = (large_share_county.loc[:,'STATE'] == '48') | (large_share_county.loc[:,'STATE'] == '06') \
                    | (large_share_county.loc[:,'STATE'] == '17') | (large_share_county.loc[:,'STATE'] == '12') 
large_share_county = large_share_county.loc[state_ind,:]



device_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/device_total.csv', 
                           index_col = 0, dtype = {'origin_census_block_group':str})
device_total.loc[:,'FIPS'] = device_total.loc[:,'origin_census_block_group'].str[0:5]
device_total.drop(columns = {'origin_census_block_group'}, inplace = True)
list_dates = device_total.columns
device_total_county = device_total.groupby('FIPS')[list_dates[:-1]].sum()
device_total_county.reset_index(inplace = True)
device_total_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/device_total_county.csv')


device_rate = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/device_rate.csv',
                          index_col = 0, dtype = {'origin_census_block_group':str})
device_rate.loc[:,'FIPS'] = device_rate.loc[:,'origin_census_block_group'].str[0:5]
device_rate.drop(columns = {'origin_census_block_group'}, inplace = True)
list_dates = device_rate.columns
device_rate_county = device_rate.groupby('FIPS')[list_dates[:-1]].mean()    ## Non-weighted
device_rate_county.reset_index(inplace = True)



visits_total_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/visits_total_county.csv')
visits_large_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/visits_large_county.csv')
large_share_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/large_share_county.csv')
device_total_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/device_total_county.csv')
device_rate_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/device_rate_county.csv')

url = 'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv'
temp_df = pd.read_csv(url, dtype = {'STATE':str,'COUNTY':str}, usecols = ['STATE','COUNTY','POPESTIMATE2019'])
temp_df.loc[:,'FIPS'] = temp_df.loc[:,'STATE'] + temp_df.loc[:,'COUNTY']

county_pop = pd.DataFrame()
temp = large_share_county['FIPS']

for i in temp:
    temp_list = temp_df.loc[temp_df.loc[:,'FIPS'] == i,:]
    county_pop = pd.concat([county_pop,temp_list], axis = 0)

county_pop = county_pop[['FIPS','POPESTIMATE2019']]  
county_pop.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/county_pop.csv')

device_total_county.loc[:,'base_device']= device_total_county.iloc[:,1:32].mean(axis = 1)
base_device = device_total_county[['FIPS', 'base_device']]

county_pop = county_pop[['FIPS', 'POPESTIMATE2019']]
county_pop = county_pop.merge(base_device, how = 'left', on = 'FIPS')
teat = county_pop.set_index('FIPS')
teat.corr()

teat.loc[:,'factor'] = teat.iloc[:,0] / teat.iloc[:,1]
teat.loc[:,'factor'].mean()


## JHU confirmed
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
confirmed = pd.read_csv(url,  dtype = {'UID':str})

confirmed.drop(columns = {'FIPS','iso2','iso3','code3','FIPS','Admin2','Country_Region',
                          'Lat','Long_','Combined_Key'}, inplace = True)
confirmed.loc[:,'FIPS'] = confirmed.loc[:,'UID'].str[3:]
confirmed.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/confirmed.csv')

temp = large_share_county['FIPS']
confirmed_county = pd.DataFrame()
for i in temp:
    temp_list = confirmed.loc[confirmed.loc[:,'FIPS'] == i,:]
    confirmed_county = pd.concat([confirmed_county,temp_list], axis = 0)
confirmed_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/confirmed_county.csv')


url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
death = pd.read_csv(url,  dtype ={'UID':str})

death.drop(columns = {'FIPS','iso2','iso3','code3','FIPS','Admin2','Country_Region',
                          'Lat','Long_','Combined_Key'}, inplace = True)
death.loc[:,'FIPS'] = death.loc[:,'UID'].str[3:]
death.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/death.csv')

temp = large_share_county['FIPS']
death_county = pd.DataFrame()
for i in temp:
    temp_list = death.loc[death.loc[:,'FIPS'] == i,:]
    death_county = pd.concat([death_county,temp_list], axis = 0)
death_county.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/reg/death_county.csv')
