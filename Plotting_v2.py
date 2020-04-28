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

#%% turn off interactive mode for plotting

plt.ioff()

#%% multiplots
# zwei datenreihen, davon jeweil ein lineplot, und dann ein scatterplot

# function defintion
def MultiPlot(df_A, df_B, i_A, i_B):
    """ A = input, B = output """
    fig, axes = plt.subplots(3, 1, figsize=(11, 10))
    # first plot
    ax = df_A.loc['2015':'2019', df_A.columns[i_A]].plot(marker='.', alpha=0.5, 
                                                            linestyle='-', ax=axes[0],)
    ax.set(ylabel= df_A.columns[i_A], xlabel='Jahr [y]')
    # second plot
    bx = df_B.loc['2015':'2019', df_B.columns[i_B]].plot(marker='.', alpha=0.5, 
                                                                 linestyle='-', ax=axes[1])
    bx.set(ylabel= df_B.columns[i_B], xlabel='Jahr [y]')
    # third plot
    cx = sns.scatterplot(x=df_A[df_A.columns[i_A]], y=df_B[df_B.columns[i_B]], ax=axes[2])
    cx.set(ylabel= df_B.columns[i_B], xlabel= df_A.columns[i_A])
    
    return(fig)

# Main call
# nested plots
for i, in_feat in enumerate(df_in_plt.columns):
    
    for j, out_feat in enumerate(df_out_plt.columns):
        
        # plotting
        figure = MultiPlot(df_in_plt, df_out_plt, i, j) 
        
        # preparation of saving name in windoof, no "/" allowed
        in_feat = in_feat.replace("/","_")
        out_feat = out_feat.replace("/","_")       
 
        # saving of plot
        figure.savefig('plots/' + in_feat + '_vs_' + out_feat + '.png', dpi=800)  
        
        plt.close(figure)

# turn interactive mode back on
plt.ion()          