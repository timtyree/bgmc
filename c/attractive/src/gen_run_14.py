#run_14.py
import numpy as np
niter=1500 #trials per worker
num_trials_per_setting=1

L=10 #cm per domain
force_code=2 #2 :: QED2, 4 :: QED2 + constant repulsion
dt=1e-5
Dt=1e-5
Nmax=100  #Caution: might not be actually connected to anything...

#model parameters
D_values=np.array([0.3,0.5,0.7])# cm^2/s #5
x0_values=np.array([0])#1.5,3.,5.,10.,100.,10000.]) #10
r_values=np.array([0.025,0.1,0.2,0.3,0.4,0.5,1.])#,0.2,0.3,0.4,0.5])# cm
kappa_values = np.array([500,1000,1500]) #Hz
varkappa_values = np.array([0,1,5,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150]) #cm^2/s

#simulation parameters
set_second_values=np.array([0])
reflect_values=np.array([0])
no_repulsion_values=np.array([0])#1 means no repulsion is true
no_attraction_values=np.array([0])
neighbor_values=np.array([0,1])

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
                                            print(f"{r} {D} {L} {kappa:.5f} {varkappa} {x0} {Dt} {dt} {Nmax} {niter} {reflect} {set_second} {no_repulsion} {no_attraction} {neighbor} {force_code}")
# print(count) #~2k jobs
