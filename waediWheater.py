# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 08:45:29 2020

@author: Imre Antalfy
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


###
# functions

def MakeSubset(data,start,end):
    """ If a read file contains multiple dataset, make subsets
        returns subset
    """
    subset = list(range(start,end))
    result = data.filter(items= subset, axis=0)
    return result
  
def FillEmpties_Convert(df,colname,dtype):
    """ takes a column as input
        searches for "-" values, replaces with NaN, fowardfills NaN
        reworks the datatype of the column
    """
    df.loc[df[colname] == '-',colname] = np.NaN  
    df[colname].fillna(method='pad', inplace=True)
    df[colname] = df[colname].astype(dtype)
    
    
###
# Main call
    
# read all data and merge into two dataframes, with daily and hourly basis
wae = pd.read_csv('order_74784_data.csv', sep=';')

#look at the data
wae.shape # look at shape

# del WAE, not needed
wae = wae.drop(columns="stn")

# CAREFUL!!! from row 339509 a new dataset begins
# Extract first subset
# rename columns
colnames1 = ["time","AirTemp","WindSpeed","WindDir"]
wae_hourly = MakeSubset(wae,0,339509)
wae_hourly.columns = colnames1

# good cut?
wae_hourly.tail(3)

wae_daily =  MakeSubset(wae,339510,353656)
colnames2 = ["time", "AirTemp_Dmax", "AirTemp_Dmin", "AirTemp_Dmean"]
wae_daily.columns = colnames2

### wae daily and wae hourly contain different datasets
wae_daily.dtypes
wae_hourly.dtypes

# the datatypes are wrong
# rework daily first
wae_daily['time'] = pd.to_datetime(wae_daily['time'])
wae_daily['AirTemp_Dmax'] = wae_daily['AirTemp_Dmax'].astype(float)
wae_daily['AirTemp_Dmin'] = wae_daily['AirTemp_Dmin'].astype(float)
wae_daily['AirTemp_Dmean'] = wae_daily['AirTemp_Dmean'].astype(float)

# correct?
wae_daily.dtypes

# time based indexing
wae_daily = wae_daily.set_index('time')
wae_daily.head(3)

# same procedure for the hourly data
wae_hourly['time'] = wae_hourly['time'].astype(str)
wae_hourly['time'] = pd.to_datetime(wae_hourly['time'],format='%Y%m%d%H')

wae_hourly = wae_hourly.set_index('time')

### Handling missing data, forward fill, convert
FillEmpties_Convert(wae_hourly,'AirTemp',float)
FillEmpties_Convert(wae_hourly,'WindSpeed',float)
FillEmpties_Convert(wae_hourly,'WindDir',int)

#####################################################
# order_74785, hourly data
wae = pd.read_csv('order_74785_data.csv', sep=';')
wae = wae.drop(columns="stn")

wae.dtypes

wae['time'] = pd.to_datetime(wae['time'],format='%Y%m%d%H')
wae = wae.set_index('time')
wae.head(3)
wae.columns = ["SoilTemp_Hmean","GlobRad_Hmean","Rain_Hsum","RelHumid_Hmean","Press_Hmean"]

FillEmpties_Convert(wae,'SoilTemp_Hmean',float)
FillEmpties_Convert(wae,'GlobRad_Hmean',int)
FillEmpties_Convert(wae,'Rain_Hsum',float)
FillEmpties_Convert(wae,'RelHumid_Hmean',float)
FillEmpties_Convert(wae,'Press_Hmean',float)

#this dataset is hourly based, append it to wae_hourly
wae_hourly = pd.merge(wae_hourly, wae, on='time',how='outer')

#####################################################
# order_74831, daily data
wae = pd.read_csv('order_74831_data.csv', sep=';')
wae = wae.drop(columns="stn")

wae.dtypes
# ths data is correctly assigned., also, no missing values

# at closer inspection, this datafile was the the same as the second dataframe
# appearing halway into order 74784. This is airtemp_dmax and airtemp_dmin
# => this data has not been taken into account, as it was already present

#####################################################
# order_75248, daily data

# this order contains Airtemp_Dmean, which is already accounted for in 
# oder 74784

#####################################################
### Plotting
# based on the tutorial, lets make some data visible

# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(11, 4)})

# some first testplots
wae_daily['AirTemp_Dmean'].plot(linewidth=0.5);
wae_hourly['WindSpeed'].plot(linewidth=0.5);

# lets see, how the rain, temperature and rain changed over the years
cols_plot = ['AirTemp', 'GlobRad_Hmean', 'Rain_Hsum']
axes = wae_hourly[cols_plot].plot(marker='.', alpha=0.5, linestyle='None', figsize=(11, 9), subplots=True)
for ax in axes:
    ax.set_ylabel('Hourly Totals')

# conclusion:
# there is way to much ink with the hourly data. But there is clearly 
# periodicity. resampling surely needed, but lets take alook at periodicity
    
# periocity
ax = wae_hourly.loc['2017', 'AirTemp'].plot()
ax.set_ylabel('Hourly temperature (°C)');
# this plot has still a lot of ink, although it shows the periodicity of the 
# temp during the year nicely

ax = wae_hourly.loc['2017', 'GlobRad_Hmean'].plot()
ax.set_ylabel('Radiation (W/m^2');
# this plot is not that usefuel, as a lot of the values are 0.
# maybe a rolling window?

ax = wae_hourly.loc['2017', 'Rain_Hsum'].plot()
ax.set_ylabel('Rainfall hourly sum (mm)');
# same story as with the global radiation

