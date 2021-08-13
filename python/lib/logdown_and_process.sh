echo '''lambda x:True''' > utils/logdown.input
echo '''run_X_all''' >> utils/logdown.input
./logdown.sh
./utils/filter_folder.py < utils/logdown.input
#TODO: compute df from run_7_all.csv
