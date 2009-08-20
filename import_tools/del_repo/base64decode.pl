#!/usr/bin/perl
# Bryan Bishop 2008-10-14

use MIME::Base64;
#use Compress::Zlib::Perl;

# $ARGV[0]
$file = $ARGV[0];

open(HANDLER,"<$file");
@lines = <HANDLER>;
close(HANDLER);

if($#lines > 1) { print "Hrm, the array is greater than one. What's going on here? It's .. ", $#lines; }

# PREVIOUSLY:
$output = decode_base64($lines[0]);
# *but* we've already ran this now .. so now we're just going to decompress each of the files.


#($i, $status) = inflateInit(-WindowBits => -MAX_WBITS);
#($out, $status) = $i->inflate($lines[0]);


# print $output;

open(HANDLER,">$file");
print HANDLER $output;
close(HANDLER);


