#!/usr/bin/perl -w
$file_in = "sum.N.output";
$file_out= "output.txt";

open FILE, "<", $file_in
or die "Cannot open $file_in: $!\n";

open FILE_OUT, ">", $file_out
or die "Cannot create $file_out: $!\n"

@array=<FILE>
grep("Tavg",@array)


$command="ls /";
system($commmand);

# while ($line = <FILE>) {
#   print FILE_OUT uc $line
# }

# while ($line = <STDIN>) {
#   # print STDERR #exit code ?
#   print STDOUT $line;
# }

close FILE;
close FILE_OUT;

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
