#!/bin/bash
run_number=48

read -p "Is the current run_number=${run_number}? (y/n)" answer

# echo "notabene: the results are looked for in two places, both in :~/bgmc/c/oscillatory, or the folder indicated in logdown.sh"

case ${answer:0:1} in
    y|Y )
        echo "answer was Yes\nnow downloading results from the osg..."
    ;;
    * )
        echo "answer was No..."
        read -p "Please enter the current integer run_number:" run_number
        #update the first line of this file with the user supplied run_number
        new_line="#!/bin/bash\nrun_number=${run_number}"
        sed -i "1s/.*/$new_line/" logdown_and_process_and_rename.sh
    ;;
esac

#DONE: prompt user for run number
./logdown_and_process.sh
cd ../data/osg_output
#DONE: add support for string parsing, X=14-->$RUN_NUMBER

#TODO: make sure DST is where run_X_all is renamed to and DST is not the folder which run_X_all is moved into...
DST=run_${run_number}_all
DST_FN=run_${run_number}_all.csv
#clear any previous cache
rm $DST_FN
rm -r $DST
rmdir $DST
#move results to cache
mv run_X_all ${DST}
mv run_X_all.csv $DST_FN
#then compute
#inputs: all trial parameters
#outputs: apparent m,M with their summary statistics
