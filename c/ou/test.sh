FN='test-1.input'
clear
date
gcc return_CollTime.c -o return_CollTime.x -lm
echo $FN
./return_CollTime.x < $FN
date
