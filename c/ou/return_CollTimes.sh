#!/bin/bash
# module load py-numpy
# module load py-pandas
# clear
# date
FN_IN=$1
TMP_IN='tmp.input'
perl deprecate_inputs.pl < $FN_IN > $TMP_IN

#TODO(simpler): just pick Nmax and hold it fixed...
#TODO(?): parse input passed to x_run.sh
Nmin=6
Nmax=100
echo "Nmin is $Nmin and Nmax is $Nmax"

# perl deprecate_inputs.pl < 1-control.input > $TMP_IN
#TODO: shift outputs to be on the same line and comma separated
#TODO: dev run.sh, which takes 1 line of arguments, saves them to params.input
#TODO: print results of original params.input up until 'Printing Outputs...'
#TODO: detect Nmax from params.input

#TODO: print N_values on one csv line
#TODO: print Tavg_values on one csv line


# niter=$10
# Process=$11
# $(r) $(D) $(L) $(kappa) $(Dt) $(ntips) $(Process) $(reflect) $(set_second)
# $(1) $(2) $(3) $(4) $(5) $(ntips_batchsize) $(Process_batch) $(8) $(9)

OUT_FN='out.txt'
./return_CollTime.x < $FN_IN > $OUT_FN
#TODO: print log up until Printing Outputs...
perl prepare-CollTimes.pl < $OUT_FN


# let ntips_batchsize=10
# Process_batch=$Process
# numberof_batches=$ntips/$ntips_batchsize
# SUM_FN='sum.csv'

# echo $SUM_FN
# echo $OUT_FN
# Nmin=11
# Nmax=200
# run the simulation with a small cache size
# let foo=./xrun.sh

#print N_values
ntips=$Nmax
while [ $ntips -ge $Nmin ]
do
  #TODO: dev/test the following to compute Tavg given N and params
  #TODO(then): append Tavg to an array of double precision floats (...OR some temporary .csv file)
  # Process_batch=$((Process_batch*Process_batch))
  # Process_batch=($Process_batch * $Process_batch)

  printf "%d," $ntips
  ntips=$[$ntips-1]
  # shift
done
printf "\n"
#print Tavg_valuess
ntips=$Nmax
while [ $ntips -ge $Nmin ]
do
  ntips=$[$ntips-1]
  perl deprecate_inputs.pl < $TMP_IN > $FN_IN
  cp $FN_IN $TMP_IN
  export Tavg=$(./return_CollTime.x < $FN_IN | grep 'Tavg=' | grep -Eo '[+-]?[0-9]+([.][0-9]+)?')
  printf "%f," $Tavg
  # printf "$Tavg"
  # shift
done
printf "\n"
# date

  #TODO: modify the nth entry of an array in perl
  #TODO: echo parameters to FN_IN in the N field
  # TODO: copy input to params.input as in
  # perl dev/test-return-CollTimes.pl < 1-control.input > $OUT_FN
  # ./xrun.sh $(1) $(2) $(3) $(4) $(5) $(6) $(7) $(8) $(9) $(10) $niter_batchsize $Process_batch $(13) $(14) $(15) $(16) > $OUT_FN
  # grep 'Tavg=' $OUT_FN #| grep -Eo '[+-]?[0-9]+([.][0-9]+)?';
  # # echo $Process_batch
  # ./xrun.sh $(1) $(2) $(3) $(4) $(5) $(6) $(7) $(8) $ntips $(10) $Process $(13) $(14) $(15) $(16) > $OUT_FN
  #  # grep "Tavg=" $OUTFN #| grep -Eo '[+-]?[0-9]+([.][0-9]+)?'
  #  grep 'Tavg=' $OUTFN | grep -Eo '(?=(\d+))\w+\1'
  # # /*                              |
  # # |  Record Mean Collision Times  |
  # # |                              */
  # # // print mean output of T_lst to stdout
  # # printf("\nPrinting Outputs...\n");
  # # printf("exit_code=%d\n",exit_code);
  # # printf("ntips=%d\n",Nmax);
  # # printf("Tcount=%d\n",count_net);
  # # printf("Tsum=%g\n",T_net);
  # # printf("Tavg=%g\n",T_net/count_net);
  #
  # # TODO: parse the response to the simulation
  # grep 'exit_code=' $OUTFN #| grep -Eo '[+-]?[0-9]+([.][0-9]+)?'
  # grep 'ntips=' $OUTFN #| grep -Eo '[+-]?[0-9]+([.][0-9]+)?'
  # grep "Tcount=" $OUTFN #| grep -Eo '[+-]?[0-9]+([.][0-9]+)?'
  # grep "Tsum=" $OUTFN #| grep -Eo '[+-]?[0-9]+([.][0-9]+)?'
  # # grep "Tavg=" $OUTFN #| grep -Eo '[+-]?[0-9]+([.][0-9]+)?'
  # grep 'Tavg=' $OUTFN | grep -Eo '(?=(\d+))\w+\1'
  # ntips=$[$ntips-1]

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
  # python3 python/parse_output_remote.py $OUT_FN $SUM_FN
  # ntips_net=$ntips_net+$ntips_batchsize
# done

#TODO: print $OUTFN up to Printing Outputs

#   count=$((count + 1))
#   ntips_net=$((ntips_net + ntips_batchsize))
#   Process_batch=$((Process_batch * (Process_batch + 1) % 1000000))
# }
# done
# echo "The sum of the {$(ntips)} trials is:"
# python3 python/print_summary.py $OUT_FN $SUM_FN
# TODO: printin put
