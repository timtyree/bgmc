date
rm -f params.input
touch params.input
while (( $# > 0 ))    # or [ $# -gt 0 ]
do
    echo "$1" >> params.input
    shift
done
# gcc return_CollTimes.c -o return_CollTimes.x -lm
./return_CollTimes.x < params.input
date
