#!/usr/bin/perl

use strict;
use warnings;

# Open the input file for reading
open(my $input_fh, '<', 'fort.81') or die "Failed to open input.txt: $!";

# Read the entire content of the input file
my $content = do { local $/; <$input_fh> };

# Close the input file
close($input_fh);

# Replace consecutive whitespace (excluding new lines) with a comma
$content =~ s/(?<!\n)\s+(?!\n)/,/g;

# Open the output file for writing
open(my $output_fh, '>', 'output.txt') or die "Failed to open output.txt: $!";

# Write the modified content to the output file
print $output_fh $content;

# Close the output file
close($output_fh);

print "Successfully processed the file and saved the output as output.txt.\n";
