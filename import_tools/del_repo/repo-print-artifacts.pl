#!/usr/bin/perl
# Bryan Bishop kanzure@gmail.com http://heybryan.org/
# 2009-06-10
# just a utility script to print out a list of artifact names from a .repo file
use XML::Simple;
use Data::Dumper;


#print "\$#ARGV is: $#ARGV\n";
$numArgs = $#ARGV+1;
if ($numArgs <= 0) {
	print "\n\nproper usage (you passed $numArgs arguments)\n\n";
	print "./repo-print-artifacts example.repo\n";
	exit;
}

#foreach $myArg (@ARGV) {
#	print $myArg . "\n";
#}

$xml = new XML::Simple(ForceArray => 1);
$data = $xml->XMLin($ARGV[0], forcearray => 1); # set ARGV0 to something like: "/home/bryan/lab/summer2009/something.repo"

foreach $system ((@{$data->{System}})) { # take the <System> element from the XML file (it's in a hashref variable)
	foreach $artifact ((@{$system->{Artifact}})) {
		$name = $artifact->{ArtifactName};
		print "$name\n";
	}
}