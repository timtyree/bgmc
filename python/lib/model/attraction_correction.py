#attraction_correction.py
#Programmer: Tim Tyree
#Date: 1.22.2022
import numpy as np

#####################################################
# results from the mean squared power spectrum limit
#####################################################
#####################################################
# results from the mean squared power spectrum limit
#####################################################
def comp_ahat_mslim(z,a,D,phi):
    """
    correction_mslim returns the real correction value
    that evaluates the expected attraction coefficient
    in terms of the parameters of the oscilatory model
    relative to the lifetime of the particle.

    here, the lifetime of the particle has been taken
    to be exponentially distributed
    with an expected value
    proportional to z.

    Note that z is also
    inversely proportional
    to the dynamic period of oscillation.
    """
    dasum=np.exp(1j*phi)/(1-1j*z)
    dasum-=np.exp(-1j*phi)/(1+1j*z)
    dasum-=np.sin(phi)
    ahat=a+2*D/z*dasum.astype('float')
    return ahat

#####################################################
# results from the mean squared power spectrum limit
#####################################################
def comp_ahat_squared_mslim(z,a,D,phi):
    squared_ahat_values =correction_diffusion(z,a=a,D=D,phi=phi)
    squared_ahat_values+=correction_cross(z,a=a,D=D,phi=phi)
    squared_ahat_values+=a**2
    return np.sqrt(squared_ahat_values)

def correction_diffusion(z,a,D,phi):
    """
    correction_diffusion returns the real correction value
    that evaluates the expected attraction coefficient
    in terms of the parameters of the oscilatory model
    relative to the lifetime of the particle.

    here, the lifetime of the particle has been taken
    to be exponentially distributed
    with an expected value
    proportional to z.

    Note that z is also
    inversely proportional
    to the dynamic period of oscillation.
    """
    dasum=np.sin(phi)**2 - 2.*np.sin(phi)
    dasum+=(1. + 4.*z**2 + 2.*z*np.sin(2.*phi) - np.cos(2.*phi))/(2.+8.*z**2)
    dahat=2.*D**2/z**2
    dahat*=dasum
    return dahat

def correction_diffusion_lr(z,a):
    """
    correction_diffusion_lr returns the correction
    to the attraction coefficient due to diffusion
    as the float expected
    in the mean squared power spectrum limit
    for parameters fit to the Luo-Rudy model.
    """
    return correction_diffusion(z,a,a/2.,phi=0.)

def correction_diffusion_fk(z,a):
    """
    correction_diffusion_lr returns the correction
    to the attraction coefficient due to diffusion
    as the float expected
    in the mean squared power spectrum limit
    for parameters fit to the Fenton-Karma model.
    """
    return correction_diffusion(z,a,a/2.,phi=-np.pi/2.)

def correction_cross(z,a,D,phi):
    """
    correction_cross returns the real correction value
    that evaluates the expected attraction coefficient
    in terms of the parameters of the oscilatory model
    relative to the lifetime of the particle.

    here, the lifetime of the particle has been taken
    to be exponentially distributed
    with an expected value
    proportional to z.

    z = 2 * pi * mean_lifetime / dynamic_period

    Note that z is also
    inversely proportional
    to the dynamic period of oscillation.
    """
    dasum=(np.sin(phi) + 2.*z*np.cos(phi) - z**2*np.sin(phi))/((1. + z**2)**2)
    dasum-=np.sin(phi)
    dahat=D*a/z
    dahat*=dasum
    return dahat

def correction_cross_lr(z,a):
    """
    correction_diffusion_lr returns the cross correction
    to the attraction coefficient
    as the float expected
    in the mean squared power spectrum limit
    for parameters fit to the Luo-Rudy model.
    """
    return correction_cross(z,a,a/2.,phi=0.)

def correction_cross_fk(z,a):
    """
    correction_diffusion_lr returns the cross correction
    to the attraction coefficient
    as the float expected
    in the mean squared power spectrum limit
    for parameters fit to the Fenton-Karma model.
    """
    return correction_cross(z,a,a/2.,phi=-np.pi/2.)
