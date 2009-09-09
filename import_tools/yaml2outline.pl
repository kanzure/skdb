#!/usr/bin/perl -w

$VERSION = '0.35';


=head1 NAME

yaml2outline - Convert a YAML outline into a standard one

=head1 USAGE

    yaml2outline outline.yaml > outline.txt

=head1 DESCRIPTION

This program converts a YAML file that conforms to a particular outline format, into a standard looking outline. It is really just a proof of concept, and not intended for any serious purpose.

Example:

    ---
    - Intro
    - Part 1:
       - Life
       - Love:
          - True Love:
             - Mexican Cuisine
             - Perl
          - Love at First Sight
       - Pursuit of YAML
    - Part 2:
       - Scissors:
          - Sewing
          - Hair
       - Paper
       - Rock:
          - Granite
          - Pixies
    - Part3:
       - Perl
       - Python
       - Ruby
    - Conclusion

yields:

    I) Intro

    II) Part 1
       A) Life
       B) Love
           1) True Love
               i) Mexican Cuisine
               ii) Perl
           2) Love at First Sight
       C) Pursuit of YAML

    III) Part 2
       A) Scissors
           1) Sewing
           2) Hair
       B) Paper
       C) Rock
           1) Granite
           2) Pixies

    IV) Part3
       A) Perl
       B) Python
       C) Ruby

    V) Conclusion

=head1 AUTHOR

Brian Ingerson <ingy@cpan.org>

=head1 COPYRIGHT

Copyright 2002, Brian Ingerson - All rights reserved

You may use this hack under the same terms as Perl itself.

=cut

use strict;
use YAML;

my ($yaml, $perl, $outline, $level, $symbol_level, $symbol_format, $lookup);

$yaml = join '', <>;
eval { $perl = Load($yaml); };
die "Error in YAML input:\n$@" if $@;

$level = -1;
$symbol_format = ['ROMAN', 'ALPHA', 'NUMERIC'];
$lookup = Load(join '', <DATA>);

walk_tree($perl);
print $outline;

sub walk_tree {
    my $node = shift;
    $level++;
    $symbol_level->[$level] = 0;
    my $ref = ref($node);
    die "Data structure is not valid for outline\n" 
      unless $ref eq 'ARRAY';
    for my $elem (@$node) {
	$ref = ref($elem) || 'STRING';
	if ($ref eq 'STRING') {
	    $outline .= (' ' x (4 * $level -1)) . 
	                symbol($level) . ') ' . $elem . "\n";
        }		
	elsif ($ref eq 'HASH') {
	    die "Data structure is not valid for outline\n" 
	      unless keys(%$elem) == 1;
	    my ($key) = keys(%$elem);
	    $outline .= (' ' x (4 * $level -1)) . 
	                symbol($level) . ') ' . $key . "\n";
	    walk_tree($elem->{$key});
        } 
	else {
	    die "Data structure is not valid for outline\n"; 
	}
	$outline .= "\n" unless $level;
    }
    $level--;
}

sub symbol {
    my $level = shift;
    my $format = $symbol_format->[$level % @$symbol_format];
    $format = lc($format) unless $level < @$symbol_format;
    return $lookup->{$format}[$symbol_level->[$level]++];
}

__DATA__
ROMAN: [I, II, III, IV, V, VI, VII, VIII, IX, X, XI, XII, XIII, XIV, XV, XVI]
ALPHA: [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, w, x]
NUMERIC: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
roman: [i, ii, iii, iv, v, vi, vii, viii, ix, x, xi, xii, xiii, xiv, xv, xvi]
alpha: [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x]
numeric: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
