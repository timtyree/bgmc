#gen_run_1.py
import numpy as np
niter=250 #trials per worker
r_values=np.array([0.1,0.2,0.3,0.4,0.5,1.0])#cm
D_values=np.array([0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0])#cm^2/s
A_values=np.array([20.25,25,39,50,56.25,100,156.25,189])[::-1]#cm^2
L_values=np.sqrt(A_values)#cm
kappa_values=np.array([1,10,100])#1/s
num_trials_per_setting=6
#iterate over settings, scheduling the longest jobs first
count=0
for r in r_values:
	for D in D_values:
		for L in L_values:
			for kappa in kappa_values:
				num_trials=0
				while num_trials<num_trials_per_setting:
					num_trials+=1
					count=count+1
					print(f"{r} {D} {L} {kappa} {niter}")