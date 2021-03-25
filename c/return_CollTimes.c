/* Program to compute using Monte Carlo methods */
#include "CommonDefines.h"

// // using namespace std;
int main(int argc, char* argv[])
{
   double r,D,L,refl,nite;
   /* parse inputs */
   printf("\nEnter the minimum radius: ");
   scanf("%le",&r);printf("r=%le",r);
   printf("\nEnter the diffusion coefficient: ");
   scanf("%le",&D);printf("D=%le",D);
   printf("\nEnter the domain width/height: ");
   scanf("%le",&L);printf("L=%le",L);
   printf("\nUse reflecting boundary conditions? ");
   scanf("%le",&refl);
   int reflect=(int)refl;printf("reflect=%d",reflect);
   printf("\nEnter the number of trials: ");
   scanf("%le",&nite);
   int Nmax=15;
   int niter=(int)nite;printf("niter=%d\n",niter);
   int i,j;double x[Nmax];double y[Nmax];

   /* TODOing: transcribe pm's code to c */
   /* initialize random numbers to a fixed value */
   // TODOlater: randomize seed?
   // srand(RAND_MAX);
   // TODO: /* initialize uniform random points in the unit square n*/

   for (j = 0; j < Nmax; j++ ) {
     x[j] = L*uniformRandom();
   }
   for (j = 0; j < Nmax; j++ ) {
     y[j] = L*uniformRandom();
   }
   printf("\nPrinting all current locations...\n");
   for (j = 0; j < Nmax; j++ ) {
      printf("p%d = (%.3le,%.3le)\n", j, x[j],y[j] );
   }
   // the number of diffusing particles

   // TODO: compute the distance between the first two particles
   // TODO: compute the matrix of all distances between particles
   // TODO: select which of the first n=11,12,13,...,Nmax moving particles are within range of eachother
   // int n[60];// = 11:70;


   /* TODO: initialize queue of N particle position movements */
   /* TODO: take one normal step, then print particle positions  */






   /* TODO: initialize queue of N particle positions */







   // /* print each array element's value */
   // for (j = 0; j < Nmax; j++ ) {
   //   n[j] = normalRandom();
   //    printf("Normal Element[%d] = %le\n", j, n[j] );
   // }

    return 0;
   // /* this old stuff */
   // count=0;
   // for ( i=0; i<niter; i++) {
   //    x = (double)rand()/RAND_MAX;
   //    y = (double)rand()/RAND_MAX;
   //    z = x*x+y*y;
   //    if (z<=1) count++;
   //    }
   // pi=(double)count/niter*4;
   // printf("\n# of trials= %d , estimate of pi is %g \n",niter,pi);
}
