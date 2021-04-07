from .compute_slope import *
import numpy as np

def compute_sliding_slope_loglog(x_values,y_values,x_min=None,window_width=None,stepsize=None):
    '''x_values and y_values are numpy arrays of the values before computing the log-log values.
    Example Usage:
    xavg_values,slope_values,Rsquared_values = compute_sliding_slope_loglog(x_values,y_values)
    '''
    if x_min is None:
        x_min=np.min(x_values)
    if stepsize is None:
        stepsize=np.mean(np.diff(x_values))
    if window_width is None:
        window_width=30*stepsize
    x_min_values=np.arange(x_min,np.max(x_values)-window_width,stepsize)

    #compute the slope over a sliding window
    slope_lst=[];Rsquared_lst=[];
    for x_min in x_min_values:
        #get the slice
        x_max=x_min+window_width
        boo=(x_values>=x_min)&(x_values<=x_max)

        #measure the slope
        dict_output=compute_95CI_ols(np.log(x_values[boo]), np.log(y_values[boo]))
        slope=dict_output['m']
        Rsquared=dict_output['Rsquared']
        slope_lst.append(slope)
        Rsquared_lst.append(Rsquared)
    slope_values=np.array(slope_lst)
    Rsquared_values=np.array(Rsquared_lst)
    xavg_values=(x_min_values+window_width/2)
    return xavg_values,slope_values,Rsquared_values

def compute_sliding_slope_linlin(x_values,y_values,x_min=None,window_width=None,stepsize=None):
    '''x_values and y_values are numpy arrays of the values.
    Example Usage:
    xavg_values,slope_values,Rsquared_values = compute_sliding_slope_loglog(x_values,y_values)
    '''
    if x_min is None:
        x_min=np.min(x_values)
    if stepsize is None:
        stepsize=np.mean(np.diff(x_values))
    if window_width is None:
        window_width=40*stepsize
    x_min_values=np.arange(x_min,np.max(x_values)-window_width,stepsize)

    #compute the slope over a sliding window
    slope_lst=[];Rsquared_lst=[];
    for x_min in x_min_values:
        #get the slice
        x_max=x_min+window_width
        boo=(x_values>=x_min)&(x_values<=x_max)

        #measure the slope
        dict_output=compute_95CI_ols(x_values[boo], y_values[boo])
        slope=dict_output['m']
        Rsquared=dict_output['Rsquared']
        slope_lst.append(slope)
        Rsquared_lst.append(Rsquared)
    slope_values=np.array(slope_lst)
    Rsquared_values=np.array(Rsquared_lst)
    xavg_values=(x_min_values+window_width/2)
    return xavg_values,slope_values,Rsquared_values
