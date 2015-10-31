#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 stk <stk@101337>
#
# Distributed under terms of the MIT license.

"""

"""
import unittest
import cProfile, pstats, StringIO
import encoder.base_encoder as encoder
from media.media import ImageMedia
from os import path
from os import unlink 

class TestBaseEncoder(unittest.TestCase):

  def test_decode(self):
    print('loading lena')
    m=ImageMedia('./test/lenna.png')
    #e=encoder.EncoderLSB(m)
    #pr = cProfile.Profile()
    #s = StringIO.StringIO()
    #pr.enable()
    #data=e.decode()
    #pr.disable()
    #sortby = 'cumulative'
    #ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    #ps.print_stats()
    #print s.getvalue()
    #print('decoded {} bytes'.format(len(data)))
    #self.assertIsNotNone(data)
    print('test lsb w performance')
    e=encoder.EncoderLSB(m, channels='rgb')
    pr = cProfile.Profile()
    s = StringIO.StringIO()
    pr.enable()
    data0='CIAO!'
    e.encodeRect(data0,(0,10),(10,15))
    data=e.decodeRect((0,10),(10,15))
    pr.disable()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print('decoded {} bytes. Head={} Orig={}'.format(len(data),data[:5].encode('hex'),data0.encode('hex')))
    self.assertIsNotNone(data)
    self.assertEqual(data0,data[:5])
    print('test lsb stopbit w performance')
    e=encoder.EncoderLSBStopbit(m, channels='rgb')
    pr = cProfile.Profile()
    s = StringIO.StringIO()
    pr.enable()
    data0='NOAH!'
    e.encodeRect(data0,(0,10),(10,15))
    data=e.decodeRect((0,10),(10,15))
    pr.disable()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    #print s.getvalue()
    print('decoded {} bytes. Head={} Orig={}'.format(len(data),data[:5].encode('hex'),data0.encode('hex')))
    self.assertIsNotNone(data)
    self.assertEqual(data0,data[:5])
    print('test lsb y then x direction')
    e=encoder.EncoderLSB(m, channels='r',direction=(0,1))
    data0='CIA0!'
    e.encodeRect(data0,(0,10),(10,15))
    data1=e.decodeRect((0,10),(10,15))
    print('decoded {} bytes. Head={}, Orig={}'.format(len(data1),data1[:5].encode('hex'),data0[:5].encode('hex')))
    self.assertIsNotNone(data1)
    self.assertEqual(data0[:5],data1[:5])
    print('test lsb x then y direction')
    e=encoder.EncoderLSB(m, channels='r',direction=(1,0))
    data00='CIAK!'
    e.encodeRect(data00,(0,10),(10,15))
    data2=e.decodeRect((0,10),(10,15))
    print('decoded {} bytes. Head={}, Orig={}'.format(len(data2),data2[:5].encode('hex'),data00[:5].encode('hex')))
    self.assertIsNotNone(data2)
    self.assertNotEqual(data1[:5],data2[:5])
    self.assertEqual(data00[:5],data2[:5])


if __name__ == '__main__':
  unittest.main()
