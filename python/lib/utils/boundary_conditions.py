# //utils for boundary conditions
# // Author: Tim Tyree
# // Date: 6.8.2021
# // Group: Rappel Group, UCSD
from numba import njit
@njit
def reflection(X, L):
  return L-abs(L-abs(X % 2.*L))
@njit
def periodic(X, L):
  x=X % L
  if (x<0.):
    return x+L
  return x
