lsb-toolkit
===========

This is a small and simple toolkit that might be useful during steganalysis, it is currently composed by several general purpose command line tools.

- Version: 0.3
- Author: luca.mella@studio.unibo.it
- License : Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)

##### STEGANALYSIS TOOLS
--------------------------------------------------------------------------------

###### lsb-enancher
  	Produce a picture from input image that enhance bit variations. 
	This particular picture might reveal suspicious patterns inside the analyzed image.

###### lsb-extract
	Dump the 'LSBs' of the image pixel with several modalities. For instance is
	possible to select wich channel consider during extraction ([a][r][g][b]) or 
	which bit consiter ([0..7]). 

	Supported algorithms:
	RAW LSB - examples (pixel/data-bits)
		channels=argb 
			pixel | rgba | rgba | rgba | rgba | 
			data  | 7654   3210 | 7654   3210 | 
		channels=rgb
			pixel | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb |
			data  | 765   432   107 | 654   321   076 | 543   210   765 | 432   107 |
		channels=rg
			pixel | rg | rg | rg | rg | rg  
			data  | 76 Basic Profile
		channels=r
			pixel | r | r | r | r 
			data  | 7   6   5   4 
	CLASSIC LSB - examples (pixel/data-bits)
		channel= rgb (mandatory)
			| rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | 
			| 765   432   10- | 765   432   10- | 765   432   10E |
			 '-' means unused, 'E' means end of bit stream (our "EOF")
			 In practice '-' is a 0-bit and 'E' becomes 1-bit

###### lsb-embed
	lsb-extract's dual tool.
	Embed data from STDINPUT into a picture using the same algorithms

###### lsb-randomness-b
	Calculate the randomness of a bit string.

###### lsb-autocorr-b
	Calculate theautocorrelation of a bit string measuring how much the shifted
	version of the bit string is similar to the original bit string.
	Number of shits and shift step are configurable.

###### lsb-chisquare
	Perform a chi-square test on an image pixel stream. This statistical test
	helps to determinate when the distribution of lsb is similar to a random 
	distribution (might reveal encrypted or compressed payload).
	If you need graphics use some external tool like gnuplot.

###### lsb-echo-pixels
	Utiliy that produce a pixel stream in output, in other world it 
	print out the integer values of the image pixels.
	Typical usage: /lsb-echo-pixels -f image.png | ./lsb-chisquare
	
###### lsb-image-create
	Create pictures from a pixel stream. It could be useful for visualizing raw files 
	in order to observe the presence of regular patterns, or also for recreate image 
	from an extracted pixel stream (eg. with lsb-echo-pixels)
	
###### lsb-imageop
	Utility for performing pixel per pixel operation on a couple of images.
	Can be really useful if user has access to the original steganography carrier. 

#### USAGE:
-----------------------------------------------------------------------------
	./lsb-extract.py -f image.png -o dump -c rgb -b 012
Means that you will extract the bit 0,1 and 2 from every pixel considering rgb 
channels. Note that rgb is different than grb and 012 is different than 102 !

Use --help on each tool for further detail.

#### FUTURE DEVELOPMENT:
-----------------------------------------------------------------------------
	- Support audio too..
	- Support more algorithms
	- Support more analysis (RS analysis?)

