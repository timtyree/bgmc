from .. import *
from ..getterdone_gpu import *
import cupy as cp
import cudf, cuml, xgboost
# import dask_cudf
import cuxfilter, cusignal
from ..measures.bootstrap import *
# from ..viewer.PlotBootstrap import *


def comp_square_displacement_rapids(df,t_col='t',pos_col_lst=['x','y']):
    '''computes the squared displacement for one trajectory stored in cudf.DataFrame instance, df.
    Example Usage:
    df=comp_square_displacement_rapids(df,t_col='t',pos_col_lst=['x','y'])
    '''
    t_values=df[t_col].values
    xy_values=df[pos_col_lst].values
    # print((xy_values.shape,t_values.shape))
    t0=t_values[0]
    xy0=xy_values[0]
    # print((t0,xy0))
    tau_values=t_values-t0
    sd_values=cp.sum((xy_values-xy0)**2,axis=1)
    df['tau']=tau_values
    df['sd']=sd_values
    return df

def resample_linearly_rapids(df,dt=0.0036,t_col='tau',pos_col='sd'):
    '''compute the linearly interpolated time series at a regular interval of dt
    Example Usage:
    tau_values_interpolated, sd_values_interpolated=resample_linearly_rapids(df,dt=0.0036,t_col='tau',pos_col='sd')
    '''
    sd_values=df[pos_col].values
    tau_values=df[t_col].values
    tau_values_interpolated=cp.arange(tau_values.min(),tau_values.max(),dt)
    sd_values_interpolated=cp.interp(x=tau_values_interpolated, xp=tau_values, fp=sd_values, left=None, right=None, period=None)
    return tau_values_interpolated, sd_values_interpolated

def comp_ewma_rapids(data, window, n):
    '''returns the exponentially weighted moving average of 1D cupy array, dat.
    n is data.get().shape[0]'''
    alpha = 2 /(window + 1.0)
    alpha_rev = 1-alpha
    pows = alpha_rev**(cp.arange(n+1))
    scale_arr = 1/pows[:-1]
    offset = data[0]*pows[1:]
    pw0 = alpha*alpha_rev**(n-1)
    mult = data*pw0*scale_arr
    cumsums = mult.cumsum()
    out = offset + cumsums*scale_arr[::-1]
    return out

def routine_csv_to_smoothed_squared_displacement(input_fn,t_col='t',pos_col_lst=['x','y'],dt_smooth=0.036,**kwargs):
    #load one token matching trial
    df = cudf.read_csv(input_fn)
    df=comp_square_displacement_rapids(df,t_col=t_col,pos_col_lst=pos_col_lst)
    # assert not df.isnull().any().any()
    # df.head()

    #pick a reasonable time step
    dt_values=df['tau'].diff().dropna().values.get()
    dt=np.around(np.quantile(dt_values,0.25),8)
    # print(f'the time step is {dt} seconds')

    # plt.hist(dt_values)
    # plt.show()

    # compute the linearly interpolated time series at a regular interval of dt
    tau_values_interpolated, sd_values_interpolated=resample_linearly_rapids(df,dt=dt,t_col='tau',pos_col='sd')

    #smoothing
    # dt_smooth=0.036# seconds
    window=int(dt_smooth/dt)
    n = sd_values_interpolated.shape[0]
    sd_values_smoothed=comp_ewma_rapids(sd_values_interpolated, window, n)
    tau_values_smoothed=comp_ewma_rapids(tau_values_interpolated, window, n)

    t_values=df[t_col].values
    xy_values=df[pos_col_lst].values
    # print((xy_values.shape,t_values.shape))
    t0=float(t_values[0].get())+0.*tau_values_smoothed
    return t0,tau_values_smoothed,sd_values_smoothed

def routine_folder_to_bootstrapped_msd(input_fn,npartitions=None,num_bootstrap_samples=1000.,**kwargs):
    '''
    Example Usage:
    x_values, y_values, x_err_values, y_err_values=routine_folder_to_bootstracpped_msd(input_fn)
    '''
    if npartitions is None:
        npartitions=os.cpu_count()
    t0,tau_values_smoothed,sd_values_smoothed=routine_csv_to_smoothed_squared_displacement(input_fn)

    #define map input_fn to df functionally
    def routine(input_fn):
        try:
            t0,tau_values_smoothed,sd_values_smoothed=routine_csv_to_smoothed_squared_displacement(input_fn)
            return cudf.DataFrame({'t0':t0.get(),'tau':tau_values_smoothed,'sd':sd_values_smoothed})
            #         return {'t0':t0.get(),'tau':tau_values_smoothed,'sd':sd_values_smoothed}
        except Exception as e:
            return None

    #compute a few single particle squared displacements
    bag = db.from_sequence(input_fn_lst[:3], npartitions=10).map(routine)
    start = time.time()
    df = cudf.concat(list(bag)).dropna().copy()
    print(f"the run time for filtering files was {(time.time()-start)/60:.2f} minutes.")

    ##### Nota Bene: the remaining is run on cpu only... and therefore is the computational bottleneck

    #compute smoothed squared displacement for all match trials
    bag = db.from_sequence(input_fn_lst, npartitions=os.cpu_count()).map(routine)
    start = time.time()
    df = cudf.concat(list(bag)).dropna().copy()
    print(f"the run time for filtering files was {(time.time()-start)/60:.2f} minutes.")

    #compute mean squared displacement via bootstrap
    df['t']=df['tau']+df['t0']

    #extract bootstraped 95% CI for the mean
    df_out = bootstrap_and_bin_xy_values_parallel(x=df['t'].values.get(),
                                                  y=df['sd'].values.get(),
                                                  xlabel='tau',
                                                  ylabel='msd',
                                                 npartitions=os.cpu_count(),
                                                 min_numobs=100,
                                                num_bootstrap_samples=1000,printing=True)

    #extract xy values
    x_values=df_out['tau'].values
    y_values=df_out['msd'].values
    x_err_values=df_out['Delta_tau'].values
    y_err_values=df_out['Delta_msd'].values
    return x_values, y_values, x_err_values, y_err_values
