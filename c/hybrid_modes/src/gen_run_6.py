import numpy as np
niter=1500 #trials per worker
r_values=np.array([0.1,0.2,0.3,0.4,0.5,.6,.7,.8,.9,1.,2.])#cm
D_values=np.array([0.2,1.0,1.5,2.0,3.,4.,5.])#cm^2/s
A_values=np.array([20.25,25,39,50,56.25,100,156.25,189,250])[::-1]#cm^2
L_values=np.sqrt(A_values)#cm
kappa_values=np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,250,500])#1/s
# beta_values=np.array([0.01,0.05,0.01,0.1,0.5,1])#cm
Dt_values=np.array([10**-i for i in range(6)])
num_trials_per_setting=1
reflect_values=np.array([0,1])
set_second_values=np.array([0])
#iterate over settings, scheduling the longest jobs first
count=0
for set_second in set_second_values:
	for r in r_values:
		for D in D_values:
			for L in L_values:
				for kappa in kappa_values:
					# for beta in beta_values:
					for Dt in Dt_values:
						for reflect in reflect_values:
							num_trials=0
							while num_trials<num_trials_per_setting:
								num_trials+=1
								count=count+1
								print(f"{r} {D} {L} {kappa} {Dt} {niter} {reflect} {set_second}")
# print(count)
