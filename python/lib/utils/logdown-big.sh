# logdown.py
#suppose preprocessed already (solves timeout with broken pipe)
# ssh TimtheTyrant@login05.osgconnect.net '
# cd bgmc/c/gev;
# rm Log.tar.gz;
# ./post_process.sh
# '
cd ../../data
cd osg_output
scp TimtheTyrant@login05.osgconnect.net:bgmc/c/hybrid_modes/Log.tar.gz Log.tar.gz
# scp TimtheTyrant@login05.osgconnect.net:bgmc/c/gev/Log.tar.gz Log.tar.gz
tar -xzf Log.tar.gz

# SAVEFN='run_1.csv'
# SAVEFN='longest_traj_by_area_pbc.csv'
# python3 consolidate-osg-output.py $SAVEFN
# #move result to care
# mv /home/timothytyree/Documents/GitHub/care_worker/python/osg_output/$(SAVEFN).csv /home/timothytyree/Documents/GitHub/care_worker/python/osg_output/longest_traj_by_area_fk_pbc.csv
cd ../../lib
./utils/compute_runtime.py
