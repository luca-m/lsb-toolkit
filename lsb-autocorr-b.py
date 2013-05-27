#!/usr/bin/python
# -*- coding: latin1 -*-
"""
SYNOPSIS

Calculate the autocorrelation of a bitstream (presumably extracted from an image)

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
from bitstring import Distance
from collections import deque
from optparse import OptionParser

def calcAutocorrs(infile,dst,num,shft):
    """ Calculate autocorrelations """
    distance=Distance()
    d=deque()
    autocorr=list()
    char = infile.read(1) 
    while char != '': 
        [ d.append(x) for x in bits(ord(char)) ]
        char = infile.read(1) 
    original = ''.join( x for x in d )

    for i in range(1,num+1):
        d.rotate(shft)
        shifted = ''.join(x for x in d)
        corr = getattr(distance, dst )( original , shifted )
        autocorr.append((i*shft , corr))
    return autocorr

#-------------------------------------------------------------------------------
# MAIN 
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    dists = [ y for y in dir(Distance)if callable(getattr(Distance,y))]

    parser = OptionParser("usage: %prog [OPTIONS] ARGS \nBitstring will be picked from STDIN")

    parser.add_option("-n", "--num",dest="num", action="store", type="int",
                      default=8,help="number of autocorrelation to compute", metavar="NITERATIONS")
    parser.add_option("-s", "--shift",dest="shift", action="store", type="int",
                      default=1,help="bit shift for each iteration", metavar="BITSHIFT")
    parser.add_option("-d", "--distance",dest="distance", action="store", type="string",
                      default=dists[0],help="distance to use for calculation. Options: "+str(dists), metavar="DISTANCE")

    (options, args) = parser.parse_args()

    dst = options.distance
    num = abs(options.num)
    shft = abs(options.shift)

    autocorr=calcAutocorrs(sys.stdin,dst,num,shft)
    for (shift,corr) in autocorr:
        print " Shift %d Corr %f" % ( shift , corr )

