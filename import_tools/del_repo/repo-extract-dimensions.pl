#!/usr/bin/perl
# Bryan Bishop
# 2009-06-11
# kanzure@gmail.com http://heybryan.org/
#
# repo-extract-dimensions.pl
# usage: ./repo-extract-dimensions.pl input.repo output.fennfile.po
# extracts dimensioning information from a dot repo file and puts it into a fennfile.po format thingy.
#
# written to be used in combination with gxml-add-dimensions.pl

use XML::Simple;
use Data::Dumper;


print "\$#ARGV is: $#ARGV\n";
$numArgs = $#ARGV+1;
if ($numArgs <= 1) {
	print "\n\nproper usage (you passed $numArgs arguments)\n\n";
	print "./repo-extract-dimensions.pl example.repo output.fennfile.fennpo\n\n";
	exit;
}

print "the arguments that were passed to repo-extract-dimensions.pl were as follows:\n";
foreach $myArg (@ARGV) {
	print "\t" . $myArg . "\n";
}
print "\n"; # pew-pew!

# down to business
$xml = new XML::Simple(ForceArray => 1);
$data = $xml->XMLin($ARGV[0], forcearray => 1); # set ARGV0 to something like: "/home/bryan/lab/summer2009/something.repo"

print "checking the artifact names in $ARGV[0]:\n";
foreach $system ((@{$data->{System}})) { # take the <System> element from the XML file (it's in a hashref variable)
	foreach $artifact ((@{$system->{Artifact}})) {
		$name = $artifact->{ArtifactName};
		print "\t$name\n";
	}
}
print "\n";

# DEBUG
# the following will print the entire hashref. good for quick debugging.
# print "XML => " . Dumper($data);

# get the input information from fennfile.fenpo
$fennfile = $ARGV[2];
open(FENNFILE, "<$ARGV[2]");
@lines = <FENNFILE>;
close(FENNFILE);

$thehash = {};
foreach my $line (@lines) {
	@parts = split(/\;/, $line);
	$thehash{$parts[0]} = $parts[1];
}

# <Parameters ParameterDimension="length" ParameterUnits="inches" ParameterValue="16.9" />
# http://www.perlmonks.org/?node_id=253934
$fennfileoutput = "";

foreach $system ((@{$data->{System}})) { # take the <System> element from the XML file (it's in a hashref variable)
	foreach $artifact ((@{$system->{Artifact}})) {
		$name = $artifact->{ArtifactName};
		$theoutput = "$name;";
		#$parameters = $artifact->{Parameters}->[0]->{ParameterValue};
		#print "$parameters";
		@parameters = @{$artifact->{Parameters}};
		#print $parameters->[0]->{ParameterValue};
		#print "total: " . ($#parameters);

		# FIXME TODO
		# choose only the first material type (David Agu's format doesn't account for multiple materials)
		# <Material MaterialName="plastic">
		# add this to the fennfile output thingy. 
		if(!($artifact->{Material}->[0]->{MaterialName} eq "")) {
			$theoutput .= " M" . $artifact->{Material}->[0]->{MaterialName};
		}

		for($i = 0; $i < $#parameters; $i++) { # ((@{$artifact->{Parameters}})) {
			#print "ha"; #$color = $artifact->{Color}->[0]->{ColorName};; #[0];
			$ParameterValue = @parameters[$i]->{ParameterValue};
			$ParameterDimension = @parameters[$i]->{ParameterDimension};
			#print $ParameterDimension;
			if($ParameterDimension eq "length") {
				$theoutput .= " L" . $ParameterValue;
			} elsif (($ParameterDimension eq "outer diameter") || ($ParameterDimension eq "diameter")) {
				$theoutput .= " D" . $ParameterValue;
			} elsif (($ParameterDimension eq "mass") || ($ParameterDimension eq "weight")) {
				$theoutput .= " m" . $ParameterValue;
			} elsif ($ParameterDimension eq "shaft diameter") {
				$theoutput .= " D" . $ParameterValue;
			} elsif ($ParameterDimension eq "width") {
				$theoutput .= " W" . $ParameterValue;
			} elsif (($ParameterDimension eq "thickness") || ($ParameterDimension eq "depth")) {
				$theoutput .= " T" . $ParameterValue;
			} elsif ($ParameterDimension eq "height") {
				$theoutput .= " H" . $ParameterValue;
			} else {
				$theoutput .= "\n\n** UNKNOWN DIMENSION ** " . $ParameterDimension . "\n";
			}
			# other if statements here for the different types of parameters (H=height, L=length, T=thickness, W=width, D=diameter, m=mass)
		}
		$theoutput .= "\n";
		$theoutput =~ s/\; /\;/g;
		$fennfileoutput .= $theoutput;
		print $theoutput;
	}
}

open(OUT1, ">$ARGV[1]");
print OUT1 $fennfileoutput;
close(OUT1);

