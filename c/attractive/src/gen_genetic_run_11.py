import numpy as np
# DONE: genetic algorithm k-parents
#     1. consider the k trials with RMSE for (i) the FK model and (ii) the LR model
#     1. take random linear combinations of ^those parents, run them on the OSG, and then take the k best fits
#     1. repeat until desired convergence is met
#     1. repeat for various k, and visualize any (in)dependence of k

niter=1500 #trials per worker
r_values=np.array([0.1])#,0.2,0.3,0.4,0.5,.6,.7,.8,.9,1.,2.])#cm
# D_values=np.array([2.,20.])#0.2,1.0,1.5,2.0,3.,4.,5.])#cm^2/s
# A_values=np.array([25.])#20.25,25,39,50,56.25,100,156.25,189,250])[::-1]#cm^2
# L_values=np.sqrt(A_values)#cm
L_values=[10]
kappa_values=np.array([1500])#100,500,1500])#5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,250,500])#1/s
# varkappa_values=np.array([-20.,-10.,-5,0,5,10,20])#1/s
# x0_values=np.array([0.,0.5,1.0,1.5,2.0,3.0,4.0,5.0])#cm
Dt_values=np.array([1e-5])#,1e-2])#10**-i for i in range(6)])
dt=1e-5
Nmax=100
num_trials_per_setting=5
reflect_values=np.array([0])
set_second_values=np.array([0])
no_repulsion_values=np.array([1])#1 means no repulsion is true
no_attraction_values=np.array([1,0])

num_trials_born=100 # the total number of daughters
# print the breeding_values of the top 5
# num_breeders=5
# num_breeding_params=3
# breeding_cols=['D','varkappa','x0']
# num_breeding_params=len(breeding_cols)
# # taken from the *.ipynb located here: 'analyzing the effect of strong attractive forces between nearest neighbors.ipynb'
# breeder_values=dh[breeding_cols].head(num_breeders).values
# breeder_values_LR=breeder_values
# print(breeder_values)
#the top 5 for the LR model. Epoch 0
np.random.seed(1234)
breeder_values=np.array(
    [[  2.,   -5.,    5. ],
     [ 20.,   -5.,    5. ],
     [ 20.,  -20.,    1.5],
     [ 20.,  -10.,    3. ],
     [  2.,  -20.,    1.5]])

#breed the given most-fit trials omnisexually.
num_breeders, num_breeding_params = breeder_values.shape
rand_matrix=np.random.rand(num_trials_born-num_breeders,num_breeders) # each entry is uniformly distributed on the interval from 0 to 1.

breeder_trials=np.matmul(rand_matrix,breeder_values)/num_breeders
#prepend the breeding_values of the top 5 to breeder_trials
trial_values=np.concatenate((breeder_values,breeder_trials),axis=0)

#iterate over settings, scheduling the longest jobs first
count=0
for Dt in Dt_values:
    for set_second in set_second_values:
        for reflect in reflect_values:
            for r in r_values:
                # for D in D_values:
                for L in L_values:
                    for kappa in kappa_values:
                        # for varkappa in varkappa_values:
                        #     for x0 in x0_values:
                        for trial in trial_values:
                            D,varkappa,x0=trial
                            for no_repulsion in no_repulsion_values:
                                for no_attraction in no_attraction_values:
                                    num_trials=0
                                    while num_trials<num_trials_per_setting:
                                        num_trials+=1
                                        count=count+1
                                        print(f"{r} {D:.5f} {L} {kappa} {varkappa:.5f} {x0:.5f} {Dt} {dt} {Nmax} {niter} {reflect} {set_second} {no_repulsion} {no_attraction}")
# print(count)
