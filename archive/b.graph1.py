#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 15:20:54 2020

@author: yeabinmoon
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BaseList = pd.read_csv('/Volumes/LaCie/cg-data/working_data/ClassificationCA.csv',
                       usecols = ['safegraph_place_id','shutdown', 'large'])

BaseVisits = pd.read_csv('/Volumes/LaCie/cg-data/working_data/BaseVisits.csv', index_col = 0)
Alameda = BaseVisits.loc[BaseVisits.countyName == 'Alameda County',:]

Alameda.drop(columns = 'base', inplace = True)

Alameda = Alameda.merge(BaseList, how = 'left', on = 'safegraph_place_id')

small = Alameda.loc[Alameda.large == 0,:]
large = Alameda.loc[Alameda.large == 1,:]

visitor_small_before = small.iloc[:,11:19].sum().mean()
visitor_large_before = large.iloc[:,11:19].sum().mean()

#visitor_small_after = small.iloc[:,20:26].sum().mean()
#visitor_large_after = large.iloc[:,20:26].sum().mean()

#visitor_small_after / visitor_small_before * 100
#visitor_large_after / visitor_large_before * 100



v_s_b = small.iloc[:,11:19].mean().mean()
v_l_b = large.iloc[:,11:19].mean().mean()
v_s_a = small.iloc[:,20:26].mean().mean()
v_l_a = large.iloc[:,20:26].mean().mean()


df = pd.DataFrame({'worship places':['small before', 'small after', 'large before', 'large after'], 'Avg visitors':[v_s_b, v_s_a, v_l_b, v_l_a]})
ax = df.plot.bar(x='worship places', y='Avg visitors', rot=0)




def ecdf(data):
    """Compute ECDF for a one-dimensional array of measurements."""
    # Number of data points: n
    n = len(data)
    # x-data for the ECDF: x
    x = np.sort(data)
    # y-data for the ECDF: y
    y = np.arange(1, n+1) / n
    return x, y

Alameda['base'].quantile([.8769])

Alameda['base'] = Alameda.iloc[:,11:19].mean(axis = 1)
x_vers, y_vers = ecdf(Alameda['base'])
_ = plt.plot(x_vers, y_vers, '.')
_ = plt.xlabel('tne num of unique visitors prior to pandemic')
_ = plt.ylabel('ECDF')
_ = plt.title('Distribution of worship places')
