#!/usr/bin/perl
# Bryan Bishop 2008-10-13
# There are files stored within the .repo XML files. Extract them.
# In the repo/ dir, there's .repo XML files that have <System></System> such that
#  somewhere within the <System> element there's some child of a child that has information
#  about what type of things appear after the </System>.
#
#  So, using make_pretty.pl, we can extract everything from after the </System>.
#  But first we want to see everything that should be in each of the files.
#  That's what this should be doing.
#
#  In the .repo file, that child element is a child of <Artifact> and is called <ArtifactFile>. 
#  ArtifactFile has properties: ArtifactFileType, ArtifactFileExtension, and the text within
#  the <ArtifactFile> tag is the name of the element to be looking for. 
#
# There's also <ArtifactImage> where the text within is the name of another element to find.
#
# Let's parse the XML file like we did in the 2008-10-02.pl script (the XML->DB dumper).
# Ok. New plan. Just spitting out the name of the elements to look for.
# /home/bryan/lab/2008-10-13_newrepo/cd_player/index.txt
# The index.txt file consists of comma separated values (name of element, new extension)

use XML::Simple;

opendir(DIR, "2008-10-13_newrepo/");
while (defined($file = readdir(DIR))) {
	if($file =~ ".repo") {

		$xml = new XML::Simple (ForceArray => 1, ContentKey => 'text');
		$data = $xml->XMLin("repo/$file", forcearray=>1);
		# Let's modify the file name a bit.
		$file =~ s/ /_/g;
		$file =~ s/\.repo//;
		print "Opening 2008-10-13_newrepo/$file/index.txt\n";
		open(WRITER, ">2008-10-13_newrepo/$file/index.txt");
		foreach $system ((@{$data->{System}})) {
			foreach $artifact ((@{$system->{Artifact}})) {
				foreach $ArtifactFile ((@{$artifact->{ArtifactFile}})) {
					$ArtifactFileType = $ArtifactFile->{ArtifactFileType};
					$ArtifactFileExtension = $ArtifactFile->{ArtifactFileExtension};
					print $ArtifactFile->{text}, ", ", $ArtifactFileExtension, "\n";
					$name = $ArtifactFile->{text};
					#open(WRITER,">2008-10-13_newrepo/$file/index.txt");
					print WRITER $ArtifactFile->{text}, ", ", $ArtifactFileExtension, "\n";
					# Let's test this a bit.
					#foreach $internals ((@{data->{roomba5-FILE}})) {
					#	print $internals->{text};
					#}
					#->{text}, "\n";
				}
				foreach $ArtifactImage ((@{$artifact->{ArtifactImage}})) {
					print $ArtifactImage->{text}, "\n";
					print WRITER $ArtifactImage->{text}, "\n";
				}
			}
		}

		close(WRITER);
	}
}


closedir(DIR);
