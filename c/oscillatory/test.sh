# NOTE: this function does not test whether return_CollTime.c compiles
FN='1-test.input'
# clear
date
gcc return_CollTime.c -o return_CollTime.x -lm
echo $FN
./return_CollTime.x < $FN
date
