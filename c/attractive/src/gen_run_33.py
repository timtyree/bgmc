#run_30.py - dense grid search over r,kappa with a = amax - 2*D, D fixed to observed
#run_31.py can be a bonus repeat at L=10...
# or... i could take the MLE fit on the entire corpus at L=10, which would be both easier and more baller.
import numpy as np
niter=1500 #trials per worker
num_trials_per_setting=1
# niter=150 #trials per worker
# num_trials_per_setting=10

L=10 #cm per domain
# L=5 #cm per domain
force_code=2 #2 :: QED2, 4 :: QED2 + constant repulsion
x0_values=np.array([0])#1.5,3.,5.,10.,100.,10000.]) #10 #doesn't matter for force_code=2

dt=1e-5
Dt=1e-5
Nmax=100  #Warning: not be actually connected to anything. goto return_Coltimes.sh to modify Nmin,Nmax.

#measured values for FK
#amax
amax_lst_fk=[1.84020234,
    0.657625095,
    1.932490123,
    2.735488034,
    1.781,
    ]
#D
D_lst_fk=[0.0372,
        0.1145,#* <--good one
        #0.05,#from table 1
        #37.2
            ]
#measured values for LR
#amax
amax_lst_lr=[8.585030313,
    3.29811395,
    8.630303341,
    12.01694823,
    10.147,
    ]
#D
D_lst_lr=[0.0014,#<--> i think this one was slow...
    1.4,#ibid times 1e3
    0.4158,]#from table 1

min_alinear=0.2 #cm^2/s <-- had some straggler w/  >20hours run time...
#define attractive and diffusive force parameters
alinear_lst=[]
D_lst=[]
for amax in amax_lst_fk:
    for D in D_lst_fk:
        alinear=amax-2*D
        if alinear>min_alinear:
            alinear_lst.append(alinear)
            D_lst.append(D)
for amax in amax_lst_lr:
    for D in D_lst_lr:
        alinear=amax-2*D
        if alinear>min_alinear:
            alinear_lst.append(alinear)
            D_lst.append(D)
#len(alinear_lst)

# kappa from 200 to 1000
# kappa_values = np.arange(200,1000,25) #Hz
kappa_values = np.arange(200,1000,50) #Hz
#include specific hypothesized values for kappa

# #kappa (reaction rate) notes:
kappa_values_addendum=np.array([
    436.74, #A=25 cm^2
    1614.16,#A=25 cm^2
    48.64,  #A=25 cm^2
    167.02, #A=25 cm^2
    880, #250, #from table 1
])
kappa_values = np.concatenate([kappa_values,kappa_values_addendum])
#src: http://localhost:8888/notebooks/estimation%20of%20intrinsic%20reaction%20rate.ipynb
#kappa_values.shape

#min_reaction=0.1 #cm^2/s# <--- had some stragglers past 20 hours of run time...
min_reaction=0.2 #cm^2/s #same value as alinear threshold.
# r from 0.02 to 0.2
r_values = np.arange(0.005,0.1,0.005)   #cm
r_values = np.concatenate((r_values,np.arange(0.1,0.2,0.005))) #cm
r_values_addendum=np.array([
    #0.02,#0.095,0.1,
    0.14,
])
r_values = np.concatenate((r_values,r_values_addendum))   #cm
# r_values = np.concatenate((r_values,np.arange(0.12,0.2,0.02)))   #cm
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
                                if min_reaction<=kappa*r**2:
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
# print(count)#37850
