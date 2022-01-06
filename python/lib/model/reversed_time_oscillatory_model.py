import numpy as np, time,matplotlib.pyplot as plt, pandas as pd
from scipy.signal import savgol_filter
from ..lib_care.measure.bootstrap import bin_and_bootstrap_xy_values_parallel
from ..measure.compute_slope import *
# from ..viewer.bluf.plot_func import print_dict
def print_dict(input_dict,*argv):
    for key in input_dict.keys():
        print(f"{key}={input_dict[key]}")
    # args=sorted(argv)
    # if len(args)>0:
    #     print(str_btwn)
    # type_dict=type(dict())
    for arg in sorted(argv):
        print(f'\n#{arg}')
        obj=input_dict[arg]
        if type(obj) is type(dict()):
            print_dict (obj)

        else:
            print(arg)

def gener_positions_oscillatory_reversed(
    num_pairs=150, #number of independent pairs of particles
    a=8.5, #cm^2/s known attraction coefficient
    D=0.3, #cm^2/s known diffusion coefficient
    Dt=1e-5, #s
    initial_phase_orientation=0.,#radians
    period_of_oscillation=90.,#ms
    rstart=1e-4,
    rend=4, #cm
    tmax=1,
    printing=False,print_every=50000,
    mode='oscillatory',
    use_early_stopping=True,
    seed=42,
    use_testing=False,
    **kwargs
    ):
    '''
    Example Usage:
    dict_out,positions_out=gener_positions_oscillatory_reversed(a=a,D=D,initial_phase_orientation=0.,printing=True)
    '''
    np.random.seed(seed)
    dont_break=not use_testing
    #initialize particles locations as being at the same locations
    t=0
    x1=0
    x2=np.sqrt(rstart)
    y1=0
    y2=np.sqrt(rstart)
    zero_values=np.zeros(num_pairs)

    x1_values=zero_values.copy()+x1
    x2_values=zero_values.copy()+x2
    y1_values=zero_values.copy()+y1
    y2_values=zero_values.copy()+y2

    stepscale = np.sqrt(2 * D * Dt)
    impulse_prefactor = a * Dt

    #tmax=1#10#0.1#1 #seconds
    num_steps=np.int64(np.around(tmax/Dt))

    position_array=np.zeros(shape=(num_steps,4,num_pairs))+np.nan
    mean_array=np.zeros(shape=(num_steps,3))
    std_array=np.zeros(shape=(num_steps,3))

    #add support for still_running
    boo_still_running=zero_values==zero_values

    #compute the distance between each pair of particles
    dx_values=(x2_values-x1_values)
    dy_values=(y2_values-y1_values)
    Rsq_values=dx_values*dx_values+dy_values*dy_values
    omega=((1e-3*period_of_oscillation/(2*np.pi))**-1)
    ##enforces the alignment boundary condition. smart, but might be messing up the oscillations
    time_constant=initial_phase_orientation/omega
    #time_constant=0.
    if printing:
        print(f"running simulation for {num_steps} steps...")
    start=time.time()
    step_num=0
    while dont_break and (step_num < num_steps):
        t=step_num*Dt + time_constant
        #compute the attractive step between all pairs
        f_values=impulse_prefactor/Rsq_values
        F1x=f_values*dx_values
        F1y=f_values*dy_values
        if mode=='oscillatory':
            F1x*=np.cos(omega*t)
            F1y*=np.cos(omega*t)

        #compute the diffusive step between all pairs
        dxW1_values=stepscale*np.random.normal(size=num_pairs)
        dxW2_values=stepscale*np.random.normal(size=num_pairs)
        dyW1_values=stepscale*np.random.normal(size=num_pairs)
        dyW2_values=stepscale*np.random.normal(size=num_pairs)

        #the mean distance between all pairs of particles
        R_values=np.sqrt(Rsq_values)
        mean_R=np.mean(R_values)
        std_R=np.std(R_values)

        #the mean magnitude of the diffusive step
        diffusive_step_values=0.5*np.sqrt(dxW1_values**2+dyW1_values**2)+0.5*np.sqrt(dxW2_values**2+dyW2_values**2)
        mean_diffusive_step=np.mean(diffusive_step_values)
        std_diffusive_step=np.std(diffusive_step_values)

        #the mean magnitude of the attractive step
        attractive_step_values=np.sqrt(F1x**2+F1y**2)
        mean_attractive_step=np.mean(attractive_step_values)
        std_attractive_step=np.std(attractive_step_values)
        if printing:
            if (step_num+1) % print_every == 0:
                relative_percent=100*mean_diffusive_step/mean_attractive_step
                print(f"simulation {100*(step_num+1)/num_steps:.0f}% completed: R={mean_R:.4f}+/-{1.96*std_R:.4f}, diffusion/attraction is {relative_percent:.2f}%")
                # print(f"the mean range is {mean_R:.4f} cm")
                # print(f"the mean diffusive step was {100*mean_diffusive_step/mean_attractive_step:.2f}% larger than the mean attractive step")

        #compute the net change in position (with signs chosed s.t. repulsive at zero phase)
