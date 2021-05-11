double sigmoid(double x, double r, double beta){
  // returns radially dependent scale that is 0 at x=0, 1/2 at x=r, and 0 at x=infinity.
  // a sigmoidal function at location r with scale beta.
  return 1./(1. + exp((x - r)/beta));
}