### 
# For the temperature, a boxplot is also quiet nice
# Boxplot for min/max/mean temperature on daily basis
# for this, we need to first group the data by month
wae_daily['Month'] = wae_daily.index.month

fig, axes = plt.subplots(3, 1, figsize=(11, 10), sharex=True)
for name, ax in zip(['AirTemp_Dmax', 'AirTemp_Dmin', 'AirTemp_Dmean'], axes):
    sns.boxplot(data=wae_daily, x='Month', y=name, ax=ax)
    ax.set_ylabel('°C')
    ax.set_title(name)

###
# resampling 
# instead of having hourly temperature data, weekly temperature data would 
# make plots less crowded
data_columns = ['AirTemp', 'GlobRad_Hmean', 'Rain_Hsum']
# Resample to weekly frequency, aggregating with mean
wae_hourly_mean = wae_hourly[data_columns].resample('W').mean()
wae_hourly_mean.head(3)

# compare hourly and weekly data for 6 month
# Start and end of the date range to extract
start, end = '2017-01', '2017-06'
# Plot daily and weekly resampled time series together
fig, ax = plt.subplots()
ax.plot(wae_hourly.loc[start:end, 'GlobRad_Hmean'],
marker='.', linestyle='-', linewidth=0.5, label='Hourly')
ax.plot(wae_hourly_mean.loc[start:end, 'GlobRad_Hmean'],
marker='o', markersize=8, linestyle='-', label='Weekly Mean Resample')
ax.set_ylabel('Global Radiation (W/m^2)')
ax.legend();

# for the global radiation, this smooths the data to see the structure way
# easier by the eye. 

###
# rolling windows
# for rain, coulda rolling mean provide better visuals?

# Compute the centered 7-day rolling mean
wae_hourly_7d = wae_hourly[data_columns].rolling(7, center=True).mean()
wae_hourly_7d.head(10)
# Start and end of the date range to extract
start, end = '2017-01', '2017-06'
# Plot daily, weekly resampled, and 7-day rolling mean time series together
fig, ax = plt.subplots()
ax.plot(wae_hourly.loc[start:end, 'Rain_Hsum'],
marker='.', linestyle='-', linewidth=0.5, label='Daily')

ax.plot(wae_hourly_mean.loc[start:end, 'Rain_Hsum'],
marker='o', markersize=8, linestyle='-', label='Weekly Mean Resample')

ax.plot(wae_hourly_7d.loc[start:end, 'Rain_Hsum'],
marker='.', linestyle='-', label='7-d Rolling Mean')
ax.set_ylabel('Rainfall hourly sum (mm)')
ax.legend();

# conclusion
# 7 days are a too small window, the data is still not clearly visible
# in comparison to the Weekly resample

############################################
### Climate change discussion
# did it really get warmer?
# compare the temperature over the first three years to the last three 
# years in the dataset
data_columns = ['AirTemp_Dmax', 'AirTemp_Dmin', 'AirTemp_Dmean']

wae_daily_7d = wae_daily[data_columns].rolling(30, center=True).mean()
wae_daily_7d.head(10)

wae_daily_365d = wae_daily[data_columns].rolling(window=365, center=True, min_periods=360).mean()

start1, end1 = '1981', '1983'
start2, end2 = '2017', '2019'

fig, ax = plt.subplots()
ax.plot(wae_daily_365d.loc[start1:end1, 'AirTemp_Dmax'],
marker='.', linestyle='-', linewidth=0.5, label='Daily')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Mean 365d-rolling temperauter over 1981-1983 (°C)');

fig, ax = plt.subplots()
ax.plot(wae_daily_365d.loc[start2:end2, 'AirTemp_Dmax'],
marker='.', linestyle='-', linewidth=0.5, label='Daily')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Mean 365d-rolling temperauter over 2017-2019 (°C)');

# conclusion:
# yes, it gets warmer, but is this time period well enoguh defined?
# the next step needs to be to merge both lines into onefigure

###
# But, did more extreme wheater situations happen in this time period?
# rain?
# make frequency plot (histogram), based on weekyl resample
wae_hourly_mean.head(3)

fig, ax = plt.subplots()
n, bins, patches = ax.hist(wae_hourly_mean["Rain_Hsum"][0:161], 30, density=1)
ax.set_xlabel('Rainfall hourly sum (mm')
ax.set_ylabel('Probability density')
ax.set_title('Histogram of weekly rainfall from 1981 to 1983')

fig, ax = plt.subplots()
n, bins, patches = ax.hist(wae_hourly_mean["Rain_Hsum"][1861:2022], 30, density=1)
ax.set_xlabel('Rainfall hourly sum (mm')
ax.set_ylabel('Probability density')
ax.set_title('Histogram of weekly rainfall from 2017 to 2019')

# or together
fig, ax = plt.subplots()
n, bins, patches = ax.hist(wae_hourly_mean["Rain_Hsum"][0:161], 30, density=1)
ax.set_xlabel('Rainfall hourly sum (mm')
ax.set_ylabel('Probability density')
ax.set_title('Histogram  of weekly rainfall from 1981 to 1983')

#fig, ax = plt.subplots()
n, bins, patches = ax.hist(wae_hourly_mean["Rain_Hsum"][1862:2022], 30, density=1)
ax.set_xlabel('Rainfall hourly sum (mm')
ax.set_ylabel('Probability density')
ax.set_title('Histogram of weekly Rainfall from 2017 to 2019')