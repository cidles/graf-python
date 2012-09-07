# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2012 Poio Project
# Author: António Lopes <alopes@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT
"""This module contains the tests to the class
PyGraph in module PyGraph.

This test serves to ensure the viability of the
methods of the class PyGraph in PyGraph.py.
"""

from graf.PyGraph import PyGraph
from graf.PyAnnotationSet import PyAnnotationSet
from graf.PyAnnotationSpace import PyAnnotationSpace
from graf.PyNode import PyNode
from graf.PyEdge import PyEdge
from graf.PyRegion import PyRegion
from graf.PyStandoffHeader import PyStandoffHeader

# Create the Annotation Graph
graph = PyGraph()

class TestPyGraph:
    """
    This class contain the test methods if the class PyGraph.

    """

    def test_add_as_create(self):
        """Raise an assertion if can't create the PyAnnotationSet.

        Return a PyAnnotationSet.

        Raises
        ------
        AssertionError
            If the results there aren't the expected.

        """

        # Test values
        name = 'name'
        type = 'type'

        expected_result = PyAnnotationSet(name, type)

        error_message = 'Fail - Creating Annotation Set'

        assert(graph.add_as_create(name, type),error_message)

    def test_add_annotation_set(self):
        """Raise an assertion if can't add a PyAnnotationSet
        space.

        Raises
        ------
        AssertionError
            If can't set the annotation.

        """

        # Test values
        name = 'name'
        type = 'type'

        # Create the Annotation Set
        aset = PyAnnotationSet(name, type)

        error_message = 'Fail - Adding Set Annotation'

        assert(graph.add_annotation_set(aset),error_message)

    def test_add_aspace_create(self):
        """Raise an assertion if can't create the PyAnnotationSpace.

        Return a PyAnnotationSpace.

        Raises
        ------
        AssertionError
            If the results there aren't the expected.

        """

        # Test values
        name = 'name'

        expected_result = PyAnnotationSpace(name)

        error_message = 'Fail - Creating Annotation Space'

        assert(graph.add_aspace_create(name),error_message)

    def test_add_annotation_space(self):
        """Raise an assertion if can't add a PyAnnotationSpace
        space.

        Raises
        ------
        AssertionError
            If can't set the annotation.

        """

        # Test values
        as_id = 'name'

        # Create the Annotation Space
        aspace = PyAnnotationSpace(as_id)

        error_message = 'Fail - Adding Space Annotation'

        assert(graph.add_annotation_space(aspace),error_message)

    def test_add_edge(self):
        """Raise an assertion if can't add a PyAnnotationSpace
        space.

        Raises
        ------
        AssertionError
            If can't set the edge.

        """

        # Test values
        fnode = PyNode('node_1') # From Node
        tnode = PyNode('node_2') # To Node

        edge = PyEdge('id_test', fnode, tnode)

        error_message = 'Fail - Setting the edge'

        assert(graph.add_edge(edge),error_message)

    def test_add_edgeToFromID(self):
        """Raise an assertion if can't add a certain edge.

        Raises
        ------
        AssertionError
            If can't add a certain edge.

        """

        # Test values
        fnode = PyNode('node_1') # From Node
        tnode = PyNode('node_2') # To Node

        error_message = 'Fail - Adding edge from - to'

        assert(graph.add_edgeToFromID('3', fnode, tnode),error_message)


    def test_add_feature(self):
        """Raise an assertion if can't add a feature.

        Raises
        ------
        AssertionError
            If can't add a feature.

        """

        name = 'feature'
        value = 'value'

        error_message = 'Fail - Adding a feature'

        assert(graph.add_feature(name, value),error_message)

    def test_add_node(self):
        """Raise an assertion if can't add a node.

        Raises
        ------
        AssertionError
            If can't add a node.

        """

        node = PyNode('test_node')

        error_message = 'Fail - Adding a node'

        assert(graph.add_node(node),error_message)

    def test_add_region(self):
        """Raise an assertion if can't add a region.

        Raises
        ------
        AssertionError
            If can't add a region.

        """

        # Test values
        # The PyRegion needs at least 2 anchors
        #anchor = PyAnchor(t) # Tokenizer
        anchors = []
        anchor = 'anchor1'
        anchors.append(anchor)
        anchor = 'anchor2'
        anchors.append(anchor)
        id = '1'

        region = PyRegion(id, anchors)

        error_message = 'Fail - Adding a region'

        #assert(graph.add_region(region),error_message) Fix to the correct version
        assert(graph.addRegion(region),error_message)

    def test_annotation_sets(self):
        """Raise an assertion if can't return a list of
        AnnotationSet.

        Raises
        ------
        AssertionError
            If can't return a list of AnnotationSet.

        """

        error_message = 'Fail - Return annotation set list'

        assert(graph.annotation_sets(),error_message)

    def test_annotation_spaces(self):
        """Raise an assertion if can't return a list of
        AnnotationSpace.

        Raises
        ------
        AssertionError
            If can't return a list of AnnotationSpace.

        """

        error_message = 'Fail - Return annotation space list'

        assert(graph.annotation_spaces(),error_message)

    def test_edges(self):
        """Raise an assertion if can't return a list of
        Edges.

        Raises
        ------
        AssertionError
            If can't return a list of Edges.

        """

        error_message = 'Fail - Return edges list'

        assert(graph.edges(),error_message)

    def test_find_edge_from_id(self):
        """Raise an assertion if can't return a specific edge.

        Raises
        ------
        AssertionError
            If can't return a specific edge.

        """

        error_message = 'Fail - Cant find a specific edge'

        assert(graph.find_edge_from_id(id),error_message)

    def test_find_node(self):
        """Raise an assertion if can't return a specific node.

        Raises
        ------
        AssertionError
            If can't return a specific node.

        """

        error_message = 'Fail - Cant find a specific node'

        assert(graph.find_node(id),error_message)

    def test_get_annotation_set(self):
        """Raise an assertion if can't return a specific
        annotation set.

        Raises
        ------
        AssertionError
            If can't return a specific annotation set.

        """

        # Test values
        name = 'ann'

        error_message = 'Fail - Cant find a specific annotation set'

        assert(graph.get_annotation_set(name),error_message)

    def test_get_annotation_sets(self):
        """Raise an assertion if can't return a specific
        list of annotation set.

        Raises
        ------
        AssertionError
            If can't return a specific list of annotation set.

        """

        error_message = 'Fail - Cant find a specific annotation ' \
                        'set list'

        assert(graph.get_annotation_sets(),error_message)

    def test_get_annotation_space(self):
        """Raise an assertion if can't return a specific
        annotation space.

        Raises
        ------
        AssertionError
            If can't return a specific annotation space.

        """

        # Test values
        name = 'name'

        error_message = 'Fail - Cant find a specific annotation space'

        assert(graph.get_annotation_space(name),error_message)

    def test_get_annotation_spaces(self):
        """Raise an assertion if can't return a specific
        list of annotation space.

        Raises
        ------
        AssertionError
            If can't return a specific list of annotation space.

        """

        error_message = 'Fail - Cant find a specific annotation '\
                        'space list'

        assert(graph.get_annotation_spaces(),error_message)

    def test_get_content(self):
        """Raise an assertion if can't return a content.

        Raises
        ------
        AssertionError
            If can't return a content.

        """

        error_message = 'Fail - Cant return content'

        assert(graph.get_content(),error_message)

    def test_get_edge_set_size(self):
        """Raise an assertion if can't return a edge.

        Raises
        ------
        AssertionError
            If can't return a edge.

        """

        error_message = 'Fail - Cant return content'

        assert(graph.get_edge_set_size(),error_message)

    def test_get_feature(self):
        """Raise an assertion if can't return a feature.

        Raises
        ------
        AssertionError
            If can't return a feature.

        """


        error_message = 'Fail - Cant return feature'

        assert(graph.get_feature('feature1'),error_message)

    def test_get_features(self):
        """Raise an assertion if can't return a features.

        Raises
        ------
        AssertionError
            If can't return a features.

        """

        error_message = 'Fail - Cant return features'

        assert(graph.get_features(),error_message)

    def test_get_header(self):
        """Raise an assertion if can't return a _header.

        Raises
        ------
        AssertionError
            If can't return a _header.

        """

        error_message = 'Fail - Cant return _header'

        assert(graph.get_header(),error_message)

    def test_get_node_set_size(self):
        """Raise an assertion if can't return a node.

        Raises
        ------
        AssertionError
            If can't return a node.

        """

        error_message = 'Fail - Cant return node'

        assert(graph.get_node_set_size(),error_message)

    def test_get_region_from_id(self):
        """Raise an assertion if can't return a specific
        region.

        Raises
        ------
        AssertionError
            If can't return a region.

        """

        error_message = 'Fail - Cant return a specific region'

        assert(graph.get_region_from_id(id),error_message)

    def test_get_regions(self):
        """Raise an assertion if can't return a list of
        regions.

        Raises
        ------
        AssertionError
            If can't return a list of regions.

        """

        error_message = 'Fail - Cant return a list of regions'

        assert(graph.get_regions(),error_message)

    def test_get_root(self):
        """Raise an assertion if can't return root.

        Raises
        ------
        AssertionError
            If can't return root.

        """

        error_message = 'Fail - Cant return root'

        assert(graph.get_root(),error_message)

    def test_get_roots(self):
        """Raise an assertion if can't return a list of root.

        Raises
        ------
        AssertionError
            If can't return a list of root.

        """

        error_message = 'Fail - Cant return a list of root'

        assert(graph.get_roots(),error_message)

    def test_get_user_object(self):
        """Raise an assertion if can't return a user object.

        Raises
        ------
        AssertionError
            If can't return a user object.

        """

        error_message = 'Fail - Cant return a user object'

        assert(graph.get_user_object(),error_message)

    def test_nodes(self):
        """Raise an assertion if can't return node set
        values.

        Raises
        ------
        AssertionError
            If can't return values from a node set.

        """

        error_message = 'Fail - Cant return node set values'

        assert(graph.nodes(),error_message)

    def test_regions(self):
        """Raise an assertion if can't return node set
        values.

        Raises
        ------
        AssertionError
            If can't return values from a region set.

        """

        error_message = 'Fail - Cant return region set values'

        assert(graph.regions(),error_message)

    def test_roots(self):
        """Raise an assertion if can't return roots.

        Raises
        ------
        AssertionError
            If can't return roots.

        """

        error_message = 'Fail - Cant return roots'

        assert(graph.roots(),error_message)

    def test_set_content(self):
        """Raise an assertion if can't set a content.

        Raises
        ------
        AssertionError
            If can't set content.

        """

        content = 'Content'

        error_message = 'Fail - Cant set content'

        assert(graph.set_content(content),error_message)

    def test_set_header(self):
        """Raise an assertion if can't set a header.

        Raises
        ------
        AssertionError
            If can't set header.

        """

        header = PyStandoffHeader()

        error_message = 'Fail - Cant set header'

        assert(graph.set_header(header),error_message)

    def test_set_root(self):
        """Raise an assertion if can't set a root.

        Raises
        ------
        AssertionError
            If can't set root.

        """

        node = PyNode('root_node')

        error_message = 'Fail - Cant set root'

        assert(graph.set_root(node),error_message)

    def test_set_user_object(self):
        """Raise an assertion if can't set a user object.

        Raises
        ------
        AssertionError
            If can't set user object.

        """

        error_message = 'Fail - Cant set user object'

        assert(graph.set_user_object(object),error_message)

