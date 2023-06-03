from lib.pylib import *
import numpy as np
# from numpy.random import MT19937
# from numpy.random import RandomState, SeedSequence

force_code=2
N=150
# N=16
# Nfinal=8
Nfinal=0
# Nfinal=2
# niter=200
# niter=500
niter=15000
#HERETIM

L=5
# L=10
seed=42
np.random.seed(seed)
# rs = RandomState(MT19937(SeedSequence(seed)))
t=0
#define model parameters
# # #FK
# r=0.7 #cm
# varkappa=1.552 #cm^2/s
# D=0.115 #cm^2/s
# # save_every=25
# save_every=5
# # save_every=1 #45 min

#LR
# r=0.5 #cm
varkappa=9.3 #cm^2/s
D=0.42 #cm^2/s

# save_every=5
# # save_every=1
# save_every=1000000000
# # varkappa=0 #no attraction

# kappa=1e5 #Hz
# kappa=1e3 #Hz
# kappa=50
# r=0.135;kappa=60
# r=0.5;kappa=20
r=0.3;kappa=20
# kappa=100;
# kappa=100; r=0.125 #<<< WJ says this worked well for LR

Dt=1e-5;dt=1e-5
# tmax=500
tmax=10000 #s

#for forces
x0=5
# no_repulsion=1
# no_attraction=1
no_repulsion=0
no_attraction=0
seed=123456789
#skipping reflect,set_second, and neighbor functionality

#define constants
alpha=1. #ballistic
alpha=2. #diffusive
# alpha=1.5 #levy-esque
message=f'with {alpha=}'

stepscale=np.sqrt(2*D*Dt) #diffusive
# stepscale=(2*D*Dt)**(1/alpha)
probreact=kappa*dt
T_net=0;count_net=0
np.random.seed(seed)
dist_cutoff=1e-2
iter_per_movestep = round(Dt/dt)
impulse_prefactor= varkappa * Dt
tiarray=np.zeros(N)
tfarray=np.zeros(N)
epsilon=5e-2  #reactions happen
#for csv output
# data_folder=f"{nb_dir}/data/local_results/collision_test"
# data_folder=f"{nb_dir}/data/local_results/levy_test"
# if not os.path.exists(data_folder):
#     os.mkdir(data_folder)
# data_folder=data_folder+"/Log"
# if not os.path.exists(data_folder):
#     os.mkdir(data_folder)
# data_fn=f"pbc_seed_{seed}_fc_{force_code}_r_{r}_D_{D}_L_{L}_kappa_{kappa}_varkappa_{varkappa}_alpha_{alpha}_log.csv"

# initialize record to zero
Tsum_array=np.zeros(N+1)
Tcount_array=np.zeros(N+1)


