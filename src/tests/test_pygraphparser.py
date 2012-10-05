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

from graf.PyDocumentHeader import PyDocumentHeader
from graf.PyGraphParser import PyGraphParser

import xml

# Create the Graph Parser
gparser = PyGraphParser()

class TestPyGraphParser:
    """
    This class contain the test methods if the class PyGraphParser.

    """

    def test_parse(self):
        """Raise an assertion if can't find a file.

        Return a PyGraph.

        Raises
        ------
        AssertionError
            If the can't find the file.

        """

        # Test values
        # Initialize the graph parser
        parser = PyGraphParser()

        # Change directory
        file = '/home/alopes/nltk_data/corpora/masc/spoken/Day3PMSession-vc.xml'

        assert(parser.parse(file, None))

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
        assert(gparser.startElement(name, attrs) == gparser.graph_start(attrs))

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

    def test_characters(self):
        """Raise an assertion if can't set the character.

        Processes any characters within the xml file.
        It's a method from ContentHandler class.

        Raises
        ------
        AssertionError
            If can't set the character.

        """

        # Test values
        ch = '\n'

        error_message = 'Fail - Processing the characteres'

        assert(gparser.characters(ch),error_message)

    def test_graph_start(self):
        """Raise an assertion if can't set the tag value.

        Processes the opening xml tags, according to their type.
        It's a method from ContentHandler class.

        Raises
        ------
        AssertionError
            If can't set the tag value.

        """

        # Test values
        attrs = {'xmlns': 'http://www.xces.org/ns/GrAF/1.0/'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        error_message = 'Fail - Starting the graph'

        assert(gparser.graph_start(attrs),error_message)

    def test_graph_end(self):
        """Raise an assertion if can't set the tag value.

        Executes when the parser encounters the end graph tag.
        Sets the root node and adds all the edges to the graph.
        Neither of these tasks can be safely performed until all nodes
        have been added.

        Raises
        ------
        AssertionError
            If can't set the tag value.

        """

        # Test values
        # Initialize a new GraphParser
        parser = PyGraphParser()

        attrs = {'xmlns': 'http://www.xces.org/ns/GrAF/1.0/'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        # Initialize the annotations arrays
        parser.graph_start(attrs)

        error_message = 'Fail - Ending the graph'

        assert(parser.graph_end(), error_message)

    def test_fs_start(self):
        """Raise an assertion if can't set inside feature start.

        Used to parse <fs> elements in the XML representation.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        # Test values
        attrs = {'xml:id': 'penn-n0'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        error_message = 'Fail - Parsing the start of fs'

        assert(gparser.fs_start(attrs),error_message)

    def test_fs_end(self):
        """Raise an assertion if can't set inside feature end.

        Used to parse </fs> elements in the XML representation.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        # Test values
        attrs = {'xml:id': 'penn-n0'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        # First is need to create the inner fs
        gparser.fs_start(attrs)

        error_message = 'Fail - Parsing the end of fs'

        assert(gparser.fs_end(), error_message)

    def test_root_start(self):
        """Raise an assertion if can't find the start root.

        Used to parse start root elements in the XML representation.
        The root characters are processed by the characters() method
        and stored in self._buffer.

        self._root_element is a flag indicating the presence of a root.

        Raises
        ------
        AssertionError
            If can't set the value.

        """

        # Test values
        attrs = {'xml:id': 'penn-n0'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        error_message = 'Fail - Starting the root'

        assert(gparser.root_start(attrs),error_message)

    def test_root_end(self):
        """Raise an assertion if can't find the end root.

        Used to parse end root elements in the XML representation.

        Raises
        ------
        AssertionError
            If can't set the value.

        """

        error_message = 'Fail - Ending the root'

        assert(gparser.root_end(),error_message)

    def test_node_start(self):
        """Raise an assertion if can't set the tag value.

        Executes when the parser encounters the end graph tag.
        Sets the root node and adds all the edges to the graph.
        Neither of these tasks can be safely performed until all nodes
        have been added.

        Raises
        ------
        AssertionError
            If can't set the tag value.

        """

        # Test values
        attrs = {'xml:id': 'penn-n0'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        error_message = 'Fail - Starting a node'

        assert(gparser.node_start(attrs),error_message)

    def test_node_end(self):
        """Raise an assertion if can't set the tag value.

        Executes when the parser encounters the end graph tag.
        Sets the root node and adds all the edges to the graph.
        Neither of these tasks can be safely performed until all nodes
        have been added.

        Raises
        ------
        AssertionError
            If can't set the tag value.

        """

        # Test values
        attrs = {'xml:id': 'penn-n0'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        # This test is mandatory the existence of at least
        # a node. So a node is created to test the method.
        gparser.node_start(attrs)

        error_message = 'Fail - Ending a node'

        assert(gparser.node_end(),error_message)

    def test_annotation_space_start(self):
        """Raise an assertion if can't set the annotation sapce
        start.

        Used to parse <annotationSpace .../> elements in the XML
        representation.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        # Test values
        attrs = {'xmlns': 'http://www.xces.org/ns/GrAF/1.0/'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        # Initialize the annotations arrays
        gparser.graph_start(attrs)

        # Attributes for to start the Annotation Space
        attrs = {'as.id': 'xces'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        error_message = 'Fail - Setting the Annotation Space'

        assert(gparser.annotation_space_start(attrs),error_message)

    def test_depends_on_start(self):
        """Raise an assertion if can't set the dependencies.

        Used to parse dependsOn elements in the XML representation.
        Finds other XML annotation files on which depend the current
        XML file. Parses the dependency files and adds the resulting graph
        to the current graph.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        # Test values
        attrs = {'type': 'penn'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        # Is need too that the header in PyGraphParser have a location
        # file (any file) to see if the type in tag have some kind of
        # dependency in a file (set in header)
        file = '/home/alopes/nltk_data/corpora/masc/'\
               'spoken/Day3PMSession'

        gparser._header = PyDocumentHeader(file)

        error_message = 'Fail - Verifying the dependencies'

        assert(gparser.depends_on_start(attrs),error_message)

    def test_region_start(self):
        """Raise an assertion if can't set region.

        Used to pare the region elements in the XML representation.
        A tolkenizer is used to separate the anchors listed in the XML tag,
        and a new PyAnchor instance is created for each one.
        A PyRegion instance is then created with the id from the
        XML tag and added to the graph.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        # Test values
        attrs = {'xml:id': 'seg-r0', 'anchors': '5 7'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        error_message = 'Fail - Starting the region'

        assert(gparser.region_start(attrs),error_message)

    def test_as_start(self):
        """Raise an assertion if can't set the start of the
        annotation set.

        Used to parse start <as/ ...> elements in the XML representation.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        # Test values
        attrs = {'type': 'penn'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        error_message = 'Fail - Parsing the start of elements'

        assert(gparser.as_start(attrs), error_message)

    def test_as_end(self):
        """Raise an assertion if can't set the end of the
        annotation set.

        Used to parse end /as> elements in the XML representation.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        error_message = 'Fail - Parsing the Annotation Set End'

        assert(gparser.as_end(),error_message)

    def test_link_start(self):
        """Raise an assertion if can't set the link.

        Used to parse link elements in the XML representation.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        # Test values
        attrs = {'targets': 'seg-r0'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        error_message = 'Fail - Link the elements in parsing'

        assert(gparser.link_start(attrs), error_message)

    def test_ann_end(self):
        """Raise an assertion if can't set annotation end.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        error_message = 'Fail - Setting the Annotation Set end'

        assert(gparser.ann_end(),error_message)

    def test_feature_start(self):
        """Raise an assertion if can't set feature start.

        Used to parse start features elements in the XML
        representation.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        # Test values
        attrs = {'name': 'msd', 'value': 'IN'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        error_message = 'Fail - Parsing the feature start'

        assert(gparser.feature_start(attrs),error_message)

    def test_feature_end(self):
        """Raise an assertion if can't set the feature end.

        Used to parse end features elements in the XML representation.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        # Test values
        attrs = {'name': 'msd', 'value': 'IN'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        # First is need to start a feature to close it
        gparser.feature_start(attrs)

        # Creating inner feature values fs
        fs_attrs = {'xml:id': 'penn-n0'}
        fs_attrs = xml.sax.xmlreader.AttributesImpl(fs_attrs)

        # Is need to create at least on fs to have values in
        # _fs_stack
        gparser.fs_start(fs_attrs)

        error_message = 'Fail - Parsing the feature end'

        assert(gparser.feature_end(),error_message)

    def test_edge_start(self):
        """Raise an assertion if can't set edge.

        Used to parse edge elements in the XML representation.
        Edge information is stored and the edges are added after
        all nodes/spans have been parsed.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        # Test values
        attrs = {'to': 'penn-n3853', 'xml:id': 'lnk4679', 'from': 'n569'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        error_message = 'Fail - Setting the edges'

        assert(gparser.edge_start(attrs), error_message)

    def test_annotation_set_start(self):
        """Raise an assertion if can't set the annotation set
        start.

        Used to parse <annotationSet .../> elements in the XML
        representation.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        # Test values
        attrs = {'xmlns': 'http://www.xces.org/ns/GrAF/1.0/'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        # Initialize the annotations arrays
        gparser.graph_start(attrs)

        # Attributes for to start the Annotation Set
        attrs = {'type': 'http://www.xces.org/schema/2003', 'name': 'xces'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        error_message = 'Fail - To Start Annotation Set'

        assert(gparser.annotation_set_start(attrs),error_message)

    def test_ann_start(self):
        """Raise an assertion if can't set annotation start.

        Raises
        ------
        AssertionError
        If can't set the value.

        """

        # Test values
        attrs = {'xmlns': 'http://www.xces.org/ns/GrAF/1.0/'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        # Initialize the annotations arrays
        gparser.graph_start(attrs)

        # Attributes for to start the Annotation Set
        attrs = {'type': 'http://www.xces.org/schema/2003', 'name': 'xces'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        gparser.annotation_set_start(attrs)

        # Attributes for to start the Annotations it's important
        # to have the label tag
        attrs = {'as': 'xces', 'ref': 'penn-n10002', 'label': 'tok'}

        # Is need to instance the value to the SAX type
        attrs = xml.sax.xmlreader.AttributesImpl(attrs)

        error_message = 'Fail - To Start Annotation'

        assert(gparser.ann_start(attrs),error_message)