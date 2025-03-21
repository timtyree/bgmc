#gpu accelerated bootstrapping. it is no longer the current time (and thus attention) bottleneck...
# programmer: Tim Tyree
# date: 10.3.2021
import dask.bag as db, time
from scipy.stats import normaltest
import cupy as cp, cudf

def bootstrap_mean_95CI_and_print_cu(values,seed=42,printing=True,num_samples=1000, include_normaltest_slowly=True,use_seed=True,**kwargs):
    """
    Example Usage:
    mean_value,Delta_mean,p=bootstrap_mean_95CI_and_print_cu(values)
    """
    if use_seed:
        cp.random.seed(seed)
    Delta_mean,p=bootstrap_95CI_Delta_mean_cu(cp.array(values),num_samples=num_samples, include_normaltest_slowly=include_normaltest_slowly)
    mean_value=np.mean(values)
    if printing:
        print(f"the mean value is {mean_value:.4f}+/-{Delta_mean:.4f}, with test for normality (p={p:.4f})")
    return mean_value,Delta_mean,p

def bootstrap_mean_cu(x,num_samples):
    sizex=x.shape[0]
    return cp.mean(x[cp.random.randint(low=0, high=sizex, size=sizex*num_samples, dtype=int).reshape((sizex,num_samples))],axis=0)

def bootstrap_95CI_Delta_mean_cu(x,num_samples=1000, include_normaltest_slowly=False):
    '''
    Example Usage:
    Delta_mean,p=bootstrap_95CI_Delta_mean_cu(values,num_samples=1000)
    '''
    mean_values=bootstrap_mean_cu(x,num_samples=num_samples)
    sig=cp.std(mean_values)
    if include_normaltest_slowly:
        stat,p = normaltest(mean_values.get())
    else:
        p=-9999.#+0.*mean_values#floating point rep of nan that won't raise exceptions
    Delta_mean=1.96*float(sig)
    return Delta_mean,p

def bootstrap_95CI_Delta_mean_cudf(df,incol,num_samples=1000, include_normaltest_slowly=False):
    x=df[incol].values
    mean_values=bootstrap_mean_cu(x,num_samples=num_samples)
    sig=cp.std(mean_values)
    if include_normaltest_slowly:
        p = normaltest(mean_values.get())
    else:
        p=-9999.+0.*mean_values#floating point rep of nan that won't raise exceptions
    Delta_mean=1.96*sig
    return Delta_mean,p

def get_routine_bootstrap_bin_cu(x_values,y_values,x_bin_edges,counts,num_samples=100,min_numobs=100,**kwargs):
    '''x_values,y_values,x_bin_edges are 1 dimensional numpy arrays.
    returns the function, routine_bootstrap_bin.'''
    type_in=type(cp.ndarray([]))
    if type(x_values)!=type_in:
        raise "InputError: x and y must have type cp.ndarray!"
    if type(y_values)!=type_in:
        raise "InputError: x and y must have type cp.ndarray!"
    R_values=x_values
    dRdt_values=y_values
    r_edges=x_bin_edges
    def routine_bootstrap_bin_cu(bin_id):
        j=bin_id
        numobs=counts[j]
        if numobs>min_numobs:
            boo=(R_values>=r_edges[j])&(R_values<r_edges[j+1])
            r_values=R_values[boo]
            drdt_values=dRdt_values[boo]
            #compute mean values in bin
            r=cp.mean(r_values)
            drdt=cp.mean(drdt_values)
            # compute 95% CI for mean
            Delta_r,p_r=bootstrap_95CI_Delta_mean_cu(r_values,
                                                 num_samples=num_samples)
            Delta_drdt,p_drdt=bootstrap_95CI_Delta_mean_cu(drdt_values,
                                                 num_samples=num_samples)
            return cp.array((r,drdt,Delta_r,Delta_drdt,p_r,p_drdt,numobs))
        else:
            return cp.array((-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.))
    return routine_bootstrap_bin_cu

def bin_and_bootstrap_xy_values_cu(x,
                               y,
                               xlabel='x',
                               ylabel='y',
                               bins='auto',
                               min_numobs=None,
                               num_bootstrap_samples=1000,
                               npartitions=1,
                               use_test=True,
                               test_val=0,printing=False,**kwargs):
    '''
    bin_and_bootstrap_xy_values_parallel returns a pandas.DataFrame instance with the following columns
    columns=[xlabel,ylabel,f'Delta_{xlabel}',f'Delta_{ylabel}',f'p_{xlabel}',f'p_{ylabel}','counts']
    Output Field for a given x bin include:
    - y       : the simple mean value of y
    - Delta_y : difference between the mean value and the edge of the 95% confidence interval of the mean value
    - p_y     : p value estimating the liklihood to reject the null hypothesis which claims the boostrapped distribution is normally distributed.
    - counts  : the number of observations in this bin

    Arguments x and y are assumed to be 1 dimensional numpy.array instances.
    If p_y reliably has values less than 0.05, then consider increasing num_bootstrap_samples

    bin_and_bootstrap_xy_values_parallel passes the kwarg, bins, to numpy.histogram
    to generate x bins, it then passes each x bin to npartitions dask workers, each of which
    selects the y values that correspond to the x values within its respective bin.  With these
    x and y values in hand, that worker bootstraps num_bootstrap_samples samples of approximations of
    the mean value for those x and y values.

    A bin is ignored if it contains no more than min_numobs
    observations.  If min_numobs=None, then min_numobs=cp.mean(counts)/8, where counts is the array of
    counts in each bin.

    Example Usage: compute the bootstrapped mean dRdt (y_values) binning by one_over_R (x_values)
boo=x_values>0
df_out=bin_and_bootstrap_xy_values_parallel(x=x_values[boo],
                               y=y_values[boo],
                               xlabel='one_over_R',
                               ylabel='dRdt',
                               bins='auto',
                               min_numobs=None,
                               num_bootstrap_samples=1000,
                               npartitions=os.cpu_count(),#full cylinders
                               use_test=False,
                               test_val=0,printing=False)#,**kwargs)

    '''
    x_values=x
    y_values=y
    num_samples=num_bootstrap_samples
    counts,x_bin_edges=cp.histogram(x_values,bins=bins)
    bin_id_lst=list(range(x_bin_edges.shape[0]-1))
    if min_numobs is None:
        min_numobs=cp.mean(counts)/8

    #bake method to bootstrap 95%CI of mean of y conditioned on x being within a given bin
    routine_bootstrap_bin_cu=get_routine_bootstrap_bin_cu(x_values,y_values,x_bin_edges,counts,num_samples=num_samples,min_numobs=min_numobs)
    def routine(input_val):
        # try:
        return routine_bootstrap_bin_cu(input_val)
        # except Exception as e:
        #     return f"Warning: something went wrong, {e}"

    #optionally test the routine
    if use_test:
        retval=routine(test_val)

    #all CPU version
    b = db.from_sequence(bin_id_lst, npartitions=npartitions).map(routine)
    start = time.time()
    retval = list(b)
    if printing:
        print(f"run time for bootstrapping was {time.time()-start:.2f} seconds.")

    array_out=cp.stack(retval)#[x for x in retval if x is not None])
    columns=[xlabel,ylabel,f'Delta_{xlabel}',f'Delta_{ylabel}',f'p_{xlabel}',f'p_{ylabel}','counts']
    # columns=['r','drdt','Delta_r','Delta_drdt','p_r','p_drdt','counts']
    df=cudf.DataFrame(data=array_out,columns=columns)
    df=df.astype({'counts': 'int32'})
    return df
