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
   int niter=(int)nite;printf("niter=%d\n",niter);
   /* initialize random numbers */
   srand(RAND_MAX);

   double x,y;
   int i,j;
   int count=0; /* # of points in the 1st quadrant of unit circle */
   double z;
   double pi;


   /* TODO: transcribe pm's code to c */
   // /* initialize random elements of array n*/

   /* TODO: initialize queue of N particle positions */

   /* TODO: initialize queue of N particle positions */






   int Nmax = 15;
   // double n[Nmax] = randu(Nmax);

   double u[Nmax];// = randu(Nmax);
   /* print each array element's value */
   for (j = 0; j < Nmax; j++ ) {
     u[j] = uniformRandom();
      printf("Uniform Element[%d] = %le\n", j, u[j] );
   }
   double n[Nmax];// = randn(Nmax);
   /* print each array element's value */
   for (j = 0; j < Nmax; j++ ) {
     n[j] = normalRandom();
      printf("Normal Element[%d] = %le\n", j, n[j] );
   }

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
