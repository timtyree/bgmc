/* Program to compute Pi using Monte Carlo methods */
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#define SEED 35791246
// void main(int niter)
void main(int argc, char* argv[])
{
   // int niter=0;
   double r,D,L;
   // int reflect=0;
   double refl;
   double nite;
   // int niter=(int)argv[1];
   double x,y;
   int i,count=0; /* # of points in the 1st quadrant of unit circle */
   double z;
   double pi;

   /* parse inputs */
   printf("\nEnter the minimum radius: ");
   scanf("%le",&r);
   printf("\nEnter the diffusion coefficient: ");
   scanf("%le",&D);
   printf("\nEnter the domain width/height: ");
   scanf("%le",&L);
   printf("\nUse reflecting boundary conditions? ");
   scanf("%le",&refl);
   int reflect=(int)reflect;
   printf("\nEnter the number of trials: ");
   scanf("%le",&nite);
   int niter=(int)nite;
   /* initialize random numbers */
   srand(SEED);
   count=0;
   for ( i=0; i<niter; i++) {
      x = (double)rand()/RAND_MAX;
      y = (double)rand()/RAND_MAX;
      z = x*x+y*y;
      if (z<=1) count++;
      }
   pi=(double)count/niter*4;
   printf("# of trials= %d , estimate of pi is %g \n",niter,pi);
}

double pbc(double x, double L){
  if(x<0){
    double X = x+L;
  }
  if(x>=L){
    double X = x-L;
  }
  return X;
}
