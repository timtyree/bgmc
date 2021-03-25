/* Program to compute Pi using Monte Carlo methods */
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#define SEED 35791246
#include "random.h"
#include "pbc.h"
// #include <cstdlib>
// #include <cmath>
// #include <ctime>
// #include <iostream>
// using namespace std;
void main(int argc, char* argv[])
{
   double r,D,L,refl,nite;
   double x,y;
   int count=0; /* # of points in the 1st quadrant of unit circle */
   double z;
   double pi;

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
   srand(SEED);

   /* TODO: transcribe pm's code to c */

   /* TODO: initialize queue of N particle positions */

   /* TODO: initialize queue of N particle positions */

   double n[ 10 ]; /* n is an array of 10 integers */
   int i,j;

   // /* initialize random elements of array n*/
   // for ( i = 0; i < 10; i++ ) {
   //    n[ i ] = rand()/RAND_MAX; /* set element at location i to i + 100 */
   // }

   /* output each array element's value */
   // for (j = 0; j < 10; j++ ) {
   //    printf("Element[%d] = %le\n", j, n[j] );
   // }

   // time_t t;
   //  m = 5;
   //  /* Intializes random number generator */
   //  srand((unsigned) time(&t));
   //  /* Print 5 random numbers from 0 to 49 */
   //  for( i = 0 ; i < m ; i++ ) {
   //     printf("%d\n", rand() % 50);
   //  }

    double sigma = 82.0;
    double Mi = 40.0;
    for(int i=0;i<10;i++) {
      // n[i] = normalRandom()*sigma+Mi;
      n[i] =rand_gen();
       printf("Element[%d] = %le\n", i, n[i] );
    }

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
