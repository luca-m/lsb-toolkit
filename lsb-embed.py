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

    0.2
"""
import numpy as np
import Image, sys, re
from optparse import OptionParser

class Embedder:
    """
    | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | 
    | 765   432   10- | 765   432   10- | 765   432   10END |
    """
    @classmethod
    def classic_lsb (self, image , filetoembed ,channels = 'rgb' , bits = [0], vertical = False):
        m = image.load()
        s = image.size 
        index=0
        bindex=7
        bitnum = bits[0]%7
        char = filetoembed.read(1) 
        if char == '': 
            return image
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
                if bindex > 1 :
                    r = ( r & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                    bindex-=1
                    g = ( g & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                    bindex-=1
                    b = ( b & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                    bindex-=1
                elif bindex == 1 : 
                    r = ( r & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                    bindex-=1
                    g = ( g & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                    b = ( b & (0xfe << bitnum ) ) | 0x00 
                    bindex=7
                    char = filetoembed.read(1) 
                    if char == '': 
                        b = ( b & (0xfe << bitnum ) ) | 0xff    # mark the end of embeddings
                        if vertical == True:
                            m[(y,x)] = r,g,b,a
                        else:
                            m[(x,y)] = r,g,b,a
                        return image
                if vertical == True:
                    m[(y,x)] = r,g,b,a
                else:
                    m[(x,y)] = r,g,b,a
        return image
    """
    """
    @classmethod
    def raw_lsb_fast (self, image, filetoembed ,channels = 'rgb' , bits = [0] , vertical = False):
        
        m = image.load()
        s = image.size
        index=0
        bindex=7
        char = filetoembed.read(1) 
        if char == '': 
            return image
        F = s[0]
        S = s[1]
        if vertical == True:
            F = s[1] # y
            S = s[0] # x
        for x in range(F):
            for y in range(S):
                if vertical == True:
                    r,g,b,a = m[(y,x)]
                else:
                    r,g,b,a = m[(x,y)]
                for bit in bits:
                    bitnum = bit % 7
                    for chan in channels:
                        if 'r' == chan :
                            r = ( r & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                            bindex-=1
                            if (bindex < 0 ):
                                bindex=7
                                char = filetoembed.read(1) 
                                if char == '': 
                                    if vertical == True:
                                        m[(y,x)] = r,g,b,a
                                    else:
                                        m[(x,y)] = r,g,b,a
                                    return image
                        if 'g' == chan :
                            g = ( g & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                            bindex-=1
                            if (bindex < 0 ):
                                bindex=7
                                char = filetoembed.read(1) 
                                if char == '': 
                                    if vertical == True:
                                        m[(y,x)] = r,g,b,a
                                    else:
                                        m[(x,y)] = r,g,b,a
                                    return image
                        if 'b' == chan :
                            b = ( b & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                            bindex-=1
                            if (bindex < 0 ):
                                bindex=7
                                char = filetoembed.read(1) 
                                if char == '': 
                                    if vertical == True:
                                        m[(y,x)] = r,g,b,a
                                    else:
                                        m[(x,y)] = r,g,b,a
                                    return image
                        if 'a' == chan :
                            a = ( a & (0xfe << bitnum ) ) | ( ((ord(char) & (0x01 << bindex)) >> bindex)<< bitnum )
                            bindex-=1
                            if (bindex < 0 ):
                                bindex=7
                                char = filetoembed.read(1) 
                                if char == '': 
                                    if vertical == True:
                                        m[(y,x)] = r,g,b,a
                                    else:
                                        m[(x,y)] = r,g,b,a
                                    return image
                if vertical == True:
                    m[(y,x)] = r,g,b,a
                else:
                    m[(x,y)] = r,g,b,a

        return image


#-------------------------------------------------------------------------------
# MAIN 
#-------------------------------------------------------------------------------

algs = [ y for y in dir(Embedder)if callable(getattr(Embedder,y))]

parser = OptionParser("usage: %prog [OPTIONS] ARGS \nData to embed will be picked from STDIN")

parser.add_option("-f", "--file", dest="filename", action="store", type="string",
                  help="cover image", metavar="FILE")
parser.add_option("-o", "--output",dest="output", action="store", type="string",
                  help="output file", metavar="OUTPUT")
parser.add_option("-c", "--channel",dest="channel", action="store", type="string",
                  default='rgb',help="channel to consider [r|g|b|a]. Note: order is relevant", metavar="CHANNEL")
parser.add_option("-b", "--bitnum",dest="bitnum", action="store", type="string",
                  default='0',help="bit to consider in pixel\'s channels [0-7]{1,8}", metavar="BITNUM")
parser.add_option("-a", "--algorithm",dest="algorithm", action="store", type="string",
                  default=algs[1],help="extraction algorithm to use "+str(algs), metavar="ALGORITHM")
parser.add_option("-v", "--vertical",dest="vertical", action="store_true", default=False,help="Extract per column instead of per row ", metavar="VERTICAL")
(options, args) = parser.parse_args()

if options.filename == None or options.output == None:
    parser.error("Input image and output file are mandatory!")

chnls = re.compile('[a|r|g|b]{1,4}').match(options.channel.lower())
bnms = re.compile('[0-7]{1,8}').match(options.bitnum)

if chnls is None :
    print 'ERROR: invalid channel specification'
    exit(-1)
if bnms is None :
    print 'ERROR: invalid bit specification'
    exit(-1)

algorithm = options.algorithm
coverim = options.filename
outim = options.output
channels = chnls.group()
bitnum = [int(x) for x in bnms.group() ]

n = Image.open(coverim)
n = n.convert("RGBA")
s = n.size

print 'Image size: '+str(s)

embedder = Embedder()
n = getattr(embedder, algorithm )(n ,sys.stdin , channels , bitnum ,options.vertical)

print 'Saving file to '+outim+'..'
n.save(outim, "PNG")