#         x1step_values=F1x+dxW1_values
#         y1step_values=F1y+dyW1_values
#         x2step_values=-F1x+dxW2_values
#         y2step_values=-F1y+dyW2_values
        x1step_values=-F1x+dxW1_values
        y1step_values=-F1y+dyW1_values
        x2step_values=F1x+dxW2_values
        y2step_values=F1y+dyW2_values

        #identify any particles that didn't get within the threshold distance
        #compute the distance between each pair of particles
        dx_values=(x2_values-x1_values)
        dy_values=(y2_values-y1_values)
        Rsq_values=dx_values**2+dy_values**2

        #update particle locations if they are still running
        x1_values[boo_still_running]=x1_values[boo_still_running]+x1step_values[boo_still_running]
        y1_values[boo_still_running]=y1_values[boo_still_running]+y1step_values[boo_still_running]
        x2_values[boo_still_running]=x2_values[boo_still_running]+x2step_values[boo_still_running]
        y2_values[boo_still_running]=y2_values[boo_still_running]+y2step_values[boo_still_running]
        #DONE: verified the mean distance between particles got smaller
        # if (step_count+1) % save_every == 0:
        #save particle locations to a numpy array with the correct number of positions
        # x1,y1,x2,y2
        position_array[step_num,0,boo_still_running]=x1_values[boo_still_running]
        position_array[step_num,1,boo_still_running]=y1_values[boo_still_running]
        position_array[step_num,2,boo_still_running]=x2_values[boo_still_running]
        position_array[step_num,3,boo_still_running]=y2_values[boo_still_running]
        mean_array[step_num,0]=mean_R
        mean_array[step_num,1]=mean_diffusive_step
        mean_array[step_num,2]=mean_attractive_step
        #save results for quick plotting
        std_array[step_num,0]=std_R
        std_array[step_num,1]=std_diffusive_step
        std_array[step_num,2]=std_attractive_step

    #         #identify any particles that didn't get within the threshold distance
    #         #compute the distance between each pair of particles
    #         dx_values=(x2_values-x1_values)
    #         dy_values=(y2_values-y1_values)
    #         Rsq_values=dx_values*dx_values+dy_values*dy_values
        R_values=np.sqrt(Rsq_values)
        boo_still_running=boo_still_running&(R_values<rend)

        step_num+=1
        if use_early_stopping and not boo_still_running.any():
            dont_break=False
    if printing:
        print(f"simulation complete!\nTotal run time: {time.time()-start:.4f} seconds")
        print(f"the number of particles that didn't finished is {sum(boo_still_running)} out of {boo_still_running.shape[0]}.")

    dict_out={
        #         "Gamma_max":np.float32(Gamma_max),
        #         "Gamma_values":Gamma_values.astype('float32'),
        "Rsq_values":Rsq_values.astype('float32'),
        "mean_array":mean_array.astype('float32'),
        "std_array":std_array.astype('float32')
    }
    if printing:
        print(*dict_out)
        #print_dict(dict_out)
    return dict_out,position_array#positions_out

