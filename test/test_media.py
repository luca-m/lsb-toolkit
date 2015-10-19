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
import media.media as media
from os import path
from os import unlink 

class TestImageMedia(unittest.TestCase):

  def test_load(self):
    print('loading lena')
    m=media.ImageMedia('./test/lenna.png')
    print(m.channel_bitness)
    print(m.nchannels)
    print(m.dim)
    self.assertEqual(m.channel_bitness,8)
    self.assertEqual(m.nchannels,3)
    self.assertEqual(m.dim,(512,512))
  def test_save(self):
    print('loading lena')
    m=media.ImageMedia('./test/lenna.png')
    print('saving lena')
    m.saveToFile('./test/lenna.png.copy')
    self.assertTrue(path.exists('./test/lenna.png.copy'))
    unlink('./test/lenna.png.copy')


if __name__ == '__main__':
  unittest.main()
