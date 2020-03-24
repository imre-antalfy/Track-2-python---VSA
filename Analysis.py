# -*- coding: utf-8 -*-

# %% import

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%% read gas data

Reader = pd.read_excel(r'2_Gasmengen gemessen 2015.xlsx', sheet_name='Jahr', header=0)

# types
Reader.dtypes
Reader.rename(columns = {'Unnamed: 0':'Datum'}, inplace=True)



# delete and rename
Reader = Reader.drop(columns="Unnamed: 0")
Reader = Reader.drop([0])

Reader.rename(columns = {'Unnamed: 1':'Datum'}, inplace=True)
Reader.rename(columns = {'Produktion Rohgas':'Produktion Rohgas [Bm3]'}, inplace=True)
Reader.rename(columns = {'Bezug Rohgas BGAA Cirmac':'Bezug Rohgas BGAA Cirmac [Bm3]'}, inplace=True)
Reader.rename(columns = {'Bezug Rohgas Fackel':'Bezug Rohgas Fackel [Bm3]'}, inplace=True)
Reader.rename(columns = {'Bezug Rohgas gesamt':'Bezug Rohgas gesamt [Bm3]'}, inplace=True)
Reader.rename(columns = {'Einspeisung Messung':'Einspeisung Messung [Nm3]'}, inplace=True)
Reader.rename(columns = {'Unnamed: 7':'Einspeisung Messung [kWh]'}, inplace=True)
Reader.rename(columns = {'Produktion trocken':'Produktion trocken [Nm3]'}, inplace=True)
Reader.rename(columns = {'Konsum trocken':'Konsum trocken [Nm3]'}, inplace=True)

# types
Reader.dtypes
Reader['Datum'] = pd.to_datetime(Reader['Datum'])
Reader['Produktion Rohgas [Bm3]'] = Reader['Produktion Rohgas [Bm3]'].astype(int)
Reader['Bezug Rohgas BGAA Cirmac [Bm3]'] = Reader['Bezug Rohgas BGAA Cirmac [Bm3]'].astype(float)
Reader['Bezug Rohgas Fackel [Bm3]'] = Reader['Bezug Rohgas Fackel [Bm3]'].astype(float)
Reader['Bezug Rohgas gesamt [Bm3]'] = Reader['Bezug Rohgas gesamt [Bm3]'].astype(int)
Reader['Einspeisung Messung [Nm3]'] = Reader['Einspeisung Messung [Nm3]'].astype(float)
Reader['Einspeisung Messung [kWh]'] = Reader['Einspeisung Messung [kWh]'].astype(float)
Reader['Produktion trocken [Nm3]'] = Reader['Produktion trocken [Nm3]'].astype(int)
Reader['Konsum trocken [Nm3]'] = Reader['Konsum trocken [Nm3]'].astype(int)

Reader = Reader.set_index('Datum')

# Merge
d = {}
df = pd.DataFrame(data=d)
df = Reader

df_15_16 = pd.concat([df,Reader])


#%% read sludge input data
Sludge = pd.read_excel(r'1_Frischschlamm 2015-2019.xlsx', header=0)
Sludge.dtypes
Sludge['Datetime'] = pd.to_datetime(Sludge['Datetime'])
Sludge = Sludge.set_index('Datetime')

#################
###

sns.set(rc={'figure.figsize':(11, 4)})

# some first testplots
plt.figure(1)
df_15_16['Produktion Rohgas [Bm3]'].plot(linewidth=2);
plt.figure(2)
Sludge['Frischschlamm Durchsatz Schlammaufwärmung'].plot(linewidth=2);

# subplots => ???
# currently 2 time series in 1 plot, i want 2 plots in one figure

start, end = '2015-01', '2016-12'
# Plot daily and weekly resampled time series together
fig, ax = plt.subplots()
ax.plot(df_15_16.loc[start:end, 'Produktion Rohgas [Bm3]'],
marker='.', linestyle='-', linewidth=0.5, label='Gas')

ax.plot(Sludge.loc[start:end, 'Frischschlamm Durchsatz Schlammaufwärmung'],
marker='o', markersize=8, linestyle='-', label='Sludge')

ax.set_ylabel('Gas production to sludge input')
ax.legend();

# corrplot ???
overall_pearson_r = df_15_16.corr().iloc[0,1]
print(f"Pandas computed Pearson r: {overall_pearson_r}")

# Compute rolling window synchrony ???
f,ax=plt.subplots(figsize=(7,3))
df.rolling(window=30,center=True).median().plot(ax=ax)
ax.set(xlabel='Time',ylabel='Pearson r')
ax.set(title=f"Overall Pearson r = {np.round(overall_pearson_r,2)}");

# test with merged
merged = df_15_16['Produktion Rohgas [Bm3]']
merged = pd.merge_asof(merged, Sludge['Frischschlamm Durchsatz Schlammaufwärmung'],left_index=True, right_index=True, direction='nearest')
merged