class ExtraMethGraph:
    #def test_remove_region(self):
    def remove_region(self):
        """Raise an assertion if can't remove region.

        Raises
        ------
        AssertionError
            If can't remove a region.

        """

        # The PyRegion needs at least 2 anchors
        #anchor = PyAnchor(t) # Tokenizer
        anchors = []
        anchor = 'anchor1'
        anchors.append(anchor)
        anchor = 'anchor2'
        anchors.append(anchor)
        id = '1'

        region = graph.get_region(None,None)

        error_message = 'Fail - Cant remove region'

        assert(graph.remove_region(region),error_message)

    #def test_find_edge(self):
    def find_edge(self):
        """Raise an assertion if can't return a specific edge.

        Raises
        ------
        AssertionError
            If can't return a specific edge.

        """

        # Test values
        tnode = PyNode('node_1') # To Node
        id = '3'

        error_message = 'Fail - Cant find a specific edge '\
                        'between to points'

        assert(graph.find_edge(id,tnode),error_message)

    #def test_insert_edge(self):
    def insert_edge(self):
        """Raise an assertion if can't insert a edge.

        Raises
        ------
        AssertionError
            If can't insert a edge.

        """

        edge = PyEdge('id_test')

        error_message = 'Fail - Cant insert edge'

        assert(graph.insert_edge(edge),error_message)

    #def test_get_region(self):
    def get_region(self):
        """Raise an assertion if can't return a region.

        Raises
        ------
        AssertionError
            If can't return a region.

        """

        error_message = 'Fail - Cant return region'

        assert(graph.get_region(1, 2),error_message)

    #def test_update_node(self):
    def update_node(self):
        """Raise an assertion if can't update node.

        Raises
        ------
        AssertionError
            If can't update node.

        """

        edge = PyEdge('edge_node')

        error_message = 'Fail - Cant update node'

        assert(graph.update_node(edge),error_message)

    #def test_add_edge_create(self):
    def add_edge_create(self):
        """Raise an assertion if can't return a new edge.

        Raises
        ------
        AssertionError
            If can't retrieve the new edge.

        """

        # Test values
        fnode = PyNode('node_1') # From Node
        tnode = PyNode('node_2') # To Node

        value = '1'

        error_message = 'Fail - Returning the edge'

        assert(graph.add_edge_create(value, fnode, tnode),error_message)

    #def test_add_edge_from_to(self):
    def add_edge_from_to(self):
        """Raise an assertion if can't return a new edge.

        Raises
        ------
        AssertionError
            If can't retrieve the new edge.

        """

        # Test values
        fnode = PyNode('node_1') # From Node
        tnode = PyNode('node_2') # To Node

        # It's necessary for the nodes get an ID
        graph.add_node(fnode)
        graph.add_node(tnode)

        error_message = 'Fail - Returning the edge from place'

        assert(graph.add_edge_from_to(fnode, tnode),error_message)