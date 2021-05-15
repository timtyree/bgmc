#!/bin/bash
sum=0
count=0
# TODO: parse input passed to x_run.sh
niter=$6
Process=$7
# $(r) $(D) $(L) $(kappa) $(Dt) $(niter) $(Process) $(reflect) $(set_second)
# $(1) $(2) $(3) $(4) $(5) $(niter_batchsize) $(Process_batch) $(8) $(9)

niter_batchsize=10
Process_batch=Process
numberof_batches=$(niter/niter_batchsize)
Nmin=11
Nmax=200
# run the simulation with a small cache size
while (niter_net<niter)
  ./xrun.sh $(1) $(2) $(3) $(4) $(5) $(niter_batchsize) $(Process_batch) $(8) $(9) > out.txt
  # explicitly find the output
  grep -n -E 'Printing Outputs...' out.txt > lineno.txt
  # TODO: add ^this output line to the sum, which is listed in the only line of sum.out
  # TODO:
  # TODO: redirect ^that output in a meaningful way
  count=$((count + 1))
  niter_net=$((niter_net + niter_batchsize))
  Process_batch=$((Process_batch * (Process_batch + 1) % 1000000))
done
echo "The sum of the {$(niter)} trials is:"

TODO: printin put
