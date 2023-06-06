#run_41.py - dense grid search over kappa with others fixed to observed
import numpy as np
niter=1500 #trials per worker
num_trials_per_setting=1
force_code=2 #2 :: QED2, 4 :: QED2 + constant repulsion
x0_values=np.array([0])
dt=1e-5
Dt=1e-5
Nmax=150
#simulation parameters
set_second_values=np.array([0])
reflect_values=np.array([0])
no_repulsion_values=np.array([0])#1 means no repulsion is true
no_attraction_values=np.array([0])
# neighbor_values=np.array([0,1])
neighbor_values=np.array([0])
L_lst=[5,10]

r_values=np.array([0.314])
kappa_values=np.arange(60,80,0.1)
D_values=np.array([
#     0.115, #0.1145, #fk from msr
    0.42, #0.4158  #lr from msr
])
#define linear search over alinear
alinear_lst=[
#     1.5520, #1.781 - 2*0.115, #0.1145,
    9.3,
    ###the varkappa sweep####
#     0,1,2,3,4,5,
#     6,7,8,9, # <--- optional bc otherwise I had <60 jobs...
#     10,15,20,25,30,
#     40,50,60,70,80,90,100, # <--- optional bc otherwise I had <60 jobs...
]
#iterate over settings, scheduling the longest jobs first
count=0
task_str_lst=[]
for L in L_lst:
    for set_second in set_second_values:
        for reflect in reflect_values:
            for no_repulsion in no_repulsion_values:
                for no_attraction in no_attraction_values:
                    for neighbor in neighbor_values:
                        for D in D_values:
                            for r in r_values:
                                for kappa in kappa_values:
                                    for varkappa in alinear_lst:
                                        for x0 in x0_values:
                                            num_trials=0
                                            while num_trials<num_trials_per_setting:
                                                num_trials+=1
                                                count=count+1
                                                task_str=f"{r:.5f} {D:.5f} {L} {kappa:.5f} {varkappa:.5f} {x0} {Dt} {dt} {Nmax} {niter} {reflect} {set_second} {no_repulsion} {no_attraction} {neighbor} {force_code}"
                                                task_str_lst.append(task_str)


r_values=np.array([0.457])
kappa_values=np.arange(5,25,0.1)
D_values=np.array([
    0.115, #0.1145, #fk from msr
#     0.42, #0.4158  #lr from msr
])
#define linear search over alinear
alinear_lst=[
    1.5520, #1.781 - 2*0.115, #0.1145,
#     9.3,
    ###the varkappa sweep####
#     0,1,2,3,4,5,
#     6,7,8,9, # <--- optional bc otherwise I had <60 jobs...
#     10,15,20,25,30,
#     40,50,60,70,80,90,100, # <--- optional bc otherwise I had <60 jobs...
]
#iterate over settings, scheduling the longest jobs first
# count=0
# task_str_lst=[]
for L in L_lst:
    for set_second in set_second_values:
        for reflect in reflect_values:
            for no_repulsion in no_repulsion_values:
                for no_attraction in no_attraction_values:
                    for neighbor in neighbor_values:
                        for D in D_values:
                            for r in r_values:
                                for kappa in kappa_values:
                                    for varkappa in alinear_lst:
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
# print(count)
# 800
