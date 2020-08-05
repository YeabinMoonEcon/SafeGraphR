#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 22:14:06 2020

@author: yeabinmoon
"""

import pandas as pd

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
nyt_data = pd.read_csv(url,  dtype = {'fips':str}, nrows = 10)


## JHU confirmed
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
confirmed = pd.read_csv(url,  dtype = {'UID':str})

confirmed.drop(columns = {'FIPS','iso2','iso3','code3','FIPS','Admin2','Country_Region',
                          'Lat','Long_','Combined_Key'}, inplace = True)
confirmed.loc[:,'FIPS'] = confirmed.loc[:,'UID'].str[3:]
confirmed.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/confirmed.csv')


url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
death = pd.read_csv(url,  dtype ={'UID':str})

death.drop(columns = {'FIPS','iso2','iso3','code3','FIPS','Admin2','Country_Region',
                          'Lat','Long_','Combined_Key'}, inplace = True)
death.loc[:,'FIPS'] = death.loc[:,'UID'].str[3:]
death.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/data/temp/death.csv')




#url = 'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv'
#countypop = pd.read_csv(url, nrows = 1000, dtype = {'STATE':str,'COUNTY':str})

url = 'http://johncostella.com/covid-19/data/latest.csv'
temp = pd.read_csv(url, nrows = 100)


url = 'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/asrh/cc-est2019-alldata.csv'
temp = pd.read_csv(url, nrows = 100)
temp.columns
