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
from PIL import Image 
import re
import inspect
import sys 
import stego_algs
from optparse import OptionParser

#-------------------------------------------------------------------------------
# MAIN 
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    algs=[k for (k,v) in stego_algs.__dict__.items() if inspect.isclass(v) and k != 'Algorithm']

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
                      default=algs[0],help="extraction algorithm to use "+str(algs)+" (Default:"+algs[0]+")", metavar="ALGORITHM")
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

    extractor = stego_algs.__dict__.get(algorithm)(n,channels,bitnum,options.vertical)
    by = extractor.read(subimage[0],subimage[1],subimage[2],subimage[3])

    if len(by) > 0 :
        if outfile is None:
            by.tofile(sys.stdout)
        else:
            print 'Writing output to file: %s' %outfile
            with open(outfile,"wb") as of:
                by.tofile(of)
    else:
        print 'No data extracted.'

