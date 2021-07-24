#functionally generates a log of particle locations for a given randomization seed.  Uses uniform initial conditions
#Programmer: Tim Tyree
#Date: 7.1.2021
from ..my_initialization import *
from ..utils.pbc import *
import shutil
from numpy.random import MT19937
from numpy.random import RandomState, SeedSequence

#helper functions
from numba import jit,njit
@njit
def normalRandom():
    return np.random.normal()

@njit
def uniformRandom():
    return np.random.uniform(0,1)
normalRandom(),uniformRandom()

# @njit
def format_particles(frameno,t,x_values,y_values,pid_values,round_t_to_n_decimals=5,tscale=1000):
    '''tscale scales from seconds to milliseconds.
    round_t_to_n_decimals=5 corrects arithmatic error, minimizes output memory requirements, and matches Dt=dt=1e-5 seconds
    '''
    n_tips = x_values.shape[0]
    dict_out = {
        'frame':frameno,
        't': np.around(t,round_t_to_n_decimals)*tscale,
        'n': n_tips,
        'x': x_values,
        'y': y_values,
        'pid_explicit':pid_values}
    return dict_out

##########################
## Primay routine function
##########################
def get_routine_gener_logs(
        results_folder,
        N=16,
        L=10,
        r=0.1,
        D=2,
        kappa=1500,
        Dt=1e-5,
        dt=1e-5,
        tmax=10,
        force_code=2,
        varkappa=5,
        save_every=25,
        dist_cutoff=1e-2,
        x0=5,
        no_repulsion=1,
        no_attraction=0,
        use_neighbors=0,
        explicitly_uniform_ic=False,
        **kwargs):
    '''
    TODO: implement use_neighbors kwarg. integrate it's manipulation from the cooresponding .ipynb

    defines model parameters baked into simulation
    Example Usage:
    results_folder=f"{nb_dir}/data/local_results"
    routine_gener_logs=get_routine_gener_logs(results_folder,tmax=10)
    routine_gener_logs(seed=123)
    '''
    #prepare folders for csv output
    data_folder = f"{results_folder}/euic_{str(explicitly_uniform_ic)}_fc_{force_code}_r_{r}_D_{D}_L_{L}_kappa_{kappa}_varkappa_{varkappa}"
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    data_folder = data_folder + "/Log"
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)

    def routine_gener_logs(seed):
        os.chdir(data_folder)
        data_fn = f"pbc_particle_log{seed}_log.csv"

        #random number stream A
        rs = RandomState(MT19937(SeedSequence(seed)))
        #random number stream B
        # rs = RandomState(MT19937(SeedSequence(987654321)))
        np.random.seed(seed)

        ###############################
        ## Start Simulation
        ###############################
        #define constants
        stepscale = np.sqrt(2 * D * Dt)
        probreact = kappa * dt
        T_net = 0
        count_net = 0
        iter_per_movestep = round(Dt / dt)
        impulse_prefactor = varkappa * Dt

        step = 0
        recording_locations = True
        recording_snapshots = False
        printing = False
        if printing:
            print("running simulation...")
        Time = 0
        t = 0
        still_running = True
        exit_code = -1
        T = -9999.
        saving = recording_locations

        #initialize positions
        #uniform random ic
        x_values=rs.uniform(size=N)*L
        y_values=rs.uniform(size=N)*L
        pid_values=np.array(range(N)) #fixed for explicit particle tracking purposes
        if explicitly_uniform_ic:
            #explicitely uniform ic
            uvals=np.linspace(0,L,int(np.sqrt(N))+1)
            x_values,y_values=np.meshgrid(uvals,uvals)
            x_values=x_values.flatten()
            y_values=y_values.flatten()
        #initialize times
        t = 0
        frameno = 1

        #lower case: world coordinates
        #upper case: material coordinates
        x = x_values.copy()
        y = y_values.copy()
        x_old = x_values.copy()
        y_old = y_values.copy()
        x_new = x_values.copy()
        y_new = y_values.copy()
        X = x_values.copy()
        Y = y_values.copy()
        X_old = x_values.copy()
        Y_old = y_values.copy()
        X_new = x_values.copy()
        Y_new = y_values.copy()
        zeros = np.zeros_like(x_values)
        zerosint = np.zeros_like(x_values).astype('int')
        still_running = zerosint == zerosint
        # //start set_second kernel
        # //end set_second kernel
        #TODO: make still_running into still_running_values
        dict_out_lst = []
        while (still_running.any()):
            # //reinitialize_kernel, which copies X,Y_new to X,Y_old
            min_dist_old = zeros + 9999999
            i_neighbor = zerosint - 1
            X_old = X_new
            Y_old = Y_new
            # //enforce boundary conditions
            for i in range(N):
                x_old[i] = periodic(X_old[i], L)
                y_old[i] = periodic(Y_old[i], L)

            t = Time - dt
            #//for an insignificant edge case
            Time = Time + Dt

            # reset the net forces
            Fx_net = zeros.copy()
            Fy_net = zeros.copy()

            #sum_each_force_kernel
            for i in range(N):
                if (still_running[i]):
                    for j in range(i + 1, N - 1):
                        if (still_running[j]):
                            #compute displacement vector with pbc
                            dx = subtract_pbc_1d(x_old[j], x_old[i], L)
                            dy = subtract_pbc_1d(y_old[j], y_old[i], L)

                            dist2 = dx * dx + dy * dy
                            if (dist2 < 1e-8):
                                dist2 = float(1e-8)
                            dist = np.sqrt(dist2)

                            #compute displacement due to drift
                            impulse_factor = 0.
                            if (force_code == 1):
                                #spring
                                impulse_factor = impulse_prefactor * (
                                    dist - x0) / dist
                            if (force_code == 2):
                                #QED2: force ~ inverse power law
                                impulse_factor = impulse_prefactor / dist2
                            if (force_code == 3):
                                #QED3: force ~ inverse square power law
                                impulse_factor = impulse_prefactor / dist2 / dist

                            #set impulse_factor to zero if it is explicitly forbidden by the user input
                            if ((no_attraction == 1) & (impulse_factor > 0)):
                                impulse_factor = 0.
                            if ((no_repulsion == 1) & (impulse_factor < 0)):
                                impulse_factor = 0.

                            #sum Fx_net, Fy_net according to a symplectic (momentum conserving) integrator
                            Fx_net[i] = Fx_net[i] + dx * impulse_factor
                            Fy_net[i] = Fy_net[i] + dy * impulse_factor
                            Fx_net[j] = Fx_net[j] - dx * impulse_factor
                            Fy_net[j] = Fy_net[j] - dy * impulse_factor

            #compute the one_step given the net force, F_net
            for i in range(N):
                if (still_running[i]):
                    dxt = Fx_net[i]
                    dyt = Fy_net[i]
                    # compute displacement due to gaussian white noise
                    dxW = stepscale * normalRandom()
                    dyW = stepscale * normalRandom()
                    # next spatial position, time integrating by a duration, Dt.
                    X_new[i] = X_old[i] + dxW + dxt
                    Y_new[i] = Y_old[i] + dyW + dyt
                    # enforce PBC
                    x_new[i] = periodic(X_new[i], L)
                    y_new[i] = periodic(Y_new[i], L)

            #interpolation_kernel at short timescale, dt
            for s in range(iter_per_movestep):
                # compute local time
                t = t + dt
                frac = (Time - t) / Dt
                cfrac = 1. - frac
                # kernel_interpolate, which enforces b.c.'s
                for i in range(N):
                    if (still_running[i]):
                        # linear interpolation
                        X[i] = frac * X_old[i] + cfrac * X_new[i]
                        Y[i] = frac * Y_old[i] + cfrac * Y_new[i]
                        # impose boundary conditions
                        # enforce PBC
                        x[i] = periodic(X[i], L)
                        y[i] = periodic(Y[i], L)

            #reaction_kernel
            for i in range(N):
                if (still_running[i]):
                    # // each i,j pair is reached once per call to kernel_measure
                    for j in range(i + 1, N - 1):
                        if (still_running[j]):
                            # // compute distance between particles that are still running
                            dist = dist_pbc(x[i], y[i], x[j], y[j], L)
                            in_range = dist < r
                            # // in_range=true;//uncomment for smeared method
                            # // if two particles are in range
                            if (in_range):
                                # // determine whether those two particles react via the simple method
                                reacts = probreact > uniformRandom()
                                # // determine whether those two particles react via the smeared method
                                # // sig=sigmoid(dist, r, beta);
                                # // reacts=probreact*sig>uniformRandom();
                                if (reacts):
                                    T = t
                                    still_running[i] = False
                                    still_running[j] = False
                                    exit_code = 1

            if step % save_every == 0:
                x_plot = x_new[still_running]
                y_plot = y_new[still_running]
                pid_plot = pid_values[still_running]
                #         if recording_snapshots:
                #             #save result as png
                #             SaveScatterPlotSnapshot(x_plot,y_plot,t,width=L,height=L,
                #                             frameno=frameno,save_folder=save_folder,
                #                             annotating=annotating,message=message)
                if (recording_locations) & (x_plot.shape[0] > 0):
                    #append particle locations to log, dict_out_lst
                    dict_out = format_particles(frameno, t, x_plot, y_plot, pid_plot)
                    dict_out_lst.append(dict_out)

                frameno += 1

            #shut simulation down if it's taking too long...
            if (t > tmax):
                for i in range(N):
                    still_running[i] = False
                    exit_code = -99

            step += 1
            #end while running

        #record this trial
        if (exit_code > 0):
            if (T > 0.):
                T_net = T_net + T
                count_net = count_net + 1
        if printing:
            print(f"simulation complete!")

        ####################################
        ## Save particle locations as csv
        ####################################
        if saving:
            df = pd.concat(
                [pd.DataFrame(dict_out) for dict_out in dict_out_lst])
            df.reset_index(inplace=True, drop=True)
            #save the recorded data
            os.chdir(data_folder)
            df.to_csv(data_fn, index=False)
            out_dir = os.path.abspath(data_fn)
            if printing:
                print('saved to:')
                print(out_dir)
            return out_dir
        return "Warning: output csv not saved for seed={seed}."

    return routine_gener_logs

if __name__=="__main__":
    #simplest test case
    results_folder=f"{nb_dir}/data/local_results"
    routine_gener_logs=get_routine_gener_logs(results_folder,tmax=.00001)
