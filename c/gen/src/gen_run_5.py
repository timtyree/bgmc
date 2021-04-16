import numpy as np
niter=250 #trials per worker
r_values=np.array([0.6])#cm
D_values=np.array([0.2,2.,20.,])#cm^2/s
A_values=np.array([20.25,25,39,50,56.25,100,156.25,189,250])[::-1]#cm^2
L_values=np.sqrt(A_values)#cm
kappa_values=np.array([10])#1/s
beta_values=np.array([0.01,0.05,0.1,0.5,1])#cm
num_trials_per_setting=6
reflect_values=np.array([0,1])
set_second_values=np.array([1,0])
#iterate over settings, scheduling the longest jobs first
count=0
for set_second in set_second_values:
	for r in r_values:
		for D in D_values:
			for L in L_values:
				for kappa in kappa_values:
					for beta in beta_values:
						for reflect in reflect_values:
							num_trials=0
							while num_trials<num_trials_per_setting:
								num_trials+=1
								count=count+1
								print(f"{r} {D} {L} {kappa} {beta} {niter} {reflect} {set_second}")
# print(count)
