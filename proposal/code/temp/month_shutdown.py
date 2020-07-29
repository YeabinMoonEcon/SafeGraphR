#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 19:18:34 2020

@author: yeabinmoon
"""

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt


def ecdf(data):
    """Compute ECDF for a one-dimensional array of measurements."""
    # Number of data points: n
    n = len(data)
    # x-data for the ECDF: x
    x = np.sort(data)
    # y-data for the ECDF: y
    y = np.arange(1, n+1) / n
    return x, y


raw_df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/df_CA_Reli_raw.csv',
                     index_col = 0, dtype ={'postal_code':str, 'stateFIPS':str,
                                            'countyFIPS':str, 'poi_cbg':str})

WorshipPlace = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/WorshipPlace.csv'
                           , index_col=0)

WorshipPlace = WorshipPlace.merge(raw_df, how = 'left', on = 'safegraph_place_id')


data_1 = WorshipPlace.copy()


month_list = ['01','02','03','04']

list_files = ['patterns-part1.csv', 'patterns-part2.csv','patterns-part3.csv',
              'patterns-part4.csv']

for month in month_list:
    start_time = time.time()
    df = pd.DataFrame()
    for file in list_files:
        temp_df = pd.read_csv('/Volumes/LaCie/cg-data/Pattern/2020/' + month +'/' + file,
                              usecols = ['safegraph_place_id','raw_visitor_counts'])
        temp_df.rename(columns = {'raw_visitor_counts': '2020-'+month}, inplace = True)
        df = pd.concat([df,temp_df], axis = 0)
    data_1 = data_1.merge(df, how = 'left', on = 'safegraph_place_id')
    print("Done",month,'!')
    print("%f seconds" % (time.time() - start_time))
    
temp_df = data_1.copy()
temp_df.fillna(0, inplace = True)

temp_df.loc[:,'base'] = temp_df.iloc[:,11:13].mean(axis = 1)
BaseVisitsMonthly = temp_df.loc[temp_df.base > 4, :]

BaseVisitsMonthly.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data//BaseVisitsMonthly.csv')

BaseVisitsMonthly.base.quantile([.5,.75,.9,.99])

#test = BaseVisitsMonthly.loc[BaseVisitsMonthly.countyName == 'Alameda County',:]


x_vers, y_vers = ecdf(BaseVisits.loc[:,'base'])
_ = plt.plot(y_vers, x_vers, '.')
_ = plt.xlabel('percentile')
_ = plt.ylabel('num of unique visitors prior to pandemic')
#_ = plt.title('Percentile distribution of religious POIs in CA')
plt.savefig('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/figures/1.percentile.png')
