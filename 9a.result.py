#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 23:14:17 2020

@author: yeabinmoon
"""

import pandas as pd


baseline_total_visitor = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/baseline_total_visitor.csv',
                                     index_col = 0, dtype = {'ZIP':str})
baseline_large_visitor=pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/baseline_large_visitor.csv',
                                   index_col = 0, dtype = {'ZIP':str})
baseline_large_visitor.fillna(0, inplace = True)

baseline_total_device=pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/baseline_total_device.csv',
                                  index_col = 0, dtype = {'ZIP':str})


baseline_total_visitor.loc[:,'base'] = baseline_total_visitor.iloc[:,1:9].mean(axis = 1)
baseline_total_visitor.loc[:,'after'] = baseline_total_visitor.iloc[:,10:14].min(axis = 1)
temp_df = baseline_total_visitor[['ZIP','base','after']]

baseline_large_visitor.loc[:,'large'] = baseline_large_visitor.iloc[:,1:9].mean(axis = 1)
temp_df2 = baseline_large_visitor[['ZIP','large']]

baseline_total_device.loc[:,'device'] = baseline_total_device.iloc[:,1:9].mean(axis = 1)
temp_df3 = baseline_total_device[['ZIP','device']]

temp_df = temp_df.merge(temp_df2, how = 'left', on = 'ZIP')
temp_df = temp_df.merge(temp_df3, how = 'left', on = 'ZIP')

temp_df.loc[:,'share'] = temp_df.loc[:, 'large'] / temp_df.loc[:, 'base'] 
temp_df.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/output.csv')
