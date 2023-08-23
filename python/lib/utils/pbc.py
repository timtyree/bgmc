# //utils for periodic boundary conditions
# // Author: Tim Tyree
# // Date: 6.8.2021
# // Group: Rappel Group, UCSD
from numba import njit
import numpy as np
@njit
def pbc(x, L):
    if(x<0):
        X = x+L
        return X
    if(x>=L):
        X = x-L
        return X
    return x

@njit
def min2(num1, num2):
    if (num1 > num2):
        mn=num2
    else:
        mn=num1
    return mn

@njit
def max2(num1, num2):
    if (num1 < num2):
        mn=num2
    else:
        mn=num1
    return mn

@njit
def sqdiff(x1, x2):
    return pow((x1-x2),2)

@njit
def min3(num1, num2, num3):
    if (num1 > num2 ):
        mn=num2
    else:
        mn=num1
    if (mn>num3):
        mn=num3
    return mn

@njit
def dist_pbc(x1, y1, x2, y2, L):
    # returns the smallest dist of each possible pbc combination
    xsq1 = sqdiff(x1,x2)
    xsq2 = sqdiff(x1,x2+L)
    xsq3 = sqdiff(x1,x2-L)
    ysq1 = sqdiff(y1,y2)
    ysq2 = sqdiff(y1,y2+L)
    ysq3 = sqdiff(y1,y2-L)
    xsq  = min3(xsq1,xsq2,xsq3)
    ysq  = min3(ysq1,ysq2,ysq3)
    return np.sqrt(xsq+ysq)

@njit
def subtract_pbc_1d(x1, x2, L):
    # returns the smallest dist of each possible pbc combination
    dx = x1-x2
    dx1 = x1-x2+L
    dx2 = x1-x2-L
    if (abs(dx1)<abs(dx)):
        dx=dx1;
    else:
        if (abs(dx2)<abs(dx)):
            dx=dx2
    return dx
