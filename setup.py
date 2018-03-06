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
from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'HISTORY.md'), encoding='utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    'setuptools',
    'setuptools-lint',
    'flake8',
    'ddt'
]

setup(
    name='vatsim_status',
    description="Status data API for VATSIM",
    long_description=readme,
    author="Pedro Rodrigues",
    author_email='prodrigues1990@gmai.com',
    url='https://github.com/pedro2555/vatsim-status',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,
    install_requires=requirements,
    license="GPLv2",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
