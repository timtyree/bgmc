echo '''lambda x:True''' > utils/logdown.input
echo '''run_X_all''' >> utils/logdown.input
./logdown.sh
./utils/filter_folder.py < utils/logdown.input
#NOTA BENE: value in  utils/logdown.input can be used to query the pandas dataframe, x.
