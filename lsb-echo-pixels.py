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

import numpy as np
import Image, sys, re
from optparse import OptionParser

parser = OptionParser("usage: %prog [OPTIONS] ARGS \nDefault output in STDOUT")

parser.add_option("-f", "--file", dest="filename", action="store", type="string",
                  help="image where to read pixels", metavar="FILE")
parser.add_option("-c", "--channel",dest="channel", action="store", type="string",
                  default='rgb',help="channel to consider [r][g][b][a]. Order is relevant.", metavar="CHANNEL")

(options, args) = parser.parse_args()

if options.filename == None :
    parser.error("Input image is mandatory!")

mtch = re.compile('[a|r|g|b]{1,4}').match(options.channel.lower())

if mtch is None :
    print 'ERROR: invalid channel specification'
    exit(-1)

inputim = options.filename
channels = mtch.group()

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

        if ( 'r' in channels ):
             sys.stdout.write(chr(r))
        if ( 'g' in channels ):
             sys.stdout.write(chr(g))
        if ( 'b' in channels ):
             sys.stdout.write(chr(b))
        if ( 'a' in channels ):
             sys.stdout.write(chr(a))

