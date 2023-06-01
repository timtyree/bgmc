# pylib.py
import numpy as np
from numba import njit
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

@njit
def reflection(X, L):
  return L-abs(L-abs(X % 2.*L))
@njit
def periodic(X, L):
  x=X % L
  if (x<0.):
    return x+L
  return x

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



# @njit
def format_particles(frameno,t,x_values,y_values,pid_values,round_t_to_n_decimals=5):
    n_tips = x_values.shape[0]
    dict_out = {
        'frame':frameno,
        't': np.around(t,round_t_to_n_decimals),
        'n': n_tips,
        'x': x_values,
        'y': y_values,
        'particle':pid_values,
    }
    return dict_out

from numba import jit,njit
@njit
def normalRandom():
    return np.random.normal()

@njit
def uniformRandom():
    return np.random.uniform(0,1)
# normalRandom(),uniformRandom()

@njit
def levyRandom2D(alpha):
    th = 2*np.pi*np.random.uniform(0,1)
    ul = np.random.uniform(0,1)**(-1./alpha)
    dWx = ul*np.cos(th)
    dWy = ul*np.sin(th)
    return np.array([dWx,dWy])
# dWx,dWy = stepscale*levyRandom2D(alpha)
# dWx,dWy
