#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 15:47:37 2020

@author: yeabinmoon



Data created:
    1. BaseVisits.csv: From the church list, calcuate the number of avg unique visitors before March. 
                        Keep the POI, if the visitors are greater than 4.
    2. ClassificationCA.csv: classification complete whether large or whether shutdown
    
    The place is shutdown either:
        a. zero unique visitors during the mid March and early April
        b. For large churches, the unique visitors are less than 5
        c. Attendance rate compared to the base (Jan, Feb), is less than 5 percent
        
    Church is large if the unique base visitors are greater than 30.

"""

import pandas as pd
import time

raw_df = pd.read_csv('/Volumes/LaCie/cg-data/working_data/df_CA_Reli_raw.csv', 
                     index_col = 0, dtype ={'postal_code':str, 'stateFIPS':str,
                                            'countyFIPS':str, 'poi_cbg':str})

WorshipPlace = pd.read_csv('/Volumes/LaCie/cg-data/working_data/WorshipPlace.csv', index_col=0)

WorshipPlace = WorshipPlace.merge(raw_df, how = 'left', on = 'safegraph_place_id')


week_list = ['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
             '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17', 
             '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16', 
             '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
             '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
             '2020-05-18', '2020-05-25']

#week_list = ['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20',
#             '2020-01-27', '2020-02-03', '2020-02-10', '2020-02-17', 
#             '2020-02-24', '2020-03-02', '2020-03-09', '2020-03-16', 
#             '2020-03-23', '2020-03-30', '2020-04-06', '2020-04-13',
#             '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11', 
#             '2020-05-18', '2020-05-25', '2020-06-01', '2020-06-08', 
#             '2020-06-15']


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

temp_df.loc[:,'base'] = temp_df.iloc[:,10:18].mean(axis = 1)
BaseVisits = temp_df.loc[temp_df.base > 4, :]
BaseVisits.to_csv('/Volumes/LaCie/cg-data/working_data/BaseVisits.csv')


# 2. Define the shutdown church
BaseVisits = pd.read_csv('/Volumes/LaCie/cg-data/working_data/BaseVisits.csv', index_col = 0)


BaseVisits.loc[:,'pandemic'] = BaseVisits.iloc[:,21:25].min(axis = 1)
BaseVisits.loc[:,'att rate'] = BaseVisits.loc[:,'pandemic'] / BaseVisits.loc[:,'base'] * 100
BaseVisits.loc[:,'shutdown'] = 0

## a. 0 visitors during mid March - early April
BaseVisits.loc[BaseVisits.pandemic == 0, 'shutdown'] = 1
BaseVisits.shutdown.sum()

temp = (BaseVisits.pandemic <= 5) & (BaseVisits.base >= 30)
BaseVisits.loc[temp,'shutdown'] = 1
BaseVisits.shutdown.sum()
temp = BaseVisits.loc[:, 'att rate'] <= 5
BaseVisits.loc[temp,'shutdown'] = 1
BaseVisits.shutdown.sum()


## set 30+ as a large church
temp = BaseVisits.base >= 30
BaseVisits.loc[:,'large'] = 0
BaseVisits.loc[temp,'large'] = 1
BaseVisits.to_csv('/Volumes/LaCie/cg-data/working_data/ClassificationCA.csv')
 