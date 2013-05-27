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
import Image
import sys
import re
import inspect
from optparse import OptionParser

#-------------------------------------------------------------------------------
# MAIN 
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    algs=[k for (k,v) in sys.modules['stego_algs'].__dict__.items() if inspect.isclass(v) and k != 'Algorithm']

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
                      default=algs[0],help="extraction algorithm to use "+str(algs), metavar="ALGORITHM")
    parser.add_option("-v", "--vertical",dest="vertical", action="store_true", default=False,help="Extract per column instead of per row ", metavar="VERTICAL")
    parser.add_option("-r", "--rectangle",dest="rectangle", action="store",type="string",default="0,0,max,max",help="define a sub-image area where to extract data", metavar="RECTANGLE")


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
    coverim = options.filename
    outim = options.output
    channels = chnls.group()
    bitnum = [int(x) for x in bnms.group() ]

    n = Image.open(coverim)
    n = n.convert("RGBA")
    s = n.size

    embedder = sys.modules['stego_algs'].__dict__.get(algorithm)(n,channels,bitnum,options.vertical)

    n = embedder.write(sys.stdin,subimage[0],subimage[1],subimage[2],subimage[3])

    print 'Saving file to '+outim

    n.save(outim, "PNG")

