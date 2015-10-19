#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 stk <stk@101337>
#
# Distributed under terms of the MIT license.

"""

"""
from media.media import Media
from StringIO import StringIO
import re
from bitstring import BitString, BitStream
from math import floor

class AEncoder(object):
  ''' Abstract Encoder, do not use. Should only provide an useful base for specific encoders '''

  def __init__(self, media, direction=None):
    if media is None:
      raise Exception("Cannot create the encoder with None media")
    self.media=media
    if direction is None:
      self.direction=tuple(xrange(len(media.dim)))
    elif len(media.dim) == len(direction) and all(map(lambda x: x<len(media.dim) and x>=0,direction)):
      self.direction=direction
    else:
      raise Exception("Direction specified in the encoder sucks. double check it ({})".format(direction))

  def decodeStream(self):
    return StringIO(self.decode()) 
  def decodeRectStream(self, p1, p2):
    return StringIO(self.decodeRect(p1,p2))
  def decode(self):
    return self.decodeRect(tuple([0]*len(self.media.dim)),self.media.dim)
  def decodeRect(self, p1, p2):
    if len(self.media.dim)!=len(p1) or len(p1)!=len(p2):
      raise Exception("Dimension of the specified coordinates does not match dimensions of the space of the media")
    if all(map(lambda x,y: x<y, p1,self.media.dim)) and all(map(lambda x: x>=0,p1)) and \
       all(map(lambda x,y: x<y, p2,self.media.dim)) and all(map(lambda x: x>=0,p2)):
      raise Exception("Coordinates out of the media space range")
    self.reset()
    bits=BitString()
    for c_val in self.iterateValues(p1,p2,self.direction):
       try:
         bbb=self.decodeValue(c_val, payload, c_val[:-1])
         bits.append(bbb)
       except Exception,e:
         # TODO: log exception
         pass
    return bits.tobytes()

  def availableSpace(self):
    ''' Estimate available space in the media '''
    return 0

  def reset(self):
    ''' Reset the encoder '''
    # Put here your algorithm initial conditions
    pass

  def encodeRectStream(self, data, p1, p2):
    self.encodeRect(data.read(),p1,p2)
  def encodeStream(self,data):
    self.encode(data.read()) 
  def encode(self, data):
    self.encodeRect(data, tuple([0]*len(self.media.dim)), self.media.dim)
  def encodeRect(self, data, p1, p2):
    if len(self.media.dim)!=len(p1) or len(p1)!=len(p2):
      raise Exception("Dimension of the specified coordinates does not match dimensions of the space of the media")
    if all(map(lambda x,y: x<y, p1,self.media.dim)) and all(map(lambda x: x>=0,p1)) and \
       all(map(lambda x,y: x<y, p2,self.media.dim)) and all(map(lambda x: x>=0,p2)):
      raise Exception("Coordinates out of the media space range")
    self.reset()
    bits=BitStream(bytes=data)
    for c_val in self.iterateValues(p1,p2,self.direction):
      try:
        vvv=self.encodeValue(c_val, bits)
        self.media.set(vvv, c_val[:-1])
      except Exception,e:
        # TODO: log exception
        pass
      
  def decodeValue(self, coords_and_chunk, **params):
    ''' Must return a BitString '''
    raise Exception('please do not use AEncoder.decodeValue, A is for Abstract..')
    return BitString(coords_and_chunk[:-1])
  def encodeValue(self, coords_and_chunk, valuebitstream, **params):
    ''' Must return the new value for the specified coordinates '''
    raise Exception('please do not use AEncoder.encodeValue, A is for Abstract..')
    return coords_and_chunk[:-1]

  def iterateValues(self, p1, p2, direction):
    raise Exception('please do not use AEncoder. A is for Abstract..')
    for coord in [p1, p2]:
      yield tuple(list(coord)+[self.media.toNumpy(coord)]) # You must return coordinates AND values


class AEncoderChannels(AEncoder):
  ''' Channels encoder '''
  def __init__(self, media, direction=None, channels='rgb', bits=[0], channelmap={'r':0,'g':1,'b':2,'a':3}):
    super(AEncoderChannels,self).__init__(media, direction=direction)
    if not all(map(lambda x:x>=0, channelmap.values())) or len(set(channelmap.values())) != len(channelmap.values()):
      raise Exception("invalid channel map specification '{}'".format(str(channelmap)))
    self.channelmap=channelmap
    if not re.match("^({})+$".format('|'.join(channelmap.keys())),channels) or len(set(channels))!=len(channels):
      raise Exception("invalid channel specification '{}'. Current channel mapping: {}".format(channels,str(channelmap)))
    self.channels=channels
    self._channels=map(lambda x: x[1],[(c,channelmap.get(c)) for c in self.channels])
    if not all(map(lambda x:x>=0 and x<self.media.channel_bitness, bits)) or len(set(bits)) != len(bits):
      raise Exception("invalid bit position specification '{}'".format(bits))
    self.bits=bits
  
  def availableSpace(self):
    return int(floor(reduce(lambda x,y: x*y, self.media.dim)*len(self.bits)*len(self.channels)/8.0))


