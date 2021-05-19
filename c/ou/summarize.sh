#!/bin/bash
# module load py-numpy
# module load py-pandas
clear
# sum=0
# count=0
# TODO: parse input passed to x_run.sh
niter=$11
Process=$12
# $(r) $(D) $(L) $(kappa) $(Dt) $(niter) $(Process) $(reflect) $(set_second)
# $(1) $(2) $(3) $(4) $(5) $(niter_batchsize) $(Process_batch) $(8) $(9)

let niter_batchsize=10
let Process_batch=Process
numberof_batches=$niter/$niter_batchsize
SUM_FN=Log/sum.csv
OUT_FN=Log/out.txt
# echo $SUM_FN
# echo $OUT_FN
# Nmin=11
# Nmax=200
# run the simulation with a small cache size
# let foo=./xrun.sh
let niter_net=0
while (($niter_net<$niter))
do
  Process_batch=($Process_batch * $Process_batch)
  echo $niter_batchsize
  echo $Process_batch
  ./xrun.sh $(1) $(2) $(3) $(4) $(5) $(6) $(7) $(8) $(9) $(10) $niter_batchsize $Process_batch $(13) $(14) $(15) $(16) > $OUT_FN
  #DONE: explicitly parse the exit_code
  # exit_code_lineno=grep -n -E 'exit_code=' out.txt
  # explicitly find the output
  # output_lineno=grep -n -E 'Printing Outputs...' out.txt
  # grep -n -E 'Printing Outputs...' out.txt > lineno.txt
  # TODO: add ^this output line to the sum, which is listed in the only line of sum.out
  # TODO: redirect ^that output in a meaningful way
  # TODO(goal): if exit_code_lineno gives exit_code that is not -99, then record the trial!
  # cd python
  # TODO: integrate ^that with the following:
  python3 python/parse_output_remote.py $OUT_FN $SUM_FN
  niter_net=$niter_net+$niter_batchsize
done
#   count=$((count + 1))
#   niter_net=$((niter_net + niter_batchsize))
#   Process_batch=$((Process_batch * (Process_batch + 1) % 1000000))
# }
# done
# echo "The sum of the {$(niter)} trials is:"
# python3 python/print_summary.py $OUT_FN $SUM_FN
# TODO: printin put
