#include <stdio.h>
// maybe needed only by rand and srand
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>
#include <time.h>
/* function to generate and return random numbers */
int * getRandom( ) {

   static int  v[2];
   int i;

   /* set the seed */
   srand( (unsigned)time( NULL ) );

   for ( i = 0; i < 2; ++i) {
      v[i] = rand();
      printf( "drew rv, v[%d]    , %d\n", i, v[i]);
   }

   return v;
}

/* main function to call above defined function */
int main () {

   /* a pointer to an int */
   int *p;
   int i;

   p = getRandom();

   for ( i = 0; i < 2; i++ ) {
      printf( "point to *(p + %d), %d\n", i, *(p + i));
   }

   return 0;
}
