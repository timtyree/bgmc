double rrate(double r, double kap, double param){
  // Reaction rate based on base rate kap and interaction distance r between two particles.
  double kappa;
  if(param > r){
    kappa = kap;
  }
  else{
    kappa = 0.;
  }
  return kappa;
}
