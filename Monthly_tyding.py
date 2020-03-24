# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 17:06:06 2020

@author: Imre Antalfy
"""

import functions as fun
import seaborn as sns

df = pd.DataFrame(data=d)

#%% monthly, tidy data
# Specify the data columns we want to include (i.e. exclude Year, Month, Weekday Name)
data_columns = ['Produktion Rohgas [Bm³]']
# Resample to weekly frequency, aggregating with mean
Gas_monthly_15_17 = Gas_daily_15_17[data_columns].resample('MS').mean()
Gas_monthly_18_19['Produktion Rohgas Ø [Bm³]'] = Gas_monthly_18_19['Produktion Rohgas [Bm³]'] / 31

# concat gas data
df['Produktion Rohgas Ø [Bm³]'] = pd.concat([Gas_monthly_15_17['Produktion Rohgas [Bm³]'],Gas_monthly_18_19['Produktion Rohgas Ø [Bm³]']])

# resample loads and sum it up
FS_int_monthly = pd.DataFrame(data=d)
FS_ext_monthly = pd.DataFrame(data=d)

FS_int_monthly = FS_int.resample('MS').mean()
FS_ext_monthly = FS_ext.resample('MS').mean()

#fill 0 in fs external, to sum it up
FS_ext_monthly['FS extern Fracht [m³/d]'] = FS_ext_monthly['FS extern Fracht [m³/d]'].fillna(0)

# write ext & int laod into frame
df['FS intern Fracht [m³/d]'] = FS_int_monthly['FS intern Fracht [m³/d]']
df['FS extern Fracht [m³/d]'] = FS_ext_monthly['FS extern Fracht [m³/d]']

# calc total load
df['Fracht total [m³/d]'] = (    df['FS intern Fracht [m³/d]'] +
                                 df['FS extern Fracht [m³/d]']
                                  )

# year 2019, month 11 & 12 are missing, forward fill from month 10
df = df.replace({0:np.nan})
df['Produktion Rohgas Ø [Bm³]'].fillna(method='ffill', inplace=True)



#%% correlation analysis

plt.figure(1)
sns.scatterplot(x="Fracht total [m³/d]",y="Produktion Rohgas Ø [Bm³]",data=df)

df_corr = pd.DataFrame(corrlist)

corrlist = fun.CC_loop(df['Fracht total [m³/d]'], df['Produktion Rohgas Ø [Bm³]'])


plt.figure(2)
sns.lineplot(x=day,
             y=corrlist
             )



df.corr('pearson')



