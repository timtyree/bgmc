
#check argument was entered
if [[ $# -eq 0 ]] ; then
    echo 'Error: missing first argument as path to a *.m file'
    exit 0
fi
# case "$1" in
#     1) echo 'you gave 1' ;;
#     *) echo 'you gave something else' ;;
# esac

#make output directory if it doesn't exist
mkdir -p bin

#compile input .m file to binary
mcc -m -d bin -R -singleCompThread -R -nodisplay -R -nojvm $1
