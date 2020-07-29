#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 15:17:33 2020

@author: yeabinmoon

Data created:
    selected_POIs.csv: having more than 10 visitors and enough information on visitors' cbg
    1.percentile.png: emprical distribution of POIS in CA


"""

import pandas as pd
import json
import time
import numpy as np
import matplotlib.pyplot as plt

def sum_dict(inline_data):
    return sum(inline_data.values())


raw_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/df_CA_Reli_raw.csv',
                     index_col = 0, dtype ={'postal_code':str, 'stateFIPS':str,
                                            'countyFIPS':str, 'poi_cbg':str})

WorshipPlace = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/WorshipPlace.csv'
                           , index_col=0)

#WorshipPlace = WorshipPlace.merge(raw_df, how = 'left', on = 'safegraph_place_id')

filter1 = WorshipPlace.copy()

week_list = ['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
             '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17',
             '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16',
             '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
             '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
             '2020-05-18', '2020-05-25', '2020-06-01', '2020-06-08',
             '2020-06-15']

for week in week_list[:8]:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+week+'-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','raw_visitor_counts'])
    temp_df.rename(columns = {'raw_visitor_counts':week}, inplace = True)
    filter1 = filter1.merge(temp_df, how = 'left', on = 'safegraph_place_id')
temp = filter1.copy()
temp.fillna(0,inplace = True)
temp.iloc[:,1:9]    
temp.loc[:,'avg'] = temp.iloc[:,1:9].mean(axis = 1)    
temp.loc[:,'max'] = temp.iloc[:,1:9].max(axis = 1)    
temp1 = temp.loc[temp.loc[:,'avg'] >=10,:]
#temp2 = temp.loc[temp.loc[:,'max'] >=10,:]
temp3 = temp.loc[temp.loc[:,'avg'] >=15,:]

filtered_list_1 = temp1[['safegraph_place_id']]
filtered_list_2 = temp3[['safegraph_place_id']]


data_uni_visits = filtered_list_1.copy()
data_dict_total = filtered_list_1.copy()
data_rate = filtered_list_1.copy()

for week in week_list[:8]:
    start_time = time.time()
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+week+'-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','raw_visitor_counts', 'visitor_home_cbgs'])
    temp_df['raw_visitor_counts'] = temp_df['raw_visitor_counts'].astype(int)
    temp_df['raw_visitor_counts'] = pd.to_numeric(temp_df['raw_visitor_counts'], downcast = 'integer')
    temp_df.loc[:,'visitor_home_cbgs'] = temp_df.loc[:,'visitor_home_cbgs'].apply(json.loads)
    temp_df = temp_df.loc[temp_df.loc[:,'visitor_home_cbgs'].apply(len) != 0, :]
    temp_df.loc[:,'sum_dict'] = temp_df.loc[:,'visitor_home_cbgs'].apply(sum_dict)
    temp_df.loc[:,'rate'] = temp_df.loc[:,'sum_dict'] / temp_df.loc[:,'raw_visitor_counts']
    # temp_df.loc[:,'flag'] = 0    
    # temp = temp_df.loc[:,'rate'] > 1
    # temp_df.loc[temp,'flag'] = 1
    
    data_uni_visits = data_uni_visits.merge(temp_df[['safegraph_place_id','raw_visitor_counts']],
                                            how = 'left', on = 'safegraph_place_id')
    data_uni_visits.rename(columns = {'raw_visitor_counts':week}, inplace = True)
    data_dict_total = data_dict_total.merge(temp_df[['safegraph_place_id','sum_dict']],
                                            how = 'left', on = 'safegraph_place_id')
    data_dict_total.rename(columns = {'sum_dict':week}, inplace = True)
    data_rate = data_rate.merge(temp_df[['safegraph_place_id','rate']],
                                            how = 'left', on = 'safegraph_place_id')
    data_rate.rename(columns = {'rate':week}, inplace = True)
    # data_flag_info = data_flag_info.merge(temp_df[['safegraph_place_id','flag']],
    #                                         how = 'left', on = 'safegraph_place_id')
    # data_flag_info.rename(columns = {'flag':week}, inplace = True)      
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))

data_uni_visits.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/data_uni_visits.csv')
data_dict_total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/data_dict_total.csv') 
data_rate.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/data_rate.csv') 

test = data_rate.fillna(0)

test.loc[:,'ind'] = test.iloc[:,1:9].mean(axis = 1)
test.loc[:,'flag'] = test.iloc[:,1:9].max(axis = 1)
test.loc[:,'info'] = (test.iloc[:,1:9].sum(axis = 1) - test.iloc[:,1:9].max(axis = 1))/7

filtered_list_3 = test.loc[test.loc[:,'info'] >= 0.6,['safegraph_place_id']]

selected_POIs = filtered_list_3.merge(raw_df, how = 'left', on = 'safegraph_place_id')
selected_POIs.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/selected_POIs.csv')


test = filtered_list_3.merge(data_uni_visits, how = 'left', on = 'safegraph_place_id')
test.fillna(0, inplace = True)
test.loc[:,'base'] = test.iloc[:,1:].mean(axis = 1)


def ecdf(data):
    """Compute ECDF for a one-dimensional array of measurements."""
    # Number of data points: n
    n = len(data)
    # x-data for the ECDF: x
    x = np.sort(data)
    # y-data for the ECDF: y
    y = np.arange(1, n+1) / n
    return x, y



x_vers, y_vers = ecdf(test.loc[:,'base'])
_ = plt.plot(y_vers, x_vers, '.')
_ = plt.xlabel('percentile')
_ = plt.ylabel('num of unique visitors prior to pandemic')
_ = plt.title('Percentile distribution of religious POIs in CA')
_ = plt.savefig('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/graph/1.percentile.png')






########################################################################
# using more than 15 visitors


data_uni_visits = filtered_list_2.copy()
data_dict_total = filtered_list_2.copy()
data_rate = filtered_list_2.copy()

for week in week_list[:8]:
    start_time = time.time()
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+week+'-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','raw_visitor_counts', 'visitor_home_cbgs'])
    temp_df['raw_visitor_counts'] = temp_df['raw_visitor_counts'].astype(int)
    temp_df['raw_visitor_counts'] = pd.to_numeric(temp_df['raw_visitor_counts'], downcast = 'integer')
    temp_df.loc[:,'visitor_home_cbgs'] = temp_df.loc[:,'visitor_home_cbgs'].apply(json.loads)
    temp_df = temp_df.loc[temp_df.loc[:,'visitor_home_cbgs'].apply(len) != 0, :]
    temp_df.loc[:,'sum_dict'] = temp_df.loc[:,'visitor_home_cbgs'].apply(sum_dict)
    temp_df.loc[:,'rate'] = temp_df.loc[:,'sum_dict'] / temp_df.loc[:,'raw_visitor_counts']
    # temp_df.loc[:,'flag'] = 0    
    # temp = temp_df.loc[:,'rate'] > 1
    # temp_df.loc[temp,'flag'] = 1
    
    data_uni_visits = data_uni_visits.merge(temp_df[['safegraph_place_id','raw_visitor_counts']],
                                            how = 'left', on = 'safegraph_place_id')
    data_uni_visits.rename(columns = {'raw_visitor_counts':week}, inplace = True)
    data_dict_total = data_dict_total.merge(temp_df[['safegraph_place_id','sum_dict']],
                                            how = 'left', on = 'safegraph_place_id')
    data_dict_total.rename(columns = {'sum_dict':week}, inplace = True)
    data_rate = data_rate.merge(temp_df[['safegraph_place_id','rate']],
                                            how = 'left', on = 'safegraph_place_id')
    data_rate.rename(columns = {'rate':week}, inplace = True)
    # data_flag_info = data_flag_info.merge(temp_df[['safegraph_place_id','flag']],
    #                                         how = 'left', on = 'safegraph_place_id')
    # data_flag_info.rename(columns = {'flag':week}, inplace = True)      
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))


test = data_rate.fillna(0)

test.loc[:,'ind'] = test.iloc[:,1:9].mean(axis = 1)
test.loc[:,'flag'] = test.iloc[:,1:9].max(axis = 1)
test.loc[:,'info'] = (test.iloc[:,1:9].sum(axis = 1) - test.iloc[:,1:9].max(axis = 1))/7

filtered_list_4 = test.loc[test.loc[:,'info'] >= 0.6,['safegraph_place_id']]

selected_POIs_2 = filtered_list_4.merge(raw_df, how = 'left', on = 'safegraph_place_id')
selected_POIs_2.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/selected_POIs_2.csv')


test = filtered_list_4.merge(data_uni_visits, how = 'left', on = 'safegraph_place_id')
test.fillna(0, inplace = True)
test.loc[:,'base'] = test.iloc[:,1:].mean(axis = 1)
x_vers, y_vers = ecdf(test.loc[:,'base'])
_ = plt.plot(y_vers, x_vers, '.')
_ = plt.xlabel('percentile')
_ = plt.ylabel('num of unique visitors prior to pandemic')
_ = plt.title('Percentile distribution of religious POIs in CA')
_ = plt.savefig('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/graph/1.percentile_2.png')


