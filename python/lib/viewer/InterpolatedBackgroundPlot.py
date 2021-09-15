#import matplotlib.pyplot as plt
#import numpy as np
#TODO: add support for using my DataPlotterClass-associated colorbar method, using def plot_sidebar(hts, dash_xy, dash_wh, pl) from DataPlotterClass.py
def PlotInterpolatedBackground(fig,ax,x1_values,x2_values,y_values,vmin,vmax,clabel,cmap,fontsize=16,show_cbar=True,use_cbar=True,shading='auto',**kwargs):
    output_col=clabel
    pcm=ax.pcolormesh(x1_values, x2_values, y_values, vmin=vmin, vmax=vmax, cmap=cmap, shading=shading)
    if use_cbar:
        cbar=fig.colorbar(pcm, ax=ax, shrink=0.6,label=output_col)#, location='top'
        # fig.colorbar(pcm, ax=[axs[0, col]], location='top', shrink=0.6)
        #     cbar=fig.colorbar(pcm, ax=axs[:, col],shrink=0.6)#,label=output_col)
        cbar.ax.tick_params(labelsize=fontsize)
        cbar.set_label(output_col, fontsize=fontsize)
    return True

def howdo_colorbar():
    print("""import matplotlib as mpl
norm = mpl.colors.Normalize(vmin=0, vmax=.25)
cmap = plt.cm.bone
cax = fig.add_axes([0.95, 0.2, 0.02, 0.6])
cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, spacing='proportional')
cb.set_label(r'RMSE$_{particle\;vs\;full}$')
""")
