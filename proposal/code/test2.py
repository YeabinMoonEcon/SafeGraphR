#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 16:27:55 2020

@author: yeabinmoon
"""


import pandas as pd


df = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/RegionDist.csv',
                 index_col = 0, dtype = {'cbg':str,'year':str})

df = df[['date','cbg','safegraph_place_id','size','visits']]


total = df.groupby(['date', 'cbg'])['visits'].sum()
total = total.reset_index()
total = total.pivot(index= 'cbg', columns = 'date', values = 'visits')
total.fillna(0, inplace = True)
total.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_total.csv')



size0 = df.loc[df.loc[:,'size'] == 0,:]
size0 = size0.groupby(['date', 'cbg'])['visits'].sum()
size0 = size0.reset_index()
size0 = size0.pivot(index= 'cbg', columns = 'date', values = 'visits')
size0.fillna(0, inplace = True)
size0.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size0.csv')


size1 = df.loc[df.loc[:,'size'] == 1,:]
size1 = size1.groupby(['date', 'cbg'])['visits'].sum()
size1 = size1.reset_index()
size1 = size1.pivot(index= 'cbg', columns = 'date', values = 'visits')
size1.fillna(0, inplace = True)
size1.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size1.csv')


size2 = df.loc[df.loc[:,'size'] == 2,:]
size2 = size2.groupby(['date', 'cbg'])['visits'].sum()
size2 = size2.reset_index()
size2 = size2.pivot(index= 'cbg', columns = 'date', values = 'visits')
size2.fillna(0, inplace = True)
size2.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size2.csv')


size3 = df.loc[df.loc[:,'size'] == 3,:]
size3 = size3.groupby(['date', 'cbg'])['visits'].sum()
size3 = size3.reset_index()
size3 = size3.pivot(index= 'cbg', columns = 'date', values = 'visits')
size3.fillna(0, inplace = True)
size3.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size3.csv')


size4 = df.loc[df.loc[:,'size'] == 4,:]
size4 = size4.groupby(['date', 'cbg'])['visits'].sum()
size4 = size4.reset_index()
size4 = size4.pivot(index= 'cbg', columns = 'date', values = 'visits')
size4.fillna(0, inplace = True)
size4.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size4.csv')


size5 = df.loc[df.loc[:,'size'] == 5,:]
size5 = size5.groupby(['date', 'cbg'])['visits'].sum()
size5 = size5.reset_index()
size5 = size5.pivot(index= 'cbg', columns = 'date', values = 'visits')
size5.fillna(0, inplace = True)
size5.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size5.csv')


size6 = df.loc[df.loc[:,'size'] == 6,:]
size6 = size6.groupby(['date', 'cbg'])['visits'].sum()
size6 = size6.reset_index()
size6 = size6.pivot(index= 'cbg', columns = 'date', values = 'visits')
size6.fillna(0, inplace = True)
size6.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/visits_size6.csv')


# size7 = AlSfCounty.loc[AlSfCounty.loc[:,'size'] == 7,:]
# size7 = size7.groupby(['date', 'cbg'])['visits'].sum()
# size7 = size7.reset_index()
# size7 = size7.pivot(index= 'cbg', columns = 'date', values = 'visits')
# size7.fillna(0, inplace = True)
# size7.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visits_size7.csv')





# shutdown = AlSfCounty.loc[AlSfCounty.shutdown == 1,:]
# shutdown = shutdown.groupby(['date', 'cbg'])['visits'].sum()
# shutdown = shutdown.reset_index()
# shutdown = shutdown.pivot(index= 'cbg', columns = 'date', values = 'visits')
# shutdown.fillna(0, inplace = True)
# shutdown.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visist_shutdown.csv')

# Open = AlSfCounty.loc[AlSfCounty.shutdown == 0,:]
# Open = Open.groupby(['date', 'cbg'])['visits'].sum()
# Open = Open.reset_index()
# Open = Open.pivot(index= 'cbg', columns = 'date', values = 'visits')
# Open.fillna(0, inplace = True)
# Open.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visist_open.csv')


# large = AlSfCounty.loc[AlSfCounty.large == 1,:]
# large = large.groupby(['date', 'cbg'])['visits'].sum()
# large = large.reset_index()
# large = large.pivot(index= 'cbg', columns = 'date', values = 'visits')
# large.fillna(0, inplace = True)
# large.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visist_large.csv')


# small = AlSfCounty.loc[AlSfCounty.large == 0,:]
# small = small.groupby(['date', 'cbg'])['visits'].sum()
# small = small.reset_index()
# small = small.pivot(index= 'cbg', columns = 'date', values = 'visits')
# small.fillna(0, inplace = True)
# small.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visist_small.csv')





# total.loc[:,'before'] = total.iloc[:,0:8].mean(axis = 1)
# total.loc[:,'after'] = total.iloc[:,9:13].min(axis = 1)
# total.loc[:,'instrument'] = (large.iloc[:,0:8] / total.iloc[:,0:8]).mean(axis = 1)

# df_reg = total[['before','after','instrument']]
# df_reg.reset_index(inplace = True)
# df_reg.fillna(0, inplace = True)
# df_reg.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/df_reg.csv')
