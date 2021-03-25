/* Program to compute using Monte Carlo methods */
// the variable number of diffusing particles is handled by still_running
#include "CommonDefines.h"

// // using namespace std;
int main(int argc, char* argv[])
{
   /* parse exteral inputs */
   double r,D,L,nite,kap;
   printf("Enter the minimum radius (cm): ");
   scanf("%le",&r);printf("r=%le",r);
   printf("\nEnter the diffusion coefficient (cm^2/s): ");
   scanf("%le",&D);printf("D=%le",D);
   printf("\nEnter the domain width/height (cm): ");
   scanf("%le",&L);printf("L=%le",L);
   printf("\nEnter the reaction rate (Hz): ");
   scanf("%le",&kap);printf("kap=%le",kap);
   // double refl;
   // printf("\nUse reflecting boundary conditions (1/0)? ");
   // scanf("%le",&refl);
   // int reflect=(int)refl;printf("reflect=%d",reflect);
   printf("\nEnter the number of trials: ");
   scanf("%le",&nite);
   int niter=(int)nite;printf("niter=%d\n",niter);
   int Nmax=70; int Nmin=11;
   double dt=1e-5;             // Time step size.
   int i,j,k;double x[Nmax];double y[Nmax];double T[Nmax];
   bool still_running[Nmax]; bool any_running=true;
   double stepscale=sqrt(2*D*dt);
   double probreact=kap*dt;
   double distmat[Nmax][Nmax];double dist; bool in_range; bool reacts;
   // TODO: randomize seed.  via the latin square/hypercube?
   // srand(RAND_MAX);

   // double tmax=1000.; // UNCOMMENT_HERE
   double tmax=.1; // COMMENT_HERE

   /* initialize uniform random points in the unit square n*/
   double t=0.;
   for (j = 0; j < Nmax; j++ ) {
     x[j] = L*uniformRandom();
     y[j] = L*uniformRandom();
     T[j] = -9999.;
     still_running[j]=true;
   }

  printf("\nrunning simulation...\n");
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
             if(reacts){
               T[j]=t;
               still_running[j]=false;
               for(k=j+1; k<Nmax; k++){
                 if(still_running[k]){
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
 }

// Print results
printf("\nPrinting Inputs...\n");
printf("r=%le",r);
printf("D=%le",D);
printf("L=%le",L);
printf("kappa=%le\n",kap);
printf("dt=%le\n",dt);
// printf("niter=%d",niter)

// char names[][] = {"r","D","L","niter","kap","\0"};
// double values[] = {r,D,L,niter,kap};
// printf("names={%s}\n",names[:])
// printf("values={%s}\n",values[:])

printf("\nPrinting Outputs...\n");
printf("stopping times in seconds were:\n{");
for (j = 0; j < Nmax; j++ ) {
  printf("%le, ",T[j]);
}
printf("}");

return 0;
}
