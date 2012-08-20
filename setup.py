# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2001-2012 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT

import os

# Use the VERSION file to get version
version_file = os.path.join(os.path.dirname(__file__), 'src', 'graf', 'VERSION')
with open(version_file) as fh:
    grafpython_version = fh.read().strip()

import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

#
# Prevent setuptools from trying to add extra files to the source code
# manifest by scanning the version control system for its contents.
#
#from setuptools.command import sdist
#   del sdist.finders[:]

setup(
    name = "graf-python",
    description = "Python GrAF API",
    version = grafpython_version,
    url = "https://github.com/cidles/graf-python",
    long_description = "Python implementation of the Graph Annotation Framework. (http://www.americannationalcorpus.org/graf-wiki)",
    license = "Apache License, Version 2.0",
    keywords = ['NLP', 'CL', 'natural language processing',
                'computational linguistics', 'parsing', 'tagging',
                'annotation', 'linguistics', 'language',
                'natural language'],
    maintainer = "Peter Bouda",
    maintainer_email = "pbouda@cidles.eu",
    author = "Stephen Matysik",
    author_email = "smatysik@gmail.com",
    classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Human Machine Interfaces',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: General',
    'Topic :: Text Processing :: Indexing',
    'Topic :: Text Processing :: Linguistic',
    ],
    packages = [ 'graf' ],
    package_dir = {'':'src'},
    package_data = {'graf': ['VERSION']},
    #install_requires=['PyYAML>=3.09'],
    #test_suite = 'nltk.test.simple',
    )