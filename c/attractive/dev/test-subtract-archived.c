// TODO: print 2D vector value through a c function that takes pointers
// maybe needed only by rand and srand
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include <stdio.h>
#include <math.h>
#include "../lib/pbc.h"

double dist_pbc_2d(double arr1[2], double arr2[2], double width, double height) {
  double dX = arr1[0]-arr2[0];
  double dY = arr1[1]-arr2[1];
  //TODO: enforce PBC explicitely to compute the smallest possible dX
  double dist=sqrt(pow(dX,2)+pow(dY,2));
  //TODO: return the displacement vector first
  return dist;
}

/* function declaration */
// double dist_pbc_2d(double arr1[2], double arr2[2], double width, double height);

int main () {

   /* an int array with 5 elements */
   int a[2] = {0,1};
   int b[2] = {1,1};
   double dist;

   /* pass pointer to the array as an argument */
   dist = dist_pbc_2d( a, b , 2.,2.) ;

   /* output the returned value */
   printf( "dist= %f ", dist );

   return 0;
}
