#gen_block
varkappa={'fk':  ,  'lr':  }
b={'fk':  ,  'lr':  }
r={'fk':  ,  'lr':  }
nu={'fk':  ,  'lr':  }
nu={'fk':  ,  'lr':  }

r_values=np.array([0.1,0.2,0.3,0.4,0.5,1.5,2.5])# cm
D_values=np.array([0.5,1.5,2.5])# cm^2/s
f_values=np.array([0.5,0.8,0.9,1.,1.1,1.2,1.5])
#for each FK and LR Model, consider an array of multiplicative factors with the expected value
for avg in ['fk', 'lr']:
    varkappa_values=varkappa[avg]*f_values #Hz
    b_values=b[avg]*f_values #cm/s
    x0_values=varkappa_values/b_values #cm
    r_values=r[avg]*f_values #cm
    kappa_values=(B[avg]*r_values.T**nu[avg]*f_values).flatten() #Hz

#TODO: make an excel file with B values needed by ^that gen_block
#TODO: print to grid search by iterating over ^those values
#TODO: make a back of envelope estimate for run time with 1000 CPU's
