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

import Image
import re
from optparse import OptionParser

#-------------------------------------------------------------------------------
# MAIN 
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    
    parser = OptionParser("usage: %prog [OPTIONS] ARGS \nDefault output in <imagepath>-lsb.png")
    parser.add_option("-f", "--file", dest="filename", action="store", type="string",
		    help="image to analyze", metavar="FILE")
    parser.add_option("-c", "--channel",dest="channel", action="store", type="string",
		    default='rgb',help="channel to consider [r][g][b][a]", metavar="CHANNEL")
    parser.add_option("-b", "--bitnum",dest="bitnum", action="store", type="string",
		    default="0",help="bit to consider in pixel\'s channels [0..7]", metavar="BITNUM")
    (options, args) = parser.parse_args()

    if options.filename == None :
        parser.error("Input image is mandatory!")

    mtch = re.compile('[a|r|g|b]{1,4}').match(options.channel.lower())

    if mtch is None :
        print 'ERROR: invalid channel specification'
        exit(-1)

    inputim = options.filename
    channels = mtch.group()
    bitnum = [ int(b)%7 for b in options.bitnum ]
    outim = inputim+"-lsb-"+channels+"-"+options.bitnum+".png"

    n = Image.open(inputim)
    n = n.convert('RGBA')
    m = n.load()
    s = n.size

    print 'Image size: '+str(s)
    print 'Processing..'

    for x in range(s[0]):
        for y in range(s[1]):
            #print m[x,y]
            r,g,b,a = m[(x,y)]
            r1 = 0
            g1 = 0
            b1 = 0
            a1 = 255
            if ( 'r' in channels and all( [ (r&(0x01<<i))>>i==1 for i in bitnum]) ):
                 r1= 255
            else:
                 r1=0
            if ( 'g' in channels and all( [ (g&(0x01<<i))>>i==1 for i in bitnum]) ):
                 g1=255
            else:
                 g1=0
            if ( 'b' in channels and all( [ (b&(0x01<<i))>>i==1 for i in bitnum]) ):
                 b1=255
            else:
                 b1=0
            if ( 'a' in channels and all( [ (a&(0x01<<i))>>i==1 for i in bitnum]) ):
                 a1=255
            else:
                 if ( 'a' in channels):
                      a1=0
            m[(x,y)] = r1,g1,b1,a1

    print 'Writing output to file: %s' %(outim)
    n.save(outim, "PNG")

