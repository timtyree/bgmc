#!/bin/bash
module load python/3.7.0
python3 -m venv pyenv
source pyenv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install numba pandas
#python3 -m pip install scikit-image trackpy scikit-learn
#python3 -m pip install pandas scipy matplotlib
#python3 -m pip install scikit-learn cython scikit-image gdown
tar czf pyenv.tar.gz pyenv
deactivate
