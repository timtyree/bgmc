date
echo "$1 $2 $3 $4 $5 $6 $7 $8 $9" > params.input
# gcc return_CollTimes.c -o return_CollTimes.x -lm
./return_CollTimes.x < params.input
date
