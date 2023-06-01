FN='lrtest.input'
clear
date
# gcc return_CollTimes_cc.c -o return_CollTimes.x -lm # <<<uniformly reinitialized linear particle model
gcc return_CollTimes_cc.c -o return_CollTimes.x -lm # <<<modified linear particle model
# gcc return_CollTimes_cc_levy.c -o return_CollTimes.x -lm  # <<<modified levy particle model
echo $FN
./return_CollTimes.x < $FN
date
