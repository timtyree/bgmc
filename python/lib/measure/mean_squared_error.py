import numpy as np, pandas as pd

def comp_rmse_via_interp(x, *args):
    '''find a best r,kappa pair for a given a,D pair for a given full model'''
    a,D,q_values,w_values,interp=args
    r,kappa=x
    #interpolate nu and M using interp
    X=np.array([[r,kappa,a,D]])
    yhat = interp(X)
    nu=yhat[0,0]
    M=yhat[0,1]
    # M=yhat[0,2]
    what_values=M*q_values**nu
    rmse_full=np.sqrt(np.mean((what_values-w_values)**2))
    return rmse_full

def comp_mse_via_interp(x, *args):
    '''find a best r,kappa pair for a given a,D pair for a given full model
x=r,kappa
args=a,D,q_values,w_values,interp
    '''
    a,D,q_values,w_values,interp=args
    r,kappa=x
    #interpolate nu and M using interp
    X=np.array([[r,kappa,a,D]])
    yhat = interp(X)
    nu=yhat[0,0]
    M=yhat[0,1]
    # M=yhat[0,2]
    what_values=M*q_values**nu
    mse=np.mean((what_values-w_values)**2)
    return mse

def comp_mse_via_interp_unattractive(x, *args):
    '''find a best r,kappa pair for a given a,D pair for a given full model
x=r,kappa,D
args=q_values,w_values,interp
    '''
    q_values,w_values,interp=args
    r,kappa,D=x
    #interpolate nu and M using interp
    X=np.array([r,kappa,D])
    yhat = interp(X)
    nu=yhat[0,0]
    M=yhat[0,1]
    # M=yhat[0,2]
    what_values=M*q_values**nu
    mse=np.mean((what_values-w_values)**2)
    return mse
