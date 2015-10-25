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
    e=encoder.EncoderLSB(m, channels='r')
    pr = cProfile.Profile()
    s = StringIO.StringIO()
    pr.enable()
    data=e.decodeRect((0,10),(15,20))
    pr.disable()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()
    print('decoded {} bytes. Head={}'.format(len(data),data[:5].encode('hex')))
    self.assertIsNotNone(data)
    e=encoder.EncoderLSB(m, channels='r',direction=(1,0))
    pr = cProfile.Profile()
    s = StringIO.StringIO()
    pr.enable()
    data=e.decodeRect((0,10),(15,20))
    pr.disable()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()
    print('decoded {} bytes. Head={}'.format(len(data),data[:5].encode('hex')))
    self.assertIsNotNone(data)


if __name__ == '__main__':
  unittest.main()
