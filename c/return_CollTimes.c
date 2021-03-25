/* Program to compute using Monte Carlo methods */
// the variable number of diffusing particles is handled by still_running
#include "CommonDefines.h"

// // using namespace std;
int main(int argc, char* argv[])
{
   /* parse exteral inputs */
   double r,D,L,refl,nite,kap;
   printf("Enter the minimum radius (cm): ");
   scanf("%le",&r);printf("r=%le",r);
   printf("\nEnter the diffusion coefficient (cm^2/s): ");
   scanf("%le",&D);printf("D=%le",D);
   printf("\nEnter the domain width/height (cm): ");
   scanf("%le",&L);printf("L=%le",L);
   printf("\nEnter the reaction rate (Hz): ");
   scanf("%le",&kap);printf("kap=%le",kap);
   // printf("\nUse reflecting boundary conditions (1/0)? ");
   // scanf("%le",&refl);
   // int reflect=(int)refl;printf("reflect=%d",reflect);
   printf("\nEnter the number of trials: ");
   scanf("%le",&nite);
   int niter=(int)nite;printf("niter=%d\n",niter);
   int Nmax=70; int Nmin=11;
   double dt=1e-5;             // Time step size.
   int i,j;double x[Nmax];double y[Nmax];double T[Nmax];
   bool still_running[Nmax];
   double stepscale=sqrt(2*D*dt);
   double distmat[Nmax][Nmax];double dist; bool in_range;
   // TODO: randomize seed.  via the latin square/hypercube?
   // srand(RAND_MAX);

   /* initialize uniform random points in the unit square n*/
   double t=0.;
   for (j = 0; j < Nmax; j++ ) {
     x[j] = L*uniformRandom();
     y[j] = L*uniformRandom();
     T[j] = -9999.;
     still_running[j]=true;
   }

   // TODO: compute the matrix of all distances between particles

   for (i = 0; i < Nmax; i++ ) {
     for (j = i; j < Nmax; j++ ) {
       dist=dist_pbc(x[i],y[i],x[j],y[j],L);
       distmat[i][j]=dist;
       in_range=dist<r;
       // if two particles are in range
       if(in_range){
         // determine whether those two particles react
         // % Probabilities of reaction happening in interval dt based on particle
         // % distance and rate.
         // probs = triu(rrate(Dist,kap,minDistance),1)*dt;
         //
         // TestProb = rand(Numb,Numb);         % Generate N^2 uniformly dist random
         //                                     % numbers to compare to the
         //                                     % probabilities of an event occuring
         //                                     % based on pairwise interactions.
         // TestAns = logical(TestProb < probs);
         // if sum(TestAns,'all') > 0
         //     flag = 1;
         // end
       }
     }
   }

   printf("\nPrinting some distances...\n");
   for (j = 0; j < 3; j++ ) {
      printf("d%d = %.3le cm\n", j, distmat[j][j+2]);
   }






   /* take one normal step for each particle, enforcing periodic boundary conditions */
   for (j = 0; j < Nmax; j++ ) {
     // take step
     x[j]=pbc(x[j]+stepscale*normalRandom(),L);
     y[j]=pbc(y[j]+stepscale*normalRandom(),L);
   }
   t=t+dt;





   printf("\nPrinting some final locations...\n");
   for (j = 0; j < 3; j++ ) {
      printf("p%d = (%.3le,%.3le) cm\n", j, x[j],y[j] );
   }
    return 0;
}
