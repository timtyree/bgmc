FN='lrtest.input'
clear
date
gcc return_CollTimes_cc.c -o return_CollTimes.x -lm
echo $FN
./return_CollTimes.x < $FN
date