exit;
# 
# 
# 
# 
# 		#print "currently at name: $name\n";
# 		if($thehash{$name}) {
# 			#print "it is in the hash.\n";
# 			$thevalues = $thehash{$name};
# 			print "dimensions: $thevalues\n";
# 			# Now please parse the dimensions.
# 			@dimensions = split(/ /, $thevalues);
# 			foreach my $dimension (@dimensions) {
# 				$type = substr($dimension,0,1);
# 				print "dimension of type $type\n";
# 				$dimvalue = substr($dimension,1);
# 				chomp($dimvalue);
# 				print "the value of this dimension is $dimvalue\n";
# 				$fullexpression = "height";
# 				if($type eq "H") { $fullexpression = "height"; }
# 				if($type eq "L") { $fullexpression = "length"; }
# 				if($type eq "T") { $fullexpression = "thickness"; }
# 				if($type eq "W") { $fullexpression = "width"; }
# 				if($type eq "D") { $fullexpression = "diameter"; }
# 				#push(, [{'ParameterUnits' = "supergrams", 'ParameterDimension' = 'supermass', 'ParameterValue' = '1444'}]);
# push @{ $artifact->{Parameters} }, { ParameterDimension => $fullexpression, ParameterUnits => 'inches', ParameterValue => $dimvalue };
# 				print Dumper($artifact);
# 			}
# 		}
# 	}
# }
# 
# open(OUTFILE, ">$ARGV[1]");
# print OUTFILE XMLout($data);
# close(OUTFILE);
# 
# exit();
# 
# # print out a list of what will one day become nodes in the gxml file.
# 
# open(FWRI, ">$ARGV[1]");
# 
# print FWRI "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<designGraph xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\n<name>$ARGV[0]</name>\n<globalLables />\n<globalVariables />\n<nodes>\n";
# 
# foreach $system ((@{$data->{System}})) { # take the <System> element from the XML file (it's in a hashref variable)
# 	foreach $artifact ((@{$system->{Artifact}})) { # now take the <Artifact> element from the XML file
# 		$quantity = $artifact->{ArtifactQty};
# 		# we're doing this so that we can output multiple nodes if there are indeed that many nodes of that type within the graph or the original product
# 		for($i = 0; $i < $quantity; $i++) {
# 			$color = $artifact->{Color}->[0]->{ColorName};; #[0];
# 			print "THE COLOR IS: $color\n";
# 			$colorname = $color;
# 			$newcolor = "HotPink";
# 			if($colorname eq "black") {$newcolor = "Black"; }
# 			if($colorname eq "blue ") { $newcolor = "Blue"; }
# 			if($colorname eq "bright blue") { $newcolor = "LightBlue"; }
# 			if($colorname eq "bright cyan") { $newcolor = "LightCyan"; }
# 			if($colorname eq "bright green") { $newcolor = "LightGreen"; }
# 			if($colorname eq "bright magenta") { $newcolor = ""; }
# 			if($colorname eq "bright red") { $newcolor = "Pink"; }
# 			if($colorname eq "brown") { $newcolor = "Brown"; }
# 			if($colorname eq "clear") { $newcolor = "Tan"; }
# 			if($colorname eq "cyan") { $newcolor = "Cyan"; }
# 			if($colorname eq "gray") { $newcolor = "Gray"; }
# 			if($colorname eq "green") { $newcolor = "Green"; }
# 			if($colorname eq "light gray") { $newcolor = "LightGray"; }
# 			if($colorname eq "magenta") { $newcolor = "Magenta"; }
# 			if($colorname eq "red") { $newcolor = "Red"; }
# 			if($colorname eq "white") { $newcolor = "White"; }
# 			if($colorname eq "yellow") {$newcolor = "Yellow"; }
# 			print "The new color is $newcolor.\n";
# 
# 			print FWRI "<node>\n"; # print to the output file
# 			$name = $artifact->{ArtifactName}; # get the artifact name
# 			$name =~ s/ /\_/g;
# 			print "node name: $name\n"; # tell me what I'm doing
# 			print FWRI "<name>$name</name>\n"; # print to the output file
# 			print FWRI "<localLabels />\n<localVariables />\n<shapekey>largeCircleNode.$newcolor.30.30</shapekey>\n<screenX>0</screenX>\n<screenY>0</screenY>\n";
# 			$xmlout = XMLout($artifact);
# 			print "the xml is: $xmlout\n\n";
# 			print FWRI $xmlout; # is this cheating?
# 			print FWRI "</node>\n";
# 		}
# 	}
# }
# 
# print FWRI "</nodes>\n<arcs />\n</designGraph>";
# 
# close(FWRI);
# 
# 
# print "\n\n\nscript has naturally finished without error.\n\n";
# 
# 
# 
# 
# 
# ## some old code placed here for reference
# # foreach $system ((@{$data->{System}})) {
# # 			foreach $artifact ((@{$system->{Artifact}})) {
# # 				foreach $ArtifactFile ((@{$artifact->{ArtifactFile}})) {
# # 					$ArtifactFileType = $ArtifactFile->{ArtifactFileType};
# # 					$ArtifactFileExtension = $ArtifactFile->{ArtifactFileExtension};
# # 					print $ArtifactFile->{text}, ", ", $ArtifactFileExtension, "\n";
# # 					$name = $ArtifactFile->{text};
# # 					#open(WRITER,">2008-10-13_newrepo/$file/index.txt");
# # 					#print WRITER $ArtifactFile->{text}, ", ", $ArtifactFileExtension, "\n";
# # 					# Let's test this a bit.
# # 					#foreach $internals ((@{data->{roomba5-FILE}})) {
# # 					#	print $internals->{text};
# # 					#}
# # 					#->{text}, "\n";
# # 				}
# # 				foreach $ArtifactImage ((@{$artifact->{ArtifactImage}})) {
# # 					print $ArtifactImage->{text}, "\n";
# # 					#print WRITER $ArtifactImage->{text}, "\n";
# # 				}
# # 			}
# # 		}
