#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 15:47:37 2020

@author: yeabinmoon



Data created:
    1. BaseVisits.csv: From the church list, calcuate the number of avg unique visitors before March.
                        
    
    'Keep the POI, if the visitors are greater than 4.' -> revised
    
    2. ClassificationCA.csv: classification complete whether large or whether shutdown

    The place is shutdown either:
        a. zero unique visitors during the mid March and early April
        b. For large churches, the unique visitors are less than 5
        c. Attendance rate compared to the base (Jan, Feb), is less than 5 percent

    Church is large if the unique base visitors are greater than 30.
    
    a. 1.percentile.png: the percentile distribution of POIs 

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


week_list = ['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
             '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17',
             '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16',
             '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
             '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
             '2020-05-18', '2020-05-25', '2020-06-01', '2020-06-08',
             '2020-06-15']


# Check out the pattern of summary statistics in 2020

# 1. the number of unique visitors

data_1 = WorshipPlace.copy()

for week in week_list:
    start_time = time.time()
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/W_pattern/main-file/'+week+'-weekly-patterns.csv',
                          usecols = ['safegraph_place_id','raw_visitor_counts'])
    temp_df['raw_visitor_counts'] = temp_df['raw_visitor_counts'].astype(int)
    temp_df['raw_visitor_counts'] = pd.to_numeric(temp_df['raw_visitor_counts'], downcast = 'integer')
    temp_df.rename(columns = {'raw_visitor_counts': week}, inplace = True)

    data_1 = data_1.merge(temp_df, how = 'left', on = 'safegraph_place_id')
    print("Done",week,'!')
    print("%f seconds" % (time.time() - start_time))



####
temp_df = data_1.copy()
temp_df.fillna(0, inplace = True)

BaseVisits = temp_df.copy()

BaseVisits.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/BaseVisits.csv')



# temp_df.loc[:,'base'] = temp_df.iloc[:,10:19].mean(axis = 1)
# BaseVisits = temp_df.loc[temp_df.base > 4, :]
# BaseVisits.drop(columns = 'base', inplace = True)
# BaseVisits.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data//BaseVisits.csv')


# 2. Define the shutdown church
BaseVisits = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/BaseVisits.csv', 
                         index_col = 0, dtype = {'postal_code':str,'stateFIPS':str,
                                                 'countyFIPS':str, 'poi_cbg':str})

BaseVisits.loc[:,'base'] = BaseVisits.iloc[:,11:19].mean(axis = 1)

BaseVisits.loc[:,'MAX'] = BaseVisits.iloc[:,11:19].max(axis = 1)

temp0 = (BaseVisits.loc[:,'base'] >= 100) 
temp0.sum()
BaseVisits.loc[temp0,'base'].sum()

temp1 = (BaseVisits.loc[:,'base'] >= 50) & (BaseVisits.loc[:,'base'] < 100)
temp1.sum()
BaseVisits.loc[temp1,'base'].sum()

temp2 = (BaseVisits.loc[:,'base'] >= 30) & (BaseVisits.loc[:,'base'] < 50)
temp2.sum()
BaseVisits.loc[temp2,'base'].sum()

temp3 = (BaseVisits.loc[:,'base'] >= 25) & (BaseVisits.loc[:,'base'] < 30)
temp3.sum()
BaseVisits.loc[temp3,'base'].sum()

temp4 = (BaseVisits.loc[:,'base'] >= 20) & (BaseVisits.loc[:,'base'] < 25)
temp4.sum()
BaseVisits.loc[temp4,'base'].sum()

temp5 = (BaseVisits.loc[:,'base'] >= 15) & (BaseVisits.loc[:,'base'] < 20)
temp5.sum()
BaseVisits.loc[temp5,'base'].sum()


temp6 = (BaseVisits.loc[:,'base'] < 15) 
temp6.sum()
BaseVisits.loc[temp6,'base'].sum()


# temp6 = (BaseVisits.loc[:,'base'] >= 10) & (BaseVisits.loc[:,'base'] < 15)
# temp6.sum()
# BaseVisits.loc[temp6,'base'].sum()

# temp7 = (BaseVisits.loc[:,'base'] >= 5) & (BaseVisits.loc[:,'base'] < 10)
# temp7.sum()
# BaseVisits.loc[temp7,'base'].sum()


# temp8 = (BaseVisits.loc[:,'base'] < 5) 
# temp8.sum()
# BaseVisits.loc[temp8,'base'].sum()




# temp7 = (BaseVisits.loc[:,'base'] < 5) 
# temp7.sum()
# BaseVisits.loc[temp7,'base'].sum()


BaseVisits.loc[temp6, 'size'] = 0
BaseVisits.loc[temp5, 'size'] = 1
BaseVisits.loc[temp4, 'size'] = 2
BaseVisits.loc[temp3, 'size'] = 3
BaseVisits.loc[temp2, 'size'] = 4
BaseVisits.loc[temp1, 'size'] = 5
BaseVisits.loc[temp0, 'size'] = 6




