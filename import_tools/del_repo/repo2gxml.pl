#!/usr/bin/perl
# Bryan Bishop
# 2009-06-10
# kanzure@gmail.com http://heybryan.org/
#
# repo2gxml.pl
# this converts from the dot repo (.repo) XML file format found in repository.designengineeringlab.org to the GraphSynth 1.9 GXML format.
# 
# because of the faults with the repository data structure or data representation scheme, there is no way for us to recover the functional links, arcs or edges, so for this reason, the output of this program (the gxml) does not include any arcs connecting different components together.

use XML::Simple;
use Data::Dumper;

sub hextoint {
       my $value = shift;
       $value=unpack ('H*', $value);
       my $new = join( '', substr($value,-2,1), substr($value,-1,1) );
       $new = join( '', $new, substr($value,-4,1), substr($value,-3,1) );
       $new = join( '', $new, substr($value,-6,1), substr($value,-5,1) );
       $new = join( '', $new, substr($value,-8,1), substr($value,-7,1) );
       $new = join( '', $new, substr($value,-10,1), substr($value,-9,1) );
       my $val2=hex($new);
       return $val2;
     }

print "\$#ARGV is: $#ARGV\n";
$numArgs = $#ARGV+1;
if ($numArgs <= 0) {
	print "\n\nproper usage (you passed $numArgs arguments)\n\n";
	print "perl repo2gxml.pl example.repo example.gxml\n\n";
	exit;
}

foreach $myArg (@ARGV) {
	print $myArg . "\n";
}

$xml = new XML::Simple(ForceArray => 1);
$data = $xml->XMLin($ARGV[0], forcearray => 1); # set ARGV0 to something like: "/home/bryan/lab/summer2009/something.repo"

# DEBUG
# the following will print the entire hashref. good for quick debugging.
print "XML => " . Dumper($data);

# print out a list of what will one day become nodes in the gxml file.

open(FWRI, ">$ARGV[1]");

print FWRI "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<designGraph xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\n<name>$ARGV[0]</name>\n<globalLables />\n<globalVariables />\n<nodes>\n";

foreach $system ((@{$data->{System}})) { # take the <System> element from the XML file (it's in a hashref variable)
	foreach $artifact ((@{$system->{Artifact}})) { # now take the <Artifact> element from the XML file
		$quantity = $artifact->{ArtifactQty};
		# we're doing this so that we can output multiple nodes if there are indeed that many nodes of that type within the graph or the original product
		for($i = 0; $i < $quantity; $i++) {
			$color = $artifact->{Color}->[0]->{ColorName};; #[0];
			print "THE COLOR IS: $color\n";
			$colorname = $color;
			$newcolor = "HotPink";
			if($colorname eq "black") {$newcolor = "Black"; }
			if($colorname eq "blue ") { $newcolor = "Blue"; }
			if($colorname eq "bright blue") { $newcolor = "LightBlue"; }
			if($colorname eq "bright cyan") { $newcolor = "LightCyan"; }
			if($colorname eq "bright green") { $newcolor = "LightGreen"; }
			if($colorname eq "bright magenta") { $newcolor = ""; }
			if($colorname eq "bright red") { $newcolor = "Pink"; }
			if($colorname eq "brown") { $newcolor = "Brown"; }
			if($colorname eq "clear") { $newcolor = "Tan"; }
			if($colorname eq "cyan") { $newcolor = "Cyan"; }
			if($colorname eq "gray") { $newcolor = "Gray"; }
			if($colorname eq "green") { $newcolor = "Green"; }
			if($colorname eq "light gray") { $newcolor = "LightGray"; }
			if($colorname eq "magenta") { $newcolor = "Magenta"; }
			if($colorname eq "red") { $newcolor = "Red"; }
			if($colorname eq "white") { $newcolor = "White"; }
			if($colorname eq "yellow") {$newcolor = "Yellow"; }
			print "The new color is $newcolor.\n";

			print FWRI "<node>\n"; # print to the output file
			$name = $artifact->{ArtifactName}; # get the artifact name
			$name =~ s/ /\_/g;
			print "node name: $name\n"; # tell me what I'm doing
			print FWRI "<name>$name</name>\n"; # print to the output file
			print FWRI "<localLabels />\n<localVariables />\n<shapekey>largeCircleNode.$newcolor.30.30</shapekey>\n<screenX>0</screenX>\n<screenY>0</screenY>\n";
			$xmlout = XMLout($artifact);
			print "the xml is: $xmlout\n\n";
			print FWRI $xmlout; # is this cheating?
			print FWRI "</node>\n";
		}
	}
}

print FWRI "</nodes>\n<arcs />\n</designGraph>";

close(FWRI);


print "\n\n\nscript has naturally finished without error.\n\n";





## some old code placed here for reference
# foreach $system ((@{$data->{System}})) {
# 			foreach $artifact ((@{$system->{Artifact}})) {
# 				foreach $ArtifactFile ((@{$artifact->{ArtifactFile}})) {
# 					$ArtifactFileType = $ArtifactFile->{ArtifactFileType};
# 					$ArtifactFileExtension = $ArtifactFile->{ArtifactFileExtension};
# 					print $ArtifactFile->{text}, ", ", $ArtifactFileExtension, "\n";
# 					$name = $ArtifactFile->{text};
# 					#open(WRITER,">2008-10-13_newrepo/$file/index.txt");
# 					#print WRITER $ArtifactFile->{text}, ", ", $ArtifactFileExtension, "\n";
# 					# Let's test this a bit.
# 					#foreach $internals ((@{data->{roomba5-FILE}})) {
# 					#	print $internals->{text};
# 					#}
# 					#->{text}, "\n";
# 				}
# 				foreach $ArtifactImage ((@{$artifact->{ArtifactImage}})) {
# 					print $ArtifactImage->{text}, "\n";
# 					#print WRITER $ArtifactImage->{text}, "\n";
# 				}
# 			}
# 		}
