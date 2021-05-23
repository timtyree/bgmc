#!/bin/bash
date
rm -f params.input
touch params.input

## Confusion ##
# # store arguments in a special array
# args=("$@")
# # get number of elements
# ELEMENTS=${#args[@]}
# echo $ELEMENTS
#
# # echo each element in array
# # for loop
# for (( i=0;i<$ELEMENTS;i++)); do
#     echo ${args[${i}]}
# done
#
# while (( "$#" )); do
#  echo $1
#  shift
# done

while (( $# > 0 ))    # or [ $# -gt 0 ]
do
  echo "$1" >> params.input
    # printf "%\n" $1 >> params.input
    shift
done
# gcc return_CollTime.c -o return_CollTime.x -lm
./return_CollTimes.sh params.input
date
