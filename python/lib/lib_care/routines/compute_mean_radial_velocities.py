import numpy as np, pandas as pd, os
from ..measure.bootstrap import *
from ..measure.filter_topological_events import *
from ..measure.compute_forces_at_annihilation import *
# from ..utils.utils_traj import get_tips_in_range
import random

#####################################################
# Methods conditioned on data from topological events
#####################################################
def comp_mean_radial_velocities(df,input_fn,remove_before_jump,minR_thresh,max_speed_thresh,t_col='tdeath',id_col='event_id',
    bins='auto',min_numobs=None,num_samples=1000,flip_time=False,use_smoothing=True,tavg1=1.5,tavg2=2.5,printing=False,**kwargs):
    '''returns a dict containing results for mean radial velocities.

    computes the mean radial velocities, binning by radius.
    supposes df is from a .csv file containing annihilation or creation results,
    where rows are presorted according to event and then by t_col.
    minR_thresh is in cm and max_speed_thresh is in cm/ms.
    navg is the number of frames to average over.
    if min_numobs is None, then min_numobs is determined from the mean counts in each bin.
    - output time units is in milliseconds
    - output length units is the same as input length units

    Example Usage:
    dict_out=compute_mean_radial_velocities(df,t_col='tdeath')
    '''
    df.sort_values([id_col,t_col],ascending=False,inplace=True)
    event_id_lst=sorted(set(df[id_col].values))

    if flip_time:
        df[t_col]=-1*df[t_col]
    tvals=sorted(set(df[t_col].values))
    DT=tvals[1]-tvals[0]
    assert(DT>0)#if DT<0, then a factor of -1 is needed in a few places...

    if not use_smoothing:
        df['drdt']=df['r'].diff()/DT
        #set drdt to zero where pid changes or where tdeath jumps by more than dt
        # boo=df[t_col].diff()!=-DT
        boo=~np.isclose(df[t_col].diff(),-DT,5)

        if remove_before_jump:
            #remove any observations occuring before a jump
            book =(df['r']>=minR_thresh)&(np.abs(df['drdt'])>=max_speed_thresh)
            for event_id in event_id_lst:
                #identify any jumps in this event
                booki =book&(df[id_col]==event_id)
                if booki[booki].any(): #if there are any jumps
                    #identify the earliest time where a jump occurs
                    max_time=df[booki][t_col].min()
                    # filters all positions occuring before the final jump for a single annihilation event.
                    bookie=(df[id_col]==event_id)&(df[t_col]>=max_time) #True if a row should be dropped
                    #mark all data for this event to be dropped if it occurs earlier than this time (tdeath is larger than the earliest time)
                    boo |= bookie

        # boo&=df['drdt']>0  #when this is uncommented, the data looks good.  when it is commented, too much is filtered :(
        df.loc[boo,'drdt']=np.nan
        df.dropna(inplace=True)
    else:
        #perform smoothed differentiation for each event_id
        navg1=int(tavg1/DT)
        navg2=int(tavg2/DT)
        if navg2%2==0:
            navg2=navg2+1 #second window must be an odd integer
        if printing:
            print(f"using smoothing windows navg1,navg2={navg1,navg2}, corresponding to tavg1,tavg2=({navg1*DT:.3f},{navg2*DT:.3f}) ms...")
        df,valid_event_id_lst=get_annihilation_df(input_fn,navg1,navg2,
                        t_col = t_col,id_col = id_col,DT = DT,DT_sec=DT*0.001,printing = printing,**kwargs)
        #drop invalid events inplace
        event_id_lst=sorted(set(df[id_col].values))
        invalid_event_id_lst=list(set(event_id_lst).difference(set(valid_event_id_lst)))
        for event_id in invalid_event_id_lst:
            boo=df[id_col]==event_id
            df.loc[boo,'drdt']=np.nan
        df.dropna(inplace=True)

    #implement measure of dRdt that explicitely bins by radius
    counts,r_edges=np.histogram(df.r.values,bins=bins)
    range_values=r_edges
    if min_numobs is None:
        min_numobs=np.mean(counts)/8
    r_lst=[];drdt_lst=[];Delta_r_lst=[];Delta_drdt_lst=[];
    count_lst=[];p_r_lst=[];p_drdt_lst=[]
    for j in range(r_edges.shape[0]-1):
        numobs=counts[j]
        if numobs>min_numobs:
            boo=(df.r>=r_edges[j])&(df.r<r_edges[j+1])
            dfb=df[boo]
            r_values=dfb.r.values
            drdt_values=dfb.drdt.values
            #compute mean values in bin
            r=np.mean(r_values)
            drdt=np.mean(drdt_values)
            # compute 95% CI for mean
            Delta_r,p_r=bootstrap_95CI_Delta_mean(r_values,
                                                 num_samples=num_samples)
            Delta_drdt,p_drdt=bootstrap_95CI_Delta_mean(drdt_values,
                                                 num_samples=num_samples)
            #append results to list
            r_lst.append(r)
            drdt_lst.append(drdt)
            Delta_r_lst.append(Delta_r)
            Delta_drdt_lst.append(Delta_drdt)
            p_r_lst.append(p_r)
            p_drdt_lst.append(p_drdt)
            count_lst.append(numobs)
    r_values=np.array(r_lst)
    drdt_values=np.array(drdt_lst)
    Delta_r_values=np.array(Delta_r_lst)
    Delta_drdt_values=np.array(Delta_drdt_lst)
    p_r_values=np.array(p_r_lst)
    p_drdt_values=np.array(p_drdt_lst)
    count_values=np.array(count_lst)
    dict_out={
        'r':r_values,
        'drdt':drdt_values,
        'Delta_r':Delta_r_values,
        'Delta_drdt':Delta_drdt_values,
        'p_r':p_r_values,
        'p_drdt':p_drdt_values,
        'counts':count_values
    }
    return dict_out

