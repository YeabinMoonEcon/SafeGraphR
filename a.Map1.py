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
import webbrowser
import folium

BaseVisits = pd.read_csv('/Volumes/LaCie/cg-data/working_data/BaseVisits.csv', index_col = 0)
Alameda = BaseVisits.loc[BaseVisits.countyName == 'Alameda County',:]

Alameda['before'] = Alameda.iloc[:,11:20].mean(axis = 1)
Alameda['after'] = Alameda.iloc[:,20:26].min(axis = 1)

Alameda_map = Alameda[['location_name', 'latitude', 'longitude', 'before', 'after']]

Alameda_map.before = Alameda_map.before*5
Alameda_map.after = Alameda_map.after*5




m = folium.Map(
    location=[Alameda_map.latitude.iloc[0], Alameda_map.longitude.iloc[0]],
    #tiles = 'Stamen Toner',
    zoom_start=13
)



for i in range(len(Alameda_map)):
    folium.Circle(
    radius= Alameda_map.before.iloc[i] * 4.5,
    location= [Alameda_map.latitude.iloc[i], Alameda_map.longitude.iloc[i]],
    popup= Alameda_map.location_name.iloc[i],
    color='crimson',
    fill=False,
    ).add_to(m)

for i in range(len(Alameda_map)):
    folium.Circle(
    radius= Alameda_map.after.iloc[i] * 4.5,
    location= [Alameda_map.latitude.iloc[i], Alameda_map.longitude.iloc[i]],
    popup= Alameda_map.location_name.iloc[i],
    color='blue',
    fill=False,
    ).add_to(m)



m.save('/Volumes/LaCie/cg-data/working_data/Map1.html')    
