#PlotFits.py
#Programmer: Tim Tyree
#Date: 1.3.2022
import matplotlib.pyplot as plt, numpy as np, pandas as pd
from scipy.optimize import minimize
from .. import comp_rmse_via_interp,comp_mse_via_interp
# from .bluf import format_plot
from .bluf.plot_func import FormatAxes,format_plot
##########################
# new simple method
##########################
def plot_death_rates_loglog_full(fk,lr,ax=None,
                                x1lim = [8e-3, 11],  #[8e-2, 1.1],  #[1e-1, 1] # [5,10]
                                x2lim = [1e-2, 250],  #[1e-2, 25], #[50,350]
                                legend_alpha=1.,
                                minx=0.1,
                                alpha=0.2,
                                s=40,
                                fontsize=18,
                                use_loglog=True,
                                frameon_legend=False,
                                show_fk=True,
                                show_lr=True,
                                zorder=0,**kwargs):
    """
    Example Usage:
ax = plot_death_rates_loglog_full(fk,lr,ax)
    """
    if ax is None:
        ax = plt.gca()
    #plot the full models
    if show_fk:
        boo=fk['q']>=minx
        ax.scatter(fk[boo]['q'].values,fk[boo]['w'].values,c='C0',alpha=alpha,s=s,label='Fenton-Karma',zorder=zorder)
        # ax.scatter(fk['q'].values,fk['w'].values,c='C0',alpha=alpha,s=s,label='Fenton-Karma',zorder=zorder)
    if show_lr:
        boo=lr['q']>=minx
        ax.scatter(lr[boo]['q'].values,lr[boo]['w'].values,c='C1',alpha=alpha,s=s,label='Luo-Rudy',zorder=zorder)
        # ax.scatter(lr['q'].values,lr['w'].values,c='C1',alpha=alpha,s=s,label='Luo-Rudy',zorder=zorder)
    #format
    FormatAxes(
        ax=ax,
        x1lim=x1lim,
        x2lim=x2lim,
        x1label=r'$N/A$ (1/cm$^{2}$)',  #q$ (1/cm$^{2}$)',#r'$q=N/A$ (1/cm$^{2}$)',
        x2label=
        r'$W_{-2}/A$ (Hz/cm$^{2}$)',  #w$ (Hz/cm$^{2}$)',#r'$w=W_{-2}/A$ (Hz/cm$^{2}$)',
        title=None,
        fontsize=fontsize,
        use_loglog=use_loglog)
    format_plot(ax=ax,xlabel=r'q (1/cm$^2$)',ylabel=r'w (Hz/cm$^2$)',fontsize=fontsize,use_loglog=use_loglog,**kwargs)
    leg=ax.legend(loc='lower right',fontsize=fontsize,frameon=frameon_legend)
    for lh in leg.legendHandles:
        lh.set_alpha(legend_alpha)
    return ax

##########################
# old complicated method
##########################
def PlotParticlModelAnnihilationRateFit(a,D,wjr,interp,ax=None,model_name='lr_pbc',c='C1',**kwargs):
    """
    Example Usage:
    wjr=recall_powerlaw_fits_to_full_models()
    interp=recall_particle_model_interp()
    a_hat_FK, D_hat_FK, a_hat_FK_long, a_hat_FK_vlong, a_hat_LR, D_hat_LR, a_hat_LR_long=recall_particle_parameter_measurements()
    dict_out=PlotParticlModelAnnihilationRateFit(a=a_hat_LR,D=D_hat_LR,wjr=wjr,interp=interp,
        ax=None,model_name='lr_pbc',c='C1')
    """
    if ax is None:
        ax=plt.gca()
    plt.sca(ax)
    #compute annihilation rates
    nu_full=wjr[model_name]['m']
    M_full=wjr[model_name]['M']
    q_values=np.linspace(0,1,20)
    w_values=M_full*q_values**nu_full

    if model_name=='lr_pbc':
        model_name_string='Luo-Rudy'
    elif model_name=='fk_pbc':
        model_name_string='Fenton-Karma'
    else:
        model_name_string='??'

    #find a best r,kappa pair for a given a,D pair for a given full model
    args=a,D,q_values,w_values,interp
    bnds = ((1e-3, 2), (1e2, 1e4))
    x0 = (0.1, 500)
    # res = minimize(comp_rmse_via_interp, (0.1, 500), args, method='Nelder-Mead', bounds=bnds,tol=1e-3)
    res = minimize(comp_rmse_via_interp, (0.1, 500), args, method='Nelder-Mead', bounds=bnds,tol=1e-3)
    mse=comp_mse_via_interp(res.x, *args)
    rmse=np.sqrt(mse)
#     rmse=comp_rmse_via_interp(res.x, *args)
#     # print(f"a={a}, D={D}, r={r}, kappa={kappa}, rmse={rmse}")

    #compute the resulting annihilation rates
    r=res.x[0]
    kappa=res.x[1]
    X=np.array([[r,kappa,a,D]])
    yhat = interp(X)
    nu=yhat[0,0]
    M=yhat[0,1]
    # M=yhat[0,2]
    what_values=M*q_values**nu

    #plot the result over the original annihilation rates
    title=f'a={a:.3f}, D={D:.3f}'+r' cm$^2$/s'+f"\nr={r:.3f} cm, "+r'$\kappa$'+f'={kappa:.1f} Hz\nRMSE={rmse:.4f}\n'
    plt.plot(q_values,w_values,c='k',alpha=0.1,lw=3)
    plt.plot(q_values,what_values,'--',c=c,label=f'Fit to\n{model_name_string}',alpha=1)
    #plt.plot(q_values,w_values,c=c,label=model_name_string,alpha=0.5,lw=2)
    #plt.plot(q_values,what_values,c='C4',label='Fit to\nParticle Model',alpha=0.5)
    format_plot(ax=plt.gca(),xlabel=r'$q$ (1/cm$^2$)',ylabel=r'$w$ (Hz/cm$^2$)')
    plt.legend(fontsize=15)
    plt.title(title,fontsize=15)
    print(f"a={a}, D={D}, r={r}, kappa={kappa}, rmse={rmse}")
    return dict(r=r,kappa=kappa,nu=nu,M=M,rmse=rmse,res=res)
