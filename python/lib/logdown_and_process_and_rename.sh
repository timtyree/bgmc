run_number=19
read -p "Is the current run_number=${run_number}? (y/n)" answer

case ${answer:0:1} in
    y|Y )
        echo "answer was Yes\nnow downloading results from the osg..."
    ;;
    * )
        echo "answer was No..."
        read -p "Please enter the current integer run_number:" run_number
        #update the first line of this file with the user supplied run_number
        new_line="run_number=${run_number}"
        sed -i "1s/.*/$new_line/" logdown_and_process_and_rename.sh
    ;;
esac

#TODO: prompt user for run number
./logdown_and_process.sh
cd ../data/osg_output
#TOOD: add support for string parsing, X=14-->$RUN_NUMBER

#TODO: make sure DST is where run_X_all is renamed to and DST is not the folder which run_X_all is moved into...
DST=run_${run_number}_all
DST_FN=run_${run_number}_all.csv
mv run_X_all ${DST}
mv run_X_all.csv $DST_FN
# mv run_X_all run_16_all
# mv run_X_all.csv run_16_all.csv
#TODO: integrate m,M observation into process
#output row maps all trial parameters to the apparent m,M with their summary statistics
