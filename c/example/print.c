#include <stdio.h>

// int main()
// {
//   char C = {'q', 'w', 'e', 'r','\0'
// 	'q', 'w', 'e', 'r','\0'};
//   printf("C=%s",C[:]);
//   return 0;
// }


int main()
{
  char a_static[] = {'q', 'w', 'e', 'r','\0'};
  char b_static[] = {'a', 's', 'd', 'f','\0'};
  printf("a_static=%s,b_static=%s",a_static[:],b_static[:]);
  return 0;
}