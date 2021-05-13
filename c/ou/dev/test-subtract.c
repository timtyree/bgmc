#include <stdio.h>
// maybe needed only by rand and srand
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "../lib/pbc.h"

/* example function to generate and return random numbers */
// int * getRandom( ) {
//
//    static int  v[2];
//    int i;
//
//    /* set the seed */
//    srand( (unsigned)time( NULL ) );
//
//    for ( i = 0; i < 2; ++i) {
//       v[i] = rand();
//       printf( "drew rv, v[%d]    , %d\n", i, v[i]);
//    }
//
//    return v;
// }

/* main function to call above defined function */
int main () {
  double L=2.;

  double v1[2]={0.1,0.1};
  double v2[2]={1.9,1.9};
  //dist is 0.28

  // double v1[2]={-0.1,-0.1};
  // double v2[2]={2.1,2.1};
  // //dist is 0.28

  // double v1[2]={0,0};
  // double v2[2]={0.,2.1};
  // //dist is 0.1

  // double v1[2]={2,0};
  // double v2[2]={0,0};
  // //dist is 0
  // double v1[2]={1,0};
  // double v2[2]={0,1};
  // //dist is 1.41

  int i;
  for ( i = 0; i < 2; i++ ) {
    printf( "*(v1 + %d), %.2f\n", i, *(v1 + i));
  }
  for ( i = 0; i < 2; i++ ) {
    printf( "*(v2 + %d), %.2f\n", i, *(v2 + i));
  }
  double dx = subtract_pbc_1d(v1[0],v2[0],L);
  double dy = subtract_pbc_1d(v1[1],v2[1],L);
  double dist = sqrt(dx*dx+dy*dy);//norm(dx,dy);

  printf( "provided that L is %.2f\n", L);
  printf( "periodic displacement in x is %.2f\n", dx);
  printf( "periodic displacement in y is %.2f\n", dy);
  printf( "^their pbc distance is dist is %.2f\n", dist);

  return 0;
}
