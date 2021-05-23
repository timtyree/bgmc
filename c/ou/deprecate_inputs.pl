#TODO: write perl script that prints every line, but deprecates the 8 line by 1
@input = <STDIN>;#standard input file handle#array context filehandle
foreach $i (0..$#input) {
  if ($i eq 8){
    $val=$input[$i]-1;
    print "$val\n";
  }
  else{
    # print "$input[$i]";
    print "" . $input[$i];
  }

}






# $arr=<STDIN>;
# # print $arr;
# my @words = split ' ', $arr;
# @words[8]=@words[8]-1;
# foreach $ele (@words)
# {
#     print "$ele ";
#     # chomp;
# }
# print "\n"
