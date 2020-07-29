#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 16:31:01 2020

@author: yeabinmoon
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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




visits_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_total.csv',
                          dtype = {'cbg':str})
visits_total.loc[:,'TRACT'] =  visits_total.cbg.str[:-1] 
visits_total = visits_total.iloc[:,1:]
list_dates = visits_total.columns
visits_total_tract = visits_total.groupby('TRACT')[list_dates[:-1]].sum()
visits_total_tract.reset_index(inplace = True)
visits_total_zip = visits_total_tract.merge(zipcode, how = 'left' , on = 'TRACT')
visits_total_zip = visits_total_zip.groupby('ZIP')[list_dates[:-1]].sum()
visits_total_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_total_zip.csv')


visits_size0 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size0.csv',
                          dtype = {'cbg':str})
visits_size0.loc[:,'TRACT'] =  visits_size0.cbg.str[0:-1] 
visits_size0 = visits_size0.iloc[:,1:]
list_dates = visits_size0.columns
visits_size0_tract = visits_size0.groupby('TRACT')[list_dates[:-1]].sum()
visits_size0_tract.reset_index(inplace = True)
visits_size0_zip = visits_size0_tract.merge(zipcode, how = 'left' , on = 'TRACT')
visits_size0_zip = visits_size0_zip.groupby('ZIP')[list_dates[:-1]].sum()
visits_size0_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size0_zip.csv')


visits_size1 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size1.csv',
                          dtype = {'cbg':str})
visits_size1.loc[:,'TRACT'] =  visits_size1.cbg.str[0:-1] 
visits_size1 = visits_size1.iloc[:,1:]
list_dates = visits_size1.columns
visits_size1_tract = visits_size1.groupby('TRACT')[list_dates[:-1]].sum()
visits_size1_tract.reset_index(inplace = True)
visits_size1_zip = visits_size1_tract.merge(zipcode, how = 'left' , on = 'TRACT')
visits_size1_zip = visits_size1_zip.groupby('ZIP')[list_dates[:-1]].sum()
visits_size1_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size1_zip.csv')


visits_size1 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size1.csv',
                          dtype = {'cbg':str})
visits_size1.loc[:,'TRACT'] =  visits_size1.cbg.str[0:-1] 
visits_size1 = visits_size1.iloc[:,1:]
list_dates = visits_size1.columns
visits_size1_tract = visits_size1.groupby('TRACT')[list_dates[:-1]].sum()
visits_size1_tract.reset_index(inplace = True)
visits_size1_zip = visits_size1_tract.merge(zipcode, how = 'left' , on = 'TRACT')
visits_size1_zip = visits_size1_zip.groupby('ZIP')[list_dates[:-1]].sum()
visits_size1_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size1_zip.csv')


visits_size2 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size2.csv',
                          dtype = {'cbg':str})
visits_size2.loc[:,'TRACT'] =  visits_size2.cbg.str[0:-1] 
visits_size2 = visits_size2.iloc[:,1:]
list_dates = visits_size2.columns
visits_size2_tract = visits_size2.groupby('TRACT')[list_dates[:-1]].sum()
visits_size2_tract.reset_index(inplace = True)
visits_size2_zip = visits_size2_tract.merge(zipcode, how = 'left' , on = 'TRACT')
visits_size2_zip = visits_size2_zip.groupby('ZIP')[list_dates[:-1]].sum()
visits_size2_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size2_zip.csv')


visits_size3 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size3.csv',
                          dtype = {'cbg':str})
visits_size3.loc[:,'TRACT'] =  visits_size3.cbg.str[0:-1] 
visits_size3 = visits_size3.iloc[:,1:]
list_dates = visits_size3.columns
visits_size3_tract = visits_size3.groupby('TRACT')[list_dates[:-1]].sum()
visits_size3_tract.reset_index(inplace = True)
visits_size3_zip = visits_size3_tract.merge(zipcode, how = 'left' , on = 'TRACT')
visits_size3_zip = visits_size3_zip.groupby('ZIP')[list_dates[:-1]].sum()
visits_size3_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size3_zip.csv')



