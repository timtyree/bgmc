


##identity.pl
@input = <STDIN>;#standard input file handle#array context filehandle
# # @cache = <FILE>;
# foreach $i (0..$#input) {
#   $lineIN=@input[$i];
#   my @tokens = split /\s+/, $lineIN;
#   # lineCACHE=$cache[$i];
#   foreach $j (0..$#tokens) {
#     $val=@tokens[$j];
#     print "$j " . $val;
#   }
#   print "$i " . $lineIN;
#   # print "$i " . $lineCACHE;
# }

@arr=@input[0];
print @arr;
# print $arr[1];
system("./return_CollTime.x < $FN_IN | grep 'Tavg=' | grep -Eo '[+-]?[0-9]+([.][0-9]+)?'");

# Perl program to demonstrate qw function
# print $N;
# using qw function
# # @arr1 = qw /Helloworld! This is Tim!/;
# $file_in = <STDIN>;
# open FILE, "<", $file_in
# or die "Cannot open $file_in: $!\n";
# @arr1 = <STDIN>;
# print @arr1;
# @arr2 = @arr1;
# Creates array2 with elements at
# index 2,3,4 in array1
# @arr2 = @arr1[2,3,0];



#
# #TODO: print up to Printing Outputs for the first trial
# #TODO: print N from Nmax to Nmin
# #TODO: for N in range(Nmax,Nmin,-1)
# # TODO: pass ^that input to system(./return_Tavg)
# # TODO: print \return + ',''
#
# print "Elements of arr1 are:\n";
# foreach $ele (@arr1)
# {
#     chomp $ele;
#     print "$ele \n";
# }
#
# #TODO: check whether 9 is the correct index:
# print "@arr1[3]\n";
#
# # print "Elements of arr2 are:\n";
# # foreach $ele (@arr2)
# # {
# #      print "$ele \n";
# # }
