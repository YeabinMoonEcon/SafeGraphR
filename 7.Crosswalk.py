#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 18:34:27 2020

@author: yeabinmoon
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

zipcode = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx', 
                        dtype = {'ZIP':str, 'TRACT':str},
                        usecols = ['ZIP', 'TRACT', 'RES_RATIO'])
zipcode.set_index('ZIP',inplace = True)
zipcode = zipcode.groupby('TRACT')['RES_RATIO'].idxmax()
zipcode = zipcode.reset_index()
zipcode.rename(columns = {'RES_RATIO':'ZIP'}, inplace = True)


visit_total1 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/visits_total1.csv',
                            index_col = 0, dtype = {'cbg':str})
visit_total1.loc[:,'TRACT'] =  visit_total1.cbg.str[:-1]
visit_total1.loc[:,'FIPS'] =  visit_total1.cbg.str[0:5]

temp = (visit_total1.loc[:,'FIPS'] == '06001') | (visit_total1.loc[:,'FIPS'] == '06075') \
        | (visit_total1.loc[:,'FIPS'] == '06085') | (visit_total1.loc[:,'FIPS'] == '06081') \
        | (visit_total1.loc[:,'FIPS'] == '06013') | (visit_total1.loc[:,'FIPS'] == '06041') \

visit_total1 = visit_total1.loc[temp, :]
visit_total1.drop(columns = {'cbg', 'FIPS'}, inplace = True)
list_dates = visit_total1.columns
visit_total_tract1 = visit_total1.groupby('TRACT')[list_dates[:-1]].sum()
visit_total_tract1.reset_index(inplace = True)
visit_total_zip1 = visit_total_tract1.merge(zipcode, how = 'left' , on = 'TRACT')
visit_total_zip1 = visit_total_zip1.groupby('ZIP')[list_dates[:-1]].sum()
visit_total_zip1.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/visit_total_zip1.csv')


visits_large1 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/visits_large1.csv',
                            index_col = 0, dtype = {'cbg':str})
visits_large1.loc[:,'TRACT'] =  visits_large1.cbg.str[:-1]
visits_large1.loc[:,'FIPS'] =  visits_large1.cbg.str[0:5]

temp = (visits_large1.loc[:,'FIPS'] == '06001') | (visits_large1.loc[:,'FIPS'] == '06075') \
        | (visits_large1.loc[:,'FIPS'] == '06085') | (visits_large1.loc[:,'FIPS'] == '06081') \
        | (visits_large1.loc[:,'FIPS'] == '06013') | (visits_large1.loc[:,'FIPS'] == '06041') \

visits_large1 = visits_large1.loc[temp, :]
visits_large1.drop(columns = {'cbg', 'FIPS'}, inplace = True)
list_dates = visits_large1.columns
visit_large_tract1 = visits_large1.groupby('TRACT')[list_dates[:-1]].sum()
visit_large_tract1.reset_index(inplace = True)
visit_large_zip1 = visit_large_tract1.merge(zipcode, how = 'left' , on = 'TRACT')
visit_large_zip1 = visit_large_zip1.groupby('ZIP')[list_dates[:-1]].sum()
visit_large_zip1.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/output/data/temp/visit_large_zip1.csv')

