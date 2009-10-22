#!/usr/bin/perl
# make_pretty.pl
# Bryan Bishop 2008-10-01
# This script strips some of the stupid XML from the repository files.
# (it's not my fault ((I swear))

opendir(DIR, "repo");
while (defined($file = readdir(DIR))) {
	# do something with "$dirname/$file"
	
	open(READER, "<repo/$file");
	open(WRITER, ">new_repo/$file");
	
	$stopwriting = 0;
	foreach $line (<READER>) {
		chomp($line);
		if(!($line eq "<!DOCTYPE RepositoryXML>") && !($line eq "<RepositorySystem>") && !($line eq "</RepositorySystem>") && ($stopwriting == 0)) { print WRITER $line; print WRITER "\n"; }
		if($line =~ "</System>") { $stopwriting = 1; }
	}

	close(WRITER);
	close(READER);

}
closedir(DIR);


