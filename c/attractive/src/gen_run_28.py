#run_26.py - dense grid search with a = amax - 2*D
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
#  dense grid search with amax = a + 2*D fixed
amax_lst = [1.78,10.147]# cm^2/s
D_values=np.arange(0.05,1.5,0.15)# cm^2/s
# D_values=np.arange(0.05,1.5,0.03)# cm^2/s

alinear_lst=[]
D_lst=[]
for amax in amax_lst:
    for D in D_values:
        alinear=amax-2*D
        if alinear>0.2:
            alinear_lst.append(alinear)
            D_lst.append(D)
len(alinear_lst)

# r from 0.02 to 0.2
r_values = np.arange(0.005,0.1,0.005)   #cm
r_values = np.concatenate((r_values,np.arange(0.12,0.2,0.02)))   #cm
# kappa from 200 to 1000
# kappa_values = np.arange(200,1000,20) #Hz
kappa_values = np.arange(200,1000,50) #Hz

#simulation parameters
set_second_values=np.array([0])
reflect_values=np.array([0])
no_repulsion_values=np.array([0])#1 means no repulsion is true
no_attraction_values=np.array([0])
neighbor_values=np.array([0,1])

#iterate over settings, scheduling the longest jobs first
count=0
task_str_lst=[]
for set_second in set_second_values:
    for reflect in reflect_values:
        for no_repulsion in no_repulsion_values:
            for no_attraction in no_attraction_values:
                for neighbor in neighbor_values:
                    for varkappa,D in zip(alinear_lst,D_lst):
                        for r in r_values:
                            for kappa in kappa_values:
                                for x0 in x0_values:
                                    num_trials=0
                                    while num_trials<num_trials_per_setting:
                                        num_trials+=1
                                        count=count+1
                                        task_str=f"{r:.5f} {D:.5f} {L} {kappa:.5f} {varkappa:.5f} {x0} {Dt} {dt} {Nmax} {niter} {reflect} {set_second} {no_repulsion} {no_attraction} {neighbor} {force_code}"
                                        task_str_lst.append(task_str)
np.random.seed(42)
np.random.shuffle(task_str_lst)
for task_str in task_str_lst:
    print(task_str)
# print(count)#5248
