# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2012 Poio Project
# Author: António Lopes <alopes@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT
"""
This module contains tests for graf.graphs
"""

from graf import Graph, AnnotationSpace, Node, Edge, Region

class TestGraph:
    """
    This class contain the test methods if the class Graph.

    """
    def setUp(self):
        self.graph = Graph()

    def test_create_annotation_space(self):
        # Test values
        as_id = 'as_id'

        aspace = self.graph.annotation_spaces.create(as_id)

        assert(aspace.as_id == as_id)
        assert(list(self.graph.annotation_spaces) == [aspace])

    def test_add_annotation_space(self):
        # Test values
        as_id = 'as_id'

        aspace = AnnotationSpace(as_id)
        self.graph.annotation_spaces.add(aspace)
        assert(self.graph.annotation_spaces[as_id] == aspace)

    def test_add_edge(self):
        # Test values
        fnode = Node('node_1') # From Node
        tnode = Node('node_2') # To Node

        edge = Edge('id_test', fnode, tnode)
        self.graph.nodes.add(fnode)
        self.graph.nodes.add(tnode)
        self.graph.edges.add(edge)
        assert(list(self.graph.edges)[0] == edge)

    def test_create_edge(self):
        # Test values
        fnode = Node('node_1') # From Node
        tnode = Node('node_2') # To Node

        self.graph.create_edge(fnode, tnode, id='3')
        assert(1 == len(self.graph.edges))
        assert(self.graph.edges['3'].from_node == fnode)
        assert(self.graph.edges['3'].to_node == tnode)

    def test_add_feature(self):
        name = 'feature'
        value = 'value'
        self.graph.features[name] = value
        assert(self.graph.features[name] == value)

    def test_add_node(self):
        node = Node('test_node')
        self.graph.nodes.add(node)
        assert(list(self.graph.nodes) == [node])

    def test_add_region(self):
        # Test values
        # The Region needs at least 2 anchors
        #anchor = Anchor(t) # Tokenizer
        anchors = ['anchor1', 'anchor2']
        id = '1'
        region = Region(id, *anchors)
        self.graph.regions.add(region)
        assert(list(self.graph.regions) == [region])

    def test_get_edge_by_id(self):
        fnode = Node('node_1') # From Node
        tnode = Node('node_2') # To Node
        edge = Edge('id_test', fnode, tnode)
        self.graph.nodes.add(fnode)
        self.graph.nodes.add(tnode)
        self.graph.edges.add(edge)
        assert(self.graph.edges['id_test'] == edge)

    def test_get_edge_by_nodes(self):
        fnode = Node('node_1') # From Node
        tnode = Node('node_2') # To Node
        edge = Edge('id_test', fnode, tnode)
        self.graph.nodes.add(fnode)
        self.graph.nodes.add(tnode)
        self.graph.edges.add(edge)
        assert(self.graph.find_edge(fnode, tnode) ==edge)
        assert(self.graph.find_edge(fnode.id, tnode.id) ==edge)

    def test_get_node(self):
        node = Node('test_node')
        self.graph.nodes.add(node)
        assert(self.graph.nodes['test_node'] ==node)

    def test_get_region(self):
        node = Node('test_node')
        self.graph.nodes.add(node)
        assert(self.graph.nodes['test_node'] ==node)

    def test_get_annotation_space(self):
        aspace = AnnotationSpace('as_id')
        self.graph.annotation_spaces.add(aspace)
        assert(self.graph.annotation_spaces['as_id'] ==aspace)

    def test_get_region_from_id(self):
        region = Region('1', 'anchor1', 'anchor2')
        self.graph.regions.add(region)
        assert(self.graph.regions['1'] ==region)

    def test_get_region_from_anchors(self):
        region = Region('1', 'anchor1', 'anchor2')
        self.graph.regions.add(region)
        assert(self.graph.get_region('anchor1', 'anchor2') == region)

    def test_get_root(self):
        node = Node('test_node')
        self.graph.nodes.add(node)
        self.graph.root = node
        assert(self.graph.root == node)

    def test_iter_roots(self):
        node = Node('test_node')
        self.graph.nodes.add(node)
        self.graph.root = node
        assert(list(self.graph.iter_roots()) == [node])

    def test_parents_and_children(self):
        n1 = Node('n1')
        n2 = Node('n2')
        n3 = Node('n3')
        n4 = Node('n4')
        self.graph.nodes.add(n1)
        self.graph.nodes.add(n2)
        self.graph.nodes.add(n3)
        self.graph.nodes.add(n4)
        self.graph.create_edge(n1, n2)
        self.graph.create_edge(n2, n1)
        self.graph.create_edge(n1, n3)
        self.graph.create_edge(n3, n4)

        assert(list(n1.iter_children()) == [n2, n3])
        assert(list(n2.iter_children()) == [n1])
        assert(list(n3.iter_children()) == [n4])
        assert(list(n4.iter_children()) == [])
        assert(list(n1.iter_parents()) == [n2])
        assert(list(n2.iter_parents()) == [n1])
        assert(list(n3.iter_parents()) == [n1])
        assert(list(n4.iter_parents()) == [n3])