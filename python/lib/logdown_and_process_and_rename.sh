#TODO: prompt user for run number
./logdown_and_process.sh
cd ../data/osg_output
#TOOD: add support for string parsing, 14-->$RUN_NUMBER
mv run_X_all run_14_all
mv run_X_all.csv run_14_all.csv
#TODO: integrate m,M observation into process
#output row maps all trial parameters to the apparent m,M with their summary statistics
