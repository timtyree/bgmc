#run_15.py
import numpy as np
niter=1500 #trials per worker
num_trials_per_setting=1

L=10 #cm per domain
force_code=2 #2 :: QED2, 4 :: QED2 + constant repulsion
x0_values=np.array([0])#1.5,3.,5.,10.,100.,10000.]) #10 #doesn't matter for force_code=2

dt=1e-5
Dt=1e-5
Nmax=100  #Caution: might not be actually connected to anything...

#model parameters
D_values=np.linspace(0.7,2,14)# cm^2/s #14
r_values=np.array([0.05,0.1,0.15,0.2,0.3,0.4,0.5])#,0.2,0.3,0.4,0.5])# cm
kappa_values = np.array([250,500])#,1000,1500]) #Hz
varkappa_values = np.array([0,1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,60,70,80,90,100,110]) #cm^2/s #11

#factors to multiply functionally computed parameters
# f_values=np.array([0.5,0.9,1.,1.1,1.5]) #5
# f_values=np.array([0.5,0.8,0.9,1.,1.1,1.2]) #7

#simulation parameters
set_second_values=np.array([0])
reflect_values=np.array([0,1])
no_repulsion_values=np.array([0])#1 means no repulsion is true
no_attraction_values=np.array([0])
neighbor_values=np.array([0])

#iterate over settings, scheduling the longest jobs first
count=0
for set_second in set_second_values:
    for reflect in reflect_values:
        for no_repulsion in no_repulsion_values:
            for no_attraction in no_attraction_values:
                for neighbor in neighbor_values:
                    for r in r_values:
                        for kappa in kappa_values:
                            for varkappa in varkappa_values:
                                for D in D_values:
                                    for x0 in x0_values:
                                        num_trials=0
                                        while num_trials<num_trials_per_setting:
                                            num_trials+=1
                                            count=count+1
                                            print(f"{np.around(r,2)} {np.around(D,1)} {L} {kappa} {varkappa} {x0} {Dt} {dt} {Nmax} {niter} {reflect} {set_second} {no_repulsion} {no_attraction} {neighbor} {force_code}")
# print(count)#9800
