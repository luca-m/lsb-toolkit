#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 stk <stk@101337>
#
# Distributed under terms of the MIT license.

"""
sudo apt-get install libgdal-dev libgdal1h
"""
import numpy as np
import rasterio

def dtype2nbits(dtypename):
  if dtypename in ['uint8', 'int8']:
    return 8
  elif dtypename in ['uint16', 'int16', 'float16']:
    return 16
  elif dtypename in ['uint32', 'int32', 'float', 'float32']:
    return 32
  elif dtypename in ['uint64', 'int64','float64']:
    return 64
  elif dtypename in ['uint128', 'int128','float128']:
    return 128

class Media(object):
  ''' '''
  def __init__(self):
    self.data=np.empty(0)
    self.dim=self.data.shape[:-1]
    self.nchannels = self.data.shape[-1]
    self.channel_bitness=8
  def __iter__(self):
    pass
  def get(self, coords):
    if len(coords)!=len(self.dim):
      raise Exception("Dimension of the specified coordinates does not match dimensions of the space of the media")
    pass
  def distance(points):
    pass
  def getRect(self, p1, p2):
    if len(p1)!=len(self.dim) or len(p1)!=len(p2):
      raise Exception("Dimension of the specified coordinates does not match dimensions of the space of the media")
    pass
  def set(self, value, coords):
    if len(coords)!=len(self.dim):
      raise Exception("Dimension of the specified coordinates does not match dimensions of the space of the media")
    pass
  def setRect(self, values, p1, p2, p3, p4):
    if len(p1)!=len(self.dim) or len(p1)!=len(p2) or len(p1)!=len(p3) or len(p1)!=len(p4):
      raise Exception("Dimension of the specified coordinates does not match dimensions of the space of the media")
    pass
  def loadFromFile(self,path):
    pass
  def saveToFile(self,path):
    pass
  def toNumpy(self):
    return self.data;

class ImageMedia(Media):
  ''' '''
  def __init__(self,filepath=None, matrix=None):
    super(ImageMedia,self).__init__()
    if filepath is not None:
      self.loadFromFile(filepath)
    elif matrix is not None:
      self.loadMatrix(filepath)

  def loadMatrix(self, data, channel_first=False):
    ''' '''
    if channel_first:
      tmpnewdata=np.zeros((list(data.shape[1:])+[data.shape[0]]), dtype=data.dtype)
      # TODO: support more coords
      for x in xrange(tmpnewdata.shape[0]):
        for y in xrange(tmpnewdata.shape[1]):
          tmpnewdata[x,y,0:tmpnewdata.shape[-1]]=data[0:tmpnewdata.shape[-1],x,y]
      self.data=tmpnewdata
    else:
      self.data=data
    self._channel_first=channel_first
    self.dim=self.data.shape[:-1]
    self.nchannels = self.data.shape[-1]
    self.channel_bitness = dtype2nbits(self.data.dtype.name)
    return self.data
  def loadFromFile(self,path):
    ''' '''
    super(ImageMedia,self).loadFromFile(path)
    with rasterio.open(path) as src:
      tmpdata=src.read()
      self._profile=src.profile;
      return self.loadMatrix(tmpdata,channel_first=True)
  def saveToFile(self,path):
    ''' '''
    super(ImageMedia,self).saveToFile(path)
    if self._channel_first:
      tmpnewdata=np.zeros(([self.data.shape[-1]]+list(self.data.shape[:-1])), dtype=self.data.dtype)
      for x in xrange(tmpnewdata.shape[1]):
        for y in xrange(tmpnewdata.shape[2]):
          tmpnewdata[0:tmpnewdata.shape[0],x,y]=self.data[x,y,0:tmpnewdata.shape[0]]
    else:
      tmpnewdata=self.data
    if self._profile is None:
      self._profile={
           'compress': 'lzw',
           'dtype': self.data.dtype,
           'nodata': 0}
    with rasterio.open(path,'w',**self._profile) as dst:
      dst.write(tmpnewdata)
  def get(self, coords):
    ''' '''
    super(ImageMedia,self).get(coords)
    return self.data[coords]
  def getRect(self, p1, p2):
    super(ImageMedia,self).getRect(p1,p2)
    return self.data[p1[0]:p1[1]:1,p2[0]:p2[1]:1]
  def set(self, value, coords):
    super(ImageMedia,self).set(value, coords)
    self.data[coords] = value


