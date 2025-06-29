#!/bin/bash

tar -xzf my_env.tar.gz
export PYTHONPATH=$PWD/my_env

date
rm -f params.input
touch params.input
while (( $# > 0 ))    # or [ $# -gt 0 ]
do
  echo "$1" >> params.input
    # printf "%\n" $1 >> params.input
    shift
done
python3 run_faster_logger.py < params.input
# python3 run_faster.py < params.input
# python3 run.py < params.input
# python3 run.py $1 $2 $3 $4 $5 $6 $7 $8 $9 $10 $11 $12 $13 $14 $15
date
