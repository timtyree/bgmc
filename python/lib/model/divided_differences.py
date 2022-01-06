# divided_differences.py
#Programmer: Tim Tyree
#Date: 1.5.2022
#This program functionally / recursively defines the coefficients for a polynomial that goes through every point.
import numpy as np
######################
#  Simplest Case: 1D #
######################
# Nota Bene(but really this numerical method should also work in N+M dimensional data,
# so long as the first axis indexes the observations)
def divided_differences_eval(x,a_values,x_values):
    '''returns the evaluate of the polynomial fit by fit_divided_differences
    Example Usage:
a_values=divided_differences_fit(x_values,y_values)
yhat_values=divided_differences_eval(x=x_values,a_values=a_values,x_values=x_values)
assert yhat_values==y_values
    '''
    out=a_values[0]#a0
    if a_values.shape[0]==1:
        return out
    for i,xi,ai in enumerate(zip(x_values[1:],a_values[1:])):
        #compute term
        term=ai
        for xj in x_values[:i]:
            term*=(x-xj)
        out+=term
    return out

def divided_differences_fit(x_values,y_values):
    '''returns the fit of the polynomial fit by fit_divided_differences
        Example Usage:
    a_values=divided_differences_fit(x_values,y_values)
    yhat_values=divided_differences_eval(x=x_values,a_values=a_values,x_values=x_values)
    assert yhat_values==y_values
        '''
    return divided_difference(x_values,y_values)

def divided_difference(x_values,y_values):
    """Let $$
    f[x_i]=f(x_i)
    $$, and let $$
    f[x_{i},x_{i+1},...,x_{i+k}]= \frac{f[x_{i+1},x_{i+2},...,x_{i+k}] - f[x_i,x_{i+1},...,x_{i+k-1}]}{x_{i+k} - x_i}
    $$."""
    if y_values.shape[0]==1:
        return y_values[0] #a0=f[xi]=f(xi)
    a_values =divided_difference(x_values[1:],y_values[1:])
    a_values-=divided_difference(x_values[:-1],y_values[:-1])
    a_values/=x_values[-1]-x_values[0]
    return a_values

#DONE: dev arbitrary N channel to M channel interpolation
#DONT: add support for memoization using either
#(i) a class
#(ii) ctrl+F in Github/ for memoization
# DONT do ^that bc precomputation of y_values makes memoization unnecessary...

#TODO: use divided_differences.py to map a circle path embedded in $\mathbb{R}^3$ to the local curvature tensor (in $\mathbb{R}^{2 \times 2}$?)
#HINT:
# a_values=divided_differences_fit(x_values,y_values)
# yhat_values=divided_differences_eval(x=x_values,a_values=a_values,x_values=x_values)
# assert yhat_values==y_values
