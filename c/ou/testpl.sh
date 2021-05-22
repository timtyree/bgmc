date
#Example Usage, test.pl.sh < 1-test.input
#TODO: explicitly parse input values
ntips=$9
print $ntips
#run the simulation for the given number of tips, ntips=$9
# FNIN='4-test.input'
FNOUT='4-test.output'
mkdir -p wlog
FNSUM='wlog/sum_ntips_ntips_$NTIPS.output'
# ./../../return_CollTime.x < $FNIN > $FNOUT

grep 'exit_code=' $FNOUT
grep 'Tsum=' $FNOUT
grep 'Tcount=' $FNOUT
grep 'Tavg=' $FNOUT
grep 'ntips=' $FNOUT

# local ntips=$(grep 'ntips=' $FNOUT)
# print $ntips
perl add-results.pl < $FNOUT $FNSUM
date


#TODO: save output to
