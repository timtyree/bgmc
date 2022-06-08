#method_of_simulating_oscillatory_particle_model.py
#the following is simplified for legibility. it is not executable.
stepscale = np.sqrt(2 * D * Dt)
impulse_prefactor = a * Dt
omega=((1e-3*period_of_oscillation/(2*np.pi))**-1)
time_constant=initial_phase_orientation/omega
if printing:
    print(f"running simulation for {num_steps} steps...")
step_num=0
dont_break=True #pseudo loop invariant
while dont_break and (step_num < num_steps):
    t=step_num*Dt + time_constant
    #compute the attractive step between all pairs
    f_values=impulse_prefactor/Rsq_values
    F1x=f_values*dx_values
    F1y=f_values*dy_values
    F1x*=np.cos(omega*t)
    F1y*=np.cos(omega*t)

    #randomly sample the diffusive step between all pairs
    dxW1_values=stepscale*np.random.normal(size=num_pairs)
    dxW2_values=stepscale*np.random.normal(size=num_pairs)
    dyW1_values=stepscale*np.random.normal(size=num_pairs)
    dyW2_values=stepscale*np.random.normal(size=num_pairs)

    #the mean distance between all pairs of particles
    R_values=np.sqrt(Rsq_values)
    mean_R=np.mean(R_values)
    std_R=np.std(R_values)

    #compute the net change in position (with signs chosed s.t. repulsive at zero phase)
    x1step_values=-F1x+dxW1_values
    y1step_values=-F1y+dyW1_values
    x2step_values=F1x+dxW2_values
    y2step_values=F1y+dyW2_values

    #compute the distance between each pair of particles
    dx_values=(x2_values-x1_values)
    dy_values=(y2_values-y1_values)
    Rsq_values=dx_values**2+dy_values**2

    #update particle locations if they are still running
    x1_values[boo_still_running]=x1_values[boo_still_running]+x1step_values[boo_still_running]
    y1_values[boo_still_running]=y1_values[boo_still_running]+y1step_values[boo_still_running]
    x2_values[boo_still_running]=x2_values[boo_still_running]+x2step_values[boo_still_running]
    y2_values[boo_still_running]=y2_values[boo_still_running]+y2step_values[boo_still_running]

    #record
    position_array[step_num,0,boo_still_running]=x1_values[boo_still_running]
    position_array[step_num,1,boo_still_running]=y1_values[boo_still_running]
    position_array[step_num,2,boo_still_running]=x2_values[boo_still_running]
    position_array[step_num,3,boo_still_running]=y2_values[boo_still_running]
    mean_array[step_num,0]=mean_R
    step_num+=1
