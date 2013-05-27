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

    0.3
"""
import Image
import sys
import re
from optparse import OptionParser


def echoPixels(n,subimage,channels='rgb',vertical=False):
    s = n.size
    (xinit,yinit,xend,yend)=(subimage[0],subimage[1],subimage[2],subimage[3])
    F = min(s[0],xend)
    f = xinit
    S = min(s[1],yend)
    s = yinit
    if vertical == True:
        F = min(s[1],yend)
        f = yinit
        S = min(s[0],xend)
        s = xinit
    for x in range(f,F,1):
        for y in range(s,S,1):
            if vertical == True:
                r,g,b,a = m[(y,x)]
            else:
                r,g,b,a = m[(x,y)]
            r,g,b,a = m[(x,y)]
            for chan in channels:
                if 'r' == chan :
                     sys.stdout.write(chr(r))
                if 'g' == chan :
                     sys.stdout.write(chr(g))
                if 'b' == chan :
                     sys.stdout.write(chr(b))
                if 'a' == chan :
                     sys.stdout.write(chr(a))


#-------------------------------------------------------------------------------
# MAIN 
#-------------------------------------------------------------------------------
if __name__ == "__main__":

    parser = OptionParser("usage: %prog [OPTIONS] ARGS \nDefault output in STDOUT")
    parser.add_option("-f", "--file", dest="filename", action="store", type="string",
                      help="image where to read pixels", metavar="FILE")
    parser.add_option("-c", "--channel",dest="channel", action="store", type="string",
                      default='rgb',help="channel to consider [r][g][b][a]. Order is relevant.", metavar="CHANNEL")
    parser.add_option("-v", "--vertical",dest="vertical", action="store_true", 
                      default=False,help="Extract per column instead of per row ", metavar="VERTICAL")
    parser.add_option("-r", "--rectangle",dest="rectangle", action="store",type="string",
                      default="0,0,max,max",help="define a sub-image area where to extract data", metavar="RECTANGLE")
    (options, args) = parser.parse_args()

    if options.filename == None :
        parser.error("Input image is mandatory!")

    mtch = re.compile('[a|r|g|b]{1,4}').match(options.channel.lower())

    if mtch is None :
        print 'ERROR: invalid channel specification'
        exit(-1)
    subimage=options.rectangle.replace('max',str(sys.maxint)).split(',')
    try:
        for i in range(4):
            subimage[i] = int(subimage[i])
    except:
        print 'WARNING: Subimage specification not correct, using whole image'
        subimage=[0,0,str(sys.maxint),str(sys.maxint)]
    inputim = options.filename
    channels = mtch.group()

    n = Image.open(inputim)
    n = n.convert('RGBA')
    m = n.load()
    
    echoPixels(n,subimage,channels,options.vertical)