# recording_locations=True
# recording_snapshots=True
recording_locations=False
recording_snapshots=False
print("running simulation...");
for q in range(niter):
    T=0.
    frameno=0
    step=0
    # Time=0.
    #initialize positions
    # x_values=rs.uniform(size=N)*L
    # y_values=rs.uniform(size=N)*L
    x_values=np.random.uniform(size=N)*L
    y_values=np.random.uniform(size=N)*L
    # t=-Dt
    exit_code=-1;
    # T=-9999.

    # x=x_values.copy()
    # y=y_values.copy()
    x_old=x_values.copy()
    y_old=y_values.copy()
    x_new=x_values.copy()
    y_new=y_values.copy()
    zeros=np.zeros_like(x_values)
    zerosint=np.zeros_like(x_values).astype('int')
    still_running=zerosint==zerosint
    caught=zerosint.copy()-9999#!=zerosint
    # //start set_second kernel
    # //end set_second kernel
    #make still_running into still_running_values
    # dict_out_lst=[]
    # while(still_running.any()):
    nparticles = still_running.sum()
    Fx_net=zeros.copy()
    Fy_net=zeros.copy()
    while(still_running.sum()>Nfinal):
        min_dist_old=zeros+9999999
        i_neighbor=zerosint-1
        x_old=x_new
        y_old=y_new
        t=t+Dt;
        # reset the net forces
        Fx_net*=0.
        Fy_net*=0.

        #sum_each_force_kernel
        for i in range(N):
            if(still_running[i]):
                for j in range(i+1,N):
                    if(still_running[j]):
                        #compute displacement vector with pbc
                        dx = subtract_pbc_1d(x_old[j],x_old[i],L);
                        dy = subtract_pbc_1d(y_old[j],y_old[i],L);
                        dist2=dx*dx+dy*dy;
                        if (dist2<1e-8):
                            dist2=float(1e-8)
                        dist = np.sqrt(dist2)
                        #compute displacement due to drift
                        impulse_factor=0.
                        if (force_code==1):
                          #spring
                          impulse_factor=impulse_prefactor*(dist-x0)/dist;
                        if (force_code==2):
                          #QED2: force ~ inverse power law
                          impulse_factor=impulse_prefactor/dist2;
                        if (force_code==3):
                          #QED3: force ~ inverse square power law
                          impulse_factor=impulse_prefactor/dist2/dist;
                        #set impulse_factor to zero if it is explicitly forbidden by the user input
                        if ((no_attraction==1) & (impulse_factor>0)):
                            impulse_factor=0.
                        if ((no_repulsion==1) & (impulse_factor<0)):
                            impulse_factor=0.
                        #sum Fx_net, Fy_net according to a symplectic (momentum conserving) integrator
                        Fx_net[i]=Fx_net[i]+dx*impulse_factor;
                        Fy_net[i]=Fy_net[i]+dy*impulse_factor;
                        Fx_net[j]=Fx_net[j]-dx*impulse_factor;
                        Fy_net[j]=Fy_net[j]-dy*impulse_factor
                        #determine if they are closer than epsilon
                        if dist<epsilon:
                            #remove if they are
                            still_running[i]=False
                            still_running[j]=False
                            #uncatch caught particles
                            uncatch_set=set()
                            if caught[i]>=0:
                                uncatch_set.update([caught[i]])
                                if caught[caught[i]]>=0:
                                    uncatch_set.update([caught[caught[i]]])
                            if caught[j]>=0:
                                uncatch_set.update([caught[j]])
                                if caught[caught[j]]>=0:
                                    uncatch_set.update([caught[caught[j]]])
                            if len(uncatch_set)>0:
                                for k in uncatch_set:
                                    caught[k]=-9999
                            # compute time since last reaction
                            T_prev=T;
                            T=step*dt;
                            # record
                            Tsum_array[nparticles] = Tsum_array[nparticles] + T - T_prev;
                            Tcount_array[nparticles] = Tcount_array[nparticles] + 1;
                            nparticles=nparticles-2;
        #compute the one_step given the net force, F_net
        for i in range(N):
            if(still_running[i]):
                if caught[i]<0:
                    dxt=Fx_net[i];
                    dyt=Fy_net[i];
                    # compute displacement due to levy flight
                    dxW,dyW = stepscale*levyRandom2D(alpha)
                    # next spatial position, time integrating by a duration, Dt. enforce PBC.
                    x_new[i]=periodic(x_old[i]+dxW+dxt,L);
                    y_new[i]=periodic(y_old[i]+dyW+dyt,L);
                else:
                    j=caught[i]
                    ti=tiarray[i]
                    tf=tfarray[i]
                    #compute displacement vector with pbc
                    dx = subtract_pbc_1d(x_old[j],x_old[i],L)
                    dy = subtract_pbc_1d(y_old[j],y_old[i],L)
                    xl = dx - (x_old[j]-x_old[i])
                    yl = dy - (y_old[j]-y_old[i])
                    #compute average location
                    xavg = x_old[i] + 0.5*dx
                    yavg = y_old[i] + 0.5*dy
                    #compute frac to interpolate by
                    frac = (t-ti)/(tf-ti)
                    frac = np.min((1,frac))
                    x_new[i] = periodic(x_old[i]*(1-frac) + (xavg+xl)*frac,L)
                    y_new[i] = periodic(y_old[i]*(1-frac) + (yavg+yl)*frac,L)
        #reaction_kernel
        for i in range(N):
            if(still_running[i]&(caught[i]<0)):
                # // each i,j pair is reached once per call to kernel_measure
                for j in range(i+1,N):
                    if(still_running[j]&(caught[j]<0)):
                        # // compute distance between particles that are still running
                        dist=dist_pbc(x_new[i],y_new[i],x_new[j],y_new[j],L);
                        in_range=dist<r;
                        # // in_range=true;//uncomment for smeared method
                        # // if two particles are in range
                        if(in_range):
                            # // determine whether those two particles react via the simple method
                            reacts=probreact>uniformRandom();
                            # // determine whether those two particles react via the smeared method
                            # // sig=sigmoid(dist, r, beta);
                            # // reacts=probreact*sig>uniformRandom();
                            if(reacts):
                                exit_code=1;
                                # T=t;
    #                             still_running[i]=False;
    #                             still_running[j]=False;
                                #uncatch any previous catches
                                if caught[i]>=0: caught[caught[i]]=-9999
                                if caught[j]>=0: caught[caught[j]]=-9999
                                #catch these two
                                caught[i]=j;
                                caught[j]=i;
                                #determine deltat
                                deltat = dist**2/(4*(varkappa+2*D))
                                #determine ti,tf
                                tiarray[i]=t
                                tfarray[i]=t+deltat
                                tiarray[j]=t
                                tfarray[j]=t+deltat
#     if step%save_every==0:
#         x_plot=x_new[still_running]
#         y_plot=y_new[still_running]
#         c_plot = np.array(['gray']*y_plot.shape[0])
#         caugh=caught[still_running]
#         for i in range(y_plot.shape[0]):
#             if caugh[i]>=0:
#                 c_plot[i]='r'
#         if recording_snapshots:
#             #save result as png
#             SaveScatterPlotSnapshot(x_plot,y_plot,t,
#                                     c=c_plot,
#                                     width=L,height=L,
#                             frameno=frameno,save_folder=save_folder,
#                             annotating=annotating,message=message)
# #             print(f"- saved pic at {frameno=}")
#         if (recording_locations)&(x_plot.shape[0]>0):
#             pid_values = np.arange(x_values.shape[0])[still_running]
#             #append particle locations to log, dict_out_lst
#             dict_out=format_particles(frameno,t,x_plot,y_plot,pid_values=pid_values)
#             dict_out_lst.append(dict_out)
#         frameno+=1

        #shut simulation down if it's taking too long...
        if (t>tmax):
            for i in range(N):
                still_running[i]=False;
                exit_code=-99;

        step+=1
    #end while running

#record this trial
if (exit_code>0):
    if (T>0.):
        T_net=T_net+T;
        count_net=count_net+1;

print(f"simulation complete!")
outstr1=''
outstr2=''
for n in list(reversed(range(Nfinal+2,N+1,2))):
    Tc=Tcount_array[n]
    Ts=Tsum_array[n]
    if Tc==0.:
        Tavg=np.nan
    else:
        Tavg=Ts/Tc

    # Tavg=Tc
#heretim


    outstr1+=f"{n},"
    outstr2+=f"{Tavg},"
print(outstr1)
print(outstr2)
# print(Tsum_array)
# print(Tcount_array)
