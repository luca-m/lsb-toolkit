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

    0.2
"""

import numpy as np
import Image, sys, re, inspect, stego_algs
from optparse import OptionParser

'''
class Extractor:

    """
    | rgba | rgba | rgba | rgba | ...
    | 7654   3210 | 7654   3210 | ...
    | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb |
    | 765   432   107 | 654   321   076 | 543   210   765 | 432   107 |
    | rg | rg | rg | rg | rg  ...
    | 76   54   32   10 | 76  ...
    | r | r | r | r ...
    | 7   6   5   4 ...
    """
    def raw_lsb_fast ( self ,image, channels = 'rgb' , bits = [0] , vertical = False):
        by = array.array('B')
        m = image.load()
        s = image.size
        index=0
        by.append(0)
        bindex=7
        F = s[0]
        S = s[1]
        if vertical == True:
            F = s[1]
            S = s[0]
        for x in range(F):
            for y in range(S):
                if vertical == True:
                    r,g,b,a = m[(y,x)]
                else:
                    r,g,b,a = m[(x,y)]
                
                for bit in bits:
                    bitnum = bit % 7
                    mask = 0x01 << bitnum
                    for chan in channels:
                        if 'r' == chan :
                            by[index]|= ((r & mask)>>bitnum )<< bindex
                            bindex-=1
                            if (bindex < 0 ):
                                by.append(0)
                                index+=1
                                bindex=7
                        if 'g' == chan :
                            by[index]|= ((g & mask)>>bitnum ) << bindex
                            bindex-=1
                            if (bindex < 0 ):
                                by.append(0)
                                index+=1
                                bindex=7
                        if 'b' == chan :
                            by[index]|= ((b & mask)>>bitnum ) << bindex
                            bindex-=1
                            if (bindex < 0 ):
                                by.append(0)
                                index+=1
                                bindex=7
                        if 'a' == chan :
                            by[index]|= ((a & mask)>>bitnum ) << bindex
                            bindex-=1
                            if (bindex < 0 ):
                                by.append(0)
                                index+=1
                                bindex=7
        return by
    """
    | rgba | rgba | rgba | rgba | ...
    | 7654   3210 | 7654   3210 | ...
    | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb |
    | 765   432   107 | 654   321   076 | 543   210   765 | 432   107 |
    | rg | rg | rg | rg | rg  ...
    | 76   54   32   10 | 76  ...
    | r | r | r | r ...
    | 7   6   5   4 ...
    """
    @classmethod
    def raw_lsb_slow (self , image , channels = 'rgb' , bits = [0] , vertical = False):
        lsb = []
        s = image.size
        m = image.load()
        F = s[0]
        S = s[1]
        if vertical == True:
            F = s[1]
            S = s[0]
        for x in range(F):
            for y in range(S):
                if vertical == True:
                    r,g,b,a = m[(y,x)]
                else:
                    r,g,b,a = m[(x,y)]
                
                for bit in bits:
                    bitnum = bit % 7
                    mask = 0x01 << bitnum
                    for chan in channels:
                        if 'r' == chan :
                            lsb.extend( str((r & mask) >> bitnum) )
                        if 'g' == chan :
                            lsb.extend( str((g & mask) >> bitnum) )
                        if 'b' == chan :
                            lsb.extend( str((b & mask) >> bitnum) )
                        if 'a' == chan :
                            lsb.extend( str((a & mask) >> bitnum) )
        lsb = "".join(lsb)
        lsb = "".join(   chr(int(lsb[i:i+8],2))  for i in range(0,len(lsb),8)   )
        by = array.array('B',lsb)
        return by
    """
    | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | 
    | 765   432   10- | 765   432   10- | 765   432   10END |
    """
    @classmethod
    def classic_lsb (self , image ,channels = 'rgb' , bitnum = 0 , vertical = False):
        by = array.array('B')
        m = image.load()
        s = image.size 
        mask =  0x01 << (bitnum%7)
        index=0
        by.append(0)
        bindex=7
        F = s[0]
        S = s[1]
        if vertical == True:
            F = s[1]
            S = s[0]
        for x in range(F):
            for y in range(S):
                if vertical == True:
                    r,g,b,a = m[(y,x)]
                else:
                    r,g,b,a = m[(x,y)]
                # | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | 
                # | 765   432   10- | 765   432   10- | 765   432   10E |
                if bindex > 1 :
                    by[index]|= ((r & mask)>>bitnum )<< bindex
                    bindex-=1
                    by[index]|= ((g & mask)>>bitnum ) << bindex
                    bindex-=1
                    by[index]|= ((b & mask)>>bitnum ) << bindex
                    bindex-=1
                else:
                    if bindex == 1 : 
                        by[index]|= ((r & mask)>>bitnum ) << bindex
                        bindex-=1
                        by[index]|= ((g & mask)>>bitnum ) << bindex
                        if (b & mask)==1:
                            return by
                        else:
                            by.append(0)
                            index+=1
                            bindex=7
                    
        return by
'''

#-------------------------------------------------------------------------------
# MAIN 
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    #algs = [ y for y in dir(Extractor)if callable(getattr(Extractor,y))]
    algs=[k for (k,v) in sys.modules['stego_algs'].__dict__.items() if inspect.isclass(v) and k != 'Algorithm']

    parser = OptionParser("usage: %prog [OPTIONS] ARGS ")

    parser.add_option("-f", "--file", dest="filename", action="store", type="string",
                      help="image to analyze", metavar="FILE")
    parser.add_option("-o", "--output",dest="output", action="store", type="string",
                      help="output file. No output file specified means output in STDOUT", metavar="OUTPUT")
    parser.add_option("-c", "--channel",dest="channel", action="store", type="string",
                      default='rgb',help="channel to consider [r|g|b|a]. Note: order is relevant", metavar="CHANNEL")
    parser.add_option("-b", "--bitnum",dest="bitnum", action="store", type="string",
                      default='0',help="bit to consider in pixel\'s channels [0-7]{1,8}", metavar="BITNUM")
    parser.add_option("-a", "--algorithm",dest="algorithm", action="store", type="string",
                      default=algs[1],help="extraction algorithm to use "+str(algs), metavar="ALGORITHM")
    parser.add_option("-v", "--vertical",dest="vertical", action="store_true", default=False,help="Extract per column instead of per row ", metavar="VERTICAL")
    parser.add_option("-r", "--rectangle",dest="rectangle", action="store",type="string",default="0,0,max,max",help="define a sub-image area where to extract data", metavar="RECTANGLE")

    (options, args) = parser.parse_args()

    if options.filename is None :
        print 'ERROR: input image is mandatory!'
        exit(-1)

    chnls = re.compile('[a|r|g|b]{1,4}').match(options.channel.lower())
    bnms = re.compile('[0-7]{1,8}').match(options.bitnum)

    if chnls is None :
        print 'ERROR: invalid channel specification'
        exit(-1)
    if bnms is None :
        print 'ERROR: invalid bit specification'
        exit(-1)

    subimage=options.rectangle.replace('max',str(sys.maxint)).split(',')
    try:
        for i in range(4):
            subimage[i] = int(subimage[i])
    except:
        print 'WARNING: Subimage specification not correct, using whole image'
        subimage=[0,0,str(sys.maxint),str(sys.maxint)]
    
    if options.algorithm not in algs :
        print "WARNING: Algorithm specification not correct, using the first valid alg"
        algorithm = algs[0]
    else:
        algorithm = options.algorithm
    
    inputim = options.filename
    outfile = options.output
    channels = chnls.group()
    bitnum = [int(x) for x in bnms.group() ]

    n = Image.open(inputim)
    n = n.convert("RGBA")
    s = n.size

    #print 'Processing..'
    extractor = sys.modules['stego_algs'].__dict__.get(algorithm)(n,channels,bitnum,options.vertical)
    by = extractor.read(subimage[0],subimage[1],subimage[2],subimage[3])

    if len(by) > 0 :
        if outfile is None:
            of = sys.stdout
        else:
            print 'Writing output to file: %s' %outfile
            of = open(outfile,"wb")
        by.tofile(of)
    else:
        print 'No data extracted.'

