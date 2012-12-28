#!/usr/bin/python
# -*- coding: latin1 -*-
"""
SYNOPSIS

Shift image pixels in several ways

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

import numpy as np
import Image, sys, re
from optparse import OptionParser

#-------------------------------------------------------------------------------
# MAIN 
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    
    parser = OptionParser("usage: %prog [OPTIONS] ARGS \nDefault output in STDOUT")
    parser.add_option("-f", "--file", dest="filename", action="store", type="string",
                      help="image where to read pixels", metavar="FILE")
    parser.add_option("-v", "--vertical", dest="vertical", action="store_true", 
                      help="Shift in vertical direction (Y)", metavar="VERTICAL")
    parser.add_option("-p", "--period", dest="period", action="store", type="int", default=1,
                      help="Specify the which line will shift, eg. 2 means once on two", metavar="PERIOD")
    parser.add_option("-s", "--shift", dest="shift", action="store", type="int", default=1,
                      help="Specify shifting step (eg. -3 means shift -3 pixel)", metavar="SHIFT")
    parser.add_option("-c", "--channel",dest="channel", action="store", type="string",
                      default='rgb',help="channel to consider [r][g][b][a].", metavar="CHANNEL")

    (options, args) = parser.parse_args()

    if options.filename == None :
        parser.error("Input image is mandatory!")

    mtch = re.compile('[a|r|g|b]{1,4}').match(options.channel.lower())

    if mtch is None :
        print 'ERROR: invalid channel specification'
        exit(-1)

    inputim = options.filename
    channels = mtch.group()
    vert=options.vertical
    shift=options.shift
    period= options.period

    outim=inputim+"-shit"+str(shift)+"-"+channels+".png"
    n = Image.open(inputim)
    n = n.convert('RGBA')
    m = n.load()
    s = n.size

    nn = Image.new( n.mode, n.size, "black")
    nn = nn.convert('RGBA')
    mm = nn.load()

    #print 'Image size: '+str(s)
    #print 'Processing..'

    if vert:
        xmax=s[1]
        ymax=s[0]
    else:
        xmax=s[0]
        ymax=s[1]

    if shift>=0:
        xmin=xmax-1
        xmax=0-1
        step=-1
    else:
        #xmax=xmax
        xmin=0
        step=1

    for x in range(xmin,xmax,step):
        for y in range(ymax):
            #print m[x,y]
            r1,g1,b1,a1 = r,g,b,a = m[(x,y)]
            xs = x
            if (y % period == 0):
                xs+=shift
                r2,g2,b2,a2=m[(xs%max([xmax,xmin]),y)]
                if ( 'r' in channels ):
                     r1=r2
                if ( 'g' in channels ):
                     g1=g2
                if ( 'b' in channels ):
                     b1=b2
                if ( 'a' in channels ):
                     a1=a2
            #print (x,xs)
            mm[(x,y)]=r1,g1,b1,a1
    print 'Writing output to file: %s' %(outim)
    nn.save(outim, "PNG")

