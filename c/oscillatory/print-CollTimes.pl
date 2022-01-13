#!/usr/bin/perl -w

$file_in = "1-test.input";
$file_out= "output.txt";
# $file_in = <STDIN>;
# $file_out= <STDIN>;

open FILE, "<", $file_in
or die "Cannot open $file_in: $!\n";

open FILE_OUT, ">>", $file_out
or die "Cannot create $file_out: $!\n";

# @array=<FILE>
# grep("exit_code=[+-]?[0-9]+([.][0-9]+)?",@array)
# grep("ntips=[+-]?[0-9]+([.][0-9]+)?",@array)
# grep("Tcount=[+-]?[0-9]+([.][0-9]+)?",@array)
# grep("Tsum=[+-]?[0-9]+([.][0-9]+)?",@array)
# grep("Tavg=[+-]?[0-9]+([.][0-9]+)?",@array)

$bool= (1 eq 0);
while (not $bool){
  while ($line = <STDIN>) {
    print FILE_OUT $line;
    #detect when 'Printing Outputs...' appears.  Break while loop there
    $bool=$line eq 'Printing Outputs...';
    # bool=$line eq 'Printing Outputs...\n'
  }
}
close FILE;
close FILE_OUT;

############################### keep it simple, stupid ########################
#in separate .pl file... or __in bash/python____
# TODO(brainwarmer): print descending list from Nmax to Nmin
# TODO: run

# #template arguments for simulation
# x=np.array([0.1, 2, 5, 500, 0., 0., 1e-5, 1e-5, 8, 500, 1234, 0, 0, 0, 0])
# log_dir="/home/timothytyree/Documents/GitHub/bgmc/c/ou/Log"
# os.chdir(log_dir)
# #make routine that generates Tavg for a given n
# def routine(n):
#     fn_out=f"Log/out_n_{n}.output"
#     os.system(f"./return_CollTime.x ${x[0]} ${x[1]} ${x[2]} ${x[3]} ${x[4]} ${x[5]} ${x[6]} ${x[7]} {n} ${x[9]} ${x[10]} ${x[11]} > {fn_out}")
#     #TODO: parse fn_out for Tavg
#     retval=os.system(f'grep "Tavg=" {fn_out}')#' #| grep -Eo "[+-]?[0-9]+([.][0-9]+)?"')
# #     retval=os.system(f'grep "Tavg=" {fn_out} #| grep -Eo "[+-]?[0-9]+([.][0-9]+)?"')
#     #TODO: return Tavg
#     return retval

#######################################################
### TODO: implement in PYTHON (and later) with DASK ###
#######################################################
#TODO: print N, from Nmax descending to $Nmin
#TODO: write params.input for this Ntips
#TODO: system(./xrun < params.input)
#TODO: change params.input to params/params_N_{N}.input
#TODO: do all ^this in dask

# # TODO: parse the response to the simulation
# grep 'exit_code=' $OUTFN #| grep -Eo '[+-]?[0-9]+([.][0-9]+)?'
# grep 'ntips=' $OUTFN #| grep -Eo '[+-]?[0-9]+([.][0-9]+)?'
# grep "Tcount=" $OUTFN #| grep -Eo '[+-]?[0-9]+([.][0-9]+)?'
# grep "Tsum=" $OUTFN #| grep -Eo '[+-]?[0-9]+([.][0-9]+)?'
# grep "Tavg=" $OUTFN #| grep -Eo '[+-]?[0-9]+([.][0-9]+)?'

# $command="";
# system($commmand);

# while ($line = <FILE>) {
#   print FILE_OUT uc $line
# }

# while ($line = <STDIN>) {
#   # print STDERR #exit code ?
#   print STDOUT $line;
# }



# ##identity.pl
# @input = <STDIN>;#standard input file handle#array context filehandle
# @cache = <FILE>;
# foreach $i (0..$#input) {
#   lineIN=$input[$i];
#   lineCACHE=$cache[$i];
#   print "$i " . $lineIN;
#   print "$i " . $lineCACHE;
# }


#
# while ($line = <STDIN>) {
#   # print STDERR #exit code ?
#   print STDOUT $line;
# }
#
# ##identity.pl
# #scalar context filehandle
# while ($line = <STDIN>) {
#   # print STDERR #exit code ?
#   print STDOUT $line;
# }



#TODO: extract these values
# exit_code=1
# 34 Tsum=51.3196
# 35 Tcount=500
# 36 Tavg=0.102639




##helloworld.pl
# print "Hello World!\n";
# $channel = <STDIN>;#standard input file handle
# print lc $channel
# ##identity.pl
# @input = <STDIN>;#standard input file handle#array context filehandle
# foreach $i (0..$#input) {
#   print "$i " . $input[$i];
# }

# foreach $line (<STDIN>) {
#   print $line;
# }

# print grep <STDIN> "Tsum"


# TODO: grep "Tavg" and store as variable


#TODO: load T_count and T_net from .csv file given this N

#TODO: run identity.pl, but updating T_count and T_net...
#TODO: update a .csv with index_col='N', and columns=[['T_count', 'T_net' ]
