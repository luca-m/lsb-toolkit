#!/usr/bin/python
# -*- coding: latin1 -*-
"""
SYNOPSIS

Perform a chi-sqare randomness test on a of a bitstream (presumably extracted from an image)

DESCRIPTION

    

EXAMPLES

    

EXIT STATUS

    

AUTHOR

    luca.mella@studio.unibo.it

LICENSE

    Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)

VERSION

    0.4
"""

import scipy.stats
import numpy as np
import sys
from optparse import OptionParser
from collections import defaultdict

class PoV:
    def __init__(self): 
        self.pov = defaultdict(lambda: 1)
        self.length = 256
        for i in range(self.length):
            self.pov[i] = 1
    def getExpected (self):
        result = defaultdict(lambda: 1 ) #[pov.length / 2];
        for i in range(self.length/2):
            avg = (self.pov[2 * i] + self.pov[2 * i + 1]) / 2.0
            result[i] = avg
        return result
    def incPov(self, i):
        self.pov[i]+=1
    def  getPov(self):
        result = defaultdict(lambda: 1 )
        for i in range(self.length/2):
            result[i] = self.pov[2 * i + 1]
        return result
    
def dochisquare( inputfile , chunksize ):
    pov = PoV()
    pvals=list()
    i = 0
    char = inputfile.read(1)
    while char != '': 
        b = ord(char)
        pov.incPov(b)
        if  i % chunksize == 0 and i != 0:
            obs = np.array( [x for x in pov.getPov().itervalues() ])
            exp = np.array( [x for x in pov.getExpected().itervalues() ])
            (chi,pval) = scipy.stats.chisquare(obs,exp)
            pvals.append(( [ max(i-1,0)*chunksize , i*chunksize ],pval))
        i+=1
        char = inputfile.read(1) 
    return pvals

#-------------------------------------------------------------------------------
# MAIN 
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = OptionParser("usage: %prog [OPTIONS] ARGS \nWill receive experimental bitstring in STDIN\nOutput:\n\t...\n\t[BlockBegin,BlockEnd]\t\t\t<PVal>\n\t...")
    parser.add_option("-s", "--size",dest="size", action="store", type="int",
                      default=128,help="block size considered in chi-square analysis", metavar="BLOCKSIZE")
    parser.add_option("-b", "--blocks",dest="blocks", action="store_true",
                      default=False,help="print also block offsets", metavar="PRINTBLOCKS")

    (options, args) = parser.parse_args()

    chnksz = abs(options.size)

    if chnksz == 0 :
        chnksz = 128

    pvals=dochisquare( sys.stdin , chnksz )
    for (block,pval) in pvals:
        if options.blocks:
            print "%s \t\t %f" % ( block , pval )
        else:
            print "%f" % ( pval )
