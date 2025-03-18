## This is a checklist for updating next run with no changes to pipeline

### Downloading and Processing any data from the previous run
1. (if not already downloaded, be sure to download any preexisting data and process/store it.
cd ~/Documents/GitHub/bgmc/python/lib
./logdown_and_process_and_rename.sh


### Designing and prepping a data run
1. design run_next.py using the previous run_prev.py dev'd in the 'dev run design.ipynb'
HINT:
cd c/attractive/src

chmod +x gen_run_36.sh

1. update return-CollTimes.submit to take run_next.dat...
nano ../return-CollTimes.submit
TODO(later): implement ^that in perl/bash and append to gen_run_next.sh

1. update github repo

1. ssh-osg and delete old  bgmc.  
rm -rf ~/bgmc

1. then pull bgmc
1. use ./gen_run_next.sh to generate run_next.dat
git clone https://github.com/timtyree/bgmc.git
cd bgmc/c/attractive
./gcc.sh
cd src
chmod +x gen_run_41.sh
./gen_run_41.sh

1. manually make run_test.dat fast (perhaps set niter to 10 or smaller...)
nano ../runs/run_test.dat

### Generating python environment tar bell (if my_env.tar.gz does not exist)
https://portal.osg-htc.org/documentation/software_examples/python/manage-python-packages/
1. load apptainer
cd ~/bgmc/c/creation
singularity shell /cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-ubuntu-20.04:latest
1. install packages
mkdir my_env
export PYTHONPATH=$PWD/my_env
pip3 install --target=$PWD/my_env pandas numpy
exit
1. zip python environment
tar -czf my_env.tar.gz my_env

### Job Submission
1. submit the unit test cloud
cd ~/bgmc/c/attractive
condor_submit return-CollTimes-test.submit

1. check whether the tests the entire unit test cloud is reasonably fast and returns reasonable results
./post_process.sh
HINT: if not, compute what num_trials_per_setting should be so the slowest setting finishes within 10 hours per job
1. if so, run
./clean-log.sh
and then run
condor_submit return-CollTimes.submit

### Releasing held jobs
1. cd ~
1. condor_q --held
1. source bash_aliases
1. release

### Downloading and Processing any data the old way
cd ~/Documents/GitHub/bgmc/python/lib
./logdown_and_process_and_rename.sh

### downloading log files recursively without compression
rsync -avP TimtheTyrant@ap21.uc.osg-htc.org:bgmc/c/creation/Log .

scp -r TimtheTyrant@ap21.uc.osg-htc.org:bgmc/c/creation/Log Log

### Downloading a single file
scp TimtheTyrant@ap21.uc.osg-htc.org:bgmc/c/creation/my_env.tar.gz my_env.tar.gz


### Cleaning (TODO: implement clean-project.sh in bash, see logdown.sh)
rm -rf ~/bgmc
#^this removes the whole repository folder on the open science grid.  
TODO(later): can I make the 'y' input automatic?
1. git clone fresh repo on the open science grid.
git clone http://github.com/timtyree/bgmc.git
