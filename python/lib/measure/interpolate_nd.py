from scipy.interpolate import LinearNDInterpolator
import numpy as np, pandas as pd

#TODO: move this into lib for the boltzaman weighted mean routine
def comp_ND_interpolation(dg,input_cols,output_col,**kwargs):
    """inputs:dg,input_cols,output_col
        output: fitted model
    dg=df[query] is a pandas.DataFrame instance assumed to have a unique trial
    for any unique combination of fields indicated by input_col
    define parameters to be varied
    input_cols=['r','D','varkappa']#,x0
    input_cols=['r','kappa','D','varkappa']#,x0

    Example Usage:
    interp=comp_ND_interpolation(dg,input_cols,output_col)
    """

    Xall=dg[input_cols].values
    yall=dg[output_col].values
    X=Xall.copy()
    y=yall.copy()
    m = len(y) # number of training examples
    print(f'the number of training examples is {m:d}')
    try:
        interp = LinearNDInterpolator(X, y)
        yhat = interp(X)
        rmse=np.sqrt(np.mean((yhat-y)**2))
    except Exception as e:
        #print('Warning: '+e) #QhullError...
        interp = LinearNDInterpolator(X, y)
        yhat = interp(X)
        rmse=np.sqrt(np.mean((yhat-y)**2))
    # # interp = CloughTocher2DInterpolator(X, y)
    # yhat = interp(X)
    # rmse=np.sqrt(np.mean((yhat-y)**2))
    print(f"the rmse of ordinairy interpolation is {rmse:.4f}")

    # #forked from:
    # interp = LinearNDInterpolator(X, y)
    # # interp = CloughTocher2DInterpolator(X, y)
    # yhat = interp(X)
    # rmse=np.sqrt(np.mean((yhat-y)**2))
    # print(f"the rmse of simple interpolation is {rmse:.4f}")
    return interp
