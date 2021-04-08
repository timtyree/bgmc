/* Program to compute using Monte Carlo methods */
// the variable number of diffusing particles is handled by still_running
#include "CommonDefines.h"

// // using namespace std;
int main(int argc, char* argv[])
{
   /* parse exteral inputs */
   double r,D,L,kap,nite,see,beta,refl,set_sec;
   printf("Enter the reaction range (cm): ");
   scanf("%lg",&r);printf("r=%g",r);
   printf("\nEnter the diffusion coefficient (cm^2/s): ");
   scanf("%lg",&D);printf("D=%g",D);
   printf("\nEnter the domain width/height (cm): ");
   scanf("%lg",&L);printf("L=%g",L);
   printf("\nEnter the reaction rate (Hz): ");
   scanf("%lg",&kap);printf("kappa=%g",kap);
   printf("\nEnter the reaction scale (cm): ");
   scanf("%lg",&beta);printf("beta=%g",beta);
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
   double dt=1e-5;             // Time step size.
   int i,j,k,q;double x[Nmax];double y[Nmax];double T[Nmax];
   bool still_running[Nmax]; bool any_running; bool all_valid;
   double stepscale=sqrt(2*D*dt);
   double probreact=kap*dt; double sig;
   double distmat[Nmax][Nmax];double dist; bool in_range; bool reacts;
   double T_lst[niter][Nmax]; double net_T; double T_value;
   // randomize seed.  TODO(later): randomize seed via the latin square/hypercube
   srand(seed);

   double tmax=1000.; // UNCOMMENT_HERE
   // double tmax=.1; // COMMENT_HERE

  printf("\nrunning simulation...\n");
  /* for each trial... */
  for (q = 0; q < niter; q++){
    /* initialize uniform random points in the unit square n*/
    double t=0.;
    any_running=true;
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
      double Rad = r*uniformRandom();
      double Theta = 2.*3.141592653589793*uniformRandom();
      if (reflect==0){
        x[1]=pbc(x[0]+Rad*cos(Theta),L);
        y[1]=pbc(y[0]+Rad*sin(Theta),L);
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

    /* run simulation for given trial */
    while(any_running){
      // kernel_onestep
      t=t+dt;
      for (j = 0; j < Nmax; j++ ) {
        if(still_running[j]){
          if (reflect==0){
            /* take one normal step for each particle, enforcing periodic boundary conditions */
            x[j]=pbc(x[j]+stepscale*normalRandom(),L);
            y[j]=pbc(y[j]+stepscale*normalRandom(),L);
          }else{
            x[j]=x[j]+stepscale*normalRandom();
            y[j]=y[j]+stepscale*normalRandom();
            //enforce RBC for x coordinate
            if (x[j]>L){
              x[j]=2.*L-x[j];
            }else if(x[j]<0){
              x[j]=-1.*x[j];
            }
            //enforce RBC for y coordinate
            if (y[j]>L){
              y[j]=2.*L-y[j];
            }else if(y[j]<0){
              y[j]=-1.*y[j];
      }}}}

      // kernel_measure
      for (i = 0; i < Nmax-1; i++ ) {
        if(still_running[i]){
          // each i,j pair is reached once per call to kernel_measure
          for (j = i+1; j < Nmax; j++ ) {
            if(still_running[j]){
              // compute distance between particles that are still running
              if (reflect==0){
                dist=dist_pbc(x[i],y[i],x[j],y[j],L);
                distmat[i][j]=dist;
              }else{
                dist=dist_eucl(x[i],y[i],x[j],y[j]);
              }
              in_range=true;//dist<r;
              // if two particles are in range
              if(in_range){
                // determine whether those two particles react
                sig=sigmoid(dist, r, beta);
                reacts=probreact*sig>uniformRandom();
                if(reacts){
                  T[j]=t;
                  still_running[j]=false;
                  for(k=j+1; k<Nmax; k++){
                    if((still_running[k]) ^ (t>tmax)){
                      T[k]=t;
                      still_running[k]=false;
    }}}}}}}}

    //check if any are still running...
    any_running=false;
    for (j = Nmin; j < Nmax; j++ ) {
      if(still_running[j]){
        any_running=true;
    }}
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
printf("beta=%g\n",beta);
printf("reflect=%d\n",reflect);
printf("set_second=%d\n",set_second);
printf("niter=%d\n",niter);
printf("dt=%g\n",dt);

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
