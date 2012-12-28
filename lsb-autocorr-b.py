#!/usr/bin/python
# -*- coding: latin1 -*-
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

import sys,re
from collections import deque
from optparse import OptionParser

class Distance:
    """
    | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | 
    | 765   432   10- | 765   432   10- | 765   432   10END |
    """
    @classmethod
    def hamming (self, bitsr1 , bitsr2 ):
        length = min(len(bitsr1),len(bitsr2))
        diff = 0
        for i in range(length):
            if bitsr1[i] != bitsr2[i]:
                diff+=1
        return 1.0-diff / float(length)

def bits(char):
    s=''
    for i in range(8):
        s = str( (char>>i) & 0x01 ) + s
    return s
#-------------------------------------------------------------------------------
# MAIN 
#-------------------------------------------------------------------------------

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

distance = Distance()
d = deque( )

char = sys.stdin.read(1) 
while char != '': 
    [ d.append(x) for x in bits(ord(char)) ]
    char = sys.stdin.read(1) 

original = ''.join( x for x in d )
for i in range(1,num+1):
    d.rotate(shft)
    shifted = ''.join(x for x in d)
    corr = getattr(distance, dst )( original , shifted )
    print " Shift %d Corr %f" % ( i*shft , corr )



