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
import encoder.base_encoder as encoder
from media.media import ImageMedia
from os import path
from os import unlink 

class TestBaseEncoder(unittest.TestCase):

  def test_decode(self):
    print('loading lena')
    m=ImageMedia('./test/lenna.png')
    e=encoder.EncoderLSB(m)
    data=e.decode()
    print(data)
    self.assertIsNotNone(data)


if __name__ == '__main__':
  unittest.main()
