# Test mapping

import pandas as pd
import folium

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### Functions for simple mapping using folium
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def make_map_plot(df_,
                  plot_limit=3000,
                  radius_col=None,
                  radius_mod=100,
                  color='black',
                  fill_color='red',
                  fill_opacity = 0.2,
                  pop_up_col=None,
                  tooltip = 'Click for more info.',
                  zoom_start=4,
                  tiles = 'OpenStreetMap',
                  map_width = 700,
                  map_height = 400,
                  marker_type= 'circle',
                  map_plot=None,
                  verbose=False):
    # Parameters:
      # df_ is a pandas dataframe. It requires a column called "latitude" and a column called "longitude".
      # radius_col is a column_name or None. If None, every point is given a fixed radius.
          # Otherwise, the value in the column radius_col is used as the radius.
      # radius_mod is to scale your radius units to correspond to units on your map.
      # zoom_start is the scale of the map. Larger numbers = higher resolution.
      # color, fill_color, fill_opacity are marker parameters, see others: https://leafletjs.com/reference-1.3.4.html#path
      # tiles determines the base layer. Open source options include 'OpenStreetMap', 'Stamen Terrain', 'Stamen Toner'
      # map_width and map_height determine the size of the map image (in pixels)
      # marker_type determines what type of marker is being drawn on the map. Options: 'circle' or 'normal'

    # check valid inputs
    valid_inputs = {'marker_type' : {'val' : marker_type, 'valids' : ['circle', 'normal']},
                    'tiles' :  {'val' : tiles, 'valids': ['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Mapbox Bright', 'Mapbox Control Room']},
                    'radius_col' : {'val' : radius_col, 'valids' : [None] + [col for col in df_.columns if pd.api.types.is_numeric_dtype(df_[col])]}}
    for param, param_valid_dict in valid_inputs.items():
      if(param_valid_dict['val'] not in param_valid_dict['valids']):
        raise Exception("Invalid parameter input for '{0}'. Valid options are {1}. input value was '{2}' .".format(param, param_valid_dict['valids'], param_valid_dict['val']))

    # create basemap
    if(not map_plot):
      map_plot = folium.Map(width=map_width,
                            height=map_height,
                            location=[df_.latitude.mean(), df_.longitude.mean()],
                            tiles=tiles,
                            zoom_start=zoom_start,
                            control_scale = True)

    # add markers
    counter = 0
    for index, row in df_.iterrows():
        counter+=1
        if(marker_type=='circle'):
          add_circle_marker_to_map(map_plot, row, radius_col, radius_mod, color, fill_color, fill_opacity, pop_up_col, tooltip)
        elif(marker_type=='normal'):
          add_marker_to_map(map_plot, row, pop_up_col, tooltip)
        if(counter>plot_limit): break
    if(verbose): print("Plotted {0} locations".format(counter))
    return(map_plot)


def add_marker_to_map(map_plot, row, pop_up_col, tooltip):
  folium.Marker([row.latitude, row.longitude],
                        popup= row[pop_up_col] if pop_up_col else None,
                        tooltip=tooltip if pop_up_col else None,
                   ).add_to(map_plot)
  return(None)


def add_circle_marker_to_map(map_plot, row, radius_col, radius_mod, color, fill_color, fill_opacity, pop_up_col, tooltip):
  folium.CircleMarker([row.latitude, row.longitude],
                        radius= row[radius_col]/radius_mod if radius_col else 2,
                        color = color,
                        fill_color = fill_color,
                        weight=0.5,
                        fill_opacity= fill_opacity,
                        popup= row[pop_up_col] if pop_up_col else None,
                        tooltip=tooltip if pop_up_col else None,
                   ).add_to(map_plot)
  return(None)
###########################################################################################

#dtypes = {'postal_code':str,'stateFIPS':str,'countyFIPS':str,'poi_cbg':str}
#list_ca = pd.read_csv('/Volumes/LaCie/cg-data/working_data/df_CA_Reli_raw.csv',
#                      index_col = 0, dtype = dtypes)
#Almeda = list_ca.loc[list_ca.countyName == 'Alameda County',:]

raw_df = pd.read_csv('/Volumes/LaCie/cg-data/working_data/df_CA_Reli_raw.csv',
                         index_col = 0, dtype ={'postal_code':str, 'stateFIPS':str,
                                            'countyFIPS':str, 'poi_cbg':str})
BaseList = pd.read_csv('/Volumes/LaCie/cg-data/working_data/ClassificationCA.csv',
                       usecols = ['safegraph_place_id','shutdown', 'large'])
BaseList = BaseList.merge(raw_df, how = 'left', on = 'safegraph_place_id')


Alameda = BaseList.loc[BaseList.countyName == 'Alameda County',:]
Alameda_shutdown = Alameda[Alameda.shutdown == 1]
Alameda_open = Alameda[Alameda.shutdown == 0]

make_map_plot(Alameda_open, zoom_start=10, fill_color='blue', fill_opacity=1)
make_map_plot(Alameda_shutdown, zoom_start=10, fill_color='red', fill_opacity=1)
