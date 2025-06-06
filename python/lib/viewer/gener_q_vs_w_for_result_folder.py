import matplotlib.pyplot as plt, numpy as np, pandas as pd,os
from ..model import recall_powerlaw_fits_to_full_models
from .. import compute_power_rmse
from .bluf import *
from ..measure.powerlaw import *

# model_name,m,M=compute_nearest_powerlaw_fit(x_values,y_values)
#TODO: push plot_horizontal to lib and define locally
def plot_horizontal(ax,xlim,Delta_thresh=1.,use_Delta_thresh=False):
    #plot the solid y=0 line
    x=np.linspace(xlim[0],xlim[1],10)
    ax.plot(x,0*x,'k-')
    if use_Delta_thresh:
        #plot the dotted +-Delta_thresh lines
        ax.plot(x,0*x+Delta_thresh,'k--',alpha=0.7)
        ax.plot(x,0*x-Delta_thresh,'k--',alpha=0.7)
    return True


def PlotFullModels(ax,xlim=[0.1,1.0],c1='C0',c2='C1',zorder=0,lw=4):
    #fk_pbc
    m_fk=1.8772341309722325
    Delta_m_fk=0.02498750277237229
    M_fk=5.572315674840435
    Delta_M_fk=0.3053120355191732

    #lr_pbc
    m_lr=1.6375562704001745
    Delta_m_lr=0.017190912126700632
    M_lr=16.73559858353835
    Delta_M_lr=0.8465090320196467

    xv=np.arange(xlim[0],xlim[1],.05)
    yv_fk=M_fk*(xv)**m_fk
    yv_lr=M_lr*(xv)**m_lr

    ax.plot(xv,yv_fk,label='Fenton-Karma model',c=c1,zorder=zorder,lw=lw)
    ax.plot(xv,yv_lr,label='Luo-Rudy model',c=c2,zorder=zorder,lw=lw)
    return True

#define an example plotter_function
def PlotTrial(ax, x_values,y_values,title,title_fontsize,label="particle model",alpha=0.3,markersize=50,c='C3',**kwargs):
    '''a plotter function that plots q vs w'''
    ax.scatter(x_values,y_values,label=label,alpha=alpha,s=markersize,c=c,**kwargs)#,cmap='bwr')
    ax.set_title(title,fontsize=title_fontsize)
    return True

#define an example plotter_function
def PlotErrorBarScatter(ax, x_values,y_values,yerr_values,title,title_fontsize,label="particle model",alpha=0.3,c='C3',markersize=6,#50,
    elinewidth=4,
    capsize=3,
    **kwargs):
    '''a plotter function that plots q vs w.  yerr_values is the error bar radius plotted'''
    # TODO:ax.scatter(x_values,y_values,label=label,alpha=alpha,s=markersize,c=c,**kwargs)#,cmap='bwr')
    ax.errorbar(x=x_values,
                y=y_values,
                yerr=yerr_values,
                c=c,
                alpha=alpha,
                fmt='o',
                markersize=markersize,
                ecolor=c,
                elinewidth=elinewidth,
                errorevery=1,
                capsize=capsize,**kwargs)
    ax.set_title(title,fontsize=title_fontsize)
    return True



def compute_nearest_powerlaw_fit(x_values,y_values):
    #TODO: dev plotter functions of residuals to closest model (smallest rmse)
    #TODO: verify whether B is M or B is B...
    #recall full model fits
    wjr=recall_powerlaw_fits_to_full_models()
    rmse_min=[9e9]
    tuple_out=None
    for key in wjr:
        dict_fit=wjr[key]
        m=dict_fit['m']
        M=dict_fit['M']
        B=dict_fit['M']**(1./m)
        #TODO: consider modifying compute_power_rmse with a mode='M' that says take M:=dict_fit['M']#!!!!
        #compare rmse against either of the full models and select the smallest rmse
        rmse=compute_power_rmse(x_values, y_values, m, B)
        if rmse<rmse_min:
            rmse_min=rmse
            #save results
            tuple_out=(key,m,M)
        assert      (tuple_out)

    return tuple_out

def q_vs_w_plotter_function(ax,data):#=input_fn
    #     TODO: figure out support for ,**kwargs):
    # #define an example plotter_function
    # def q_vs_w_plotter_function(ax, data):
    #     '''a plotter_function that plots q vs w'''
    input_fn=data

    #define kwargs
    kwargs={}
    #     'npartitions':os.cpu_count(),
    #     'fontsize':22,
    #
    # }
    #
    # #populate the local namespace with kwargs
    # loc=locals()
    # for key in kwargs:
    #     loc[key]=kwargs[key]

    #TODO: list all of the kwargs
    #TODO: abstract/collect all of the kwargs into kwargs
    npartitions=os.cpu_count()
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

    #import / process data (functionally?)
    df=pd.read_csv(input_fn)
    #derived values
    CollRate_missing=len(list(set(df.columns).intersection({'CollRate'})))==0
    if CollRate_missing:
        df['CollRate']=1./df['CollTime']
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(subset=['CollRate'], how="all",inplace=True)
    df['A']=df['L']**2
    df['q']=df['N']/df['A'] #number of tips per square centimeter
    df['w']=df['CollRate']/df['A'] #[mHz?]/cm^2

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

#TODO: incorporate ^that oneliner into functionally plotting q versus Delta_w
def q_vs_Delta_w_plotter_function(ax,data):#=input_fn
    #     TODO: figure out support for ,**kwargs):
    # #define an example plotter_function
    # def q_vs_w_plotter_function(ax, data):
    #     '''a plotter_function that plots q vs w'''
    input_fn=data

    #define kwargs
    kwargs={}
    #     'npartitions':os.cpu_count(),
    #     'fontsize':22,
    # }
    #
    # #populate the local namespace with kwargs
    # loc=locals()
    # for key in kwargs:
    #     loc[key]=kwargs[key]


    #TODO: list all of the kwargs
    #TODO: abstract/collect all of the kwargs into kwargs
    npartitions=os.cpu_count()
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
    # xlim=[-0.05,1.05]
    # ylim=[-1,1]#[1e-5,1e4]
    legend_fontsize=fontsize-6
    title_fontsize=fontsize-8

    #import / process data (functionally?)
    df=pd.read_csv(input_fn)
    #derived values
    CollRate_missing=len(list(set(df.columns).intersection({'CollRate'})))==0
    if CollRate_missing:
        df['CollRate']=1./df['CollTime']
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(subset=['CollRate'], how="all",inplace=True)
    df['A']=df['L']**2
    df['q']=df['N']/df['A'] #number of tips per square centimeter
    df['w']=df['CollRate']/df['A'] #[mHz?]/cm^2

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
