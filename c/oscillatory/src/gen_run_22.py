#run_21.py - repeating last dense grid search with a=0 and more D resolution
# --> use number of iterations my standard 1500, and the job should finish before the 10 hour mark (i.e. by morning!)
import numpy as np
niter=1500 #trials per worker
num_trials_per_setting=1

L=10 #cm per domain
force_code=2 #2 :: QED2, 4 :: QED2 + constant repulsion
# DONE: double check still performing reasonably well for LR
# TODO: see whether the FK params are reasonably fast running
# TODO: consider T,T/2 in run_22 over neighbors only
# DONE: let T go from 0.05 to 0.56, hitting values like
#DONE: include parameter versions for lengh units divided by 4, suppose we use only 500 trials instead of 1500 per trials...
#DONE: consider also trying expected a and D divided by 4 (because of the L=10 from L=5 conversion)
#DONE: consider also trying expected r divided by 2 (because of the L=10 from L=5 conversion)

x0_values=np.array([0.05,0.06,0.1, 0.12]) #period in seconds
# x0_values=np.array([0.100, 0.120 , 0.5, 0.06]) #period in seconds
dt=1e-5
Dt=1e-5
Nmax=100  #Caution: might not be actually connected to anything...
#pessimistic parameter settings with <10 hours runtime
# 0.05  0.4      10  100   .8       0.1  1e-05 1e-05 20    1500   1234 0       0          0            0             1        2
# #r    D        L kappa  varkappa  x0   Dt    dt    Nmax  niter seed reflect set_second no_repulsion no_attraction neighbor force_code

#model parameters
# D_values=np.linspace(0.7,2,14)# cm^2/s #14
# D_values=np.arange(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.4,1.6,1.8,2.0])
# r_values=np.array([0.3,0.35,.4,0.41,.45,0.5])# cm
D_values=np.array([1.767951,0.8020765])#np.arange(0.1,8.1,0.1)
D_values=np.concatenate([D_values,D_values/4])
r_values=np.array([0.05,0.06,.1,.12])# cm
r_values=np.concatenate([r_values,r_values/2])
kappa_values = np.array([100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500])#,1000,1500]) #Hz
varkappa_values = np.array([3.535902,1.604153])#1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,60,70,80,90,100,110]) #cm^2/s #11
varkappa_values=np.concatenate([varkappa_values,varkappa_values/4])

#factors to multiply functionally computed parameters
# f_values=np.array([0.5,0.9,1.,1.1,1.5]) #5
# f_values=np.array([0.5,0.8,0.9,1.,1.1,1.2]) #7

#simulation parameters
set_second_values=np.array([0])
reflect_values=np.array([0])
no_repulsion_values=np.array([0])#1 means no repulsion is true
no_attraction_values=np.array([0])
neighbor_values=np.array([1])

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
                                            print(f"{r:.5f} {D:.5f} {L} {kappa:.5f} {varkappa:.5f} {x0} {Dt} {dt} {Nmax} {niter} {reflect} {set_second} {no_repulsion} {no_attraction} {neighbor} {force_code}")
# print(count)#7680
# print((np.min(varkappa_values),np.min(D_values),np.min(r_values)))#(0.40103825, 0.200519125, 0.025)
