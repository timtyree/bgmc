import numpy as np, pandas as pd
import matplotlib.pyplot as plt

def BootstrapPlot(ax,
     x_values,
     y_values,
     y_err_values,
     data_label_name=None,
     alpha=0.5,
     c='k',
     fontsize=18,
     elinewidth=3,
     markersize=4,
     capsize=3,
     xlim=None,
     ylim=None,
     x_label=r'x',
     y_label=r'y',
     **kwargs):
    '''ax is a matplotlib ax instance.
     *_values are numpy arrays.'''
    if data_label_name is None:
        data_label_name='_'
    #line plot
    ax.plot(x_values,
                y_values,
                c=c,
                alpha=alpha)
    #plot error bars
    ax.errorbar(x=x_values,
                y=y_values,
                yerr=y_err_values,
                c=c,
                alpha=alpha,
                fmt='o',
                markersize=markersize,
                ecolor=c,
                elinewidth=elinewidth,
                errorevery=1,
                capsize=capsize, label=data_label_name)

    #format plot
    #TODO: replace with a [superior] FormatPlot call
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    ax.set_xlabel(x_label, fontsize=fontsize)
    ax.set_ylabel(y_label, fontsize=fontsize)
    ax.tick_params(axis='both', which='major', labelsize=fontsize)
    ax.tick_params(axis='both', which='minor', labelsize=1)
    return True
