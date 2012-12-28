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

    0.4
"""

import numpy as np
import Image, sys, re
from optparse import OptionParser

parser = OptionParser("usage: %prog [OPTIONS] ARGS \nDefault output in STDOUT")

parser.add_option("-f", "--file", dest="filename", action="store", type="string",
                  help="image where to read pixels", metavar="FILE")
parser.add_option("-v", "--vertical", dest="vertical", action="store_true", 
                  help="Shift in vertical direction (Y)", metavar="VERTICAL")
parser.add_option("-p", "--period", dest="period", action="store", type="int", default=1,
                  help="Specify the which line will shift, eg. 2 means once on two", metavar="PERIOD")
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
period= options.period

outim=inputim+"-pick"+str(period)+"-"+channels+".png"
n = Image.open(inputim)
n = n.convert('RGBA')
m = n.load()
s = n.size

nn = Image.new( n.mode, n.size, "black")
nn = nn.convert('RGBA')
mm = nn.load()

print 'Image size: '+str(s)
print 'Processing..'

if vert:
    xmax=s[1]
    ymax=s[0]
else:
    xmax=s[0]
    ymax=s[1]

    xmin=0
    step=1

for x in range(xmin,xmax,step):
    for y in range(ymax):
        #print m[x,y]
        r,g,b,a = m[(x,y)]
        r1,g1,b1,a1 = 0,0,0,255
        if (y % period == 0):
            if ( 'r' in channels ):
                 r1=r
            if ( 'g' in channels ):
                 g1=g
            if ( 'b' in channels ):
                 b1=b
            if ( 'a' in channels ):
                 a1=a
        #print (x,xs)
        mm[(x,y)]=r1,g1,b1,a1
print 'Writing output to file: %s' %(outim)
nn.save(outim, "PNG")

