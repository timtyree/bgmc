import matplotlib.pyplot as plt, numpy as np, pandas as pd
# general functions for plotting
# Tim Tyree
# 7.23.2021

def format_plot_general(**kwargs):
    return format_plot(**kwargs)

def format_plot(ax,xlabel,ylabel,fontsize=20,use_loglog=False,**kwargs):
    '''format plot formats the matplotlib axis instance, ax,
    performing routine formatting to the plot,
    labeling the x axis by the string, xlabel and
    labeling the y axis by the string, ylabel
    '''
    if use_loglog:
        ax.set_xscale('log')
        ax.set_yscale('log')
    ax.set_xlabel(xlabel,fontsize=fontsize,**kwargs)
    ax.set_ylabel(ylabel,fontsize=fontsize,**kwargs)
    ax.tick_params(axis='both', which='major', labelsize=fontsize,**kwargs)
    ax.tick_params(axis='both', which='minor', labelsize=0,**kwargs)
    return True

def FormatAxes(ax,x1lim,x2lim,x1label,x2label,title,fontsize=16,use_loglog=False,**kwargs):
    ax.set_xlim(x1lim)
    ax.set_ylim(x2lim)
    ax.set_title(title,fontsize=fontsize)
    format_plot(ax, x1label, x2label, fontsize=fontsize, use_loglog=use_loglog,**kwargs)
    return True

def plot_horizontal(ax,xlim,x0,Delta_thresh=1.,use_Delta_thresh=False):
    #plot the solid y=0 line
    x=np.linspace(xlim[0],xlim[1],10)
    ax.plot(x,0*x+x0,'k-')
    if use_Delta_thresh:
        #plot the dotted +-Delta_thresh lines
        ax.plot(x,0*x+Delta_thresh+x0,'k--',alpha=0.7)
        ax.plot(x,0*x-Delta_thresh+x0,'k--',alpha=0.7)
    return True
