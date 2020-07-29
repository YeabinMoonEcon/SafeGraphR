#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:04:16 2020

@author: yeabinmoon
    The center of the circle points to the worship place in Alameda county.
    The size of the circle implies the number of visitors.
Data created:
    Map1.html: the number of visistors is scaled by X 4.5
               Red circle: previous pandemic
               blue circle: during pandemic

"""

import pandas as pd
import folium

BaseVisits = pd.read_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/BaseVisits.csv', index_col = 0)
temp = (BaseVisits.countyName == 'Alameda County') | (BaseVisits.countyName == 'San Francisco County')
AlandSF = BaseVisits.loc[temp,:]

AlandSF.loc[:,'before'] = AlandSF.iloc[:,11:19].mean(axis = 1)
AlandSF.loc[:,'after']  = AlandSF.iloc[:,20:24].min(axis = 1)

AlandSF_map = AlandSF[['location_name', 'latitude', 'longitude', 'before', 'after']]


AlandSF_map.before = AlandSF_map.before*5
AlandSF_map.after = AlandSF_map.after*5




m = folium.Map(
    location=[AlandSF_map.latitude.iloc[0], AlandSF_map.longitude.iloc[0]],
    #tiles = 'Stamen Toner',
    zoom_start=13
)



for i in range(len(AlandSF_map)):
    folium.Circle(
    radius= AlandSF_map.before.iloc[i] * 4.5,
    location= [AlandSF_map.latitude.iloc[i], AlandSF_map.longitude.iloc[i]],
    popup= AlandSF_map.location_name.iloc[i],
    color='crimson',
    fill=False,
    ).add_to(m)

for i in range(len(AlandSF_map)):
    folium.Circle(
    radius= AlandSF_map.after.iloc[i] * 4.5,
    location= [AlandSF_map.latitude.iloc[i], AlandSF_map.longitude.iloc[i]],
    popup= AlandSF_map.location_name.iloc[i],
    color='blue',
    fill=False,
    ).add_to(m)



m.save('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/figures/Map1.html')
