#PlotFits.py
#Programmer: Tim Tyree
#Date: 1.3.2022
import matplotlib.pyplot as plt, numpy as np, pandas as pd
from scipy.optimize import minimize
from .. import comp_rmse_via_interp,comp_mse_via_interp
from .bluf import format_plot

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
