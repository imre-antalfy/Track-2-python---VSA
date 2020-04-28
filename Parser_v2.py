# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 15:45:01 2020

@author: imrea
"""

#%% import

import pandas as pd

#%% get data

# read both sheets
input_data = pd.read_excel('Data_arabern.xlsx', header=0, sheet_name="Rohdaten Input")
input_data = input_data.set_index('Datetime')
reader = pd.read_excel('Data_arabern.xlsx', header=0, sheet_name="Rohdaten Output")
reader = reader.set_index('Datetime')

# concat and delete unused
input_data = pd.concat([input_data,reader],axis=1,join="inner")
del reader

#--------------------------------------------------------------------
# import cosub data
cosub = pd.read_excel('CoSub_rework.xlsx', 
                      header=0, 
                      sheet_name='Input')
cosub = cosub.set_index('Datetime')

# get days per month for upsampling
days_per_month = 5*([31,28,31,30,31,30,31,31,30,31,30,31])
# deltet last two 
for i in range(1,3):
    days_per_month.pop()
cosub['days'] = days_per_month

# upsample cosub input, used later to sum input, as fs and afs are daily based
cosub_day = cosub['CoSub Menge [t/m]'] / cosub["days"]
cosub_day = cosub_day.resample('D').ffill()

#--------------------------------------------------------------------
# import gas analysis data and interpolate
gas_analysis = pd.read_excel('Gasanalysen_rework.xlsx', header=0)
gas_analysis = gas_analysis.set_index('Datetime')

gas_analysis = gas_analysis.resample('D').ffill()

#%% new dataframe - input data

p = ()
df_input = pd.DataFrame(p)

# Fresh sludge concentrations
df_input['FS TS-Konz [kg/m3]'] = input_data['Frischschlamm Trockenrückstand'] * 10
df_input['FS GR-Konz [kg/m3]'] = df_input['FS TS-Konz [kg/m3]'] * input_data['Frischschlamm Glührückstand'] / 100
df_input['FS oTS-Konz [kg/m3]'] = df_input['FS TS-Konz [kg/m3]'] - df_input['FS GR-Konz [kg/m3]']

# fresh sludge loads
df_input['FS oTS-Fracht [kg/d]'] = (input_data['Frischschlamm Durchsatz Schlammaufwärmung'] * 
                              df_input['FS oTS-Konz [kg/m3]'])
df_input['FS CSB-Fracht [kg/d]'] = (input_data['Frischschlamm Durchsatz Schlammaufwärmung'] *
                              input_data['Frischschlamm Konz CSB'])
df_input['FS N-Fracht [kg/d]'] = (input_data['Frischschlamm Durchsatz Schlammaufwärmung'] *
                            input_data['Frischschlamm Konz N gesamt'])
df_input['FS P-Fracht [kg/d]'] = (input_data['Frischschlamm Durchsatz Schlammaufwärmung'] *
                            input_data['Frischschlamm Konz P gesamt'])

# external sludge concentrations
df_input['AFS TS-Konz [kg/m3]'] = input_data['Annahme Frischschlamm Trockenrückstand'] * 10
df_input['AFS GR-Konz [kg/m3]'] = (df_input['AFS TS-Konz [kg/m3]'] * 
                             input_data['Annahme Frischschlamm Glührückstand'] / 100)
df_input['AFS oTS-Konz [kg/m3]'] = df_input['AFS TS-Konz [kg/m3]'] - df_input['AFS GR-Konz [kg/m3]']

# external sludge loads
df_input['AFS oTS-Fracht [kg/d]'] = (input_data['Annahme Frischschlamm Menge'] * 
                               df_input['AFS oTS-Konz [kg/m3]'])
df_input['AFS CSB-Fracht [kg/d]'] = (input_data['Annahme Frischschlamm Menge'] *
                              input_data['Annahme Frischschlamm Konz CSB'])
df_input['AFS N-Fracht [kg/d]'] = (input_data['Annahme Frischschlamm Menge'] *
                            input_data['Annahme Frischschlamm Konz N gesamt'])
df_input['AFS P-Fracht [kg/d]'] = (input_data['Annahme Frischschlamm Menge'] *
                            input_data['Annahme Frischschlamm Konz P gesamt'])

# CoSub loads
df_input['CoSub CSB-Fracht [kg/month]'] = cosub['CoSub CSB-Fracht [t/m]'] * 1000
df_input['CoSub N-Fracht [kg/month]'] = cosub['CoSub N-Fracht [t/m]'] * 1000
df_input['CoSub P-Fracht [kg/month]'] = cosub['CoSub P-Fracht [t/m]'] * 1000

#%% parameter data

df_input['FR3 Temp mittel [°C]'] = ( (input_data['FR3 Temperatur oben'] +
                          input_data['FR3 Temperatur unten'] / 2))

#%% output data

df_output = pd.DataFrame(p)

# digested sludge concentrations
df_output['FR3 TS-Konz [kg/m3]'] = input_data['FR3 Faulschlamm Trockenrückstand'] * 10
df_output['FR3 GR-Konz [kg/m3]'] = (df_output['FR3 TS-Konz [kg/m3]'] * 
                             input_data['FR3 Faulschlamm Glührückstand'] / 100)
df_output['FR3 oTS-Konz [kg/m3]'] = (df_output['FR3 TS-Konz [kg/m3]'] - 
                              df_output['FR3 GR-Konz [kg/m3]'])

# digested sludge concentrations
df_output['FR3 Durchsatz [m3/d]'] = (input_data['Frischschlamm Durchsatz Schlammaufwärmung'] +
                       input_data['Annahme Frischschlamm Menge'] +
                       cosub_day)

# fresh sludge loads
df_output['FR3 oTS-Fracht [kg/d]'] = (df_output['FR3 Durchsatz [m3/d]'] * 
                               df_output['FR3 oTS-Konz [kg/m3]']) 
df_output['FR3 CSB-Fracht [kg/d]'] = (df_output['FR3 Durchsatz [m3/d]'] *
                               input_data['FR3 Faulschlamm Konz CSB']
                               * 1000)
df_output['FR3 N-Fracht [kg/d]'] = (df_output['FR3 Durchsatz [m3/d]'] *
                             input_data['FR3 Faulschlamm Konz N gesamt']
                             * 1000)
df_output['FR3 P-Fracht [kg/d]'] = (df_output['FR3 Durchsatz [m3/d]'] *
                             input_data['FR3 Faulschlamm Konz P gesamt']
                             * 1000)
df_output['FR3 NH4-N-Fracht [kg/d]'] = (df_output['FR3 Durchsatz [m3/d]'] *
                                 input_data['FR3 Faulschlamm Konz NH4-N']
                                 * 1000)

# Gas analysis data
df_output['Prod. Gas, trocken [Nm3/d]'] = input_data['Gasmenge, trocken']
df_output = pd.concat([df_output,gas_analysis], 
               axis=1, 
               sort=False)

df_output['Prod. CH4, trocken [Nm3/d]'] = (df_output['Prod. Gas, trocken [Nm3/d]'] *
                                    df_output['Methan CH4  [Vol. %]'] /
                                    100)
                                    
#%% plotting dataframe
# immediate calculations are not needed to plot
# => see datalist for explanation

df_in_plt = df_input.copy() # shallow copy!!!
df_out_plt = df_output.copy()
# drop FS concentrations
df_in_plt.drop(['FS TS-Konz [kg/m3]','FS GR-Konz [kg/m3]','FS oTS-Konz [kg/m3]'], 
             axis=1, inplace=True)
# drop AFS concentrations
df_in_plt.drop(['AFS TS-Konz [kg/m3]','AFS GR-Konz [kg/m3]','AFS oTS-Konz [kg/m3]'], 
             axis=1, inplace=True)
# drop digested sludge conentrations
df_out_plt.drop(['FR3 Durchsatz [m3/d]','FR3 TS-Konz [kg/m3]','FR3 GR-Konz [kg/m3]','FR3 oTS-Konz [kg/m3]',], 
             axis=1, inplace=True)
# drop gas data
df_out_plt.drop(['Prod. Gas, trocken [Nm3/d]'], 
             axis=1, inplace=True)




