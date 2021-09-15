import matplotlib.pyplot as plt, numpy as np, pandas as pd,os
from ..model import recall_powerlaw_fits_to_full_models
from .. import compute_power_rmse
from .bluf import *
from ..measure.powerlaw import *
from .gener_q_vs_w_for_result_folder import *

def q_vs_w_plotter_function_from_df(ax,df):

#     npartitions=os.cpu_count()
    fontsize=16
    printing=False
    alpha=0.5
    markersize=50#5
    xlabel=r'q (cm$^{-2}$)'
    ylabel=r'w (Hz cm$^{-2}$)'
    c='C3'
    xlim=[.1,1.05]
    ylim=[0.,20]
    # xlim=[-0.05,1.05]
    # ylim=[1e-1,20]#[1e-5,1e4]
    legend_fontsize=fontsize-6
    title_fontsize=fontsize-8

    x_values=df.q.values
    y_values=df.w.values

    #extract column values
    r_values=np.array(sorted(set(df.r.values)))#cm
    D_values=np.array(sorted(set(df.D.values)))#cm^2/s
    L_values=np.array(sorted(set(df.L.values)))#cm
    A_values=L_values**2#cm^2
    kappa_values=np.array(sorted(set(df.kappa.values)))#1/s
    varkappa_values=np.array(sorted(set(df.varkappa.values)))#1/s
    x0_values=np.array(sorted(set(df.x0.values)))#1/s
    set_second_values=np.array(sorted(set(df.set_second.values)))
    reflect_values=np.array(sorted(set(df.reflect.values)))
    no_repulsion_values=np.array(sorted(set(df.no_repulsion.values)))
    no_attraction_values=np.array(sorted(set(df.no_attraction.values)))
    neighbor_values=np.array(sorted(set(df.neighbor.values)))
    force_code_values=np.array(sorted(set(df.force_code.values)))

    if printing:
        print(f"input parameters:")
        print(f"r~{r_values}")
        print(f"D~{D_values}")
        print(f"L~{L_values}")
        print(f"kappa~{kappa_values}")
        print(f"a~{varkappa_values}")
        print(f"x0~{x0_values}")
        print(f"set_second~{set_second_values}")
        print(f"reflect~{reflect_values}")
        print(f"no_repulsion~{no_repulsion_values}")
        print(f"no_attraction~{no_attraction_values}")
        print(f"neighbor~{neighbor_values}")
        print(f"force_code~{force_code_values}")

    #TDOO: compute xy values

    #compute title=
#     title=r"$\nu$="+f"{m:.3f}, "+f"M={M:.3f}"+r" cm$^2$/s\n"
# additional parameters optional/uncommentable...
    title=f"force_code={int(force_code_values[0])}, neighbors={int(neighbor_values[0])}, reflect={int(reflect_values[0])}\n"
    title=title+r'$r=$'+f'{r_values[0]:.5f} cm, '
    title=title+r'$\kappa=$'+f'{kappa_values[0]:.5f} Hz\n'
    title=title+r'$D=$'+f'{D_values[0]:.5f} cm'+r'$^2$/s, '
    title=title+r'$a=$'+f'{varkappa_values[0]:.5f} cm'+r'$^2$/s, '
    title=title+r'$x_0=$'+f'{x0_values[0]:.0f} cm\n'

    #DONE: plot the data
    PlotFullModels(ax,xlim=[0.1,1])
    FormatAxes(ax,xlim,ylim,xlabel,ylabel,title,fontsize=fontsize,use_loglog=False)#,**kwargs)
    PlotTrial(ax, x_values,y_values,title,title_fontsize)
    ax.legend(fontsize=legend_fontsize,ncol=1,loc='upper left')
    return True

