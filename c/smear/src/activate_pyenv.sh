#!/bin/bash
module load python/3.7.0

#unpack virtual python environment and activate it
tar -xzf pyenv.tar.gz
python3 -m venv pyenv
source pyenv/bin/activate &> ignore.txt
