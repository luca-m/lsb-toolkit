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

from PIL import Image
import re
from optparse import OptionParser


PIX_OPS=[ ('diff',lambda a,b:a-b),('add',lambda a,b:a+b),
            ('xor',lambda a,b:a^b),('div',lambda a,b:a/b),
            ('mul',lambda a,b:a*b) ]

def pixop(n,no,channels,op=lambda a,b:0):
    """ 
        Pixel per pixel (or better channel per channel) operation.
        Results in n. Returns n.
    """
    n = n.convert('RGBA')
    no = n.convert('RGBA')
    s = n.size
    so = no.size
    m = n.load()
    mo = no.load()
    for x in range(min([s[0],so[0]])):
        for y in range(min([s[1],so[1]])):
            r1,g1,b1,a1 = (255,255,255,255)
            if 'a' in channels:
                r,g,b,a = m[(x,y)]
                ro,go,bo,ao = mo[(x,y)]
            else:
                r,g,b=m[(x,y)]
                ro,go,bo=mo[(x,y)]
                a=ao=255
            if 'r' in channels : 
                r1=op(r,ro)
            if 'g' in channels: 
                g1=op(g,go)
            if 'b' in channels: 
                b1=op(b,bo)
            if 'a' in channels: 
                a1=op(a,ao)
            if 'a' in channels:
                m[(x,y)] = r1,g1,b1,a1
            else:
                m[(x,y)]=r1,g1,b1
    return n


#-------------------------------------------------------------------------------
# MAIN 
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    OPS=[x for (x,_) in PIX_OPS ]
    parser = OptionParser("usage: %prog [OPTIONS] ARGS \nDefault output in <imagepath>-lsb.png")
    parser.add_option("-f", "--file", dest="filename", action="store", type="string",
                      help="image to analyze", metavar="FILE")
    parser.add_option("-o", "--original", dest="original", action="store", type="string",
                      help="original file to subtract", metavar="FILE")
    parser.add_option("-c", "--channel",dest="channel", action="store", type="string",
                      default="rgb",help="channel to consider [r][g][b][a]", metavar="CHANNEL")
    parser.add_option("-x", "--pixop",dest="pixop", action="store", type="string",
                      default=OPS[0],help="pixel per pixel operation. Options: "+str(OPS), metavar="PIXOP")

    (options, args) = parser.parse_args()

    if options.filename == None :
        parser.error("Input image is mandatory!")

    mtch = re.compile('[a|r|g|b]{1,4}').match(options.channel.lower())

    if mtch is None :
        print 'ERROR: invalid channel specification'
        exit(-1)

    if options.pixop not in OPS:
        print 'ERROR: invalid pixel operation'
        exit(-1)

    op=[x for (y,x) in PIX_OPS if y==options.pixop][0]
    inputim = options.filename
    inputor = options.original
    channels = mtch.group()
    outim = inputim+"-diff-"+channels+".png"
    
    n = Image.open(inputim)
    no = Image.open(inputor)
    n = pixop(n,no,channels,op)
    print 'Writing output to file: %s' %(outim)
    n.save(outim,'PNG')
