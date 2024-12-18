import numpy as np, pandas as pd, os
from .. import *
from ..utils.utils_traj import unwrap_traj_and_center
from ..measure.compute_msd_simple import msd_fft
#simple routine for computation of individual mean squared displacements
# Programmer: Tim Tyree
# 7.20.2021
def compute_individual_mean_squared_displacement(df,dft1,dft2,DT,pid,pid_col,t_col='t',max_lagtime=None,**kwargs):
    '''
    Example Usage:
    lagt_values,msd_values=compute_individual_mean_squared_displacement(df,dft1,dft2,DT,pid,pid_col='pid_explicit')
    '''
    #extract the trajectory as a DataFrame instance
    t1=float(dft1[dft1.index==pid].values[0])
    t2=float(dft2[dft2.index==pid].values[0])
    # print(f"computing msd for particle {pid} from times {t1} to {t2} ms...")

    #extract the trajectory as a DataFrame instance
    boo = df[pid_col]==pid
    boo&= df[t_col]>=t1
    boo&= df[t_col]<=t2
    dff=df[boo]

    #extract r from  dff
    my_r=dff[['x','y']].values
    msd_values=msd_fft(my_r)
    lagt_values=DT*(np.arange(msd_values.shape[0]))
    return lagt_values,msd_values

#trackpy is scaling is unavoidably deprecated
# fps = 1./DT #output time units is in same time units as inputs
# if max_lagtime is None:
#     max_lagtime=dff.index.values.shape[0]
# # Input units are pixels and frames. Output units are microns and seconds.
# df_out=trackpy.motion.msd(
#     traj=dff,
#     mpp=1.,#does nothing
#     fps=fps,
#     max_lagtime=max_lagtime,
#     detail=False
# )
# lagt_values,msd_values=df_out[['lagt','msd']].values.T
# return lagt_values,msd_values
def comp_each_mean_squared_displacement_particle(df,input_fn,DT,ds,width,
                 minimum_lifetime,crop_start_by,crop_end_by,
                 pid_col,t_col,max_lagtime=None,use_unwrap=False,
                 **kwargs):
    DS = ds / width
    height=width
    # df = pd.read_csv(input_fn)
    # DT = get_DT(df, t_col=t_col, pid_col=pid_col)
    if use_unwrap is True:
        #unwrap trajectories
        pid_lst = sorted(set(df[pid_col].values))
        #(duplicates filtered earlier in full model pipeline.  Unnecessary in particle model with explicit tracking_ _  _ _ ) filter_duplicate_trajectory_indices is slow (and can probs be accelerated with a sexy pandas one liner)
        # pid_lst_filtered = filter_duplicate_trajectory_indices(pid_lst,df)
        df = pd.concat([
            unwrap_traj_and_center(df[df[pid_col] == pid],
                                   width=width,
                                   height=height,
                                   **kwargs) for pid in pid_lst
        ])

    #compute t0 and tf for each particle
    dft = df.groupby(pid_col)[t_col].describe()
    dft0 = dft['min']
    dftf = dft['max']

    #compute t1 and t2 for each particle
    dft1 = dft0 + crop_start_by
    dft2 = dftf - crop_end_by

    #get the list of particles dft2-dft1 \ge minimum_lifetime
    dflifetime_considered = dft2 - dft1
    pid_values_to_consider = dflifetime_considered[
        dflifetime_considered >= minimum_lifetime].index.values

    #compute number of num_individuals
    # pid_lst=sorted(set(df[pid_col].values))
    num_individuals = len(list(pid_values_to_consider))
    # print(f'Computing msd values for {num_individuals} particles...')

    #for each particle, set lagt equal to the zero'd time
    event_id_lst = sorted(set(df[pid_col].values))
    for pid in pid_values_to_consider:
        boo = df[pid_col] == pid
        tbirth = df.loc[boo, 't'].min()
        df.loc[boo, 'lagt'] = df.loc[boo, 't'] - tbirth

    df['msd'] = (df['x']**2 + df['y']**2) * DS**2
    df['pid'] = df[pid_col]
    df_msd = df[['pid', 'lagt', 'msd']].copy()
    df_msd.dropna(inplace=True)
    return df_msd

