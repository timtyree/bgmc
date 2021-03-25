double pbc(double x, double L){
  if(x<0){
    double X = x+L;
    return X;
  }
  if(x>=L){
    double X = x-L;
    return X;
  }
  return x;
}
