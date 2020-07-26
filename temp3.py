#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 18:02:49 2020

@author: yeabinmoon
"""

import pandas as pd

zipcode = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx',
                     dtype = {'ZIP':str,'TRACT':str}, usecols = ['ZIP','TRACT'])

zip_raw = pd.read_excel('/Volumes/LaCie/cg-data/core_place/ZIP_TRACT_032020.xlsx', nrows = 10)


zip_unique = zipcode.loc[~zipcode.TRACT.duplicated(),:]


test = zipcode.iloc[0:100]

zipcode['FIPS'] = zipcode.TRACT.str[0:5]
zipcode['state'] = zipcode.TRACT.str[0:2]

CA_zip = zipcode.loc[zipcode.state == '06',:]

dup_CA =  CA_zip.loc[CA_zip.TRACT.duplicated(),:]
uni_CA = CA_zip.loc[~CA_zip.TRACT.duplicated(),:]
