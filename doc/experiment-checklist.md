## This is a checklist for updating next run with no changes to pipeline

### Designing a data run (TODO: implement perl methods and append to gen_run_next.sh)
1. design run_next.py using the previous run_prev.py dev'd in the 'dev run design.ipynb'
1. use ./gen_run_next.sh to generate run_next.dat
HINT:
cd c/attractive/src

chmod +x gen_run_18.sh
./gen_run_18.sh
*/ DONE(implemented into ^that in bash): grab the final 1-4 lines of run_next.dat and put them in run_test.dat /*

1. update return-CollTimes.submit to take run_next.dat...
nano ../return-CollTimes.submit
TODO(later): implement ^that in perl/bash and append to gen_run_next.sh
1. manually make run_test.dat fast (perhaps set niter to 10 or smaller...)
nano ../runs/run_test.dat

1. update github repo

### Downloading and Processing any data from the previous run
1. (if not already downloaded, be sure to download any preexisting data and process/store it.
cd ../../../python/lib
<!-- cd ~/Documents/GitHub/bgmc/python/lib -->
./logdown_and_process_and_rename.sh

### Cleaning (TODO: implement clean-project.sh in bash, see logdown.sh)
rm -r ~/bgmc
#^this removes the whole repository folder on the open science grid.  
TODO(later): can I make the 'y' input automatic?
1. git clone fresh repo on the open science grid.
git clone http://github.com/timtyree/bgmc.git

### Job Submission
1. cd current simulation folder
<!-- cd ~/bgmc/c/attractive -->
cd ~/bgmc/c/attractive
./gcc.sh

1. if not done locally, gener run arguments remotely
cd src
chmod +x gen_run_27.sh
./gen_run_27.sh
1. manually make run_test.dat fast (perhaps set niter to 10 or smaller...)
nano ../runs/run_test.dat

1. submit the unit test cloud
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
1. source bash_aliases
1. release

### Downloading and Processing any data from the previous run
cd ~/Documents/GitHub/bgmc/python/lib
./logdown_and_process_and_rename.sh
