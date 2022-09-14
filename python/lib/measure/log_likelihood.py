#log_likelihood.py
#Programmer: Tim Tyree
#Date: 9.13.2022
import numpy as np, pandas as pd

def comp_log_likelihood_ols(se_values,
                            s = None, #input parameter
                            **kwargs):
    """comp_log_likelihood_ols computes log_likelihood for linear regression
    evaluated at the closed-form maximum likelhood estimator from Eqn. 1-3 from src.
    If posterior root variance, s, is None, then s is set to the apparent
    root mean squared error (rmse), which is the maximum likelihood estimate (mle) of s for the ols prior.

    __log-likliehood for linear regression:__
    $$L(b_0,b_1,s^2) = \log \Pi_{i=1}^n p(y_i | x_i; b_0,b_1,s^2)$$
    $$...$$
    $$L(b_0,b_1,s^2) = -\frac{n}{2}\log 2\pi - n\log s -\frac{1}{2s^2}\sum_{i=1}^n(y_i - (b_0 +b_1x_i))^2$$

    src: https://www.stat.cmu.edu/~cshalizi/mreg/15/lectures/06/lecture-06.pdf/

    Example Usage:
se_values = (np.log(w_values)-np.log(what_values))**2
ll = comp_log_likelihood_ols(se_values)
    """
    n = se_values.shape[0]
    if s is None:
        rmse = np.sqrt(np.mean(se_values)) # float(rmse) #
        s=float(rmse)
    sSq = s**2
    if (not np.isclose(sSq,0.) & (s>1e-2)):
        ll = float(-0.5*n*np.log(2.*np.pi))
        ll = ll - float(n*np.log(s))
        ll = ll - float(np.sum(se_values)/(2.*sSq))
    else:
        ll=np.nan
    return ll
