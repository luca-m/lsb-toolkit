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

    0.1
"""
from PIL import Image
import math
import re
import os
from optparse import OptionParser

def create_image(rawpixelfile,h,w,channels='rgb'):
	""" Create an image from a raw file """
	pxls=list()
	with open(rawpixelfile, 'rb') as f:
		bytes=f.read(len(channels))
		while bytes!='':
			if len(bytes)==len(channels):
				(a,r,g,b)=(255,0,0,0)
				for i in range(len(bytes)):
					for c in channels:
						if 'a'==c:
							a=ord(bytes[i])
						elif 'r'==c:
							r=ord(bytes[i])
						elif 'g'==c:
							g=ord(bytes[i])
						elif 'b'==c:
							b=ord(bytes[i])
				pxls.append((a,r,g,b))
			bytes=f.read(len(channels))
	img=Image.new(channels,(w,h))
	img.putdata(pxls)
	return img

if __name__=='__main__':
	
	parser=OptionParser("usage: %prog [OPTIONS] ARGS \nDefault output in <filename>.png")
	parser.add_option("-f", "--file", dest="filename", action="store", type="string",
			help="File where to load pixel data", metavar="FILE")
	parser.add_option("-c", "--channel",dest="channel", action="store", type="string",
			default='rgb',help="channels to consider [r][g][b][a]", metavar="CHANNEL")
	(options, args) = parser.parse_args()

	if options.filename == None :
        	parser.error("Pixel file is mandatory!")
	mtch=re.compile('[a|r|g|b]{1,4}').match(options.channel.lower())
	if mtch is None :
		parser.error('ERROR: invalid channel specification')
	inputf=options.filename
	channels=mtch.group()
	outim=inputf+"-"+channels+".png"
	print "Usage: image-create.py <WIDTH> <HEIGHT> <INPIXELFILE> <OUTIMAGEFILE>"
	w=h=int(math.sqrt(os.stat(inputf).st_size/len(channels)))
	img=create_image(inputf,h,w,channels)
	img.save(outim)



