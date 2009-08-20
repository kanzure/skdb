#!/usr/bin/perl
# Bryan Bishop
# 2008-10-13
# See 2008-13_newrepo.txt for explanations.
use XML::Simple;

opendir(DIR, "2008-10-13_newrepo/");
while (defined($file = readdir(DIR))) {
	if($file =~ ".repo") {
		my @lookarray; # Reset the array.
		$file =~ s/ /_/g;
		$file =~ s/\.repo//;
		open(INDEX,"<2008-10-13_newrepo/$file/index.txt");
		@lines = <INDEX>;
		foreach $line (@lines) {
			if (!($line eq "\n")) {
				$line =~ s/\n//g;
				@parts = split(/, /, $line);
				$parts[1] =~ s/\.//g; # ".cdd" for instance. We don't need that.
				# $parts[0] is the element name, $parts[1] is the new extension.
				push(@lookarray, $parts[0] . "." . $parts[1]); # is pushing an array to an array ok?
			}
		}

		# Now we open up the other files and look through @lookarray. (well, no)
		opendir(DIR2, "2008-10-13_newrepo/$file/");
		while (defined($file2 = readdir(DIR2))) {
			# First thing we're going to do is add some <System> tags. Or not.
			if(!($file2 eq "index.txt") && !($file2 eq "..") && !($file2 eq ".") && ($file2+0 eq $file2)) { # We don't want the index.
				#print "XMLin w/ $file/$file2.\n";
				$xml = new XML::Simple (ForceArray=>1, ContentKey=>'text');
				$data = $xml->XMLin("2008-10-13_newrepo/$file/$file2", forcearray=>1, KeepRoot => 1);
				foreach $attempt (@lookarray) {
					# And of course if we've found it then don't go through more loops .. 
					@splitter = split(/\./, $attempt);
					$first = $splitter[0];
					# print "Looking for $attempt ($first) in $file/$file2.\n";
					#open(ATT,"<2008-10-13_newrepo/$file/$file2");
					#@LINERS = <ATT>;
					#close(ATT);

					if ($data->{$first}) { # I think this doesn't work.
						# So, this means we've found it.
						 #print "Creating file $attempt.\n";
						 #print "The data is: ", @{$data->{$first}}[0];
						 #print "test";
						 $thingy = @{$data->{$first}}[0];
						 #print "test2";
						 open(OUTPUT,">2008-10-13_newrepo/$file/$attempt");
						 # for our record, we need to delete some files. So, let's spit out the names of those files now.
						 print "rm /home/bryan/lab/2008-10-13_newrepo/$file/$first ;\n";
						 print OUTPUT $thingy; #@{$data->{$first}}[0]; #->{text};
						 close(OUTPUT);
						 #print "Text is: ", ($data->{$first})->{text};
					} #else { if($LINERS[0] =~ /$first/) { print ".. We found it anyway.\n"; } 
				#	}
				}
			}
		}
		closedir(DIR2);


		close(INDEX);
	}
}
closedir(DIR);
