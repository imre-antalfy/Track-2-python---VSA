# -*- coding: utf-8 -*-

# %% import

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%% read gas data 15/16
# be careful, each excel needs to be of the same structure for this section to work

# construct filename
str1 = '2_Gasmengen gemessen 20'
str2 = '.xlsx'
years = [15, 16, 17]

d = {}
Gas_daily_15_17 = pd.DataFrame(data=d)

for i in years:

    # generate name of file and dataframe 
    filename = str1 + str(i)  + str2

    # import gas data
    Reader = pd.read_excel(filename, sheet_name='Jahr', header=0)
    Reader.rename(columns = {'Unnamed: 0':'Datum'}, inplace=True)
    Reader = Reader.set_index('Datum')
   
    # merge data
    Gas_daily_15_17 = pd.concat([Gas_daily_15_17,Reader])

# Purge hours for index
Gas_daily_15_17.index = Gas_daily_15_17.index.map(lambda t: t.strftime('%Y-%m-%d'))

#%% read gas data 17-19

# construct filename
str1 = '2_Gasmengen gerechnet 20'
str2 = '.xlsx'
years = [18, 19]

d = {}
Gas_monthly_17_19 = pd.DataFrame(data=d)

for i in years:

    # generate name of file and dataframe 
    filename = str1 + str(i)  + str2

    # import gas data
    Reader = pd.read_excel(filename, sheet_name='Jahr', header=0)
    Reader.rename(columns = {'Unnamed: 0':'Datum'}, inplace=True)
    Reader = Reader.set_index('Datum')
    
    # merge data
    Gas_monthly_17_19 = pd.concat([Gas_monthly_17_19,Reader])

# Purge hours for index
Gas_monthly_17_19.index = Gas_monthly_17_19.index.map(lambda t: t.strftime('%Y-%m-%d'))

#%% read internal sludge input data
FS_int = pd.read_excel('1_Frischschlamm 2015-2019_rework.xlsx', header=0)
FS_int['Datum'] = pd.to_datetime(FS_int['Datum'])
FS_int = FS_int.set_index('Datum')

# Purge hours for index
FS_int.index = FS_int.index.map(lambda t: t.strftime('%Y-%m-%d'))

# Calculating Load base on TS/oTS
FS_int['FS intern Fracht [m³/d]'] = (  FS_int['FS intern Durchsatz [m³]'] * 
                                FS_int['FS intern Trockenrückstand [%]'] *
                                (100 - FS_int['FS intern Glührückstand [% TR]']) /
                                10000
                                )


#%% read external sludge input data
FS_ext = pd.read_excel('1_Frischschlamm Fremd 2015-2019_rework.xlsx', header=0)
FS_ext['Datum'] = pd.to_datetime(FS_ext['Datum'])
FS_ext = FS_ext.set_index('Datum')

# Purge hours for index
FS_ext.index = FS_ext.index.map(lambda t: t.strftime('%Y-%m-%d'))

# Calculating Load base on TS/oTS
FS_ext['FS extern Fracht [m³/d]'] = (  FS_ext['FS extern Durchsatz [m³]'] * 
                                FS_ext['FS extern Trockenrückstand [%]'] *
                                (100 - FS_ext['FS extern Glührückstand [% TR]']) /
                                10000
                                )

#%% read gas analytics data
Gas_analytics = pd.read_excel('2_Gasanalysen 2015-2019_rework.xlsx')
Gas_analytics['Datum'] = pd.to_datetime(Gas_analytics['Datum'])
Gas_analytics = Gas_analytics.set_index('Datum')

# Purge hours for index
Gas_analytics.index = Gas_analytics.index.map(lambda t: t.strftime('%Y-%m-%d'))

#%% Data Analysis
# lets get a first impression

df1 = Gas_daily_15_17['Produktion Rohgas [Bm³]']
df2 = FS_int.loc['2015-01-01':'2017-12-31']
df2 = df2[['FS intern Durchsatz [m³]','FS intern Fracht [m³/d]']]

df = pd.merge(df1,df2,left_index=True, right_index=True)

cols_plot = ['Produktion Rohgas [Bm³]', 'FS intern Durchsatz [m³]', 'FS intern Fracht [m³/d]']
axes = df[cols_plot].plot(marker='.', alpha=0.5, linestyle='-', figsize=(11, 9), subplots=True)
for ax in axes:
    ax.set_ylabel('to be defined')

#%% correlation plot and pearson coeff
    
plt.figure(2)
sns.scatterplot(x="Produktion Rohgas [Bm³]",y="FS intern Durchsatz [m³]",data=df)

plt.figure(3)
sns.scatterplot(x="Produktion Rohgas [Bm³]",y="FS intern Fracht [m³/d]",data=df)
