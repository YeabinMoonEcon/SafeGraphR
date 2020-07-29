import pandas as pd
#import matplotlib.pyplot as plt
#from wordcloud import WordCloud, STOPWORDS

"""
Data created:
    df_CA_Reli_raw.csv: the raw list of religious POI in CA.

The number of religious places for POI in CA is 18510.
"""



cols_list = ['safegraph_place_id','location_name',
             'naics_code', 'latitude', 'longitude',
             'city', 'region', 'postal_code', ]

list_of_files = ['core_poi-part1.csv', 'core_poi-part2.csv', 'core_poi-part3.csv', 'core_poi-part4.csv','core_poi-part5.csv']

df_POI_NAICS = pd.DataFrame()

for file in list_of_files:
    temp_df = pd.read_csv('/Volumes/LaCie/cg-data/core_place/' + file,
                          usecols = cols_list,
                          dtype = {'naics_code':str, 'postal_code':str})
    df_POI_NAICS = pd.concat([df_POI_NAICS,temp_df], axis = 0, ignore_index = True)


"""
1. CA
2. NAICS code = 813110
"""
temp = (df_POI_NAICS.region == 'CA') & (df_POI_NAICS.naics_code == '813110')
df_CA_Reli = df_POI_NAICS.loc[temp,:]

"""
add POI
"""

temp_df = pd.read_csv('/Volumes/LaCie/cg-data/placeToCBGMay/placeCountyCBG.csv',
                      dtype = {'CBGFIPS':str, 'stateFIPS':str, 'countyFIPS':str},
                      usecols = ['safegraph_place_id','stateFIPS', 'countyFIPS', 'countyName', 'CBGFIPS'])
temp_df.rename(columns = {'CBGFIPS':'poi_cbg'}, inplace = True)

df_CA_Reli = df_CA_Reli.merge(temp_df, how = 'left', on = 'safegraph_place_id')
df_CA_Reli.drop(columns = 'naics_code', inplace = True)
df_CA_Reli.to_csv('/Users/yeabinmoon/Dropbox (UH-ECON)/Thesis/proposal/data/df_CA_Reli_raw.csv')



#text = " ".join(name for name in df_CA_Reli.location_name) # all words in location_name
#print ("There are {0} words across all location_name for all {1} poi.".format(len(text), df_CA_Reli.shape[0]))
#wordcloud = WordCloud(background_color="white").generate(text)

#plt.figure(figsize=(11,11))
#plt.imshow(wordcloud, interpolation='bilinear')
#plt.axis("off")
#plt.show()
