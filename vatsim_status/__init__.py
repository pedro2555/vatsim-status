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

import shelve
import vatsim_status
from os.path import isfile


__author__ = 'Pedro Rodrigues'
__email__ = 'prodrigues1990@gmai.com'

COUNTRIES = {}
GEOMETRIES = {}
AIRPORTS = {}
CALLSIGNS = {}
UIRS = {}


def _lines(file):
    with open(file=file) as lines:
        for line in lines:
            yield line.strip()


def _load_from_shelf_or_txt(shelf_file, txt_file, output, txt_parser):
    if isfile('%s.db' % shelf_file):
        with shelve.open(shelf_file) as shelf:
            output = shelf['data']
    elif isfile(txt_file):
        with shelve.open(shelf_file, writeback=True) as shelf:
            shelf['data'] = output
            txt_parser(file=txt_file)
    else:
        raise FileNotFoundError('unable to locate either %s or %s' % (
            shelf_file,
            txt_file))


def _load_callsigns(db_file, txt_file):
    _load_from_shelf_or_txt(
        db_file,
        txt_file,
        vatsim_status.CALLSIGNS,
        _load_callsigns_from_txt)


def _load_geometries(db_file, txt_file):
    _load_from_shelf_or_txt(
        db_file,
        txt_file,
        vatsim_status.GEOMETRIES,
        _load_geometries_from_txt)


def _load_geometries_from_txt(file):
    current_fir = None
    current_geometry = []
    for line in _lines(file=file):
        # early jump conditions
        if line.startswith(';'):
            continue
        if line == '':
            continue

        pieces = line.split('|')

        if len(pieces) == 10:
            if current_fir:
                if current_fir in vatsim_status.GEOMETRIES:
                    vatsim_status.GEOMETRIES[current_fir]['type'] = 'Polygon'
                    vatsim_status.GEOMETRIES[current_fir]['coordinates'] = [
                        vatsim_status.GEOMETRIES[current_fir]['coordinates'],
                        current_geometry]
                else:
                    vatsim_status.GEOMETRIES[current_fir] = {
                        'type': 'Point',
                        'coordinates': current_geometry
                    }

            (
                icao, anumber1, anumber2, anumber2, lat1, lng1, lat2, lng2,
                lat3, lng3
            ) = pieces

            current_fir = icao
            current_geometry = []

        if len(pieces) == 2:
            lat, lng = pieces
            current_geometry.append([lng, lat])

        continue


def _load_callsigns_from_txt(file):
    parsers = {
        '[Countries]': _parse_country,
        '[Airports]': _parse_airport,
        '[FIRs]': _parse_fir,
        '[UIRs]': _parse_uir,
        '[IDL]': _parse_idl
    }

    current_parser = None
    for line in _lines(file=file):

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


_load_callsigns(db_file='vatsim_status/callsigns',
                txt_file='vatsim_status/callsigns.txt')

_load_callsigns(db_file='vatsim_status/geometries',
                txt_file='vatsim_status/fir_boundaries.txt')

# FIRS = load_firs(file='vatsim_status/fir_boundaries.txt')
