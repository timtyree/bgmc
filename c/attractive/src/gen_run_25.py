#run_20.py - repeating last dense grid search with a=0 and more D resolution
import numpy as np
niter=1500 #trials per worker
num_trials_per_setting=1
# niter=150 #trials per worker
# num_trials_per_setting=10

# L=10 #cm per domain
L=5 #cm per domain
force_code=2 #2 :: QED2, 4 :: QED2 + constant repulsion
x0_values=np.array([0])#1.5,3.,5.,10.,100.,10000.]) #10 #doesn't matter for force_code=2

dt=1e-5
Dt=1e-5
Nmax=100  #Warning: not be actually connected to anything. goto return_Coltimes.sh to modify Nmin,Nmax.

#model parameters
# D_values=np.linspace(0.7,2,14)# cm^2/s #14
# D_values=np.arange(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.4,1.6,1.8,2.0])
varkappa_values =np.array([1.553,9.969])
D_values=np.array([.114,.09])
#run 25
r_values = np.arange(0.01,0.5,0.01)   #cm
kappa_values = np.arange(100,1000,10) #Hz

#TODO: back of envelope estimate
# Q: is r^2*kappa of comparable magnitude in run 25 vs. run 24?


#run 24
# r_values = np.arange(0.1,1.8,0.2)   #cm
# kappa_values = np.arange(10,600,5) #Hz
# kappa_values = np.arange(10,600,10) #Hz
# kappa_values = np.array([100,250,300,400,500,600,700,800,900,1000,1500])#,1000,1500]) #Hz

# r_values = np.array([1.7])
# kappa_values = np.array([100,250,300,400,500,600,700,800,900,1000,1500])#,1000,1500]) #Hz

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
# print(count)#17640
