import pandas as pd
import pathlib

#read csv and create dataframe
df = pd.read_csv("C:\\Task\\sector_calc_input.txt", delimiter=',')

#find site from cell_id and insert to dataframe as string data type
site = df['cell_id'].str[0]
df.insert(3, 'site', site, True)
df['site'] = df['site'].astype(str)

#count cells per band in new dataframe dc
dc = df.groupby(['site','band']).size().reset_index().rename(columns={0:'cell_count'})
#when band equals 3 divide by 2
def callculate_cell_count(row_x):
    if row_x['band'] == 3:
        row_x['cell_count'] = int(row_x['cell_count']/2)
    return row_x
#apply function on dc
dc = dc.apply(callculate_cell_count, axis=1)

#find initial sector where band = 1
distinct_sites = dc.site.unique()
for site_var in distinct_sites:
    df.loc[(df["site"]==site_var)&(df["band"]== 1),'sector'] = range(1, 1+len(df[(df["site"]==site_var)&(df["band"]== 1)]))

#fix NaN values to 0
df['sector'] = df['sector'].fillna(0).astype(int)

#create help dataframe ds where sector is not NaN or 0
ds = df.loc[(df['sector']>0)]

#find nearest azimuth and fill in sector value
def def_azimuth_new(input_row, helper_df):
    if input_row["sector"] == 0:
        for input_row["site"] in distinct_sites:
            min_diff = 666
            for azimuth_value in helper_df[helper_df["site"]==(input_row["site"])]["azimuth"]:
                x=180-abs(abs(input_row["azimuth"]- azimuth_value)-180)
                if x < min_diff:
                    min_diff = x
                    pripadajuci_sektor = helper_df[(helper_df["site"]==(input_row["site"])) & (helper_df["azimuth"]==azimuth_value)]["sector"]
                input_row["sektor_new"]=int(pripadajuci_sektor.values)
            return input_row
    input_row["sektor_new"] = 0                  
    return input_row

#apply function on dataframe
df=df.apply(def_azimuth_new, helper_df=ds, axis=1)
#perform addition of two columns as value in one of them is always 0
df['sector'] = df['sector']  + df['sektor_new']
#drop columns sektor_new and site
df = df.drop(['sektor_new', 'site'], axis=1)
#sort by azimuth
df.sort_values(by=['azimuth'], inplace=True)
#write dataframe to file
df = df.to_csv("C:\\Task\\sector_calc_output.txt", index=False)
#print(df)