double uniformRandom() {
   // return a uniformly distributed random value
   return ( (double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
}
double normalRandom() {
   // return a normally distributed random value
   double v1=uniformRandom();
   double v2=uniformRandom();
   return cos(2.*3.141592653589793*v2)*sqrt(-2.*log(v1));
}

// double levyRandom(alpha) {
//     return pow(uniformRandom(),-1./alpha);
// }

double angleRandom() {
  return 2*3.141592653589793*uniformRandom();
}

// double alpha=x0;
// double ul; double th;
// ul=levyRandom(alpha);
// th=angleRandom();
// dWx = ul*cos(th);
// dWy = ul*sin(th);

// double * randu(int N){
//   /* generate a vector of N uniform random variables on the unit interval */
//   double n[N];
//   for(int i=0;i<N;i++) {
//     n[i] =uniformRandom();
//   }
//   return n;
// }
//
// double * randn(int N){
//   /* generate a sample vector of N classical normal random variables */
//   double n[N];
//   for(int i=0;i<N;i++) {
//     n[i] = normalRandom();//*sigma+Mi;
//   }
//   return n;
// }

#include <stdio.h>
