date
echo "$1 $2 $3 $4 $5 " > params.input
# export UNIQUE_SEED=$(process)
UNIQUE_SEED=$(process)
echo "$(UNIQUE_SEED)" >> params.input 
# gcc return_CollTimes.c -o return_CollTimes.x -lm
./return_CollTimes.x < params.input
date