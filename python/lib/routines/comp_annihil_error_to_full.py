#comp_annihil_error_to_full.py
#Programmer: Tim Tyree
#Date: 9.13.2022
import numpy as np, pandas as pd
from ..measure.log_likelihood import comp_log_likelihood_ols
from ..model.recall_fits import recall_death_rates_vidmar_rappel
from ..utils.dict_func import dict_compare

def comp_defect_mean_annihil_rate(df, qlim_full, fit_full, **kwargs):
    """comp_defect_mean_annihil_rate computes the error of w(q) in df to full.
    dict_linear contains the boundaries of df intersected with full as the effective qmin,qmax.
    the linear defects at the boundary are evaluated (emin,emax) in addition to the log defects (lemin,lemax).
    defects computed include the root mean squared error (rmse) and the log-likelihood.
    if parameter s is not specified, then s is taken to be the mle for the ols prior.

    Example Usage:
dict_defects = comp_defect_mean_annihil_rate( df, qlim_full, fit_full)
    """
    #inputs: df, qlim_full, fit_full,
    #outputs:
    #compute the maximal intersection of the explanatory variable, q
    qmin = np.max((df['q'].min(),qlim_full[0]))
    qmax = np.min((df['q'].max(),qlim_full[1]))
    #constrain boundary evaluate to the closest interior points simulated value for q at either bound
    qmin = df.loc[df['q']>=qmin,'q'].min()
    qmax = df.loc[df['q']<=qmax,'q'].max()
    if not (qmin<qmax):
        return None
    #constrain to the interior
    boo  = (df['q']>=qmin)&(df['q']<=qmax)
    q_values = df[boo]['q'].values
    w_values = df[boo]['w'].values
    #evaluate the full model powerlaw fit
    what_values = fit_full['M']*(q_values**fit_full['m'])
    #evaluate boundary and compute rmse
    e_values = w_values-what_values
    emin = float(e_values[q_values==qmin])
    emax = float(e_values[q_values==qmax])
    num_obs = w_values.shape[0]
    #compute rmse
    rmse = np.sqrt(np.mean((e_values)**2))
    #evaluate boundary and compute log-likelihood
    le_values = np.log(w_values/what_values)
    lemin = float(e_values[q_values==qmin])
    lemax = float(e_values[q_values==qmax])
    #compute log-likelihood / negative mutual information / negative entropy
    if le_values.shape[0]>0:
        ll = comp_log_likelihood_ols(le_values**2,**kwargs)
    else:
        ll = np.nan
    dict_defects = dict(num_obs=num_obs,qmin=qmin,qmax=qmax,
                        rmse=rmse,log_likelihood=ll,
                       emin=emin,emax=emax,lemin=lemin,lemax=lemax)
    return dict_defects


def routine_measure_annihilation_defect(input_fn,min_num_particles=8,
        model_lst=['fk','lr'],
        rmse_lst=[0.0530, 0.0684], #Hz/cm^2
        **kwargs):
    """returns tuple of the pandas.DataFrameinstance read from input_fn
    along with associated dictionary, dict_linear.
    dict_linear contains the error of linear/powerlaw fit to full pair-annihilation rates
    kwargs are directly passed to recall_death_rates_vidmar_rappel
    in addition to being passed to comp_defect_mean_annihil_rate directly.

    Example Usage:
df,dict_linear = routine_measure_annihilation_defect(input_fn,printing=True)#,**kwargs)
    """
    df=pd.read_csv(input_fn)
    #parse input_fn for unique identifier
    lst = input_fn.split('.')
    cluster_index=eval(lst[-2])
    job_index=eval(lst[-1])
    #compute w,q and add as fields to df
    df['q']=df['N']/(df['L']**2)
    df['w']=(df['CollTime']**-1)/(df['L']**2)
    df_all=df.copy()
    df = df[df['N']>=min_num_particles].copy()
    #drop any rows that had infinite apparent mean collision rate
    boo_inf = np.isinf(df['w'].values)
    df = df[~boo_inf].copy()
    if df.shape[0]==0:
        return None,None

    #parse input_fn for unique identifier
    lst = input_fn.split('.')
    cluster_index=eval(lst[-2])
    job_index=eval(lst[-1])
    #recall annihilation rates from full model
    dict_wjr = recall_death_rates_vidmar_rappel(**kwargs)
    fk=dict_wjr['fk']
    lr=dict_wjr['lr']
    #determine a reasonable qmin,qmax
    dict_linear=dict(cluster_index=cluster_index,job_index=job_index,
            dict_min = dict(df.min()),
            dict_max = dict(df.max()),
    )
    #compute defects for either of the full models
    # for model_str in ['fk','lr']:
    for model_str,rmse in zip(model_lst,rmse_lst):
        qlim_full = dict_wjr[f'qlim_{model_str}']
        fit_full = dict_wjr['wjr'][f"{model_str}_pbc"]
        #compute defect
        dict_defects = comp_defect_mean_annihil_rate( df, qlim_full, fit_full,s=rmse,**kwargs)
        if dict_defects is None:
            return df,None
        else:
            dict_linear[f"dict_defects_{model_str}"]=dict(dict_defects)
    return df_all,dict_linear

def parse_dict_linear_to_row(dic):
    """
    Example Usage:
dict_defects_fk,dict_defects_lr = parse_dict_linear_to_row(dic = dict_linear)
    """
    added, removed, modified, same = dict_compare(dic['dict_min'],dic['dict_max'])
    #test for equality of keys
    assert set()==added
    assert set()==removed
    #test exactly the right keys are equal in the dictionary
    assert same=={'D','Dt','L','dt','force_code','kappa','neighbor','niter','no_attraction','no_repulsion','r','reflect','set_second','varkappa','x0'}

    dict_defects_fk = dict(dic['dict_defects_fk'])
    dict_defects_lr = dict(dic['dict_defects_lr'])
    #wlog, map same values in dict_min to dict_defects_...
    dict_min=dic['dict_min']
    for key in same:
        dict_defects_fk[key]=dict_min[key]
        dict_defects_lr[key]=dict_min[key]
    #for modified values, map them to ..._lo,_hi fields
    for key in modified:
        vlim=modified[key]
        dict_defects_fk[f"{key}_lo"]=vlim[0]
        dict_defects_fk[f"{key}_hi"]=vlim[1]
        dict_defects_lr[f"{key}_lo"]=vlim[0]
        dict_defects_lr[f"{key}_hi"]=vlim[1]
    #set the unique identifier index fields
    dict_defects_fk['cluster_index']=dic['cluster_index']
    dict_defects_fk['job_index']=dic['job_index']
    dict_defects_lr['cluster_index']=dic['cluster_index']
    dict_defects_lr['job_index']=dic['job_index']
    return dict_defects_fk,dict_defects_lr
