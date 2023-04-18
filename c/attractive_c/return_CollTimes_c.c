/* Program that returns collision times using a Monte Carlo method */
#include "CommonDefines.h"
// using namespace std;
int main(int argc, char* argv[])
{
  /* parse exteral inputs */
  /*                                |
  |  Parse Model Key Word Arguments |
  |                                */
  double r,D,L,kappa,Dt,dt,varkappa,x0;
  printf("Enter the reaction range (cm): ");
  scanf("%lg",&r);printf("r=%g",r);
  printf("\nEnter the diffusion coefficient (cm^2/s): ");
  scanf("%lg",&D);printf("D=%g",D);
  printf("\nEnter the domain width/height (cm): ");
  scanf("%lg",&L);printf("L=%g",L);
  printf("\nEnter the reaction rate (Hz): ");
  scanf("%lg",&kappa);printf("kappa=%g",kappa);
  printf("\nEnter the spring rate (Hz): ");
  scanf("%lg",&varkappa);printf("varkappa=%g",varkappa);
  printf("\nEnter the unpreferred distance (cm): ");
  scanf("%lg",&x0);printf("x0=%g",x0);
  printf("\nEnter the timestep of motion: ");
  scanf("%lg",&Dt);printf("Dt=%g",Dt);
  printf("\nEnter the timestep of reaction: ");
  scanf("%lg",&dt);printf("dt=%g",dt);

  /*                                      |
  |  Parse Simulation Key Word Arguments  |
  |                                      */
  // double no_rep,no_att,nite,refl,set_sec,see;
  printf("\nEnter the number of tips to observe: ");int N;
  scanf("%d",&N);printf("N=%d",N);
  printf("\nEnter the number of trials: ");
  int niter;scanf("%d",&niter);printf("niter=%d\n",niter);
  printf("Enter the randomization seed: ");
  int seed;scanf("%d",&seed);printf("seed=%d\n",seed);
  printf("Use reflecting boundary conditions? (Enter 1/0): ");
  int reflect;scanf("%d",&reflect);printf("reflect=%d\n",reflect);
  printf("Set second particle within reaction range of first? (Enter 1/0): ");
  int set_second;scanf("%d",&set_second);printf("set_second=%d\n",set_second);
  printf("Do not allow repulsive forces? (Enter 1/0): ");
  int no_repulsion;scanf("%d",&no_repulsion);printf("no_repulsion=%d\n",no_repulsion);
  printf("Do not allow attractive forces? (Enter 1/0): ");
  int no_attraction;scanf("%d",&no_attraction);printf("no_attraction=%d\n",no_attraction);
  printf("Only allow nearest neighbor forces? (Enter 1/0): ");
  int neighbor;scanf("%d",&neighbor);printf("neighbor=%d\n",neighbor);
  printf("Which force model should be used?\n(Enter 1:spring, 2:QED2, 3:QED3, 4:QED2 + const. repulsion, 5:QED3 + const. repulsion, else:no force): ");
  int force_code;scanf("%d",&force_code);printf("force_code=%d\n",force_code);

  //DONE: clean up unnecessary input variables by using
  //DONE: printf( all input parameters such that I can redirect ^this to a text file )
  printf("the repeatable inputs are:\n");
  printf("%lg %lg %lg %lg %lg %lg %lg %lg %d %d %d %d %d %d %d %d %d\n",r,D,L,kappa,varkappa,x0,Dt,dt,N,niter,seed,reflect,set_second,no_repulsion,no_attraction,neighbor,force_code);
  int i,j,k,q,s;
  int Nmax=N;
  int nparticles=Nmax;
  double x[Nmax];double y[Nmax];
  double X[Nmax];double Y[Nmax];
  double X_old[Nmax];double Y_old[Nmax];
  double X_new[Nmax];double Y_new[Nmax];
  double x_old[Nmax];double y_old[Nmax];
  double x_new[Nmax];double y_new[Nmax];
  double Fx_net[Nmax];double Fy_net[Nmax];
  double Time; double t;  // time of motion and reaction, respectivly
  double frac; // temporal fraction for interpolation
  double cfrac; //1-frac
  double T;
  double T_prev;
  double dx,dy,dxt,dyt,dxW,dyW;
  bool still_running[Nmax];
  double Tsum_array[Nmax+1];
  int Tcount_array[Nmax+1];
  bool dont_terminate_trial;
  bool all_valid;
  bool boo;
  double stepscale=sqrt(2*D*Dt);
  double probreact=kappa*dt; //double sig;
  double min_dist_old[Nmax];
  double dist; double dist2; bool in_range; bool reacts;int ineigh;
  double Tavg;
  double T_value; double Rad; double Theta;
  srand(seed); // randomize seed.
  // double tmax=5000.;
  double tmax=5000.e100;
  int iter_per_movestep = round(Dt/dt);
  int i_neighbor[Nmax];
  double impulse_prefactor= varkappa * Dt;
  double impulse_constant = -1. * impulse_prefactor / x0;
  double impulse_factor;
  // int exit_code;
  // int N0_end=50;
  // int N0_end=4;
  // int N0_end=2;
  int N0_end=0;
  // initialize record to zero
  // for (i = 0; i < Nmax+2; i++) {
  for (i = 0; i < Nmax+1; i++) {
    Tsum_array[i]=0.;
    Tcount_array[i]=0;
  }
  /*                              |
  |  N Iterations of Monte Carlo  |
  |                              */
  printf("\nrunning simulation...\n");
  /* for each trial... */
  for (q = 0; q < niter; q++) {
    t=0.;T=0.;
    Time=0.;
    dont_terminate_trial=true;
    // still_running=true;
    // exit_code=-1;
    //T = -9999.; //initialize stopping times to -9999
    /* initialize uniform random points in the unit square n*/
    for (j = 0; j < Nmax; j++ ) {
      x[j] = L*uniformRandom();
      y[j] = L*uniformRandom();
      still_running[j]=true;
      // todo(later?): check if any particles are within the minimum allowable distance
      // todo(later?): reseed any particles that are within the minimum allowable distance
    }
    nparticles=Nmax;
    // set_second particle to be within distance r of the first particle
    if (set_second==1){
      Rad = r*uniformRandom();
      Theta = 2.*3.141592653589793*uniformRandom();
      x[1]=x[0]+Rad*cos(Theta);
      y[1]=y[0]+Rad*sin(Theta);
      if (reflect==0){
        x[1]=pbc(x[1],L);
        y[1]=pbc(y[1],L);
      }else{
        //enforce RBC for x coordinate
        if (x[1]>L){
          x[1]=2.*L-x[1];
        }else if (x[1]<0){
          x[1]=-1.*x[1];
        }
        //enforce RBC for y coordinate
        if (y[1]>L){
          y[1]=2.*L-y[1];
        }else if (y[1]<0){
          y[1]=-1.*y[1];
        }
      }
    }//end set_second kernel
    // copy x,y to X_new,Y_new
    for (j = 0; j < Nmax; j++){
      X_new[j]=x[j];
      Y_new[j]=y[j];
    }
    /*                                   |
    |   run simulation for given trial   |
    |                                   */
    while(dont_terminate_trial){
      // // determine whether all particles have reacted
      // nparticles=0;
      // for (i = 0; i < Nmax; i++ ){
      //   if (still_running[i]){
      //     nparticles = nparticles + 1;
      //   }
      // }
      // if (nparticles <= N0_end){
      //   dont_terminate_trial=false;
      // }

      // DONT: move ^this solution to the end of this while statement.
      // DONE: dev record-keeping system in a 1D float array of length Nmax

      //reinitialize_kernel, which copies X,Y_new to X,Y_old
      for (i = 0; i < Nmax; i++ ){
        //reinitialize minimum distance value
        min_dist_old[i]=9999999;
        i_neighbor[i]=-1;
        // copy old coordinate values to new
        X_old[i]=X_new[i];
        Y_old[i]=Y_new[i];
        //enforce boundary conditions
        if (reflect==0){
          //enforce PBC
          x_old[i]=periodic(X_old[i],L);
          y_old[i]=periodic(Y_old[i],L);
        }else{
          //enforce RBC
          x_old[i]=reflection(X_old[i],L);
          y_old[i]=reflection(Y_old[i],L);
        }
      }
      if (neighbor==1){
        // kernel_compute_nearest_neighbor
        for (i = 0; i < Nmax-1; i++ ) {
          // each i,j pair is reached once per kernel launch
          for (j = i+1; j < Nmax; j++ ) {
            if (still_running[i] && still_running[j]){
              // compute distance between particles that are still running
              if (reflect==0){
                dist=dist_pbc(x_old[i],y_old[i],x_old[j],y_old[j],L);
              }else{
                dist=dist_eucl(x_old[i],y_old[i],x_old[j],y_old[j]);
              }
              // // update the symmetric distance matrix
              // dist_old[i][j]=dist;
              // dist_old[j][i]=dist;

              // update nearest neighbor distance and i_neighbor
              if (dist<min_dist_old[i]){
                min_dist_old[i]=dist;
                i_neighbor[i]=j;
              }
              if (dist<min_dist_old[j]){
                //this choice does not imply symplectic deterministic forces
                min_dist_old[j]=dist;
                i_neighbor[j]=i;
              }
            }
          }
        }
        // nearest neighbor one_step_ou_kernel at long timescale, Dt
        for (j = 0; j < Nmax; j++ ) {
          // // Spring forces between nearest neighbors
          // boundary conditions are already enforced
          ineigh=i_neighbor[j];// extract x,y_old of other tip

          // // compute displacement due to spring force with nearest neighbor
          if (reflect==0){
            dx = subtract_pbc_1d(x_old[ineigh],x_old[j],L);
            dy = subtract_pbc_1d(y_old[ineigh],y_old[j],L);
          }
          else{
            dx = x_old[ineigh]-x_old[j];
            dy = y_old[ineigh]-y_old[j];
          }
          dist2=dx*dx+dy*dy;
          // if (dist2<1.e-8){
          //   dist2=1.e-8;
          // }
          // Q: is ^this causing the discrep.?
          // A: nope.
          dist = sqrt(dist2);

          //FORCES_HERE
          //compute displacement due to drift
          impulse_factor=0.;
          if (force_code==1){
            //spring
            impulse_factor=impulse_prefactor*(dist-x0)/dist;
          }
          if (force_code==2){
            //QED2: force ~ inverse power law
            impulse_factor=impulse_prefactor/dist2;
          }
          if (force_code==3){
            //QED3: force ~ inverse square power law
            impulse_factor=impulse_prefactor/dist2/dist;
          }
          if (force_code==4){
            //QED3: force ~ inverse square power law + small repulsive force
            impulse_factor=impulse_prefactor/dist2 + impulse_constant;
          }
          if (force_code==5){
            //QED3: force ~ inverse square power law + small repulsive force
            impulse_factor=impulse_prefactor/dist2/dist + impulse_constant / x0;
          }

          // set impulse_factor to zero if it is explicitly forbidden by the user input
          if ((no_attraction==1) && (impulse_factor>0)){
            impulse_factor=0.;
          }
          if ((no_repulsion==1) && (impulse_factor<0)){
            impulse_factor=0.;
          }

          dxt=dx*impulse_factor;
          dyt=dy*impulse_factor;

          // compute displacement due to gaussian white noise
          dxW=stepscale*normalRandom();
          dyW=stepscale*normalRandom();
          // next spatial position, time integrating by a duration, Dt.
          X_new[j]=X_old[j]+dxW+dxt;
          Y_new[j]=Y_old[j]+dyW+dyt;
          if (reflect==0){
            //enforce PBC
            x_new[j]=periodic(X_new[j],L);
            y_new[j]=periodic(Y_new[j],L);
          }else{
            //enforce RBC
            x_new[j]=reflection(X_new[j],L);
            y_new[j]=reflection(Y_new[j],L);
          }
        }//end nearest neighbor one_step_ou_kernel
      }//end neighbor is 1
      else{//neighbor is 0, don't use nearest neighbors
        //reset the net forces
        for (i = 0; i < Nmax; i++ ) {
          Fx_net[i]=0.;
          Fy_net[i]=0.;
        }
        //sum_each_force_kernel as first part of one_step_ou_kernel at long timescale, Dt
        for (i = 0; i < Nmax-1; i++ ) {
          for (j = i+1; j < Nmax; j++ ) {
            if (still_running[i] && still_running[j]){
              // boundary conditions are already enforced
              // // compute displacement due to spring force with nearest neighbor
              if (reflect==0){
                dx = subtract_pbc_1d(x_old[j],x_old[i],L);
                dy = subtract_pbc_1d(y_old[j],y_old[i],L);
              }
              else{
                dx = x_old[j]-x_old[i];
                dy = y_old[j]-y_old[i];
              }
              dist2=dx*dx+dy*dy;
              // if (dist2<1.e-8){
              //   dist2=1.e-8;
              // }
              dist = sqrt(dist2);

              //FORCES_HERE
              //compute displacement due to drift
              impulse_factor=0.;
              if (force_code==1){
                //spring
                impulse_factor=impulse_prefactor*(dist-x0)/dist;
              }
              if (force_code==2){
                //QED2: force ~ inverse power law
                impulse_factor=impulse_prefactor/dist2;
              }
              if (force_code==3){
                //QED3: force ~ inverse square power law
                impulse_factor=impulse_prefactor/dist2/dist;
              }
              if (force_code==4){
                //QED3: force ~ inverse square power law + small repulsive force
                impulse_factor=impulse_prefactor/dist2 + impulse_constant;
              }
              if (force_code==5){
                //QED3: force ~ inverse square power law + small repulsive force
                impulse_factor=impulse_prefactor/dist2/dist + impulse_constant / x0;
              }

              // set impulse_factor to zero if it is explicitly forbidden by the user input
              if ((no_attraction==1) && (impulse_factor>0)){
                impulse_factor=0.;
              }
              if ((no_repulsion==1) && (impulse_factor<0)){
                impulse_factor=0.;
              }

              //sum Fx_net, Fy_net
              Fx_net[i]=Fx_net[i]+dx*impulse_factor;
              Fy_net[i]=Fy_net[i]+dy*impulse_factor;
              Fx_net[j]=Fx_net[j]-dx*impulse_factor;
              Fy_net[j]=Fy_net[j]-dy*impulse_factor;
            }
          }
        }
        //compute the one_step given the net force, F_net
        for (i = 0; i < Nmax; i++ ) {
          if (still_running[i]){
            dxt=Fx_net[i];
            dyt=Fy_net[i];
            // compute displacement due to gaussian white noise
            dxW=stepscale*normalRandom();
            dyW=stepscale*normalRandom();
            // next spatial position, time integrating by a duration, Dt.
            X_new[i]=X_old[i]+dxW+dxt;
            Y_new[i]=Y_old[i]+dyW+dyt;
            if (reflect==0){
              //enforce PBC
              x_new[i]=periodic(X_new[i],L);
              y_new[i]=periodic(Y_new[i],L);
            }else{
              //enforce RBC
              x_new[i]=reflection(X_new[i],L);
              y_new[i]=reflection(Y_new[i],L);
            }
          }
        }//end each force onestep kernel
      }//end switch clause for onestep kernels

      t=Time-dt;//for an edge case
      Time=Time+Dt;

      // collision_kernel at short timescale, dt
      for (s=0; s<iter_per_movestep; s++){
        // compute local time
        t=t+dt;
        frac=(Time-t)/Dt;
        cfrac=1.-frac;
        // kernel_interpolate, which enforces b.c.'s
        for (i = 0; i < Nmax; i++ ) {
          if(still_running[i]){
            // linear interpolation
            X[i]=frac*X_old[i]+cfrac*X_new[i];
            Y[i]=frac*Y_old[i]+cfrac*Y_new[i];
            // X[i]=cfrac*X_old[i]+frac*X_new[i];  //<<< looks wrong at large n
            // Y[i]=cfrac*Y_old[i]+frac*Y_new[i];  //<<< looks wrong at large n
            // impose boundary conditions
            if (reflect==0){
              //enforce PBC
              x[i]=periodic(X[i],L);
              y[i]=periodic(Y[i],L);
            }else{
              //enforce RBC
              x[i]=reflection(X[i],L);
              y[i]=reflection(Y[i],L);
            }
          }
        }
        ///////////////////////////////////////
        // reaction_kernel
        ///////////////////////////////////////
        // each i,j pair is reached once per call to kernel_measure
        for (i = 0; i < Nmax-1; i++ ) {
          for (j = i+1; j < Nmax; j++ ) {
            if(still_running[i] && still_running[j]){
              // compute distance between particles that are still running
              if(reflect==0){
                dist=dist_pbc(x[i],y[i],x[j],y[j],L);
              }else{
                dist=dist_eucl(x[i],y[i],x[j],y[j]);
              }
              in_range=dist<r;
              // in_range=true;//uncomment for smeared method
              // if two particles are in range
              if(in_range){
                // determine whether those two particles react
                reacts=probreact>uniformRandom();
                // determine whether those two particles react via the smeared method
                // sig=sigmoid(dist, r, beta);
                // reacts=probreact*sig>uniformRandom();
                if(reacts){
                  // compute time since last reaction
                  T_prev=T;
                  // T=t;
                  T=Time;
                  // Q: ^the root cause?
                  // exit_code=1;
                  // // count number of remaining particles
                  // nparticles=0;
                  // for (k = 0; k < Nmax; k++ ){
                  //   if(still_running[k]){
                  //     nparticles = nparticles + 1;
                  //   }
                  // }
                  // record
                  Tsum_array[nparticles] = Tsum_array[nparticles] + T - T_prev;
                  Tcount_array[nparticles] = Tcount_array[nparticles] + 1;
                  nparticles=nparticles-2;
                  // remove the two reacting particles from the simulation
                  still_running[i]=false;
                  still_running[j]=false;
                }
              }
            }
          }//end if still_running
        }
      }//end collision kernel
    //shut simulation down if it's taking too long...
    // if (t>tmax){
    //   exit_code=-99;
    //   for (i=0; i < Nmax; i++){
    //     still_running[i]=false;
    //   }}
      if (nparticles <= N0_end){
        dont_terminate_trial=false;
      }
    }//end while running

  }//end for each trial
  printf("simulation complete!\n");
  // Print results
  printf("\nPrinting Inputs...\n");
  printf("r=%g\n",r);
  printf("D=%g\n",D);
  printf("L=%g\n",L);
  printf("kappa=%g\n",kappa);
  printf("varkappa=%g\n",varkappa);
  printf("x0=%g\n",x0);
  printf("dt=%g\n",dt);
  printf("Dt=%g\n",Dt);
  // printf("N=%d\n",N);
  printf("niter=%d\n",niter);
  // printf("seed=%d\n",seed);
  printf("reflect=%d\n",reflect);
  printf("set_second=%d\n",set_second);
  printf("no_repulsion=%d\n",no_repulsion);
  printf("no_attraction=%d\n",no_attraction);
  printf("neighbor=%d\n",neighbor);
  printf("force_code=%d\n",force_code);
  printf("iter_per_movestep=%d\n",iter_per_movestep);

  /*                              |
  |  Record Mean Collision Times  |
  |                              */
  // print mean output of T_lst to stdout
  printf("\nPrinting Outputs...\n");
  // printf("exit_code=%d\n",exit_code);
  // printf("max ntips=%d\n",Nmax);
  // printf("max ntips_over_area=%g\n",Nmax/(L*L));
  // printf("Tcount=%d\n",count_net);
  // printf("Tsum=%g\n",T_net);
  // printf("Tavg=%g\n",T_net/count_net);
  // printf("rate=%g\n",count_net/T_net);
  // printf("rate_over_area=%g\n",count_net/(L*L*T_net));
  // T_value=T_net/count_net;
  boo=true;
  for(i = 0; i < (Nmax - N0_end);i++){ // <<< this unshifts the output
  // for(i = 0; i < (Nmax - N0_end - 2);i++){
    if (boo){
      printf ("%d,",Nmax-i);
      // printf ("%d,",i+1);
    }
    boo=!boo;
  }
  printf ("\n");
  boo=true;
  for(i = 0; i < (Nmax-N0_end);i++){  // <<< this unshifts the output
  // for(i = 2; i < (Nmax - N0_end); i++){
    if (boo){
      Tavg=Tsum_array[Nmax-i]/Tcount_array[Nmax-i];
      // printf ("%d,",Tcount_array[Nmax-i]);
      // printf ("%f,",Tsum_array[Nmax-i]);
      printf ("%f,",Tavg);
      // printf ("%d,",i+1);
    }
    boo=!boo;
  }

  // printf ("\n");
  // printf ("\n");
  // boo=true;
  // for(i = 0; i < (Nmax-N0_end);i++){  // <<< this unshifts the output
  // // for(i = 2; i < (Nmax - N0_end); i++){
  //   if (boo){
  //     // Tavg=Tsum_array[Nmax-i]/Tcount_array[Nmax-i];
  //     printf ("%d,",Tcount_array[Nmax-i]);
  //     // printf ("%f,",Tsum_array[Nmax-i]);
  //     // printf ("%f,",Tavg);
  //     // printf ("%d,",i+1);
  //   }
  //   // boo=!boo;
  // }
  // printf ("\n");
  // printf ("\n");
  // boo=true;
  // for(i = 0; i < (Nmax-N0_end);i++){  // <<< this unshifts the output
  // // for(i = 2; i < (Nmax - N0_end); i++){
  //   if (boo){
  //     // Tavg=Tsum_array[Nmax-i]/Tcount_array[Nmax-i];
  //     // printf ("%d,",Tcount_array[Nmax-i]);
  //     printf ("%f,",Tsum_array[Nmax-i]);
  //     // printf ("%f,",Tavg);
  //     // printf ("%d,",i+1);
  //   }
  //   // boo=!boo;
  // }

  //GOAL: consistency checks for output
  // Q: does the number of csv in the old output logs look like mine?
  // A: yes. equal lengths
  // Q: why is Tsum always 0 for when N0=Nmax?
  // DONE: copy an output log from run #38
  // Printing Outputs...
// 100,99,98,97,96,95,94,93,92,91,90,89,88,87,86,85,84,83,82,81,80,79,78,77,76,75,74,73,72,71,70,69,68,67,66,65,64,63,62,61,60,59,58,57,56,55,54,53,52,51,50,49,48,47,46,45,44,43,42,41,40,39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,
// 0.002600,0.002562,0.002614,0.002695,0.002698,0.002768,0.002823,0.002925,0.002862,0.002991,0.003021,0.003131,0.003164,0.003288,0.003279,0.003392,0.003352,0.003467,0.003600,0.003616,0.003849,0.003895,0.003740,0.004099,0.004160,0.004181,0.004188,0.004429,0.004489,0.004760,0.004852,0.004752,0.005010,0.005302,0.005509,0.005254,0.005494,0.005843,0.005973,0.005943,0.006514,0.006540,0.006839,0.007187,0.007134,0.007227,0.007376,0.007826,0.008216,0.008636,0.009098,0.008817,0.009682,0.009755,0.010156,0.011029,0.010946,0.011982,0.011894,0.012610,0.013467,0.013795,0.014648,0.015710,0.016109,0.016778,0.018366,0.019837,0.021938,0.022039,0.023301,0.024850,0.027689,0.029353,0.031602,0.035620,0.037761,0.042253,0.045227,0.047734,0.055359,0.061260,0.069149,0.077443,0.091110,0.104827,0.120232,0.139910,0.173815,0.217503,0.271134,0.362319,0.491164,0.765513,1.156350,2.250710,

  /* print sum and count*/
  // for(i = 0; i < Nmax;i++){
    // if all are still valid, print mean T
    // all_valid=T_value>0.;
    // if(all_valid){
    // printf ("Tsum=",T_net);
    // printf ("Tcount=",count);
    // printf ("Tavg=",T_values);
    // }else{
    //   //otherwise, print -9999
    //   printf ("%d,",-9999);

  printf("\n");
  return 0;
}

// print dense output of T_lst to stdout
// printf("\nPrinting Outputs...\n");
// for(i = 0; i < Nmax;i++){
//   printf ("%d,",i+1);
// }
// printf ("\n");
// /* print*/
// for (q = 0; q < niter; q++){
//   for(i = 0; i < Nmax;i++){
//     printf ("%.7lg,",T_lst[q][i]);
//   }
//   printf ("\n");
// }

// // save dense output of T_lst to file
// FILE * fp;
// /* open the file for writing*/
// fp = fopen ("out.csv","w");
// for(i = 0; i < Nmax;i++){
//   fprintf (fp, "%d,",i);
// }
// fprintf (fp, "\n");
// //  write into the file stream
// for (q = 0; q < niter; q++){
//   for(i = 0; i < Nmax;i++){
//     fprintf (fp, "%.5le,",T_lst[q][i]);
//   }
//   fprintf (fp, "\n");
// }
// /* close the file*/
// fclose (fp);
