#!/usr/bin/perl -w
use strict;

while (<>) {
    chomp;
    if (/^TRANSITION \S+ \S+ \S+ (\S+)$/) {
    print "$1\n";
    }
}
