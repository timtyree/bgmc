import numpy as np
Ninitial=2
# niter=1500  #<<<--- run time is ominously long... just to generate the inputs... best avoid...
# niter=150
# niter=100
niter=2000
# niter=1
dt=1e-5
# Nmax=150
creation_duration=0.1 #seconds for both full models
# L=5

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

################################
# FK
################################
# DONE: design a regular grid of (a,b) values that cover the full models at a visually nice scale
# a_values = np.arange(1,10.05,0.2)
# b_values = np.arange(1,15.05,0.1)
# b_values = np.logspace(0,3,225)
# a_values = np.array([1.82,5.73]) #for FK,LR
# b_values = np.array([2.89,7.]) #for FK,LR
# a_values = np.array([1.82]) #for FK (modified)
# b_values = np.array([2.89]) #for FK (modified)
a_values = np.array([1.552]) #for FK
b_values = np.array([3.01]) #for FK
# a_values = np.concatenate([a_values,[1.552,9.3]]) #for FK,LR
# b_values = np.concatenate([b_values,[3.01,10.0]]) #for FK, 10.0 for LR
# L_values_fk = np.array([4.5  , 4.75 , 5.   , 5.25 , 5.625, 6.25 ]) #for comparing WJ's tau estimates
# L_values_lr = np.array([5.  , 6.25, 7.5 , 8.75])  #for comparing WJ's tau estimates
# L_values_fk=np.array([3.75 , 5.   , 6.25 , 7.075, 8.75 ]) #for comparing WJ's tau(N0=2) estimates
# L_values_lr=np.array([ 5.  ,  6.25,  7.5 ,  8.75, 10.  ]) #for comparing WJ's tau(N0=2) estimates
L_values_fk=np.array([3.75 , 4.5, 4.75, 5., 5.25, 5.625   , 6.25 , 7.075, 8.75 ])
L_values_lr=np.array([ 5.  ,  6.25,  7.5 ,  8.75, 10.  ])
L_values = L_values_fk

# queue seed Ninitial Nfinal R_c_bar Mp nup chi kappa r varkappa D r0 L creation_duration dt
count = 0
args_lst  = []
for L in L_values:
    for b in b_values:
        for a in a_values:
            #for each a,b compute chi
            chi = map_b_to_chi(b,a)
            for seed in range(niter):
    #             #LR  #<-- takes too long
    #             #.                      R_c_bar Mp nup                                r0
    #             args=seed, Ninitial, 0, 1.25, 3.28, 0.715, chi, 75, 0.314, a, 0.42, 0.202, L, creation_duration, dt
    #             args_lst.append(args)
    # #             print(f"{*args}")
    # #             print(*args)
    #             count+=1
                #FK
                #.                      R_c_bar Mp nup                                r0
                args=seed, Ninitial, 0, 0.85, 0.864, 0.230, chi, 15, 0.457, a, 0.048, 0.131, L, creation_duration, dt
    #             args=seed, Ninitial, 0, 0.85, 0.864, 0.230, chi, 15, 0.457, a, 0.115, 0.131, L, creation_duration, dt
    #             print(*args)
                count+=1
                #record
                args_lst.append(args)

################################
# LR
################################
# a_values = np.array([1.82,5.73]) #for FK,LR
# b_values = np.array([2.89,7.]) #for FK,LR
# a_values = np.array([5.73]) #for LR (modified)
# b_values = np.array([7.]) #for LR (modified)
a_values = np.array([9.3]) #for LR
b_values = np.array([10.]) #for LR
# a_values = np.concatenate([a_values,[1.552,9.3]]) #for FK,LR
# b_values = np.concatenate([b_values,[3.01,10.0]]) #for FK, 10.0 for LR
# queue seed Ninitial Nfinal R_c_bar Mp nup chi kappa r varkappa D r0 L creation_duration dt
# count = 0
# args_lst  = []
L_values = L_values_lr
for L in L_values:
    for b in b_values:
        for a in a_values:
            #for each a,b compute chi
            chi = map_b_to_chi(b,a)
            for seed in range(niter):
                #LR  #<-- takes too long
                #.                      R_c_bar Mp nup                                r0
                args=seed, Ninitial, 0, 1.25, 3.28, 0.715, chi, 75, 0.314, a, 0.42, 0.202, L, creation_duration, dt
                args_lst.append(args)
    #             print(f"{*args}")
    #             print(*args)
                count+=1
    #             #FK
    #             #.                      R_c_bar Mp nup                                r0
    #             args=seed, Ninitial, 0, 0.85, 0.864, 0.230, chi, 15, 0.457, a, 0.115, 0.131, L, creation_duration, dt
    # #             print(*args)
    #             count+=1
    #             #record
    #             args_lst.append(args)



# print(count) #20000
np.random.seed(42)
np.random.shuffle(args_lst)
for args in args_lst:
    print(*args)
