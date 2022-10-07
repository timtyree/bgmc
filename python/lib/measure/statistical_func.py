# statistical_func.py
#Programmer: Tim Tyree
#Date: 10.7.2022
import scipy.stats as stats
# import numpy as np

def print_statistical_tests(err_values,printing=True):
    """print_statistical_tests prints statistical tests
    and then returns a dictionary of the p-values.

    err_values is a 1D numpy.array instance
    with the hypothetical expected value substracted
    from repeated observation of that same value.

    Example Usage:
dict_ptests = print_statistical_tests(err_values,printing=True)
    """
    num_obs = err_values.shape[0]
    statistic, p_wilcoxon = stats.wilcoxon(err_values)
    statistic, p_ttest = stats.ttest_1samp(err_values,0.)
    statistic, p_normal = stats.normaltest(err_values)
    if printing:
        print(f"""statistical tests:
        {num_obs=:d}
        {p_wilcoxon=:.8f}
        {p_ttest=:.8f}
        {p_normal=:.8f}
        """)
    dict_ptests = dict(
        num_obs=num_obs,
        p_wilcoxon=p_wilcoxon,
        p_ttest=p_ttest,
        p_normal=p_normal)
    return dict_ptests
