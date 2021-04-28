date
rm -f params.input
touch params.input
while (( $# > 0 ))    # or [ $# -gt 0 ]
do
    echo "$1" >> params.input
    shift
done

# array=($1 $2 $3 $4 $5 $6 $7 $8 $9 $10 $11 $12)
# echo ${array[@]} > params.input
# echo $1 $2 $3 $4 $5 $6 $7 $8 $9 $10 $11 $12 > params.input
# gcc return_CollTimes.c -o return_CollTimes.x -lm
./return_CollTimes.x < params.input
date
