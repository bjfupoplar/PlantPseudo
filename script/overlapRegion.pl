#!/usr/bin/perl -w
#Author: liangf

use strict;
use warnings;
use Getopt::Long;
use File::Basename;

my %opts=qw();
GetOptions(\%opts,"i1:s","i2:s","o:s","help|h!");

my @usage=qq(
============================= overlapRegion.pl ============================

Usage: overlapRegion.pl [Options]

Options:
	--i1			The first element file
	--i2			The second region file
	--o				Output file
	--h or help		Display this message
);


my $in1;
my $in2;
my $out;

if ((scalar(keys %opts) == 0) or (exists($opts{"help"})) or (exists($opts{"h"}))) {
	print join("\n",@usage)."\n";
	exit;
}

if (exists $opts{"i1"}) {
	$in1 = $opts{"i1"};
} else {
	die "Please input the first element file!!!\n";
}

if (exists $opts{"i2"}) {
	$in2 = $opts{"i2"};
} else {
	die "Please input the second region file!!!\n";
}

if (exists $opts{"o"}) {
	$out = $opts{"o"};
} else {
	die "Please input the output file!!!\n";
}

#########################################################################################################
=pod
=head file1
Chr01	27783810	27785810	+	element1 
=head file2
Chr01	810	7810	+	region1
=head output file
Region_108      Chr01   21400000        21600000        3       Chr01|21405604-21405851;Chr01|21493408-21493628;Chr01|21539630-21539783;        21405604;21493408;21539630;     21405851;21493628;21539783;     248;221;154;
=cut

my ($aa, @items, @element, $flag);

system "sort -k 1,1 -k 4,4 -k 2,2n -k 3,3n  $in1 > $in1.sort";
system "sort -k 1,1 -k 4,4 -k 2,2n -k 3,3n  $in2 > $in2.sort";

open IN, "$in1.sort" or die "can't open file $in1.sort!!!\n";
while ($aa = <IN>) {
	$aa =~ s/\s+$//;
	push @element, $aa;
}
close IN;

open IN, "$in2.sort" or die "can't open file $in2.sort!!!\n";
open OUT, ">$out" or die "Can't open file $out: $!";

while ($aa = <IN>) {
	$aa =~ s/\s+$//;
	@items = split /\s+/, $aa;
	my (@list, @start, @end, @len, $length);

	$flag = 0;
	
	for (my $i = 0; $i <= $#element; $i++) {
		my @n = split /\s+/,$element[$i]; #Chr01	27783810	27785810	+	element1
		if ($items[0] ne $n[0] or $items[3] ne $n[3]){
			if ($flag == 0){
				next;
			}else{
				last;
			}
		}
		$flag = 1;
		if ($n[2] < $items[1] or $n[1] > $items[2]) {
			next;
		}
            
		if ($n[1] <= $items[1]) {
			if ($n[2] <= $items[2]) {
				$length = $n[2] - $items[1] + 1;
			} else {
				$length = $items[2] - $items[1] + 1;
			}
		} elsif ($n[1] <= $items[2]) {
			if ($n[2] <= $items[2]) {
				$length = $n[2] - $n[1] + 1;
			} else {
				$length = $items[2] - $n[1] + 1;
			}
		}
            
        push @list,$n[0]."|".$n[1]."-".$n[2].";";
		push @start, $n[1].";";
		push @end, $n[2].";";
		push @len, $length.";";
    }

    if (defined $list[0]){
    	print OUT join ("\t",@items[4,0..3]), "\t", $#list + 1, "\t", join ("",@list), "\t", join ("",@start), "\t", join ("",@end), "\t", join ("",@len), "\n";
	}
}

system "rm $in1.sort";
system "rm $in2.sort";

close IN;
close OUT;

