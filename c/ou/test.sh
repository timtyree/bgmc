FN='test-6.input'
clear
date
gcc return_CollTimes.c -o return_CollTimes.x -lm
echo $FN
./return_CollTimes.x < $FN
date
