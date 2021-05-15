/* Program that returns collision times using a Monte Carlo method */
// the variable number of diffusing particles is handled by

//TODO: implement simplest explicit nearest neighbor spring force in the Langevin Equation in the inviscid limit (solved by a Generalized Onstein-Uhlenbeck Process)
//TODO: implement no_attraction and no_repulsion
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
   double r,D,L,kap,Dt,dt,varkappa,x0,nite,refl,set_sec,see;
   // double dt=1e-5;             // reaction time step size.
   double no_rep,no_att;
   printf("Enter the reaction range (cm): ");
   scanf("%lg",&r);printf("r=%g",r);
   printf("\nEnter the diffusion coefficient (cm^2/s): ");
   scanf("%lg",&D);printf("D=%g",D);
   printf("\nEnter the domain width/height (cm): ");
   scanf("%lg",&L);printf("L=%g",L);
   printf("\nEnter the reaction rate (Hz): ");
   scanf("%lg",&kap);printf("kappa=%g",kap);
   //DONE: handle io for each new parameter listed here:
   //varkappa // spring constant / scale of motion
   //x0        // preferred distance between particles
   printf("\nEnter the spring rate (Hz): ");
   scanf("%lg",&varkappa);printf("varkappa=%g",varkappa);
   printf("\nEnter the preferred distance (cm): ");
   scanf("%lg",&x0);printf("x0=%g",x0);
   printf("\nEnter the timescale of random motion: ");
   scanf("%lg",&Dt);printf("Dt=%g",Dt);
   printf("\nEnter the timescale of random reaction: ");
   scanf("%lg",&dt);printf("dt=%g",dt);
   printf("\nEnter the minimum number of tips to observe:");int Nmin;
   scanf("%d",&Nmin);printf("Nmin=%d",Nmin);
   printf("\nEnter the minimum number of tips to observe:");int Nmax;
   scanf("%d",&Nmax);printf("Nmax=%d",Nmax);

   /*                                      |
   |  Parse Simulation Key Word Arguments  |
   |                                      */
   printf("\nEnter the number of trials: ");
   scanf("%lg",&nite);
   int niter=(int)nite;printf("niter=%d\n",niter);
   printf("Enter the randomization seed: ");
   scanf("%lg",&see);
   int seed=(int)see;printf("seed=%d\n",seed);
   printf("Use reflecting boundary conditions? (Enter 1/0): ");
   scanf("%lg",&refl);
   int reflect=(int)refl;printf("reflect=%d\n",reflect);
   printf("Set second particle within reaction range of first? (Enter 1/0): ");
   scanf("%lg",&set_sec);
   int set_second=(int)set_sec;printf("set_second=%d\n",set_second);
   printf("Do not allow repulsive forces? (Enter 1/0): ");
   scanf("%lg",&no_rep);
   int no_repulsion=(int)no_rep;printf("no_repulsion=%d\n",no_repulsion);
   printf("Do not allow attractive forces? (Enter 1/0): ");
   scanf("%lg",&no_att);
   int no_attraction=(int)no_att;printf("no_attraction=%d\n",no_attraction);

   // int Nmax=700; int Nmin=50;//11;
   int i,j,k,q,s;
   double x[Nmax];double y[Nmax];
   double X[Nmax];double Y[Nmax];
   double X_old[Nmax];double Y_old[Nmax];
   double X_new[Nmax];double Y_new[Nmax];
   double x_old[Nmax];double y_old[Nmax];
   double x_new[Nmax];double y_new[Nmax];
   double Time; double t;  // time of motion and reaction, respectivly
   double frac; // temporal fraction for interpolation
   double cfrac; //1-frac
   double T[Nmax];
   double dx,dy,dxt,dyt,dxW,dyW;
   bool still_running[Nmax]; bool any_running; bool all_valid;
   double stepscale=sqrt(2*D*Dt);
   double probreact=kap*dt; //double sig;
   double dist_old[Nmax][Nmax];
   double min_dist_old[Nmax];
   double dist; bool in_range; bool reacts;int ineigh;
   double T_lst[niter][Nmax]; double net_T; double T_value; double Rad; double Theta;
   srand(seed); // randomize seed.
   double tmax=500.; // UNCOMMENT_HERE
   // double tmax=.1; // COMMENT_HERE
   int iter_per_movestep = round(Dt/dt);
   int i_neighbor[Nmax];
   double impulse_prefactor=-1.*varkappa*Dt;
   double impulse_factor;

   /*                              |
   |  N Iterations of Monte Carlo  |
   |                              */
  printf("\nrunning simulation...\n");
  /* for each trial... */
  for (q = 0; q < niter; q++){
    t=0.;
    Time=0.;
    any_running=true;
    /* initialize uniform random points in the unit square n*/
    for (j = 0; j < Nmax; j++ ) {
     x[j] = L*uniformRandom();
     y[j] = L*uniformRandom();
     T[j] = -9999.; //initialize stopping times to -9999
     still_running[j]=true;
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
        }else if(y[1]<0){
          y[1]=-1.*y[1];
    }}}
    // copy x,y to X_new,Y_new
    for (j = 0; j < niter; j++){
      X_new[j]=x[j];
      Y_new[j]=y[j];
    }
    /*                                   |
    |   run simulation for given trial   |
    |                                   */
    while(any_running){
      //reinitialize_kernel, which copies X,Y_new to X,Y_old
      for (i = 0; i < Nmax-1; i++ ){
        if(still_running[i]){
          //reinitialize minimum distance value
          min_dist_old[j]=2*L;
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
      }}
      t=Time;
      Time=Time+Dt;
      // kernel_map_Phi from X,Y_old to x,y_old and compute the nearest neighbor
      for (i = 0; i < Nmax-1; i++ ) {
        if(still_running[i]){
          // each i,j pair is reached once per call to kernel_measure
          for (j = i+1; j < Nmax; j++ ) {
            if(still_running[j]){
              // compute distance between particles that are still running
              if (reflect==0){
                dist=dist_pbc(x_old[i],y_old[i],x_old[j],y_old[j],L);
              }else{
                dist=dist_eucl(x_old[i],y_old[i],x_old[j],y_old[j]);
              }
              // update the symmetric distance matrix
              dist_old[i][j]=dist;
              dist_old[j][i]=dist;
              // update nearest neighbor distance and i_neighbor
              if (dist<min_dist_old[i]){
                min_dist_old[i]=dist;
                i_neighbor[i]=j;
                //this choice implies symplectic deterministic forces
                min_dist_old[j]=dist;
                i_neighbor[j]=i;
          }}}}}
      // one_step_ou_kernel at long timescale, Dt
      // TODO: debug one_step_ou_kernel... it's causing a segmentation fault
      for (j = i+1; j < Nmax; j++ ) {
        if(still_running[j]){
            // boundary conditions are already enforced
            ineigh=i_neighbor[j];// extract x,y_old of other tip
            // compute displacement due to spring force with nearest neighbor
            if (reflect==0){
              dx = subtract_pbc_1d(x_old[ineigh],x_old[j],L);
              dy = subtract_pbc_1d(y_old[ineigh],y_old[j],L);
              dist = sqrt(dx*dx+dy*dy);
            }
            else{
              dx = x_old[ineigh]-x_old[j];
              dy = y_old[ineigh]-y_old[j];
              dist = sqrt(dx*dx+dy*dy);
            }
            //compute displacement due to drift
            impulse_factor=impulse_prefactor*(dist-x0)/dist;
            // set impulse_factor to zero if it is explicitly forbidden by the user input
            if (no_attraction && (impulse_factor>0)){
              impulse_factor=0.;
            }
            if (no_repulsion && (impulse_factor<0)){
              impulse_factor=0.;
            }

            dxt=dx*impulse_factor;
            dyt=dy*impulse_factor;

            // compute displacement due to gaussian white noise
            dxW=stepscale*normalRandom();
            dyW=stepscale*normalRandom();
            // next spatial position, time integrating by a duration, Dt.
            X_new[j]=X_old[j]+dxt+dxW;
            Y_new[j]=Y_old[j]+dyt+dyW;
            // impose boundary conditions for x,y_new
            if (reflect==0){
              //enforce PBC
              x_new[j]=periodic(X_new[j],L);
              y_new[j]=periodic(Y_new[j],L);
            }else{
              //enforce RBC
              x_new[j]=reflection(X_new[j],L);
              y_new[j]=reflection(Y_new[j],L);
            }
        }}
      //TODO(later): simplify to one xy coordinate system instead of keeping track of x and X separately...
      // collision_kernel at short timescale, dt
      // t=t-dt;//for an insignificant edge case
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
            // map to world coordinates
            // impose boundary conditions
                if (reflect==0){
                  //enforce PBC
                  x[i]=periodic(X[i],L);
                  y[i]=periodic(Y[i],L);
                }else{
                  //enforce RBC
                  x[i]=reflection(X[i],L);
                  y[i]=reflection(Y[i],L);
        }}}
        // reaction_kernel
        for (i = 0; i < Nmax-1; i++ ) {
          if(still_running[i]){
            // each i,j pair is reached once per call to kernel_measure
            for (j = i+1; j < Nmax; j++ ) {
              if(still_running[j]){
                // compute distance between particles that are still running
                if (reflect==0){
                  dist=dist_pbc(x_old[i],y_old[i],x_old[j],y_old[j],L);
                }else{
                  dist=dist_eucl(x_old[i],y_old[i],x_old[j],y_old[j]);
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
                    T[j]=t;
                    still_running[j]=false;
                    for(k=j+1; k<Nmax; k++){
                      if(still_running[k]){
                        T[k]=t;
                        still_running[k]=false;
          }}}}}}}}
        }
      //check if any are still running...
      any_running=false;
      for (j = Nmin; j < Nmax; j++ ) {
        if(still_running[j]){
          any_running=true;
      }}
      //shut simulation down if it's taking too long...
      if (t>tmax){
        any_running=false;
      }
    }
    //record trial
    for (j = 0; j<Nmax; j++){
      T_lst[q][j]=T[j];
    }
  }
  printf("simulation complete!\n");

  // Print results
  printf("\nPrinting Inputs...\n");
  printf("r=%g\n",r);
  printf("D=%g\n",D);
  printf("L=%g\n",L);
  printf("kappa=%g\n",kap);
  printf("varkappa=%g\n",varkappa);
  printf("x0=%g\n",x0);
  printf("dt=%g\n",dt);
  printf("Dt=%g\n",Dt);
  printf("niter=%d\n",niter);
  // printf("seed=%d\n",seed);
  printf("reflect=%d\n",reflect);
  printf("set_second=%d\n",set_second);
  printf("no_repulsion=%d\n",no_repulsion);
  printf("no_attraction=%d\n",no_attraction);
  /*                              |
  |  Record Mean Collision Times  |
  |                              */
  // print mean output of T_lst to stdout
  printf("\nPrinting Outputs...\n");
  for(i = 0; i < Nmax;i++){
    printf ("%d,",i+1);
  }
  printf ("\n");
  /* compute mean*/
  for(i = 0; i < Nmax;i++){
    all_valid=true;
    net_T=0.;
    for (q = 0; q < niter; q++){
      T_value=T_lst[q][i];
      if (T_value==-9999.){
        all_valid=false;
      }
      net_T=net_T+T_value;
    }
    // if all are still valid, print mean T
    if(all_valid){
      printf ("%.7lg,",net_T/niter);
    }else{
      //otherwise, print -9999
      printf ("%d,",-9999);
  }}
  printf ("\n");
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
