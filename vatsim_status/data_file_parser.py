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
from contextlib import suppress


def vzip(keys, pieces):
    """Parses a string of colon separated key strings into an object with the
    corresponding keys associated with the corresponding values.

    pieces_to_object('k', 'v')
    >>> {'k': 'v'}
    pieces_to_object('k1:k2', 'v1:v2')
    >>> {'k1': 'v2', 'k2': 'v2'}
    """
    try:
        keys = keys.split(':')
        pieces = pieces.split(':')
    except AttributeError:
        raise ValueError(
            "'string', 'string' expected %s, %s given: %s, %s" % (
                keys.__class__.__name__, keys,
                pieces.__class__.__name__, pieces))

    if len(keys) != len(pieces):
        raise ValueError(
            "Pieces count doesn't match keys count for '%s'" % (
                ':'.join(pieces)))

    obj = dict(zip(keys, pieces))

    # we will use this function to blindly populate mongo documents for the raw
    # data endpoints, so we want to avoid empty keys in particular; they don't
    # make much sense either
    with suppress(KeyError):
        del obj['']

    return obj
