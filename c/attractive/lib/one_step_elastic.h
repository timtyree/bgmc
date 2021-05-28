TODO: make functional acceleration between two particles s.t. it is proportional to the disagreement between the present length and the equilibrium length, R
double[2] comp_spring_force(x1,y1,x2,y2,R,varkappa){
	//TODO: compute the force between two points
}


// DONE: double comp_distance_pbc(x1,y1,x2,y2,width,height){...}
double[2] comp_displacement_viscous(Fx,Fy,gamma){
	//compute the viscous displacement given a net force and given the ratio of the mass to the damping factor, gamma.
	return Fx/gamma,Fy/gamma
}


// double uniformRandom() {
//    // return a uniformly distributed random value
//    return ( (double)(rand()) + 1. )/( (double)(RAND_MAX) + 1. );
// }
// double normalRandom() {
//    // return a normally distributed random value
//    double v1=uniformRandom();
//    double v2=uniformRandom();
//    return cos(2.*3.141592653589793*v2)*sqrt(-2.*log(v1));
// }

// // double * randu(int N){
// //   /* generate a vector of N uniform random variables on the unit interval */
// //   double n[N];
// //   for(int i=0;i<N;i++) {
// //     n[i] =uniformRandom();
// //   }
// //   return n;
// // }
// //
// // double * randn(int N){
// //   /* generate a sample vector of N classical normal random variables */
// //   double n[N];
// //   for(int i=0;i<N;i++) {
// //     n[i] = normalRandom();//*sigma+Mi;
// //   }
// //   return n;
// // }

// #include <stdio.h>
