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
  double v1[2]={.9,0.1};
  double v2[2]={1.9,1.9};
  // double v1[2]={0.1,0.1};
  // double v2[2]={1.9,1.9};
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

  printf( "\nprovided that L is %.2f\n", L);
  printf( "periodic displacement in x is %.2f\n", dx);
  printf( "periodic displacement in y is %.2f\n", dy);
  printf( "^their pbc distance is dist is %.2f\n", dist);

  double D=1.;double dt=1.;
  //define new variables
  double x0=1.; double varkappa=1.;
  double gamma=1.; double mass=1.;
  printf( "\nlet their equilib. length be %.2f\n", x0);
  printf( "let their spring constant be %.2f\n", varkappa);
  printf( "let their gamma be %.2f\n", gamma);
  printf( "let their mass be %.2f\n", mass);
  printf( "let their diffusion coef be %.2f\n", D);


  // //compute the spring force prefactor
  // double F=varkappa*(dist-x0);
  // //project F onto impulses in the x,y direction
  // double cos_theta=dx/dist;
  // double sin_theta=dy/dist;
  // double dpx=cos_theta*F*dt/mass;
  // double dpy=sin_theta*F*dt/mass;

  //simplify ^that into three lines
  double impulse_prefactor=varkappa*dt/mass;
  double impulse_factor=impulse_prefactor*(dist-x0)/dist;
  double dpx=dx*impulse_factor;
  double dpy=dy*impulse_factor;


  // printf( "\nspring force prefactor %.2f\n", F);
  printf( "\ndpx is %.2f\n", dpx);
  printf( "dpy is %.2f\n", dpy);
  // double Dx;//=-varkappa*(fabs(dx)-x0)*sign(dx);
  // double Dy;
  // //TODO: compute the acceleration values.  print them
  // printf( "\noutput euclidian displacement in x is %.2f\n", Dx);
  // printf( "output euclidian displacement in y is %.2f\n", Dy);

  return 0;
}
