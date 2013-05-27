#!/usr/bin/python
# -*- coding: utf8 -*-
"""
SYNOPSIS

    

DESCRIPTION

    

EXAMPLES

    

EXIT STATUS

    

AUTHOR

    luca.mella@studio.unibo.it

LICENSE

    Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)

VERSION

    0.3
"""

import sys
from bitstring import bits
from optparse import OptionParser

def estimateRandomness(infile):
    zeroes = 0
    ones = 0
    char = infile.read(1) 
    while char != '': 
        for x in bits(ord(char)):
            if x == '1':
                ones+=1
            else:
                zeroes+=1
        char = infile.read(1) 
    return [ones,zeroes] 
#-------------------------------------------------------------------------------
# MAIN 
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = OptionParser("usage: %prog [OPTIONS] ARGS \nBitstring will be picked from STDIN")

    (options, args) = parser.parse_args()

    [ones,zeroes]=estimateRandomness(sys.stdin) 

    print "Perc zeroes : %f" % ( zeroes / float(ones+zeroes) )
    print "Perc ones   : %f" % ( ones / float(ones+zeroes) )



