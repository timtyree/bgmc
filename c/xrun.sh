date
echo "$1 $2 $3 $4 $5 $6" > params.input
# export UNIQUE_SEED=$(process)
# echo $(Process) >> params.input
# gcc return_CollTimes.c -o return_CollTimes.x -lm
./return_CollTimes.x < params.input
date
