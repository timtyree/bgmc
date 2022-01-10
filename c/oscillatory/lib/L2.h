//utils for periodic boundary conditions
// Author: Tim Tyree
// Date: 4.8.2021
// Group: Rappel Group, UCSD
// #include <math.h>
// #include <stdlib.h>

double _sqdiff(double x1,double x2){
  return pow((x1-x2),2);
}

double dist_eucl(double x1,double y1,double x2,double y2){
  // returns the euclidean distance between two xy positions
  double xsq = _sqdiff(x1,x2);
  double ysq = _sqdiff(y1,y2);
  return sqrt(xsq+ysq);
}
