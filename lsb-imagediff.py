#!/usr/bin/python
# -*- coding: latin1 -*-
"""
SYNOPSIS

Create a new image with the pixel per pixel subtraction result of two images

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
    
    parser = OptionParser("usage: %prog [OPTIONS] ARGS \nDefault output in <imagepath>-lsb.png")
    parser.add_option("-f", "--file", dest="filename", action="store", type="string",
                      help="image to analyze", metavar="FILE")
    parser.add_option("-o", "--original", dest="original", action="store", type="string",
                      help="original file to subtract", metavar="FILE")
    parser.add_option("-c", "--channel",dest="channel", action="store", type="string",
                      default="rgb",help="channel to consider [r][g][b][a]", metavar="CHANNEL")
    #TODO: add XOR/ADD and other pixel operations support

    (options, args) = parser.parse_args()

    if options.filename == None :
        parser.error("Input image is mandatory!")

    mtch = re.compile('[a|r|g|b]{1,4}').match(options.channel.lower())

    if mtch is None :
        print 'ERROR: invalid channel specification'
        exit(-1)

    inputim = options.filename
    inputor = options.original
    channels = mtch.group()
    #bitnum = [ int(b)%7 for b in options.bitnum ]
    outim = inputim+"-diff-"+channels+".png"

    n = Image.open(inputim)
    n = n.convert('RGBA')
    m = n.load()
    s = n.size

    no = Image.open(inputor)
    no = no.convert('RGBA')
    mo = no.load()
    so = no.size

    print 'Image size: '+str(s)
    print 'Processing..'

    for x in range(min([s[0],so[0]])):
        for y in range(min([s[1],so[1]])):
            #print m[x,y]
            r,g,b,a = m[(x,y)]
            r1,g1,b1,a1 = (255,255,255,255)
            ro,go,bo,ao = mo[(x,y)]
            if ( 'r' in channels ): 
                 r1=r-ro
            if ( 'g' in channels ): 
                 g1=g-go
            if ( 'b' in channels ): 
                 b1=b-bo
            if ( 'a' in channels ): 
                 a1=a-ao
            #print r,g,b,a,ro,go,bo,ao, r1,g1,b1,a1
            m[(x,y)] = r1,g1,b1,a1

    print 'Writing output to file: %s' %(outim)
    n.save(outim, "PNG")

