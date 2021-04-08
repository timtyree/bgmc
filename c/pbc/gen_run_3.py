#gen_run_3.py
import numpy as np
niter=250 #trials per worker
r_values=np.array([0.1,.15,0.2,.25,0.3,.35,0.4,.45,0.5,.55,.6,.65,.7,.75,.8,.85,.9,.95,1.0,2.5,5.,7.5,10.])[::-1]#cm
D_values=np.array([0.2,2.0])[::-1]#cm^2/s
A_values=np.array([1000,250])[::-1]#cm^2
L_values=np.sqrt(A_values)[::-1]#cm
kappa_values=np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,250,500,750,1000])[::-1]#1/s
num_trials_per_setting=6
#iterate over settings, scheduling the longest jobs first
count=0
for L in L_values:
	for r in r_values:
		for kappa in kappa_values:
			for D in D_values:
				num_trials=0
				while num_trials<num_trials_per_setting:
					num_trials+=1
					count=count+1
					print(f"{r} {D} {L} {kappa} {niter}")
# print(count)