visits_size4 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size4.csv',
                          dtype = {'cbg':str})
visits_size4.loc[:,'TRACT'] =  visits_size4.cbg.str[0:-1] 
visits_size4 = visits_size4.iloc[:,1:]
list_dates = visits_size4.columns
visits_size4_tract = visits_size4.groupby('TRACT')[list_dates[:-1]].sum()
visits_size4_tract.reset_index(inplace = True)
visits_size4_zip = visits_size4_tract.merge(zipcode, how = 'left' , on = 'TRACT')
visits_size4_zip = visits_size4_zip.groupby('ZIP')[list_dates[:-1]].sum()
visits_size4_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size4_zip.csv')


visits_size5 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size5.csv',
                          dtype = {'cbg':str})
visits_size5.loc[:,'TRACT'] =  visits_size5.cbg.str[0:-1] 
visits_size5 = visits_size5.iloc[:,1:]
list_dates = visits_size5.columns
visits_size5_tract = visits_size5.groupby('TRACT')[list_dates[:-1]].sum()
visits_size5_tract.reset_index(inplace = True)
visits_size5_zip = visits_size5_tract.merge(zipcode, how = 'left' , on = 'TRACT')
visits_size5_zip = visits_size5_zip.groupby('ZIP')[list_dates[:-1]].sum()
visits_size5_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size5_zip.csv')


visits_size6 = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size6.csv',
                          dtype = {'cbg':str})
visits_size6.loc[:,'TRACT'] =  visits_size6.cbg.str[0:-1] 
visits_size6 = visits_size6.iloc[:,1:]
list_dates = visits_size6.columns
visits_size6_tract = visits_size6.groupby('TRACT')[list_dates[:-1]].sum()
visits_size6_tract.reset_index(inplace = True)
visits_size6_zip = visits_size6_tract.merge(zipcode, how = 'left' , on = 'TRACT')
visits_size6_zip = visits_size6_zip.groupby('ZIP')[list_dates[:-1]].sum()
visits_size6_zip.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size6_zip.csv')


visits_size6_zip.sum(axis = 0).plot()
visits_size5_zip.sum(axis = 0).plot()
visits_size4_zip.sum(axis = 0).plot()
visits_size3_zip.sum(axis = 0).plot()
visits_size2_zip.sum(axis = 0).plot()
visits_size1_zip.sum(axis = 0).plot()
visits_size0_zip.sum(axis = 0).plot()



visits_size6_zip.sum(axis = 0)
visits_size5_zip.sum(axis = 0)
visits_size4_zip.sum(axis = 0)
visits_size3_zip.sum(axis = 0)
visits_size2_zip.sum(axis = 0)
visits_size1_zip.sum(axis = 0)
visits_size0_zip.sum(axis = 0)

plt.scatter(list(visits_size6_zip.columns), visits_size6_zip.sum(axis = 0), color = 'b')
plt.scatter(list(visits_size5_zip.columns), visits_size5_zip.sum(axis = 0), color = 'y')
plt.scatter(list(visits_size4_zip.columns), visits_size4_zip.sum(axis = 0), color = 'g')
plt.xticks(rotation=90)

plt.scatter(list(visits_size3_zip.columns), visits_size3_zip.sum(axis = 0), color = 'b')
plt.scatter(list(visits_size2_zip.columns), visits_size2_zip.sum(axis = 0), color = 'y')
plt.scatter(list(visits_size1_zip.columns), visits_size1_zip.sum(axis = 0), color = 'g')
plt.xticks(rotation=90)
plt.scatter(list(visits_size0_zip.columns), visits_size0_zip.sum(axis = 0), color = 'g')
plt.xticks(rotation=90)

a = visits_size6_zip.add(visits_size5_zip, axis = 0)
