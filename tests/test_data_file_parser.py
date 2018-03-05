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
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from ddt import ddt, data, file_data, unpack

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
    def testPiecesToObject_correctKeyValueAssigment_objectEquals(
        self, keys, pieces, expected):
        """Keys and values assigned, empty values trimmed out"""
        obj = data_file_parser.pieces_to_object(keys, pieces)
        self.assertEqual(obj, expected)

    @unpack
    @data(
        {'keys': 'k1:k2', 'pieces': 'v'},
        {'keys': 'k', 'pieces': 'v1:v2'},
        {'keys': 'k', 'pieces': 'v1:v2:'}
    )
    def testPiecesToObject_differentSizeKeysPieces_throwsValueError(
        self, keys, pieces):
        """Wrongly sized pieces should throw a ValueError with the pieces"""
        with self.assertRaisesRegex(ValueError, '(%s)' % pieces):
            obj = data_file_parser.pieces_to_object(keys, pieces)

    def tearDown(self):
        pass
