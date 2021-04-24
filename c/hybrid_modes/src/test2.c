#include <math.h>
#include <stdio.h>

double reflect(double X, double L){
  return L-fabs(L-fabs(fmod(X,2*L)));
}

double periodic(double X, double L){
  double x=fmod(X,L);
  if (x<0.){
    return x+L;
  }
  return x;
}

int main(int argc, char* argv[]){
  double L=5;int i;
  printf ("printing raw values...\n");
  for (i=-6; i<6; i++){
    printf ("%.7lg,",(double)i+0.1);
  }

  printf ("\ntesting rbc...\n");
  for (i=-6; i<6; i++){
    printf ("%.7lg,",reflect((double)i+0.1,L));
  }

  printf ("\ntesting pbc...\n");
  for (i=-6; i<6; i++){
    printf ("%.7lg,",periodic((double)i+0.1,L));
  }

  printf ("\ntests complete!\n");
  return 0;
}
