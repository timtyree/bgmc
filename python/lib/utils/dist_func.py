# for computing the distance between points.  Periodi
# Tim Tyree
# 6.8.2021

import numpy as np
from numba import njit, jit, float32

#############################################################
# Example Usage: L2 Distance using Periodic Boundary Conditions
# distance_L2_pbc = get_distance_L2_pbc(width=200,height=200)
# distance_L2_pbc(np.array([1.,1.]),np.array([199.,199.]))
#############################################################

@njit
def pbc_2D(x,y, width, height):
	'''
	(x, y) coordinates that go from 0 to width or height, respectively.
	tight boundary rounding is in use.'''
	if ( x < 0  ):				# // Left P.B.C.
		x = width - 1
	elif ( x > (width - 1) ):	# // Right P.B.C.
		x = 0
	if( y < 0 ):				# //  Bottom P.B.C.
		y = height - 1
	elif ( y > (height - 1)):	# // Top P.B.C.
		y = 0
	return x,y

def get_distance_L2_pbc(width=1,height=1):
    '''returns a function for the euclidean (L2) distance measure for a 2D rectangle with periodic boundary conditions.
    width, height are the shape of that 2D rectangle.'''
    @jit('f8(f8[:],f8[:])', nopython=True)
    def distance_L2_pbc(point_1, point_2):
        '''assumes getting shortest distance between two points with periodic boundary conditions in 2D.  point_1 and point_2 are iterables of length 2'''
        mesh_shape=np.array((width,height))
        dq2 = 0.
        #     for q1, q2, width in zip(point_1[:2], point_2[:2], mesh_shape):
        for q1, q2, wid in zip(point_1, point_2, mesh_shape):
            dq2 = dq2 + min(((q2 - q1)**2, (q2 + wid - q1 )**2, (q2 - wid - q1 )**2))
        return np.sqrt(dq2)
    return distance_L2_pbc
