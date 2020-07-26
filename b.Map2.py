#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 22:26:28 2020

@author: yeabinmoon
"""
import pandas as pd
import folium

geo_josn = '/Volumes/LaCie/cg-data/working_data/ark28722-s7888q-geojson.json'

#url = 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/'
#geo_ca = f'{url}/ca_california_zip_codes_geo.min.json'

url = 'https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Zip_Code_Boundaries/FeatureServer/0/'
geocode = f'{url}/query?where=1%3D1&outFields=*&outSR=4326&f=json'

BaseVisits = pd.read_csv('/Volumes/LaCie/cg-data/working_data/BaseVisits.csv', index_col = 0)
Alameda = BaseVisits.loc[BaseVisits.countyName == 'Alameda County',:]
Alameda_map = Alameda[['location_name', 'latitude', 'longitude']]



#total_device.to_csv('/Volumes/LaCie/cg-data/working_data/total_device.csv')
#home_device.to_csv('/Volumes/LaCie/cg-data/working_data/home_device.csv')
social_distancing = pd.read_csv('/Volumes/LaCie/cg-data/working_data/social_distancing.csv',
                                index_col = 0, dtype = {'ZIP':str})
#social_distancing['01-01'] = social_distancing['01-01'] * 100

m = folium.Map(
    location=[Alameda_map.latitude.iloc[0], Alameda_map.longitude.iloc[0]],
    #tiles = 'Stamen Toner',
    zoom_start=13
)

folium.Choropleth(
    #geo_data = geo_josn,
    geo_data = geocode,
    data=social_distancing,
    columns=['ZIP', '01-01'],
    key_on='ZIP_CODE',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Social Distancing (%)',
).add_to(m)

m.save('/Volumes/LaCie/cg-data/working_data/Map2.html')