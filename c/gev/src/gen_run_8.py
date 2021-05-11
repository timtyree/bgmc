import numpy as np
#mle fit to lr model: source: /home/timothytyree/Documents/GitHub/care/notebooks/Data/initial-conditions-lr-600x600/param_qu_tmax_30/Log/ic600x600.0.1_traj_sr_1200_mem_0.csv
shape=-0.338#74#-0.3383994872096594;
location=0.186#2#0.18616306715070396; #//cm
scale=0.139#86#5657625455955; #//cm

niter=250 #trials per worker
r_values=np.array([location])#0.1,0.2,0.3,0.4,0.5,1.0])#cm
D_values=np.array([0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0])#cm^2/s
# A_values=np.array([20.25,25,39,50,56.25,100,156.25,189])[::-1]#cm^2
A_values=np.array([25,50,100,189])[::-1]#cm^2
L_values=np.sqrt(A_values)#cm
kappa_values=np.array([500.])#1/s'
shape_values=np.array([shape,0.,-shape])#-.5,shape,0.,-shape])

beta_values=np.array([0.01,0.1,scale,1.])#cm
num_trials_per_setting=6
reflect_values=np.array([0])
set_second_values=np.array([0])
#iterate over settings, scheduling the longest jobs first
count=0
for set_second in set_second_values:
    for r in r_values:
        for D in D_values:
            for L in L_values:
                for kappa in kappa_values:
                    for beta in beta_values:
                        for reflect in reflect_values:
                            for shape in shape_values:
                                num_trials=0
                                while num_trials<num_trials_per_setting:
                                    num_trials+=1
                                    count=count+1
                                    print(f"{r} {D} {L} {kappa} {beta} {shape} {niter} {reflect} {set_second}")
# print(f"job count is {count}")
