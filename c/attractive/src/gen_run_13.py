#run_13.py
import numpy as np
niter=1500 #trials per worker
num_trials_per_setting=1

#expected values for key parameters
#values rounded from full-model-measurements.xlsx
nu_dict      ={'fk':-2.1, 'lr':-1.7}
beta_dict    ={'fk':4.4,  'lr':3.7 }  #positive varkappa implies an attractive force is present
varkappa_dict={'fk':10.,  'lr':100.}  #positive varkappa implies an attractive force is present
# b_dict={'fk':  ,  'lr':  } # 95% CI was covering zero...

def comp_kappa(r,beta,nu):
    return np.exp(beta)*r**nu

L=5 #cm per domain
force_code=4 #QED2 + constant repulsion
dt=1e-5
Dt=1e-5
Nmax=50  #Caution: might not be actually connected to anything...

#model parameters
D_values=np.array([0.5,1.5,5.,25.])# cm^2/s
x0_values=np.array([1.5,3.,5.,10.,100.,10000.])
r_values=np.array([0.1])#,0.2,0.3,0.4,0.5])# cm

#factors to multiply functionally computed parameters
f_values=np.array([0.5,0.8,0.9,1.,1.1,1.2])

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
                    #compute parameters functionally within the for loop block:
                    for mode in ['fk','lr']:
                        varkappa_values = varkappa_dict[mode]*f_values
                        for r in r_values:
                            kappa_values = comp_kappa(r,beta_dict[mode],nu_dict[mode])*f_values
                            for kappa in kappa_values:
                                for varkappa in varkappa_values:
                                    for D in D_values:
                                        for x0 in x0_values:
                                            num_trials=0
                                            while num_trials<num_trials_per_setting:
                                                num_trials+=1
                                                count=count+1
                                                print(f"{r} {D} {L} {kappa:.5f} {varkappa} {x0} {Dt} {dt} {Nmax} {niter} {reflect} {set_second} {no_repulsion} {no_attraction} {neighbor} {force_code}")
# print(count)#3456
