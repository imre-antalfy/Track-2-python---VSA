# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 14:18:25 2020

@author: imrea
"""

#%% import

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%% plotting single lineplots

# plotting all plots after on another, normal plot
for i, feat in enumerate(df_plot.columns):
    ax = df_plot.loc['2015':'2019', feat].plot(marker='.', alpha=0.5, linestyle='-')
    ax.set_ylabel(feat) 
    # prepare filename, / cant be saved in windoof
    name = feat.replace('/', '_')
    # save every plot
    figure = ax.get_figure()    
    figure.savefig('plots/' + name + '.png', dpi=800)  
    # delete current plot, to alway save the newest data
    plt.clf()


#%% multiplots
# zwei datenreihen, davon jeweil ein lineplot, und dann ein scatterplot

fig, axes = plt.subplots(3, 1, figsize=(11, 10))
# first plot
ax = df_plot.loc['2015':'2019', 'FS oTS-Fracht [kg/d]'].plot(marker='.', alpha=0.5, 
                                                        linestyle='-', ax=axes[0],)
ax.set(ylabel='FS oTS-Fracht [kg/d]', xlabel='Jahr [y]')
# second plot
bx = df_plot.loc['2015':'2019', 'FS CSB-Fracht [kg/d]'].plot(marker='.', alpha=0.5, 
                                                             linestyle='-', ax=axes[1])
bx.set(ylabel='FS CSB-Fracht [kg/d]', xlabel='Jahr [y]')
# third plot
cx = sns.scatterplot(data=df_plot, x='FS oTS-Fracht [kg/d]', 
                     y='FS CSB-Fracht [kg/d]', ax=axes[2])
cx.set(ylabel='FS CSB-Fracht [kg/d]', xlabel='FS oTS-Fracht [kg/d]')










