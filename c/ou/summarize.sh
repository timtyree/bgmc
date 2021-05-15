#!/bin/bash
sum=0
count=0
# TODO: parse input passed to x_run.sh
niter=$6
Process=$7
# $(r) $(D) $(L) $(kappa) $(Dt) $(niter) $(Process) $(reflect) $(set_second)
$(1) $(2) $(3) $(4) $(5) $(niter_batchsize) $(Process_batch) $(8) $(9)

niter_batchsize=10
Process_batch=Process
numberof batches
Nmin=11
Nmax=200
for file in "$@"
while (niter_net<niter)
  ./xrun.sh $(1) $(2) $(3) $(4) $(5) $(niter_batchsize) $(Process_batch) $(8) $(9) > out.txt
  # TODO: search out.txt for -9999 in the first 5 characters of the line
  # TODO: explicitly find the line that starts with -9999.  declare ^this line to be the output_line
  # TODO: add ^this output line to the sum, which is listed in the only line of sum.out
  # TODO:
  # TODO: redirect ^that output in a meaningful way
  count=$((count + 1))
  niter_net=$((niter_net + niter_batchsize))
  Process_batch=$((Process_batch * (Process_batch + 1) % 1000000))
done
echo "The sum of the {$(niter)} trials is:"

TODO: printin put
