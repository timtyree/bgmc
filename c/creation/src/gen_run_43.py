import numpy as np
Ninitial=2
# niter=1500  #<<<--- run time is ominously long... just to generate the inputs... best avoid...
# niter=150
niter=100
# niter=1
dt=1e-5
# Nmax=150
creation_duration=0.1 #seconds for both full models
L=5

# a (cm2/s) 1.552 ± 0.016 9.3 ±0.3
# % \textcolor{red}{$b=a(\chi -1)$}
# % b=10.0 +/- 0.5 cm^2/s (LR)
# % b=10.0399 +/- 0.4766 cm^2/s (LR)
# % 	- chi=2.0796 +/- 0.0542
# % b=3.01 +/- 0.08 cm^2/s (FK)
# % b=3.0122 +/- 0.0773 cm^2/s (FK)
# % 	- chi=2.9408 +/- 0.0508
def map_b_to_chi(b,a):
    x = b/a
    chi = x+1
    return chi

# DONE: design a regular grid of (a,b) values that cover the full models at a visually nice scale
a_values = np.arange(1,10.05,0.2)
# b_values = np.arange(1,15.05,0.1)
b_values = np.logspace(0,3,225)
# a_values = np.concatenate([a_values,[1.552,9.3]]) #for FK,LR
# a_values = np.concatenate([a_values,[1.552]]) #for FK,LR
# b_values = np.concatenate([b_values,[3.01]]) #for FK, 10.0 for LR,
a_values = np.concatenate([a_values,[1.552,9.3]]) #for FK,LR
b_values = np.concatenate([b_values,[3.01,10.0]]) #for FK, 10.0 for LR
# a_values = np.concatenate([a_values,[9.3]]) LR, already included
# b_values = np.concatenate([b_values,[3.01]]) #for FK, 10.0 for LR, already included
# b_values = np.array(list(reversed(sorted(b_values)))).flatten()
# a_values.shape[0]*b_values.shape[0]

# queue seed Ninitial Nfinal R_c_bar Mp nup chi kappa r varkappa D r0 L creation_duration dt
count = 0
args_lst  = []
for b in b_values:
    for a in a_values:
        #for each a,b compute chi
        chi = map_b_to_chi(b,a)
        for seed in range(niter):
#             #LR  #<-- takes too long
#             #.                      R_c_bar Mp nup                                r0
#             args=seed, Ninitial, 0, 1.25, 3.28, 0.715, chi, 75, 0.314, a, 0.42, 0.202, L, creation_duration, dt
# #             print(f"{*args}")
#             print(*args)
            #FK
            #.                      R_c_bar Mp nup                                r0
            args=seed, Ninitial, 0, 0.85, 0.864, 0.230, chi, 15, 0.457, a, 0.115, 0.131, L, creation_duration, dt
#             print(*args)
            count+=1
            #record
            args_lst.append(args)
# print(count) #1089600
np.random.seed(42)
np.random.shuffle(args_lst)
for args in args_lst:
    print(*args)
