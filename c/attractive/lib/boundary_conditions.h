double reflection(double X, double L){
  return L-fabs(L-fabs(fmod(X,2.*L)));
}

double periodic(double X, double L){
  double x=fmod(X,L);
  if (x<0.){
    return x+L;
  }
  return x;
}