class AEncoderLinear(AEncoderChannels):
  ''' Basic encoder operates on a linear subset of media values (eg. a rectangle)'''
  def __init__(self, media, direction=None, channels='rgb', bits=[0], channelmap={'r':0,'g':1,'b':2,'a':3}):
    super(AEncoderLinear,self).__init__(media, direction=direction, channels=channels, bits=bits, channelmap=channelmap)

  def iterateValues(self, p1, p2, direction):
    dims_and_start=zip(xrange(len(p1)), p1)  # [ (index,minvalue),]
    dims_and_end  =zip(xrange(len(p1)), p2)  # [ (index,maxvalue),]
    # sort coordinates by direction
    dim_to_iter_start=reduce(lambda x,y:x+y,[ [dd for dd in dims_and_start if dd[0]==j] for j in direction] ) 
    dim_to_iter_end  =reduce(lambda x,y:x+y,[ [dd for dd in dims_and_end   if dd[0]==j] for j in direction] ) 
    # iterate media values usinc coordinates sorted by specified direction.
    # TODO: support decreasing coords
    def recourse(dims_start, dims_end, indexes):
      if len(dims_start)==0 and len(dims_end)==0:
        tmp = map(lambda x: x[1], sorted(indexes))
        yield tuple(tmp + [ self.media.toNumpy()[tuple(tmp)] ])
      else:
        for i in xrange(dims_start[0][1],dims_end[0][1]):
          indexes.append((dims_start[0][0],i))
          recourse(dims_start[1:], dims_end[1:], indexes)

    for coord in recourse(dim_to_iter_start,dim_to_iter_end,[]):
      yield coord




#
# Actual Encoders
#

class EncoderLSBStopbit(AEncoderLinear):
  ''' 
        Classic stopbit LSB: stego on bit 0 of the rgb channel with END bit in blue channel  
        | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | 
        | 765   432   10- | 765   432   10- | 765   432   10END |

  '''
  def __init__(self,media, channels='rgb', bits=[0], channelmap={'r':0,'g':1,'b':2}):
    super(EncoderLSBStopbit,self).__init__(media, direction=None, channels=channels, bits=bits, channelmap=channelmap)

  def reset(self):
    self._iterbindex=7 # lsb
    self._iterbitnum=0
    self._checkend=2
    self._end=False

  def decodeValue(self, coords_and_chunk, **params):
    coords = coords_and_chunk[:-1]
    value  = coords_and_chunk[-1]
    mask   = 0x01
    payload=BitString()
    last_chan=self._channels[-1]
    chans=self._channels[:-1]
    if not self._end:
      # | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | 
      # | 765   432   10- | 765   432   10- | 765   432   10E |
      for i in chans:
        payload.append(BitString(bool=(value[i] & mask)))
      lastbit=BitString(bool=(value[last_chan] & mask))
      if self._checkend==0 and lastbit.bool:
        self._end=True
      else:
        self._checkend=3
        payload.append(lastbit)
      self._checkend-=1
    return payload

  def encodeValue(self, coords_and_chunk, valuebitstream, **params):
    coords = coords_and_chunk[:-1]
    value  = coords_and_chunk[:-1]
    mask   = 0x01 << (self._iterbitnum%7)
    last_chan=self._channels[-1]
    chans  = self._channels[:-1]
    payload=BitString()
    if self._end:
      return value
    new_value = [x for x in value]
    if not self._end:
      # | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | 
      # | 765   432   10- | 765   432   10- | 765   432   10E |
      for i in chans: 
        if valuebitstream.pos < valuebitstream.len:
          val = valuebitstream.read(1)
          new_value[i] = value[i]&(0xfe<<0) | ((val.int&0x01)<<0) 
      if self._checkend>0:
        self._checkend-=1
        if valuebitstream.pos < valuebitstream.len:
          val = valuebitstream.read(1)
          new_value[last_chan] = value[last_chan]&(0xfe<<0) | ((val.int&0x01)<<0)
      else:
        if not valuebitstream.pos < valuebitstream.len:
          # END BIT
          new_value[last_chan] = value[last_chan]&(0xfe<<0) | ((val.int&0x01)<<0)
          self._end=True
        self._checkend=2
    return new_value


class EncoderLSB(AEncoderLinear):
  '''
      Raw Lsb algorithm.
      | rgba | rgba | rgba | rgba | ...
      | 7654   3210 | 7654   3210 | ...
      | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb | rgb |
      | 765   432   107 | 654   321   076 | 543   210   765 | 432   107 |
      | rg | rg | rg | rg | rg  ...
      | 76   54   32   10 | 76  ...
      | r | r | r | r ...
      | 7   6   5   4 ...
  '''
  def __init__(self, media, direction=None, channels='rgb', bits=[0], channelmap={'r':0,'g':1,'b':2}):
    super(EncoderLSB,self).__init__(media, direction=direction, channels=channels, bits=bits, channelmap=channelmap)

  def decodeValue(self, coords_and_chunk, **params):
    coords = coords_and_chunk[:-1]
    value  = coords_and_chunk[:-1]
    payload=BitString()
    for chan in self._channels:
      for bit in self.bits:
        mask = 0x01 << bit
        payload.append(BitString(bool=(value[chan] & mask) ))
    return payload

  def encodeValue(self, coords_and_chunk, valuebitstream, **params):
    coords = coords_and_chunk[:-1]
    value  = coords_and_chunk[:-1]
    new_value = [x for x in value]
    for chan in self._channels:
      for bit in self.bits:
        if valuebitstream.pos < valuebitstream.len:
          val = valuebitstream.read(1)
        else:
          return new_value
        mask = 0x01 << bit
        new_value[chan] = value[chan] & (0xfd << bit) | (val & mask)
    return new_value

