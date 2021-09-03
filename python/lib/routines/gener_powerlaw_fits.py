#functionally generates a .csv file listing all powerlaw fits for a folder of trials recorded as .csv files.
# the input .csv files are returned by postprocessing the raw output data log printed in tim's custom c and perl code
# the input .csv files are repeatably saved to bgmc/python/data/osg_output/
import scipy,numpy as np,pandas as pd, os
from ..utils import *
from ..measure import *
from ..model.recall_fits import recall_powerlaw_fits_to_full_models

def gener_powerlaw_fit(input_fn,q_min=None,q_max=None,printing=False,testing=False,**kwargs):
    '''for runs 12-15 (and probably later),
    q_min is set to 0.1 particles per square centimeter, and
    q_max is set to 1.0 particles per square centimeter.

    Example Usage:
    data_dir="/home/timothytyree/Documents/GitHub/bgmc/python/data/osg_output/run_15_all.csv"
    m,Delta_m,M,Delta_M,Rsq,rmse=gener_powerlaw_fit(input_fn,**kwargs)
    '''
    df=pd.read_csv(input_fn)
    # df.head()
    if printing:
        print(f"the columns present are:")
        print(list(df.columns))
    if testing:
        assert (not (df.CollRate<0).any())
        if printing:
            print("all results from trials have nonnegative collision rates.")

    #derived values
    CollRate_missing=len(list(set(df.columns).intersection({'CollRate'})))==0
    if CollRate_missing:
        df['CollRate']=1./df['CollTime']
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(subset=['CollRate'], how="all",inplace=True)
    df['A']=df['L']**2
    df['q']=df['N']/df['A'] #number of tips per square centimeter
    df['w']=df['CollRate']/df['A'] #[mHz?]/cm^2

    if q_min is None:
        q_min=np.min(df['q'].values)
    if q_max is None:
        q_max=np.max(df['q'].values)

    # df=df[df.niter==250].copy()
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
        #make test for whether there is one input parameter present in an input DataFrame
        print(f"parameter values considered in this df:")
        print(f"D~{D_values}")
        print(f"L~{L_values}")
        print(f"kappa~{kappa_values}")
        print(f"x0~{x0_values}")
        print(f"set_second~{set_second_values}")
        print(f"reflect~{reflect_values}")
        print(f"no_repulsion~{no_repulsion_values}")
        print(f"no_attraction~{no_attraction_values}")
        print(f"neighbor~{neighbor_values}")
        print(f"force_code~{force_code_values}")
        # print(f"varkappa~{np.mean(varkappa_values):.3f}+-{2*np.std(varkappa_values):.3f}")
        print(f"varkappa~{varkappa_values}")
        print(f"r~{r_values}")

    #query functionally
    r=r_values[0]#1]
    kappa=kappa_values[0]
    D=D_values[0]#-1]#
    varkappa=varkappa_values[0]#3]# #cm^2/s in manuscript, varkappa is a
    x0=x0_values[0]        #cm
    L=L_values[0]
    set_second=set_second_values[0]#0
    no_repulsion=no_repulsion_values[0]#0
    no_attraction=no_attraction_values[0]#0
    reflect=reflect_values[0]#0
    neighbor=neighbor_values[0]#0
    force_code=force_code_values[0]#2

    #query the DataFrame
    query =(df.set_second==set_second)&(df.reflect==reflect)
    query&=df.r==r
    query&=df.D==D
    query&=df.L==L
    query&=df.varkappa==varkappa
    query&=df.x0==x0
    query&=(df.no_repulsion==no_repulsion)&(df.no_attraction==no_attraction)
    query&=(df.neighbor==neighbor)&(df.force_code==force_code)
    dg=df[query]
    dh=dg[dg.kappa==kappa]
    x_values=dh.q.values
    y_values=dh.w.values

    if printing:
        print((varkappa,x_values.shape))

    #fit powerlaw using OLS of the log-log plot
    boo=(x_values>q_min)&(x_values<q_max)
    x=x_values[boo]
    y=y_values[boo]
    B,Delta_B,m,Delta_m,Rsq=fit_power_law(x,y)
    rmse=compute_power_rmse(x,y,m,B)
    M, Delta_M= comp_power_scale(B,Delta_B,m,Delta_m)
    if printing:
        print(f"fitting from {q_min:.3f} <= q <= {q_max:.3f}")
        print(f"m={m:.6f}+-{Delta_m:.6f}; B={B:.6f}+-{Delta_B:.6f}")
        print(f"M= {M:.6f}+-{Delta_M:.6f} Hz*cm^{{2(m-1)}}")
        print(f"RMSE={rmse:.4f} Hz/cm^2")
        print(f"R^2={Rsq:.4f}")

    #record input parameters and output measures
    dict_out={
        'm':m,
        'Delta_m':Delta_m,
        'M':M,
        'Delta_M':Delta_M,
        'Rsq':Rsq,
        'rmse':rmse,
        'q_min':q_min,
        'q_max':q_max,
        'r':r,
        'kappa':kappa,
        'D':D,
        'varkappa':varkappa,
        'x0':x0,
        'L':L,
        'force_code':force_code,
        'neighbor':neighbor,
        'reflect':reflect,
        'set_second':set_second,
        'no_repulsion':no_repulsion,
        'no_attraction':no_attraction
    }

    return dict_out

