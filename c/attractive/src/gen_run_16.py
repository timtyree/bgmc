#run_16.py
import numpy as np,pandas as pd
niter=1500 #trials per worker
num_trials_per_setting=1

L=10 #cm per domain
force_code=2 #2 :: QED2, 4 :: QED2 + constant repulsion

dt=1e-5
Dt=1e-5
Nmax=100  #Caution: might not be actually connected to anything...

#define constant parameters
reflect=0
force_code=2
set_second=0
neighbor=0
no_attraction=0
no_repulsion=0
kappa=500
L=10
x0=0

input_fn=f"/home/timothytyree/Documents/GitHub/bgmc/python/data/osg_output/run_15_ar_star.csv"
df_star=pd.read_csv(input_fn)
count=0
for index,row in df_star.iterrows():
    r=row['rstar']
    varkappa=row['astar']
    kappa=row['kappa']
    D=row['D']
    print(f"{r:.5f} {D:.5f} {L} {kappa:.5f} {varkappa:.5f} {x0} {Dt} {dt} {Nmax} {niter} {reflect} {set_second} {no_repulsion} {no_attraction} {neighbor} {force_code}")
    count+=1
# print(count)