def comp_each_mean_squared_displacement(df,input_fn,DT,ds,width,
                         minimum_lifetime,crop_start_by,crop_end_by,
                         pid_col,t_col,max_lagtime=None,use_unwrap=False,
                         **kwargs):
    '''
    output is in length units of ds/width and duration units of DT.
    computes the mean squared displacements for each trajectory listed in input_fn
    input_fn gives the location of a trajectory file with columns x,y,frames, and some pid_col.
    trajectory that may have periodic periodic boundary conditions on a square domain.


    Example Usage:
    input_fn=''
    df_msd=comp_each_mean_squared_displacement(df,input_fn,DT,ds,width,
                             minimum_lifetime,crop_start_by,crop_end_by,
                             pid_col,t_col,max_lagtime=None,
                             **kwargs)
    '''
    height=width
    DS=ds/width

    if use_unwrap:
        #unwrap trajectories
        pid_lst = sorted(set(df[pid_col].values))
        #(duplicates filtered earlier in full model pipeline.  Unnecessary in particle model with explicit tracking... filter_duplicate_trajectory_indices is slow (and can probably be accelerated with a sexy pandas one liner)
        # pid_lst = filter_duplicate_trajectory_indices(pid_lst,df)
        df = pd.concat([unwrap_traj_and_center(df[df[pid_col]==pid], width=width, height=height, **kwargs) for pid in pid_lst])

    #compute t0 and tf for each particle
    dft=df.groupby(pid_col)[t_col].describe()
    dft0=dft['min']
    dftf=dft['max']

    #compute t1 and t2 for each particle
    dft1=dft0+crop_start_by
    dft2=dftf-crop_end_by

    #get the list of particles dft2-dft1 \ge minimum_lifetime
    dflifetime_considered=dft2-dft1
    pid_values_to_consider=dflifetime_considered[dflifetime_considered>=minimum_lifetime].index.values

    #compute number of num_individuals
    # pid_lst=sorted(set(df[pid_col].values))
    num_individuals=len(list(pid_values_to_consider))
    # print(f'Computing msd values for {num_individuals} particles...')

    #how long does it take 1 core to compute the msd's for every particle in this trial?
    lagt_out_lst=[];msd_out_lst=[];pid_out_lst=[]
    for pid in pid_values_to_consider:
        #compute output
        lagt_values,msd_values=compute_individual_mean_squared_displacement(df,dft1,dft2,DT,pid,pid_col=pid_col)
        pid_values=np.zeros_like(msd_values,dtype='int')
        #record output
        pid_out_lst.extend(pid_values)       #indices that identify the particles
        lagt_out_lst.extend(lagt_values)     #ms
        msd_out_lst.extend(DS**2*msd_values) #units of ds

    df_out=pd.DataFrame({'pid':pid_out_lst,'lagt':lagt_out_lst,'msd':msd_out_lst})
    return df_out


def compute_each_mean_squared_displacement(input_fn,DT,ds,width,
                         minimum_lifetime,crop_start_by,crop_end_by,
                         pid_col,t_col,max_lagtime=None,use_unwrap=False,use_particle_avg=True,
                         **kwargs):
    '''
    computes the mean squared displacements for each trajectory listed in input_fn
    input_fn gives the location of a trajectory file with columns x,y,frames, and some pid_col.
    trajectory that may have periodic periodic boundary conditions on a square domain.
    '''
    df=pd.read_csv(input_fn)
    if not use_particle_avg:
        return comp_each_mean_squared_displacement(df,input_fn,DT,ds,width,
                         minimum_lifetime,crop_start_by,crop_end_by,
                         pid_col=pid_col,t_col=t_col,max_lagtime=max_lagtime,use_unwrap=use_unwrap,
                         **kwargs)
    else:
        return comp_each_mean_squared_displacement_particle(df,input_fn,DT,ds,width,
                         minimum_lifetime,crop_start_by,crop_end_by,
                         pid_col=pid_col,t_col=t_col,use_unwrap=use_unwrap,#max_lagtime=max_lagtime,
                         **kwargs)

def routine_compute_imsd(input_fn,save_folder=None,use_unwrap=False,**kwargs):
    #compute results
    df_msd=compute_each_mean_squared_displacement(input_fn,use_unwrap=use_unwrap,**kwargs)
    #save results
    folder_name=os.path.dirname(input_fn)
    dirname = folder_name.split('/')[-1]
    if save_folder is None:
        save_folder = folder_name.replace(dirname,'msd')
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    os.chdir(save_folder)
    output_fn=os.path.basename(input_fn).replace('.csv','_emsd.csv')
    df_msd.to_csv(output_fn, index=False)
    return os.path.abspath(output_fn)
