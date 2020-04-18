# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 16:45:26 2020

@author: imrea
"""

#%% import

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%% get data

# read both sheets
df = pd.read_excel('Data_arabern.xlsx', header=0, sheet_name="Rohdaten Input")
df = df.set_index('Datetime')
reader = pd.read_excel('Data_arabern.xlsx', header=0, sheet_name="Rohdaten Output")
reader = reader.set_index('Datetime')

# concat and delete unused
df = pd.concat([df,reader],axis=1,join="inner")
del reader

# Calculating Load based on TS/oTS
# Input
df['Frischschlamm Fracht'] = (  df['Frischschlamm Durchsatz Schlammaufwärmung'] * 
                                df['Frischschlamm Trockenrückstand'] *
                                (100 - df['Frischschlamm Glührückstand']) /
                                10000
                                )
# Output
df['Annahme Frischschlamm Fracht'] = (  df['Annahme Frischschlamm Menge'] * 
                                        df['Annahme Frischschlamm Trockenrückstand'] *
                                        (100 - df['Annahme Frischschlamm Glührückstand']) /
                                        10000
                                        )

# calculate total
#pre fill with 0 for calculation, nan gives wring results
df['Annahme Frischschlamm Fracht'] = df.fillna(0)['Annahme Frischschlamm Fracht']
df['Frischschlamm Fracht total'] = (    df['Frischschlamm Fracht'] + 
                                        df['Annahme Frischschlamm Fracht']
                                        )

#%% plotting timeseries

# would a pairplot help?
# sns.pairplot(df)
# => nope, this is way too large

feature = df.columns

ax = df.loc['2015':'2019', feature[0]].rolling(7, center=True.mean())
ax.set_ylabel(feature[0]);

figure = ax.get_figure()    
figure.savefig('plots/' + feature[0] + '.png', dpi=800)

plt.clf()


# plotting all plots after on another, normal plot
for i, feat in enumerate(df.columns):
    ax = df.loc['2015':'2019', feat].plot(marker='.', alpha=0.5, linestyle='-')
    ax.set_ylabel(feat)    
    # save every plot
    figure = ax.get_figure()    
    figure.savefig('plots/' + feat + '.png', dpi=800)  
    # delete current plot, to alway save the newest data
    plt.clf()
    # uncomment thos for all plots
    # if i == 10:
    #     break
# => this procudes plots, but not all are viable

# lets try rolling window
df_7d = df[df.columns].resample('W').mean()
df_30d = df[df.columns].resample('M').mean()
    
for i, feat in enumerate(df.columns):
    ax = df_30d.loc['2015':'2019', feat].plot(marker='.', alpha=0.5, linestyle='-')
    ax.set_ylabel(feat)    
    # save every plot
    figure = ax.get_figure()    
    figure.savefig('plots/' + feat + '_30d.png', dpi=800)  
    # delete current plot, to alway save the newest data
    plt.clf()
    # uncomment thos for all plots
    # if i == 10:
    #     break    

#%% scatterplots - all vs. produced gas

# cant use rescaled data from 18 & 19, need daily data
df_gas = df.loc ['2015':'2017']

for i, feat in enumerate(df.columns):
    # ax = df.loc[feat, ].plot(marker='.', alpha=0.5, linestyle='None')
    # ax.set_ylabel(feat)       
    
    ax = sns.scatterplot(x=feat, 
                         y="Gas, Menge",
                         data=df_gas)
    
    figure = ax.get_figure()    
    figure.savefig('plots/' + feat + '_scatter_15_17.png', dpi=800)     
    
    plt.clf()
    
    # if i == 10:
    #     break        

#%% delayed scatterplots
# produce delayed scatterplots, throughput vs. prod gas

# shift data
    
df_shifted = pd.DataFrame(df['Frischschlamm Fracht total'])
for i in range(1,20):
    shifter = df['Frischschlamm Fracht total'].shift(periods=i)
    shifter = shifter.rename('FS Fracht total ' + str(i) + 'd delay')
    df_shifted = pd.concat([df_shifted,shifter], axis=1)
df_shifted = pd.concat([df_shifted,df_gas['Gas, Menge']], axis=1)



for i, feat in enumerate(df_shifted.columns):  
    ax = sns.scatterplot(x=feat, 
                         y="Gas, Menge",
                         data=df_shifted)
    
    figure = ax.get_figure()    
    figure.savefig('plots/' + feat + '_delayed_' + str(i) + '.png', dpi=800)     
    
    plt.clf()
     










