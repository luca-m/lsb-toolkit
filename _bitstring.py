# -*- coding: utf8 -*-

class Distance:
    """
    Contains static methods for calculating distances between bitstrings
    """
    @classmethod
    def hamming (self, bitsr1 , bitsr2 ):
    	""" 
    		Returns the hamming distance of 2 bitstrings in interval [0.0,1.0]
    		Where 1.0 means maximum distance and 0.0 means equals
    	"""
        length = min(len(bitsr1),len(bitsr2))
        diff = 0
        for i in range(length):
            if bitsr1[i] != bitsr2[i]:
                diff+=1
        return diff / float(length+abs(len(bitsr1)-len(bitsr2)))

def bits(char):
	""" Convert a character to a bit-string """
	s=''
	for i in range(8):
		s = str( (char>>i) & 0x01 ) + s
	return s