# def save_mean_radial_velocities(input_fn,t_col='tdeath',output_fn=None,bins='auto',flip_time=False,
#     remove_before_jump=True,minR_thresh=0.25,max_speed_thresh=0.4,**kwargs):
def save_mean_radial_velocities(input_fn,remove_before_jump,minR_thresh,max_speed_thresh,t_col='tdeath',output_fn=None,bins='auto',flip_time=False,**kwargs):
    if output_fn is None:
        output_fn=input_fn.replace('.csv',f'_mean_radial_velocities_bins_{bins}_minRthresh_{minR_thresh}_maxspeedthresh_{max_speed_thresh}.csv')

    df=pd.read_csv(input_fn)
    dict_out=comp_mean_radial_velocities(df=df,input_fn=input_fn,t_col=t_col,bins=bins,
        flip_time=flip_time,minR_thresh=minR_thresh,
        remove_before_jump=remove_before_jump,
        max_speed_thresh=max_speed_thresh,**kwargs)
    df_drdt=pd.DataFrame(dict_out)
    df_drdt.to_csv(output_fn,index=False)
    return os.path.abspath(output_fn)

#########################################################
# Methods not conditioned on data from topological events
#########################################################
def get_ranges_to_others(xy_self,xy_others, pid_others, distance_L2_pbc,dist_thresh):
    pid_lst = []
    R_lst=[]
    xy_self=xy_self[0]
    for j,pid_other in enumerate(pid_others):
        dist = distance_L2_pbc ( xy_others[j], xy_self)
        if dist<dist_thresh:
            pid_lst.append (  int(pid_other) )
            R_lst.append (  float(dist) )
    return np.array(R_lst), np.array(pid_lst)

