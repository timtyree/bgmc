#run_30.py - dense grid search over r,kappa with a = amax - 2*D, D fixed to observed
#run_31.py can be a bonus repeat at L=10...
# or... i could take the MLE fit on the entire corpus at L=10, which would be both easier and more baller.
import numpy as np
niter=1500 #trials per worker
num_trials_per_setting=1
# niter=150 #trials per worker
# num_trials_per_setting=10

# L=10 #cm per domain
# L=5 #cm per domain
L_lst=[5,10]
force_code=2 #2 :: QED2, 4 :: QED2 + constant repulsion
x0_values=np.array([0])#1.5,3.,5.,10.,100.,10000.]) #10 #doesn't matter for force_code=2

dt=1e-5
Dt=1e-5
Nmax=100  #Warning: not be actually connected to anything. goto return_Coltimes.sh to modify Nmin,Nmax.

# amax_lst=[
#     1.781, #fk from osc fit to msr
#     10.147, #lr from osc fit to msr
# ]


kappa_values=np.arange(100,400,5)
r_values=np.arange(0.1,0.4,0.005)

#inpute exactly what is listed in table 1
# r_values=np.array([
#     # 0.135, #fk from table 1
#     # 0.155  #lr from table 1
#     0.175,
#     0.1
# ])
# kappa_values=np.array([
#     100.,
#     200.,
#     # 167., #167.02, #fk from table 1
#     300.  #lr from table 1
# ])
D_values=np.array([
    0.115, #0.1145, #fk from msr
    0.42, #0.4158  #lr from msr
#     0.4158,
#     0.2,
#     #0.4,
#     0.6,
#     0.8,
#     1.2,
#     1.6,
])
#define linear search over alinear
alinear_lst=[
    1.5520, #1.781 - 2*0.115, #0.1145,
    9.3,
#     9.3154,
#     9.307,
#     9.3, #10.147- 2*0.42, #0.4158
    ###the varkappa sweep####
#     0,1,2,3,4,5,
#     6,7,8,9, # <--- optional bc otherwise I had <60 jobs...
#     10,15,20,25,30,
#     40,50,60,70,80,90,100, # <--- optional bc otherwise I had <60 jobs...
]

#simulation parameters
set_second_values=np.array([0])
reflect_values=np.array([0])
no_repulsion_values=np.array([0])#1 means no repulsion is true
no_attraction_values=np.array([0])
neighbor_values=np.array([0])
# neighbor_values=np.array([0,1])

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
np.random.seed(42)
np.random.shuffle(task_str_lst)
for task_str in task_str_lst:
    print(task_str)
# print(count)#58560
