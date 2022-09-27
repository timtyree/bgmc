#PlotGridValues.py
#Programmer: Tim Tyree
#Date: 8.3.2022
from .bluf import *
import matplotlib as mpl
import matplotlib.pyplot as plt, numpy as np
#, pandas as pd, sys, os

def GridValuePlotter_simple(ax,x,y,zerr,title,cmap,norm,
        fontsize=14,
        xlabel='Trial',
        ylabel='Neuron',**kwargs):
    """ the input grid needs to be evenly spaced

    GridValuePlotter_simple plots zerr colored according to cmap,norm.
    kwargs are passed to format_plot directly

    Example Usage:
dict_error_labels = {0:'No Error', 1:'No Spikes', 2:'One Spike', 3:'Exceeds Max FR'}
dict_error_colors = {0:'white', 1:'black', 2:'gray', 3:'red'}
levels=list(dict_error_colors.keys())
levels.append(np.max(levels)+1)
cmap, norm = mpl.colors.from_levels_and_colors(levels=levels, colors=list(dict_error_colors.values()), extend='neither')
ax = GridValuePlotter_simple(ax,x,y,zerr,title,cmap,norm,
        fontsize=14,xlabel='Trial',ylabel='Neuron')#,**kwargs)
    """
    # plot colored grid
    c = ax.pcolormesh(x, y, zerr, cmap=cmap, norm=norm)
    #format plot
    ax.set_title(title,fontsize=fontsize+2)
    format_plot(ax=ax,xlabel=xlabel,ylabel=ylabel,
        fontsize=fontsize,**kwargs)
    # set the limits of the plot to the limits of the data
    ax.axis([x.min(), x.max(), y.min(), y.max()])
    # ax.set_aspect('equal', 'box')
    return ax

def GridValuePlotter_colorbar(fig,ax,x,y,z,title,cmap,vmin,vmax,
                              fontsize=14,
                              xlabel='Trial',
                              ylabel='Neuron',
                              cbar_label='Number of Spikes',
                              fraction=0.07,
                              shrink=0.85,
                              aspect=35,
                              orientation='horizontal',
                              extend='max',
                              **kwargs):
    """ the input grid needs to be evenly spaced

    GridValuePlotter_simple plots 2D numpy.array instance, z, colored according to cmap,norm.
    x and y are 2D numpy.array instances that possess the x,y coordinates.
    kwargs are passed to format_plot directly.
    other default arguments format the color bar.

    Example Usage:
ax = GridValuePlotter_colorbar(fig,ax,x,y,z,title,cmap,vmin,vmax,
                              fontsize=14, xlabel='Trial', ylabel='Neuron', cbar_label='Number of Spikes',
                              fraction=0.07, shrink=0.85, aspect=35, orientation='horizontal', extend='max')#,**kwargs)

    Example Usage:
#visualize the heatmap constrained to predictive neurons
pred_nid_values=np.unique(df_pred_tbins_agg['nid'].values)
nid_list = pred_nid_values
#generate 2 coordinate grids for the x & y bounds
num_trials,num_neurons = error_code_array_.shape
num_neurons = len(nid_list)
xcoord_values = np.arange(num_trials+1)  #as corners of pixels
ycoord_values = np.arange(num_neurons+1) #as corners of pixels

# nid_list = nid_lst_reasonable
x, y = np.meshgrid(xcoord_values, ycoord_values)
y=y[::-1,::-1].copy() #flip y axis
x=x.copy()
z=spike_count_array_.copy().T[nid_list]
zerr=error_code_array_.copy().T[nid_list]
x.shape,y.shape,z.shape,zerr.shape

#visualize heatmap showing the number of spikes per trial,neuron pair
title = 'Spike Counts For '
title+= 'Predictive Neurons\n'
# title+= "All" + ' Trials\n'
vmin=1
vmax=150.
fontsize=14
figsize=(16,6)
cmap='jet'#'PuBu_r'#
fig, ax = plt.subplots(figsize=figsize,constrained_layout=True)
ax = GridValuePlotter_colorbar(fig,ax,x,y,z,title,cmap,vmin,vmax,
        fontsize=14,xlabel='Trial',ylabel='Neuron')#,**kwargs)
# ax = GridValuePlotter_colorbar(fig,ax,x,y,z,title,cmap,vmin,vmax,
#                               fontsize=14, xlabel='Trial', ylabel='Neuron', cbar_label='Number of Spikes',
#                               fraction=0.07, shrink=0.85, aspect=35, orientation='horizontal', extend='max')#,**kwargs)
plt.show()

    """
    # plot colored grid
    c = ax.pcolormesh(x, y, z, cmap=cmap, vmin=vmin, vmax=vmax,
                       norm=mpl.colors.LogNorm(vmin=vmin, vmax=vmax),shading='auto')
    #add formated colorbar
    cax, kw = mpl.colorbar.make_axes_gridspec(ax, orientation=orientation,#pad=0.1,
                                           fraction=fraction, shrink=shrink, aspect=aspect)
    cbar=fig.colorbar(c, cax=cax, orientation=orientation, extend=extend)#, fontsize=fontsize)
    cbar.ax.tick_params(labelsize=fontsize)
    cbar.set_label(label=cbar_label,size=fontsize)

    #format plot
    ax.set_title(title,fontsize=fontsize+2)
    format_plot(ax=ax,xlabel=xlabel,ylabel=ylabel,
        fontsize=fontsize,**kwargs)
    # set the limits of the plot to the limits of the data
    ax.axis([x.min(), x.max(), y.min(), y.max()])
    # ax.set_aspect('equal', 'box')
    return ax