def gener_df_powerlaw_fits(input_fn,printing=True,testing=True,npartitions=None,return_warnings=False,**kwargs):
    '''
    Example Usage:
    df=gener_df_powerlaw_fits(input_fn,printing=True,testing=True)
    '''
    def routine(input_fn):
        try:
            return gener_powerlaw_fit(input_fn,**kwargs)
        except Exception as e:
            return f"Warning: for input_fn={input_fn}...\n {e}"

    if testing is True:
#         input_fn="/home/timothytyree/Documents/GitHub/bgmc/python/data/osg_output/run_15_all/job.out.13954413.14"
    #     input_fn="/home/timothytyree/Documents/GitHub/bgmc/python/data/osg_output/run_15_all.csv"
        dict_out=routine(input_fn)
        if printing:
            print(f"testing input_fn")
            print(dict_out)
    if npartitions is None:
        npartitions=os.cpu_count()

    #run all ^this over dask (~9800 jobs over 12 cores... 1.5 seconds per job... this supports 0.34 hours to process this step)
    # Estimated run time equals 1.5*9800/12=0.34 hours
    # 1.5*9800/12/60/60
    if printing:
        print(f"parsing absolute directory of input_fn={input_fn}...")
    input_folder=os.path.dirname(input_fn)
    trial_folder_name=os.path.dirname(input_folder)

    os.chdir(input_folder)
    # trgt=''#input_fn[input_fn.find('.csv'):]
    # assert(input_fn[-len(trgt):]==trgt)
    # input_fn_lst=get_all_files_matching_pattern(input_fn,trgt)
    input_fn_lst=os.listdir()
    if printing:
        print(f"We're about to use {npartitions} cores to obliterate {len(input_fn_lst)} csv files from {input_folder}")

    #all CPU version
    b = db.from_sequence(input_fn_lst, npartitions=npartitions).map(routine)
    start = time.time()
    retval = list(b)
    if printing:
        print(f"run time for computing powerlaw fits was {time.time()-start:.2f} seconds.")
    # beep(3)

    if return_warnings:
        dict_out_lst=retval
    else:
        dict_out_lst=[fn for fn in retval if not (type(fn)==type(str()) )]# or not fn.find('Warning:')==-1]
    if printing:
        print(f"computed powerlaw fits for  {len(dict_out_lst)} trials successfully.")
    if testing:
        assert (len(dict_out_lst)>0)

    df=pd.DataFrame(dict_out_lst)
    return df

def gener_df_powerlaw_fits_and_to_csv(input_fn,save_folder=None,save_fn=None,printing=True,**kwargs):
    '''
    Example Usage:
    save_dir=gener_df_powerlaw_fits_and_to_csv(input_fn)
    '''

    df=gener_df_powerlaw_fits(input_fn,printing=printing,**kwargs)
    #run all ^this over dask (~9800 jobs over 12 cores... 1.5 seconds per job... this supports 0.34 hours to process this step)
    # Estimated run time equals 1.5*9800/12=0.34 hours
    # 1.5*9800/12/60/60
    if printing:
        print(f"parsing absolute directory of input_fn={input_fn}...")
    input_folder=os.path.dirname(input_fn)
    trial_folder_name=os.path.dirname(input_folder)
    if save_folder is None:
        save_folder=trial_folder_name
    if save_fn is None:
        save_fn = os.path.basename(input_folder)+'_powerlaw_fits.csv'
    #save df as .csv
    os.chdir(save_folder)
    df.to_csv(save_fn,index=False)
    save_dir=os.path.abspath(save_fn)
    if printing:
        print(f"powerlaw fits from particle model were successfully saved in \n{save_dir}")
    return save_dir

if __name__=='__main__':
    from ..utils import *
    input_fn=search_for_file()
    # input_fn="/home/timothytyree/Documents/GitHub/bgmc/python/data/osg_output/run_15_all/job.out.13954413.14"
    printing=True
    kwargs={}
    npartitions=os.cpu_count()
    save_dir=gener_df_powerlaw_fits_and_to_csv(input_fn,**kwargs)
