$arr=<STDIN>;
# print $arr;
my @words = split ' ', $arr;
@words[8]=@words[8]-1;
foreach $ele (@words)
{
    print "$ele ";
    # chomp;
}
print "\n"
