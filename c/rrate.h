double rrate(double r, double kap, double Param){
  // Reaction rate based on base rate kap and interaction distance r between two particles.
  double kappa;
  if(Param > r){
    kappa = kap;
  }
  else{
    kappa = 0.;
  }
  return kappa;
}
