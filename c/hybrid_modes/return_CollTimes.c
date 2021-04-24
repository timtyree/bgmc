/* Program that returns collision times using a Monte Carlo method */
// the variable number of diffusing particles is handled by still_running
#include "CommonDefines.h"

// // using namespace std;
int main(int argc, char* argv[])
{
   /* parse exteral inputs */
   double r,D,L,kap,nite,see,refl,set_sec,Dt;//,beta;
   printf("Enter the reaction range (cm): ");
   scanf("%lg",&r);printf("r=%g",r);
   printf("\nEnter the diffusion coefficient (cm^2/s): ");
   scanf("%lg",&D);printf("D=%g",D);
   printf("\nEnter the domain width/height (cm): ");
   scanf("%lg",&L);printf("L=%g",L);
   printf("\nEnter the reaction rate (Hz): ");
   scanf("%lg",&kap);printf("kappa=%g",kap);
   // printf("\nEnter the reaction scale (cm): ");
   // scanf("%lg",&beta);printf("beta=%g",beta);
   printf("\nEnter the timescale of random motion: ");
   scanf("%lg",&Dt);printf("Dt=%g",Dt);
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

   int Nmax=700; int Nmin=11;//11;
   double dt=1e-5;             // reaction time step size.
   int i,j,k,q,s;
   double x[Nmax];double y[Nmax];
   double X[Nmax];double Y[Nmax];
   double X_old[Nmax];double Y_old[Nmax];
   double X_new[Nmax];double Y_new[Nmax];
   double Time; double t;  // time of motion and reaction, respectivly
   double frac; // temporal fraction for interpolation
   double cfrac; //1-frac
   double T[Nmax];
   bool still_running[Nmax]; bool any_running; bool all_valid;
   double stepscale=sqrt(2*D*Dt);
   double probreact=kap*dt; //double sig;
   //double distmat[Nmax][Nmax];
   double dist; bool in_range; bool reacts;
   double T_lst[niter][Nmax]; double net_T; double T_value; double Rad; double Theta;
   srand(seed); // randomize seed.
   double tmax=1000.; // UNCOMMENT_HERE
   // double tmax=.1; // COMMENT_HERE
   int iter_per_movestep = round(Dt/dt);

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
     // TODO(later?): check if any particles are within the minimum allowable distance
     // TODO(later?): reseed any particles that are within the minimum allowable distance
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

    /* run simulation for given trial */
    while(any_running){
      // kernel_onestep at long timescale, Dt
      t=Time;
      Time=Time+Dt;
      for (j = 0; j < Nmax; j++ ) {
        if(still_running[j]){
            // copy X_new,Y_new to X_old,Y_old
            X_old[j]=X_new[j];
            Y_old[j]=Y_new[j];
            // take a step in the unbounded real plane
            X_new[j]=X_old[j]+stepscale*normalRandom();
            Y_new[j]=Y_old[j]+stepscale*normalRandom();
      }}

      // collisions at short timescale, dt
      for (s=0; s<iter_per_movestep; s++){
        // compute local time
        t=t+dt;
        frac=(Time-t)/Dt;
        cfrac=1.-frac;
        // kernel_interpolate
        for (i = 0; i < Nmax; i++ ) {
          if(still_running[i]){
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
            }}}

          // kernel_measure
          for (i = 0; i < Nmax-1; i++ ) {
            if(still_running[i]){
              // each i,j pair is reached once per call to kernel_measure
              for (j = i+1; j < Nmax; j++ ) {
                if(still_running[j]){
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
  }}
printf("simulation complete!\n");

// Print results
printf("\nPrinting Inputs...\n");
printf("r=%g\n",r);
printf("D=%g\n",D);
printf("L=%g\n",L);
printf("kappa=%g\n",kap);
// printf("beta=%g\n",beta);
printf("reflect=%d\n",reflect);
printf("set_second=%d\n",set_second);
printf("niter=%d\n",niter);
printf("dt=%g\n",dt);
printf("Dt=%g\n",Dt);

// if (set_second==1){
//   printf("Rad=%g\n",Rad);
// }

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

return 0;
}
