/* Program to compute using Monte Carlo methods */
// the variable number of diffusing particles is handled by still_running
#include "CommonDefines.h"

// // using namespace std;
int main(int argc, char* argv[])
{
   /* parse exteral inputs */
   double r,D,L,kap,nite,see;
   printf("Enter the minimum radius (cm): ");
   scanf("%lg",&r);printf("r=%g",r);
   printf("\nEnter the diffusion coefficient (cm^2/s): ");
   scanf("%lg",&D);printf("D=%g",D);
   printf("\nEnter the domain width/height (cm): ");
   scanf("%lg",&L);printf("L=%g",L);
   printf("\nEnter the reaction rate (Hz): ");
   scanf("%lg",&kap);printf("kap=%g",kap);
   printf("\nEnter the number of trials: ");
   scanf("%lg",&nite);
   int niter=(int)nite;printf("niter=%d\n",niter);
   printf("Enter the randomization seed: ");
   scanf("%lg",&see);
   int seed=(int)see;printf("seed=%d\n",seed);
   // double refl;
   // printf("\nUse reflecting boundary conditions (1/0)? ");
   // scanf("%g",&refl);
   // int reflect=(int)refl;printf("reflect=%d",reflect);
   int Nmax=70; int Nmin=11;
   double dt=1e-5;             // Time step size.
   int i,j,k,q;double x[Nmax];double y[Nmax];double T[Nmax];
   bool still_running[Nmax]; bool any_running;
   double stepscale=sqrt(2*D*dt);
   double probreact=kap*dt;
   double distmat[Nmax][Nmax];double dist; bool in_range; bool reacts;
   double T_lst[niter][Nmax];
   // randomize seed.  TODO(later): randomize seed via the latin square/hypercube
   srand(seed);   

   double tmax=1000.; // UNCOMMENT_HERE
   // double tmax=.1; // COMMENT_HERE 

  printf("\nrunning simulation...\n");
  for (q = 0; q < niter; q++){
    /* initialize uniform random points in the unit square n*/
    double t=0.;
    any_running=true;
    for (j = 0; j < Nmax; j++ ) {
     x[j] = L*uniformRandom();
     y[j] = L*uniformRandom();
     T[j] = -9999.;
     still_running[j]=true;
     // TODO: check if any particles are within the minimum allowable distance
     // TODO: reseed any particles that are within the minimum allowable distance
    }

    while(any_running){
     // kernel_measure
      for (i = 0; i < Nmax-1; i++ ) {
        if(still_running[i]){
          for (j = i+1; j < Nmax; j++ ) {
            if(still_running[j]){
              // compute distance between particles still running
              dist=dist_pbc(x[i],y[i],x[j],y[j],L);
              distmat[i][j]=dist;
              in_range=dist<r;
              // if two particles are in range
              if(in_range){
                // determine whether those two particles react
                reacts=probreact>uniformRandom();
                // TODO(later): try reacting at a rate proportional to suprise (-log(distance))
                if(reacts){
                  T[j]=t;
                  still_running[j]=false;
                  for(k=j+1; k<Nmax; k++){
                    if((still_running[k]) ^ (t>tmax)){
                      T[k]=t;
                      still_running[k]=false;
    }}}}}}}}

    // kernel_onestep
    t=t+dt;
    for (j = 0; j < Nmax; j++ ) {
      if(still_running[j]){
        /* take one normal step for each particle, enforcing periodic boundary conditions */
        x[j]=pbc(x[j]+stepscale*normalRandom(),L);
        y[j]=pbc(y[j]+stepscale*normalRandom(),L);
    }}

    //check if any are running...
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
printf("dt=%g\n",dt);

// print dense output of T_lst to stdout
printf("\nPrinting Outputs...\n");
// TODO: convert .json output to summary statistics?
for(i = 0; i < Nmax;i++){
  printf ("%d,",i);
}
printf ("\n");
/* print*/
for (q = 0; q < niter; q++){
  for(i = 0; i < Nmax;i++){
    printf ("%.7lg,",T_lst[q][i]);
  }
  printf ("\n");
}

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
