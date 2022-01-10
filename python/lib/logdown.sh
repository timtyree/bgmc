#!/bin/bash
# logdown.py
# ssh TimtheTyrant@login05.osgconnect.net '
# cd bgmc/c/attractive;
ssh TimtheTyrant@login05.osgconnect.net '
cd bgmc/c/oscillatory;
rm Log.tar.gz;
./post_process.sh
'
cd ../data
cd osg_output
rm Log.tar.gz;
rm -r Log
scp TimtheTyrant@login05.osgconnect.net:bgmc/c/oscillatory/Log.tar.gz Log.tar.gz
mkdir Log
tar -xzf Log.tar.gz  -o Log

# SAVEFN='run_1.csv'
# SAVEFN='longest_traj_by_area_pbc.csv'
# python3 consolidate-osg-output.py $SAVEFN
# #move result to care
# mv /home/timothytyree/Documents/GitHub/care_worker/python/osg_output/$(SAVEFN).csv /home/timothytyree/Documents/GitHub/care_worker/python/osg_output/longest_traj_by_area_fk_pbc.csv
cd ../../lib
./utils/compute_runtime.py
