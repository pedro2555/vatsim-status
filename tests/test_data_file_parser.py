#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Vatsim Status API
Copyright (C) 2018  Pedro Rodrigues <prodrigues1990@gmai.com>

This file is part of Vatsim Status API.

Vatsim Status API is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

Vatsim Status API is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Vatsim Status API.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest
from ddt import ddt, data, unpack

from vatsim_status import data_file_parser


@ddt
class TestDataFileParser(unittest.TestCase):

    def setUp(self):
        pass

    @unpack
    @data(
        {
            'keys': 'k', 'pieces': 'v',
            'expected': {'k': 'v'}
        },
        {
            'keys': 'k1:k2', 'pieces': 'p1:p2',
            'expected': {
                'k1': 'p1',
                'k2': 'p2'
              }
        },
        {
            'keys': 'k::', 'pieces': 'v::',
            'expected': {
                'k': 'v'
            }
        }
    )
    def test_vzip_returns_expectedObject(self, keys, pieces, expected):
        self.assertEqual(data_file_parser.vzip(keys, pieces), expected)

    @unpack
    @data(
        {'keys': 'k1:k2', 'pieces': 'v'},
        {'keys': 'k', 'pieces': 'v1:v2'},
        {'keys': 'k', 'pieces': 'v1:v2:'}
    )
    def test_vzip_keyValuesDontMatch_throwsValueError(self, keys, pieces):
        with self.assertRaisesRegex(ValueError, '(%s)' % pieces):
            data_file_parser.vzip(keys, pieces)

    @unpack
    @data(
        {'keys': [], 'pieces': 'v'},
        {'keys': 'k', 'pieces': []},
        {'keys': [], 'pieces': []}
    )
    def test_vzip_nonStrings_throwsValueError(self, keys, pieces):
        with self.assertRaisesRegex(ValueError, '(%s)' % 'list'):
            data_file_parser.vzip(keys, pieces)

    def tearDown(self):
        pass
