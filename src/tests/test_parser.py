# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2012 Poio Project
# Author: António Lopes <alopes@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT
"""This module contains the tests to the class
PyGraphParser in module PyGraphParser.

This test serves to ensure the viability of the
methods of the class PyGraphParser in PyGraphParser.py.
"""

from graf.PyGraphParser import PyGraphParser

import xml
import os

class TestPyGraphParser:
    """
    This class contain the test methods if the class PyGraphParser.

    """

    # Create the Graph Parser
    gparser = PyGraphParser()

    def test_parse(self):
        """Raise an assertion if can't find a file.

        Return a PyGraph.

        Raises
        ------
        AssertionError
            If the can't find the file.

        """

        # Change directory
        # Opening the expected file result
        file_result = os.path.dirname(__file__) + '/sample_files/' + \
                      'Balochi Text1-graid1.xml'

        g = self.gparser.parse(file_result)

        expected_result = 33

        assert(len(g.nodes()) == expected_result)

    def test_startElement(self):
        """Raise an assertion if can't set the tag value.

        Processes the opening xml tags, according to their type.
        It's a method from ContentHandler class.

        Raises
        ------
        AssertionError
            If can't set the tag value.

        """

        # Test values
        name = 'graph' # This value changes among the results.
        attrs = {'xmlns': 'http://www.xces.org/ns/GrAF/1.0/'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        # If name variable change to newname requires the graph_'newname'
        assert(self.gparser.startElement(name, attrs) == self.gparser.graph_start(attrs))

    def test_endElement(self):
        """Raise an assertion if can't find the node to end.

        Processes the end xml tags, according to their type.
        It's a method from ContentHandler class.

        Raises
        ------
        AssertionError
            If value is not the expected.

        """

        # Test values
        # Initialize a new GraphParser
        parser = PyGraphParser()

        name = 'graph' # This value changes among the results.
        attrs = {'xmlns': 'http://www.xces.org/ns/GrAF/1.0/'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        # Is need to start at least one node
        parser.startElement(name, attrs)

        # If name variable change to newname requires the graph_'newname'
        assert(parser.endElement(name) == parser.graph_end())