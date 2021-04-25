import numpy as np
niter=250 #trials per worker
r_values=np.array([0.1,0.5,1.,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.,2.5,5.,10.,20.])#cm
D_values=np.array([0.2,1.0,1.5,2.0,5.,10,20])#cm^2/s
A_values=np.array([20.25,25,39,50,56.25,100,156.25,189,250])[::-1]#cm^2
L_values=np.sqrt(A_values)#cm
# kappa_values=np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,250,500])#1/s
# beta_values=np.array([0.01,0.05,0.01,0.1,0.5,1])#cm
Dt_values=np.array([1.])
reflect_values=np.array([0])
set_second_values=np.array([0])
m_values=np.array([1.8772341309722325, 1.6375562704001745])
M_values=np.array([5.572315674840435,16.73559858353835])
num_trials_per_setting=6

Dratio_values=np.array([1,10,100,1000])
energy_gap_values=np.array(sorted([0.,-10,10,0.5,1,2,-1]))
temperature_energy_values=np.array([1.])

def comp_M_tilde(m):
    '''non-quadratic trend is guessed to make bounds'''
    val_lst=[]
    val_lst.append(np.pi**(m-1)/m)
    val_lst.append(np.pi**(m-1)/2)
    val_lst.append(np.pi/2)
    val_lst.append((np.pi/2)**(m-1))
    mn=np.min(val_lst)
    mx=np.max(val_lst)
    return mn,mx

def comp_kappa(M,m,r):
    '''returns a min/max estimate for kappa using the emergent universal law'''
    mn,mx=comp_M_tilde(m)
    kappa_mn=r**(-2*(m-1))*M/mx
    kappa_mx=r**(-2*(m-1))*M/mn
    return kappa_mn,kappa_mx

#iterate over settings, scheduling the longest jobs first
count=0
for set_second in set_second_values:
    for r in r_values:
        for D in D_values:
            for L in L_values:
                for Dt in Dt_values:
                    for reflect in reflect_values:
                        for m,M in zip(m_values,M_values):
                            kappa_mn_mx=comp_kappa(M,m,r)
                            kappa_values=np.array(sorted(set([kappa_mn_mx[0],(kappa_mn_mx[0]+kappa_mn_mx[1])/2.,kappa_mn_mx[1]])))
                            for kappa in kappa_values:
                                for Dratio in Dratio_values:
                                    for temperature_energy in temperature_energy_values:
                                        for energy_gap in energy_gap_values:
                                            num_trials=0
                                            while num_trials<num_trials_per_setting:
                                                num_trials+=1
                                                count=count+1
                                                print(f"{r} {D} {L} {Dt} {niter} {reflect} {set_second} {temperature_energy} {energy_gap} {Dratio}")
# print(count)
