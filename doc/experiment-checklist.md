## This is a checklist for updating next run with no changes to pipeline

### Designing a data run (TODO: implement perl methods and append to gen_run_next.sh)
1. design run_next.py from the previous run_prev.py
1. use ./gen_run_next.sh to generate run_next.dat
1. (implement in perl, append to gen_run_next.sh) grab the final 1-4 lines of run_next.dat and put them in run_test.dat
1. (implement in perl, append to gen_run_next.sh) update non-test submit file to take run_next.dat
1. manually make run_test.dat fast (perhaps set niter to small)
1. update github repo

### Post-processing any previous data
1. (if not already downloaded, download any preexisting data and process/store it.

### Cleaning (TODO: implement clean-project.sh in bash, see logdown.sh)
1. rm whole repository folder on the open science grid.
1. git clone fresh repo on the open science grid.

### Job Submission
1. cd current simulation folder
1. submit the unit test cloud
1. if the entire unit test cloud is reasonably fast and returns reasonable results, submit the main cloud...