##########################################
# local viewer
##########################################
def visualize_model_oscillatory_reversed(ax=None,
    a=1.6,#8.5,
    D=0.6,#0.3,
    initial_phase_orientation=np.pi,#0#np.pi/2,#-np.pi/2,
    period_of_oscillation=45.,
    num_pairs=1000,
    rstart=1e-4,#1.5,
    Dt=1e-5,
    xmin=0,
    xmax=0.1,
    ymin=0,
    ymax=0.6,
    alpha=0.7,
    show_inputted_a=True,show_title=True,show_legend=True,use_xylim=True,
    show_label_black_dotted=False,
    printing=True,
    plotting=True,c='C3',label=r"Simulation",**kwargs):
    """generate MSR using the time-reversed oscillatory model. estimated run time is 15 seconds for 100 statistically independent trials.
    Example Usage:
    dict_fit=visualize_model_oscillatory_reversed(a=1.6,D=0.3,c='C0',label='Fenton-Karma')
    dict_fit=visualize_model_oscillatory_reversed(a=8.5,D=0.6,c='C1',label='Luo-Rudy')
    plt.show()
    """
    dict_out,position_array = gener_positions_oscillatory_reversed(
                a=a, D=D, printing=False,num_pairs=num_pairs,period_of_oscillation=period_of_oscillation,initial_phase_orientation=initial_phase_orientation,**kwargs)
    positions_out=position_array
    if printing:
        print(*dict_out)
        print(f"positions_out.shape={positions_out.shape}")

    title=f"a={a:.1f}, D={D:.1f}, T={period_of_oscillation:.1f}, "+r"$\phi_f$"+f"={initial_phase_orientation:.4f}, "+r"R$_f$"+f"={rstart:.0e}, "+r" N$_{trials}$"+f"={num_pairs}\n"

    #compute the distance between each pair of particles after aligning by annihilation (unshifted)
    x1_values=positions_out[:,0]
    y1_values=positions_out[:,1]
    x2_values=positions_out[:,2]
    y2_values=positions_out[:,3]
    dx_values=(x2_values-x1_values)
    dy_values=(y2_values-y1_values)
    Rsq_values=dx_values**2+dy_values**2
    #compute the ensemble averaged values
    MSR_values=np.mean(Rsq_values,axis=1)
    aligned_coordinates_values=np.mean(positions_out,axis=-1)
    # maxt=Dt*MSR_values.shape[0]
    t_values=np.arange(MSR_values.shape[0])*Dt
    boo=~(np.isnan(t_values)|np.isnan(MSR_values))
    dict_fit=compute_95CI_ols(t_values[boo],MSR_values[boo])
    if printing:
        print_dict(dict_fit)
        print(f"num_samples={positions_out.shape[-1]}")
        print(f"num_timepoints={t_values.shape[0]}")
        print(f"ahat = {dict_fit['m']/4:.4f}+/-{dict_fit['Delta_m']/4:.4f}")

    if plotting:
        if ax is None:
            ax=plt.gca()
        xv=np.linspace(xmin,xmax,100)
        if show_inputted_a:
            if show_label_black_dotted:
                ax.plot(xv,4*a*xv,'k--',label=r'$4a(t_f-t)$')
            else:
                ax.plot(xv,4*a*xv,'k--')#,label=r'$4a(t_f-t)$')
        if use_xylim:
            ax.set_xlim([xmin,xmax])
            ax.set_ylim([ymin,ymax])
        ax.plot(t_values,MSR_values,c=c,label=label,alpha=alpha)
        if show_title:
            plt.title(title,fontsize=16)
        if show_legend:
            plt.legend(fontsize=16)
        #plt.plot(t_values,t_values*0.,'--',c='gray',alpha=0.5)
    #record
    dict_fit['title']=title
    dict_fit['tdeath']=t_values
    dict_fit['MSR']=MSR_values
    return dict_fit