# BaseVisits.loc[temp8, 'size'] = 0
# BaseVisits.loc[temp7, 'size'] = 1
# BaseVisits.loc[temp6, 'size'] = 2
# BaseVisits.loc[temp5, 'size'] = 3
# BaseVisits.loc[temp4, 'size'] = 4
# BaseVisits.loc[temp3, 'size'] = 5
# BaseVisits.loc[temp2, 'size'] = 6
# BaseVisits.loc[temp1, 'size'] = 7
# BaseVisits.loc[temp0, 'size'] = 8



# BaseVisits.loc[:,'after'] = BaseVisits.iloc[:,20:36].mean(axis = 1)

# BaseVisits.loc[:,'after2'] = BaseVisits.iloc[:,25:36].mean(axis = 1)

# a = BaseVisits.loc[BaseVisits.loc[:,'MAX'] < 10,:]

# a = BaseVisits.loc[BaseVisits.loc[:,'after'] <= 0.6,:]
# b = BaseVisits.loc[BaseVisits.loc[:,'after'] > 0.6,:]

# c = BaseVisits.loc[BaseVisits.loc[:,'after2'] < 1,:]



BaseVisits.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/ClassificationCA.csv')






#temp = (BaseVisits.countyName == 'Alameda County') | (BaseVisits.countyName == 'San Francisco County')
	
# AlSf_df = BaseVisits.loc[temp,:]
# AlSf_df.base.quantile([.5])

# temp0 = (AlSf_df.loc[:,'base'] >= 100) 
# temp0.sum()
# AlSf_df.loc[temp0,'base'].sum()

# temp1 = (AlSf_df.loc[:,'base'] >= 50) & (AlSf_df.loc[:,'base'] < 100)
# temp1.sum()
# AlSf_df.loc[temp1,'base'].sum()

# temp2 = (AlSf_df.loc[:,'base'] >= 30) & (AlSf_df.loc[:,'base'] < 50)
# temp2.sum()
# AlSf_df.loc[temp2,'base'].sum()

# temp3 = (AlSf_df.loc[:,'base'] >= 20) & (AlSf_df.loc[:,'base'] < 30)
# temp3.sum()
# AlSf_df.loc[temp3,'base'].sum()

# temp4 = (AlSf_df.loc[:,'base'] >= 10) & (AlSf_df.loc[:,'base'] < 20)
# temp4.sum()
# AlSf_df.loc[temp4,'base'].sum()

# temp5 = (AlSf_df.loc[:,'base'] < 10)
# temp5.sum()
# AlSf_df.loc[temp5,'base'].sum()


BaseVisits.loc[:,'att1'] = BaseVisits.iloc[:,20] / BaseVisits['base']
BaseVisits.loc[:,'att2'] = BaseVisits.iloc[:,21] / BaseVisits['base']
BaseVisits.loc[:,'att3'] = BaseVisits.iloc[:,22] / BaseVisits['base']
BaseVisits.loc[:,'att4'] = BaseVisits.iloc[:,23] / BaseVisits['base']
BaseVisits.loc[:,'att5'] = BaseVisits.iloc[:,24] / BaseVisits['base']
BaseVisits['base']
test = BaseVisits[['safegraph_place_id', 'countyName','base', 'att1', 'att2', 'att3', 'att4', 'att5']]
test.fillna(0, inplace = True)
test = test.loc[test['base'] != 0,:]
temp = (test['countyName'] == 'Alameda County') | (test['countyName'] == 'San Francisco County')
df = test.loc[temp, :]

temp0 = test['base'] < 5
temp1 = (test['base'] >= 5) & (test['base'] < 10)
temp2 = (test['base'] >= 10) & (test['base'] < 15)
temp3 = (test['base'] >= 15) & (test['base'] < 20)
temp4 = (test['base'] >= 20) & (test['base'] < 25)
temp5 = (test['base'] >= 25) & (test['base'] < 30)
temp6 = (test['base'] >= 30) & (test['base'] < 40)
temp7 = (test['base'] >= 40) & (test['base'] < 80)
temp8 = (test['base'] >= 80)

df.loc[temp0,'size'] = 0
df.loc[temp1,'size'] = 1
df.loc[temp2,'size'] = 2
df.loc[temp3,'size'] = 3
df.loc[temp4,'size'] = 4
df.loc[temp5,'size'] = 5
df.loc[temp6,'size'] = 6
df.loc[temp7,'size'] = 7
df.loc[temp8,'size'] = 8

aa = df.groupby('size')['att1', 'att2', 'att3', 'att4', 'att5'].mean()
aa.plot(y = 'att1')
aa.plot(y = 'att2')
aa.plot(y = 'att3')
aa.plot(y = 'att4')
