# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:50:20 2020

@author: Imre Antalfy
"""
#%% functions

import functions


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

df.corr('pearson')
# => do the NaN wrong the correlation? no, stated in documentation
# NaN wont be calculated
# still bad correlation

#%% lets take a look at timeshifted correlation
# HRT can usually range from 10 to 14 days, maybe look there

CC_loop(df['FS intern Fracht [m³/d]'],df['Produktion Rohgas [Bm³]'])

CC_loop(df['FS intern Durchsatz [m³]'],df['Produktion Rohgas [Bm³]'])

#%% the total of all input should correlate... pls...

df['Fracht total [m³/d]'] = (   FS_int['FS intern Fracht [m³/d]'] +
                                FS_ext['FS extern Fracht [m³/d]']
                            )

CC_loop(df['Fracht total [m³/d]'],df['Produktion Rohgas [Bm³]'])

# it looks better, but it might be better to make monthly data, to really see 
# the correlations. A lot of data is missing







