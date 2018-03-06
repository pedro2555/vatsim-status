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

__author__ = 'Pedro Rodrigues'
__email__ = 'prodrigues1990@gmai.com'

COUNTRIES = {}
AIRPORTS = {}
CALLSIGNS = {}
UIRS = {}


def lines(file):
    with open(file=file) as lines:
        for line in lines:
            yield line.strip()


def _load_callsigns(file):
    parsers = {
        '[Countries]': _parse_country,
        '[Airports]': _parse_airport,
        '[FIRs]': _parse_fir,
        '[UIRs]': _parse_uir,
        '[IDL]': _parse_idl
    }

    current_parser = None
    for line in lines(file=file):

        # early jump conditions
        if line.startswith(';'):
            continue
        if line == '':
            continue

        # verify if we're in a new section
        if line in parsers:
            current_parser = line
            continue

        if current_parser is not None:
            parsers[current_parser](line.split('|'))


def _parse_country(pieces):
    name, identifier, callsign = pieces

    pieces = filter(lambda p: p != '' and p != identifier, pieces)
    COUNTRIES[identifier] = pieces


def _parse_airport(pieces):
    icao, name, lat, lng, callsign, fir, anumber = pieces

    identifier = callsign if callsign != '' else icao
    pieces = filter(lambda p: p != '' and p != callsign, pieces)

    CALLSIGNS[identifier] = icao
    AIRPORTS[icao] = {
        'name': name,
        'location': {'type': 'Point', 'coordinates': [lng, lat]}
    }


def _parse_fir(pieces):
    icao, name, callsign, fir = pieces

    if callsign != '':
        CALLSIGNS[callsign] = fir if fir != '' and fir != '0' else icao
    if fir != '' and fir != '0':
        CALLSIGNS[icao] = fir


def _parse_uir(pieces):
    identifier, name, firs = pieces

    pieces = filter(lambda p: p != identifier, pieces)
    UIRS[identifier] = pieces


def _parse_idl(pieces):
    pass


def _load_firs(file):
    pass


_load_callsigns(file='vatsim_status/callsigns.txt')

# FIRS = load_firs(file='vatsim_status/fir_boundaries.txt')
