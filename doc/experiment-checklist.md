## This is a checklist for updating next run with no changes to pipeline

### Designing a data run (TODO: implement perl methods and append to gen_run_next.sh)
1. design run_next.py using the previous run_prev.py dev'd in the 'dev run design.ipynb'
1. use ./gen_run_next.sh to generate run_next.dat
*/ DONE(implemented into ^that in bash): grab the final 1-4 lines of run_next.dat and put them in run_test.dat /*

1. update return-CollTimes.submit to take run_next.dat...
TODO(later): implement ^that in perl/bash and append to gen_run_next.sh
1. manually make run_test.dat fast (perhaps set niter to 10 or smaller...)
1. update github repo

### Post-processing any previous data
1. (if not already downloaded, download any preexisting data and process/store it.
HINT: try something like ./bgmc/python/lib/logdown.sh

### Cleaning (TODO: implement clean-project.sh in bash, see logdown.sh)
1. rm -r ~/bgmc #remove the whole repository folder on the open science grid.  
TODO(later): can I make the 'y' input automatic?
1. git clone fresh repo on the open science grid.
HINT:
git clone http://github.com/timtyree/bgmc.git

### Job Submission
1. cd current simulation folder
cd ~/bgmc/c/attractive
1. ./gcc.sh;
submit the unit test cloud
condor_submit return-CollTimes-test.submit
1. check whether the tests the entire unit test cloud is reasonably fast and returns reasonable results
./post_process.sh
1. if so, run 
./clean-log.sh 
and then run 
condor_submit return-CollTimes.submit
