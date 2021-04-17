//utils for periodic boundary conditions
// Author: Tim Tyree
// Date: 3.25.2021
// Group: Rappel Group, UCSD
#include <math.h>
#include <stdlib.h>

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

double sqdiff(double x1,double x2){
  return pow((x1-x2),2);
}

double min3(double num1, double num2, double num3) {
    double mn=(num1 > num2 ) ? num2 : num1;
    return (mn > num3 ) ? num3 : mn;
} 

double min2(double num1, double num2, double num3) {
    return (num1 > num2 ) ? num2 : num1;
}

double max2(double num1, double num2) {
    return (num1 < num2 ) ? num2 : num1;
}

double dist_pbc(double x1,double y1,double x2,double y2, double L){
  // returns the smallest dist of each possible pbc combination
  double xsq1 = sqdiff(x1,x2);
  double xsq2 = sqdiff(x1,x2+L);
  double xsq3 = sqdiff(x1,x2-L);
  double ysq1 = sqdiff(y1,y2);
  double ysq2 = sqdiff(y1,y2+L);
  double ysq3 = sqdiff(y1,y2-L);
  double xsq = min3(xsq1,xsq2,xsq3);
  double ysq = min3(ysq1,ysq2,ysq3);
  return sqrt(xsq+ysq);
}
