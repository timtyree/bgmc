#!/bin/bash
# logdown.py
# ssh TimtheTyrant@login05.osgconnect.net '
# cd bgmc/c/attractive_c;
# rm Log.tar.gz;
# ./post_process.sh
# '
# ssh TimtheTyrant@login05.osgconnect.net '
ssh TimtheTyrant@ap21.uc.osg-htc.org '
cd bgmc/c/creation;
rm Log.tar.gz;
./post_process.sh
'
# ssh TimtheTyrant@login05.osgconnect.net '
# cd bgmc/c/oscillatory;
# rm Log.tar.gz;
# ./post_process.sh
# '
cd ../data
cd osg_output
rm Log.tar.gz;
rm -r Log
#beep three times so you know you need to enter the access code again.
echo -n '\\a';sleep 0.2;
echo -n '\\a';sleep 0.2;
echo -n '\\a';sleep 0.2;
# # scp TimtheTyrant@login05.osgconnect.net:bgmc/c/attractive_c/Log.tar.gz Log.tar.gz
# scp TimtheTyrant@login05.osgconnect.net:bgmc/c/attractive/Log.tar.gz Log.tar.gz
# # scp TimtheTyrant@login05.osgconnect.net:bgmc/c/oscillatory/Log.tar.gz Log.tar.gz
scp TimtheTyrant@ap21.uc.osg-htc.org:bgmc/c/creation/Log.tar.gz Log.tar.gz
mkdir Log
tar -xzf Log.tar.gz  -o Log

# SAVEFN='run_1.csv'
# SAVEFN='longest_traj_by_area_pbc.csv'
# python3 consolidate-osg-output.py $SAVEFN
# #move result to care
# mv /home/timothytyree/Documents/GitHub/care_worker/python/osg_output/$(SAVEFN).csv /home/timothytyree/Documents/GitHub/care_worker/python/osg_output/longest_traj_by_area_fk_pbc.csv
cd ../../lib
./utils/compute_runtime.py

#beep three times so you know you can move on with the analysis.
echo -n '\\a';sleep 0.2;
echo -n '\\a';sleep 0.2;
echo -n '\\a';sleep 0.2;