def q_vs_Delta_w_plotter_function_from_df(ax,df):
    fontsize=16
    use_Delta_thresh=True
    use_error_bars=True
    percent_uncertainty=1.
    printing=False
    alpha=0.5
    markersize=50#5
    xlabel=r'q (cm$^{-2}$)'
    ylabel=r'w (Hz cm$^{-2}$)'
    c='C3'
    xlim=[.1,1.05]
    ylim=[-1,1]
    legend_fontsize=fontsize-6
    title_fontsize=fontsize-8
    use_error_bars=True
    percent_uncertainty=1.

    x_values=df.q.values
    y_values=df.w.values
    if use_error_bars:
        yerr_values=percent_uncertainty/100*y_values

    #compute the error
    model_name,m,M=compute_nearest_powerlaw_fit(x_values,y_values)
    yhat_values=M*x_values**m
    Delta_y_values=y_values-yhat_values
    y_values=Delta_y_values

    # TODO: compute rmse between
    # the particle model and the full model
    rmse_particle_vs_full=np.sqrt(np.mean(Delta_y_values**2))
    Delta_thresh=rmse_particle_vs_full

    #TODO: compute the apparent powerlaw fit of the particle model
    x_values=df.q.values
    y_values=df.w.values
    B,Delta_B,m,Delta_m,Rsq=fit_power_law(x_values,y_values)
    rmse_particle_vs_powerlawfit=compute_power_rmse(x_values,y_values, m, B)
    M, Delta_M= comp_power_scale(B,Delta_B,m,Delta_m)
    Delta_y_values=y_values-yhat_values
    y_values=Delta_y_values


    #extract column values
    r_values=np.array(sorted(set(df.r.values)))#cm
    D_values=np.array(sorted(set(df.D.values)))#cm^2/s
    L_values=np.array(sorted(set(df.L.values)))#cm
    A_values=L_values**2#cm^2
    kappa_values=np.array(sorted(set(df.kappa.values)))#1/s
    varkappa_values=np.array(sorted(set(df.varkappa.values)))#1/s
    x0_values=np.array(sorted(set(df.x0.values)))#1/s
    set_second_values=np.array(sorted(set(df.set_second.values)))
    reflect_values=np.array(sorted(set(df.reflect.values)))
    no_repulsion_values=np.array(sorted(set(df.no_repulsion.values)))
    no_attraction_values=np.array(sorted(set(df.no_attraction.values)))
    neighbor_values=np.array(sorted(set(df.neighbor.values)))
    force_code_values=np.array(sorted(set(df.force_code.values)))

    if printing:
        print(f"input parameters:")
        print(f"r~{r_values}")
        print(f"D~{D_values}")
        print(f"L~{L_values}")
        print(f"kappa~{kappa_values}")
        print(f"a~{varkappa_values}")
        print(f"x0~{x0_values}")
        print(f"set_second~{set_second_values}")
        print(f"reflect~{reflect_values}")
        print(f"no_repulsion~{no_repulsion_values}")
        print(f"no_attraction~{no_attraction_values}")
        print(f"neighbor~{neighbor_values}")
        print(f"force_code~{force_code_values}")

#TODO: compute the powerlaw fit for the x and y values and set them equal to m,M,Delta_m,Delta_M
#TODO: modify title to take m,M,Delta_m,Delta_M
    #compute title= string
    title=r"$\nu$="+f"{m:.3f}"+r"$\pm$"+f"{Delta_m:.3f}"
    title=title+f", M={M:.3f}"+r"$\pm$"+f"{Delta_M:.3f} "+r"cm$^{2(\nu-1)}$/s"
    title=title+f"\n"+r"RMSE$_{particle\;vs\;full}=$"+f"{rmse_particle_vs_full:.3f} Hz/cm"+r"^2"+f"\n"
    #additional parameters optional/uncommentable...
    #     title=f"force_code={int(force_code_values[0])}, neighbors={int(neighbor_values[0])}, reflect={int(reflect_values[0])}\n"
    #     title=title+r'$r=$'+f'{r_values[0]:.2f} cm, '
    #     title=title+r'$\kappa=$'+f'{kappa_values[0]:.2f} Hz\n'
    #     title=title+r'$D=$'+f'{D_values[0]:.2f} cm'+r'$^2$/s, '
    #     title=title+r'$a=$'+f'{varkappa_values[0]:.2f} cm'+r'$^2$/s, '
    #     title=title+r'$x_0=$'+f'{x0_values[0]:.0f} cm\n'

    # plot_horizontal solid & dashed
    plot_horizontal(ax,xlim,Delta_thresh=Delta_thresh,use_Delta_thresh=use_Delta_thresh)
    FormatAxes(ax,xlim,ylim,xlabel,ylabel,title,fontsize=fontsize,use_loglog=False)#,**kwargs)
    #plot the data
    if not use_error_bars:
        PlotTrial(ax, x_values,y_values,title,title_fontsize)
    else:
        PlotErrorBarScatter(ax, x_values,y_values,yerr_values,title,title_fontsize)
#     ax.legend(fontsize=legend_fontsize,ncol=1,loc='upper left')
    return True
