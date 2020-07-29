#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 22:20:15 2020

@author: yeabinmoon
"""

import pandas as pd

#zip_code = pd.read_excel('/Volumes/LaCie/cg-data/core_place/TRACT_ZIP_032020.xlsx', 
#                        dtype = {'ZIP':str,'TRACT':str}, usecols = ['ZIP','TRACT'])
#zip_unique = zip_code.loc[~zip_code.TRACT.duplicated(),:]

zipcode = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx',
                     dtype = {'ZIP':str,'TRACT':str}, usecols = ['ZIP','TRACT'])

zip_unique = zipcode.loc[~zipcode.TRACT.duplicated(),:]




device_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/total_device.csv',
                           index_col = 0, dtype = {'origin_census_block_group':str})
device_home = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/home_device.csv',
                          index_col = 0, dtype = {'origin_census_block_group':str})
device_distance = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/social_distancing.csv',
                              index_col = 0, dtype = {'origin_census_block_group':str})
visit_total = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visist_total.csv',
                          dtype = {'cbg':str})
visit_large = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/visist_large.csv',
                          dtype = {'cbg':str})

visit_total.loc[:,'TRACT'] = visit_total.cbg.str[:-1]
visit_total = visit_total.merge(zip_unique, how = 'left', on = 'TRACT')
temp = visit_total.iloc[:,1:]
visit_total_zip = temp.groupby('ZIP')['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20', '2020-01-27',
                                      '2020-02-03', '2020-02-10', '2020-02-17', '2020-02-24', '2020-03-02',
                                      '2020-03-09', '2020-03-16', '2020-03-23', '2020-03-30', '2020-04-06',
                                      '2020-04-13', '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11',
                                      '2020-05-18', '2020-05-25'].sum()


visit_large.loc[:,'TRACT'] = visit_large.cbg.str[:-1]
visit_large = visit_large.merge(zip_unique, how = 'left', on = 'TRACT')
temp = visit_large.iloc[:,1:]
visit_large_zip = temp.groupby('ZIP')['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20', '2020-01-27',
                                      '2020-02-03', '2020-02-10', '2020-02-17', '2020-02-24', '2020-03-02',
                                      '2020-03-09', '2020-03-16', '2020-03-23', '2020-03-30', '2020-04-06',
                                      '2020-04-13', '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11',
                                      '2020-05-18', '2020-05-25'].sum()


visit_total_zip.reset_index(inplace = True)
visit_large_zip.reset_index(inplace = True)
large_list = visit_total_zip.loc[:,['ZIP']]
large_list = large_list.merge(visit_large_zip, how = 'left', on = 'ZIP')
large_list.fillna(0, inplace = True)


visit_total_zip.loc[:,'before'] = visit_total_zip.iloc[:,1:9].mean(axis = 1)
visit_total_zip.loc[:,'after'] = visit_total_zip.iloc[:,10:14].min(axis = 1)
visit_total_zip.loc[:,'instrument'] = (large_list.iloc[:,1:9] / visit_total_zip.iloc[:,1:9]).mean(axis = 1)


df_reg = visit_total_zip[['before','after','instrument']]
#df_reg.reset_index(inplace = True)
df_reg.fillna(0, inplace = True)
df_reg.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/df_reg3.csv')









#visit_total.loc[:,'FIPS'] = visit_total.cbg.str[0:5]
#visit_total.loc[:,'TRACT'] = visit_total.cbg.str[5:10]

# visit_total.loc[:,'TRACT'] = visit_total.cbg.str[0:10]
# temp = visit_total.iloc[:,1:]
# visit_total_tract = temp.groupby('TRACT')['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20', '2020-01-27',
#                                           '2020-02-03', '2020-02-10', '2020-02-17', '2020-02-24', '2020-03-02',
#                                           '2020-03-09', '2020-03-16', '2020-03-23', '2020-03-30', '2020-04-06',
#                                           '2020-04-13', '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11',
#                                           '2020-05-18', '2020-05-25'].sum()
        
# visit_large.loc[:,'TRACT'] = visit_large.cbg.str[0:10]
# temp = visit_large.iloc[:,1:]
# visit_large_tract = temp.groupby('TRACT')['2019-12-30', '2020-01-06', '2020-01-13', '2020-01-20', '2020-01-27',
#                                           '2020-02-03', '2020-02-10', '2020-02-17', '2020-02-24', '2020-03-02',
#                                           '2020-03-09', '2020-03-16', '2020-03-23', '2020-03-30', '2020-04-06',
#                                           '2020-04-13', '2020-04-20', '2020-04-27', '2020-05-04', '2020-05-11',
#                                           '2020-05-18', '2020-05-25'].sum()

# visit_total_tract.reset_index(inplace = True)
# visit_large_tract.reset_index(inplace = True)
# large_list = visit_total_tract.loc[:,['TRACT']]
# large_list = large_list.merge(visit_large_tract, how = 'left', on = 'TRACT')
# large_list.fillna(0, inplace = True)

# visit_total_tract.loc[:,'before'] = visit_total_tract.iloc[:,1:9].mean(axis = 1)
# visit_total_tract.loc[:,'after'] = visit_total_tract.iloc[:,10:14].min(axis = 1)
# visit_total_tract.loc[:,'instrument'] = (large_list.iloc[:,1:9] / visit_total_tract.iloc[:,1:9]).mean(axis = 1)


# df_reg = visit_total_tract[['before','after','instrument']]
# #df_reg.reset_index(inplace = True)
# df_reg.fillna(0, inplace = True)
# df_reg.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/temp/df_reg2.csv')