def comp_radial_velocities_between_frames(df,frame,frame_nxt,distance_L2_pbc,dist_thresh,pid_col,
    DS,DT,pid=None,use_forward_R=False):
    #get data in the current frame
    dff=df[df.frame==frame]
    xy_values=dff[['x','y']].values
    pid_values=dff[pid_col].values

    if pid is None:
        #(optional) randomly pick 1 particle from the current frame
        pid=random.choice(pid_values)

    #compute the range to each tip in the current frame
    xy_self=xy_values[pid_values==pid]
    boo=pid_values!=pid
    pid_others=pid_values[boo]
    xy_others=xy_values[boo]
    # pid_in_range=get_tips_in_range(xy_self,xy_others, pid_others, distance_L2_pbc, dist_thresh=dist_thresh)
    R_lst, pid_lst=get_ranges_to_others(xy_self,xy_others, pid_others, distance_L2_pbc,dist_thresh)

    #get data in the next frame
    dff=df[df.frame==frame_nxt]
    xy_values=dff[['x','y']].values
    pid_values=dff[pid_col].values

    R_out_lst=[]
    dRdt_out_lst=[]
    #if the randomly selected particle is still present
    if (pid==pid_values).any():
        xy_self=xy_values[pid_values==pid]
        #for each pid_other in pid_lst
        for j,pid_other in enumerate(pid_lst):
            #if the other particle is still present
            boo=pid_other==pid_values
            if boo.any():
                #get the next location of that other particle
                xy_other=xy_values[boo]
                #compute the range between those tips in the next frame
                R_nxt=distance_L2_pbc ( xy_other[0], xy_self[0])
                R_prv=R_lst[j]
                #compute dRdt and average R for those tips
                dRdt_out=DS*(R_nxt-R_prv)/DT
                #optionally, measure range from previous time point only
                if use_forward_R:
                    R_out=R_prv
                else:
                    R_out=DS*0.5*(R_nxt+R_prv)

                #append results to list
                R_out_lst.append(R_out)
                dRdt_out_lst.append(dRdt_out)

                #TODO(later, optionally): mark rows that have been visited as visited
    return R_out_lst, dRdt_out_lst

def comp_neighboring_radial_velocities_between_frames(df,frame,num_frames_between,distance_L2_pbc,dist_thresh,DS,DT,pid_col='particle',**kwargs):
    '''Computes radial velocities between frames, frame and frame_nxt, for particles that are nearest to eachother.  Filters values when minimum R is larger than Rthresh
    Double counting is removed using a method that rounds to 12 digits because of floating point arithmetic error.  14 seemed to work, but 12 is satisfies my paranoia more...
    Example Usage:
    R_values, dRdt_values = comp_neighboring_radial_velocities_between_frames(df,frame=frame,frame_nxt=frame+num_frames_between)
    '''
    frame_values=np.array(sorted(set(df.frame.values)))
    #get data in the current frame
    dff=df[df.frame==frame]
    xy_values=dff[['x','y']].values
    pid_values=dff[pid_col].values
    R_lst=[];dRdt_lst=[]
    for pid in pid_values:
        _R_lst,_dRdt_lst = comp_radial_velocities_between_frames(df,frame=frame,frame_nxt=frame+num_frames_between,pid=pid,DS=DS,DT=DT,distance_L2_pbc=distance_L2_pbc,dist_thresh=dist_thresh,pid_col=pid_col)
        if len(_R_lst)>0:
            Rmin=np.min(_R_lst)
            arg=np.argmin(_R_lst)
            dRdtmin=_dRdt_lst[arg]
            R_lst.append(Rmin)
            dRdt_lst.append(dRdtmin)
    #remove duplicates
    d=pd.DataFrame()
    d['R']=R_lst
    d['dRdt']=dRdt_lst
    d=d.round(12).drop_duplicates()
    R_values=d['R'].values
    dRdt_values=d['dRdt'].values
    return R_values, dRdt_values

def comp_all_radial_velocities_between_frames(df,frame,frame_nxt,distance_L2_pbc,Rthresh=9999.):
    '''Computes all radial velocities between frames, frame and frame_nxt.  Filters values when minimum R is larger than Rthresh
    TODO(later): remove the frequent double counting of observations...
    I don't currently expect this function to be useful to me...
    Example Usage:
    R_lst, dRdt_lst = comp_all_radial_velocities_between_frames(df,frame=frame,frame_nxt=frame+num_frames_between,Rthresh=0.8)
    '''
    #simplest way to compute the smallest R:
    #compute R and dRdt for each choice of pid_self and choose the smallest...
    #in that case, I might as well just choose all of them...
    #but then the resulting data would be huge...
    #use Rthresh to filter the data that isn't near anything and thus contains no information.
    frame_values=np.array(sorted(set(df.frame.values)))
    #get data in the current frame
    dff=df[df.frame==frame]
    xy_values=dff[['x','y']].values
    pid_values=dff[pid_col].values
    R_lst=[];dRdt_lst=[]
    for pid in pid_values:
        _R_lst,_dRdt_lst = comp_radial_velocities_between_frames(df,frame=frame,frame_nxt=frame+num_frames_between,pid=pid)
        Rmin=np.min(_R_lst)
        if Rmin<=Rthresh:
            R_lst.extend(_R_lst)
            dRdt_lst.extend(_dRdt_lst)
    return R_lst, dRdt_lst
