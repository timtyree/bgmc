#!/usr/bin/perl

use strict;
use warnings;

# Open the input file for reading
open(my $input_fh, '<', 'fort.81') or die "Failed to open input.txt: $!";

# Open the output file for writing
open(my $output_fh, '>', 'output.txt') or die "Failed to open output.txt: $!";

# Process the input file line by line
while (my $line = <$input_fh>) {
    chomp $line;  # Remove trailing newline

    # Replace consecutive whitespace with a comma
    $line =~ s/\s+/,/g;

    # Write the modified line to the output file
    print $output_fh $line . "\n";
}

# Close the input and output files
close($input_fh);
close($output_fh);

print "Successfully processed the file and saved the output as output.txt.\n";
