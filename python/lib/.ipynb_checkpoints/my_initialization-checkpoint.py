#my_initialization.py
import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns
from scipy import stats

#load the libraries
from . import *
# from .utils.operari import *
#automate the boring stuff
# from IPython import utils
import time, os, sys, re
import dask.bag as db
beep = lambda x: os.system("echo -n '\\a';sleep 0.2;" * x)
if not 'nb_dir' in globals():
    nb_dir = os.getcwd()


darkmode=False
if darkmode:
	# For darkmode plots
	from jupyterthemes import jtplot
	jtplot.style(theme='monokai', context='notebook', ticks=True, grid=False)
    
gpumode=True
if gpumode:
    import cudf