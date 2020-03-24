# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 15:56:38 2020

@author: Imre Antalfy
"""

#%% functions

def crosscorr(datax, datay, lag=0):
    """ Lag-N cross correlation. 
    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length

    Returns
    ----------
    crosscorr : float
    """
    return datax.corr(datay.shift(lag))

def CC_loop(d1,d2):
    
    corrlist = []
    day = []
    
    for daylag in range(0,21):  
        day.append(day)
        N = crosscorr(d1,
                      d2, 
                      daylag)
        
        corrlist.append(N)
    
    return(corrlist)
