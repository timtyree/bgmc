#run_18.py
import numpy as np,pandas as pd
niter=1500 #trials per worker
num_trials_per_setting=1
np.random.seed(42)
L=10 #cm per domain
force_code=2 #2 :: QED2, 4 :: QED2 + constant repulsion
x0_values=np.array([0])#1.5,3.,5.,10.,100.,10000.]) #10 #doesn't matter for force_code=2

dt=1e-5
Dt=1e-5
Nmax=100  #Caution: might not be actually connected to anything...

#compute model parameters
#TODO: merge and move to dev run .ipynb
# intersection_dir='/home/timothytyree/Documents/GitHub/bgmc/python/data/osg_output/run_15_ar_star.csv'
intersection_dir='/home/timothytyree/Documents/GitHub/bgmc/python/data/osg_output/run_17_ar_star.csv'
df_star=pd.read_csv(intersection_dir)
# df_star.head()

input_cols=['rstar', 'kappa', 'D', 'astar']
output_col_lst=['m', 'M']
X=df_star[input_cols].values
num_stars=X.shape[0]

#TODO: make a num_samples by num_stars matrix
num_samples=10000

def gener_offspring(X,num_partners=2):
    #TODO: randomly draw two parameter settings from
    #TODO: randomly draw two numbers
    #TODO: return a randomly weighted average of these two parameter settings
    a=np.random.random(num_partners)
    a=a/np.sum(a)
    #TODO: verify that it looks reasonableX
    partners=np.random.permutation(X)[:num_partners]
    weights=a
    return np.matmul(partners.T,weights)

#TODO: generate 10000 such parameter settings
X_lst=[]
for j in range(num_samples):
    X_lst.append(gener_offspring(X))
random_parameter_values=np.array(X_lst)
# rarr.shape,X.shape,random_parameter_values.shape,random_parameter_weights.shape
# random_parameter_values=np.divide(random_parameter_values.T,random_parameter_weights).T
#augment with arr
r_values,kappa_values,D_values,varkappa_values=np.concatenate((X,random_parameter_values)).T

#later #TODO: augment the 4 bwm parameters for lr,fk_pbc_M,m
# df_bwm

#old parameter grid
# D_values=np.linspace(0.7,2,14)# cm^2/s #14
# r_values=np.array([0.05,0.1,0.15,0.2,0.3,0.4,0.5])#,0.2,0.3,0.4,0.5])# cm
# kappa_values = np.array([250,500])#,1000,1500]) #Hz
# varkappa_values = np.array([0,1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,60,70,80,90,100,110]) #cm^2/s #11

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
                    for r,kappa,varkappa,D in zip(r_values,kappa_values,varkappa_values,D_values):
#                     for r in r_values:
#                         for kappa in kappa_values:
#                             for varkappa in varkappa_values:
#                                 for D in D_values:
                        for x0 in x0_values:
                            num_trials=0
                            while num_trials<num_trials_per_setting:
                                num_trials+=1
                                count=count+1
                                print(f"{r:.5f} {D:.5f} {L} {kappa:.5f} {varkappa:.5f} {x0} {Dt} {dt} {Nmax} {niter} {reflect} {set_second} {no_repulsion} {no_attraction} {neighbor} {force_code}")
# print(count)#20304
