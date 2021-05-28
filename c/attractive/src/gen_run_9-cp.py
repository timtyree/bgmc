import numpy as np
niter=1500 #trials per worker
r_values=np.array([0.1,1.0])#,0.2,0.3,0.4,0.5,.6,.7,.8,.9,1.,2.])#cm
D_values=np.array([2.,20.])#0.2,1.0,1.5,2.0,3.,4.,5.])#cm^2/s
A_values=np.array([25.])#20.25,25,39,50,56.25,100,156.25,189,250])[::-1]#cm^2
L_values=np.sqrt(A_values)#cm
kappa_values=np.array([500,1500])#5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,250,500])#1/s
varkappa_values=np.array([-5,-1.5,-0.2,0,0.2,1.5,5])#1/s
x0_values=np.array([0.,0.1,0.2,0.3,0.4,0.5,1.0])#cm
Dt_values=np.array([1e-5,1e-2])#10**-i for i in range(6)])
dt=1e-5
Nmax=100
num_trials_per_setting=1
reflect_values=np.array([0])
set_second_values=np.array([0])
no_repulsion_values=np.array([0,1])
no_attraction_values=np.array([0,1])
#iterate over settings, scheduling the longest jobs first
count=0
for Dt in Dt_values:
	for set_second in set_second_values:
	    for reflect in reflect_values:
	        for r in r_values:
	            for D in D_values:
	                for L in L_values:
	                    for kappa in kappa_values:
	                        for varkappa in varkappa_values:
	                            for x0 in x0_values:
									for no_repulsion in no_repulsion_values:
										for no_attraction in no_attraction_values:
	                                        num_trials=0
	                                        while num_trials<num_trials_per_setting:
	                                            num_trials+=1
	                                            count=count+1
	                                            print(f"{r} {D} {L} {kappa} {varkappa} {x0} {Dt} {dt} {Nmax} {niter} {reflect} {set_second} {no_repulsion} {no_attraction}")
# print(count)
