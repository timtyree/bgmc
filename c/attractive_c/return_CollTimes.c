/* Program that returns collision times using a Monte Carlo method */
// the variable number of diffusing particles is handled by

//Scrum 6.22.2021: implementing (I) starting outside a particular distance and (II) additional choices of force_code
// I (Option A)
// alter set_second to choose each particle to be outside of each previous particle.
// if a certain number of attempts doesn't work, then give up and rename Nmax... that's complicated...
//TODO: I (Option B)
// write python function that saves M*MM locations to /public/TimtheTyrant/ic-2d/
// load a set of example initial positions from /public/TimtheTyrant/ic-2d/ using Process mod some value
// set N (or Nmax) to the number of particles

//TODO: II (Option A) just code the new forces inline and copy to the second locations
// II (Option B) move the force computation to a separate file and call it.

//Ye Olde Scrum
//TODO(later): consider whether I might see any new behaviour returned/effect on collision times, if I
// - consider exponential solution in computing motion... with dt=1e-6... probably not...
// - consider other SDE discretizations to solve the motion
#include "CommonDefines.h"
// // using namespace std;
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
  //TODO: generalize to a set of forces of interest

  int i,j,k,q,s;
  int Nmax=N;
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
  double dx,dy,dxt,dyt,dxW,dyW;
  bool still_running; bool all_valid;
  double stepscale=sqrt(2*D*Dt);
  double probreact=kappa*dt; //double sig;
  double min_dist_old[Nmax];
  double dist; double dist2; bool in_range; bool reacts;int ineigh;
  double T_net=0.;int count_net=0;
  double T_value; double Rad; double Theta;
  srand(seed); // randomize seed.
  double tmax=5000.;
  // double tmax=500.; // UNCOMMENT_HERE
  // // double tmax=.1; // COMMENT_HERE
  double dist_cutoff=1e-6;
  // double dist_cutoff=1e-2; // UNCOMMENT_HERE
  int iter_per_movestep = round(Dt/dt);
  int i_neighbor[Nmax];
  double impulse_prefactor= varkappa * Dt;
  double impulse_constant = -1. * impulse_prefactor / x0;
  double impulse_factor;
  int exit_code;
  /*                              |
  |  N Iterations of Monte Carlo  |
  |                              */
  printf("\nrunning simulation...\n");
  /* for each trial... */
  for (q = 0; q < niter; q++) {
    t=0.;
    Time=0.;
    still_running=true;
    exit_code=-1;
    T = -9999.; //initialize stopping times to -9999
    /* initialize uniform random points in the unit square n*/
    for (j = 0; j < Nmax; j++ ) {
      x[j] = L*uniformRandom();
      y[j] = L*uniformRandom();
      // todo(later?): check if any particles are within the minimum allowable distance
      // todo(later?): reseed any particles that are within the minimum allowable distance
    }
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
    while(still_running){
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
      t=Time-dt;//for an insignificant edge case
      Time=Time+Dt;
      if (neighbor==1){
        // kernel_compute_nearest_neighbor
        for (i = 0; i < Nmax-1; i++ ) {
            // each i,j pair is reached once per kernel launch
            for (j = i+1; j < Nmax; j++ ) {
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
          if (dist2<1.e-8){
            dist2=1.e-8;
          }
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
            if (dist2<1.e-8){
              dist2=1.e-8;
            }
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
        //compute the one_step given the net force, F_net
        for (i = 0; i < Nmax; i++ ) {
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
        }//end each force onestep kernel
      }//end switch clause for onestep kernels

      // collision_kernel at short timescale, dt
      for (s=0; s<iter_per_movestep; s++){
        // compute local time
        t=t+dt;
        frac=(Time-t)/Dt;
        cfrac=1.-frac;
        // kernel_interpolate, which enforces b.c.'s
        for (i = 0; i < Nmax; i++ ) {
          if(still_running){
            // linear interpolation
            X[i]=frac*X_old[i]+cfrac*X_new[i];
            Y[i]=frac*Y_old[i]+cfrac*Y_new[i];
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
        // reaction_kernel
        for (i = 0; i < Nmax-1; i++ ) {
          if(still_running){
            // each i,j pair is reached once per call to kernel_measure
            for (j = i+1; j < Nmax; j++ ) {
              if(still_running){
                // compute distance between particles that are still running
                if (reflect==0){
                  dist=dist_pbc(x[i],y[i],x[j],y[j],L);
                }else{
                  dist=dist_eucl(x[i],y[i],x[j],y[j]);
                }
                in_range=dist<r;
                // in_range=true;//uncomment for smeared method
                // if two particles are in range
                if(in_range){
                  // determine whether those two particles react via the simple method
                  reacts=probreact>uniformRandom();
                  // determine whether those two particles react via the smeared method
                  // sig=sigmoid(dist, r, beta);
                  // reacts=probreact*sig>uniformRandom();
                  if(reacts){
                    T=t;
                    still_running=false;
                    exit_code=1;
                  }
                }
              }
            }
          }//end if still_running
        }
      }//end collision kernel
    //shut simulation down if it's taking too long...
    if (t>tmax){
        still_running=false;
        exit_code=-99;
      }
    }//end while running
    //record this trial
    if (exit_code>0){
      if (T>0.){
        T_net=T_net+T;
        count_net=count_net+1;
      }
    }
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

  /*                              |
  |  Record Mean Collision Times  |
  |                              */
  // print mean output of T_lst to stdout
  printf("\nPrinting Outputs...\n");
  printf("exit_code=%d\n",exit_code);
  printf("ntips=%d\n",Nmax);
  printf("ntips_over_area=%g\n",Nmax/(L*L));
  printf("Tcount=%d\n",count_net);
  printf("Tsum=%g\n",T_net);
  printf("Tavg=%g\n",T_net/count_net);
  printf("rate=%g\n",count_net/T_net);
  printf("rate_over_area=%g\n",count_net/(L*L*T_net));
  // T_value=T_net/count_net;
  // for(i = 0; i < Nmax;i++){
  //   printf ("%d,",i+1);
  // }
  // printf ("\n");
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
