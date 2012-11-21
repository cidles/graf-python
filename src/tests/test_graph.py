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

import unittest
from graf import Graph, AnnotationSpace, Node, Edge, Region

class TestGraph(unittest.TestCase):
    """
    This class contain the test methods if the class Graph.

    """
    def setUp(self):
        self.graph = Graph()

    def test_create_annotation_space(self):
        # Test values
        as_id = 'as_id'

        aspace = self.graph.annotation_spaces.create(as_id)
        self.assertIsInstance(aspace, AnnotationSpace)
        self.assertEqual(aspace.as_id, as_id)
        self.assertListEqual(list(self.graph.annotation_spaces), [aspace])

    def test_add_annotation_space(self):
        # Test values
        as_id = 'as_id'

        aspace = AnnotationSpace(as_id)
        self.graph.annotation_spaces.add(aspace)
        self.assertEqual(self.graph.annotation_spaces[as_id], aspace)

    def test_add_edge(self):
        # Test values
        fnode = Node('node_1') # From Node
        tnode = Node('node_2') # To Node

        edge = Edge('id_test', fnode, tnode)
        self.graph.nodes.add(fnode)
        self.graph.nodes.add(tnode)
        self.graph.edges.add(edge)
        self.assertListEqual(list(self.graph.edges), [edge])

    def test_create_edge(self):
        # Test values
        fnode = Node('node_1') # From Node
        tnode = Node('node_2') # To Node

        self.graph.create_edge(fnode, tnode, id='3')
        self.assertEqual(1, len(self.graph.edges))
        self.assertEqual(self.graph.edges['3'].from_node, fnode)
        self.assertEqual(self.graph.edges['3'].to_node, tnode)

    def test_add_feature(self):
        name = 'feature'
        value = 'value'
        self.graph.features[name] = value
        self.assertEqual(self.graph.features[name], value)

    def test_add_node(self):
        node = Node('test_node')
        self.graph.nodes.add(node)
        self.assertListEqual(list(self.graph.nodes), [node])

    def test_add_region(self):
        # Test values
        # The Region needs at least 2 anchors
        #anchor = Anchor(t) # Tokenizer
        anchors = ['anchor1', 'anchor2']
        id = '1'
        region = Region(id, *anchors)
        self.graph.regions.add(region)
        self.assertListEqual(list(self.graph.regions), [region])

    def test_get_edge_by_id(self):
        fnode = Node('node_1') # From Node
        tnode = Node('node_2') # To Node
        edge = Edge('id_test', fnode, tnode)
        self.graph.nodes.add(fnode)
        self.graph.nodes.add(tnode)
        self.graph.edges.add(edge)
        self.assertEqual(self.graph.edges['id_test'], edge)

    def test_get_edge_by_nodes(self):
        fnode = Node('node_1') # From Node
        tnode = Node('node_2') # To Node
        edge = Edge('id_test', fnode, tnode)
        self.graph.nodes.add(fnode)
        self.graph.nodes.add(tnode)
        self.graph.edges.add(edge)
        self.assertEqual(self.graph.find_edge(fnode, tnode), edge)
        self.assertEqual(self.graph.find_edge(fnode.id, tnode.id), edge)

    def test_get_node(self):
        node = Node('test_node')
        self.graph.nodes.add(node)
        self.assertEqual(self.graph.nodes['test_node'], node)

    def test_get_region(self):
        node = Node('test_node')
        self.graph.nodes.add(node)
        self.assertEqual(self.graph.nodes['test_node'], node)

    def test_get_annotation_space(self):
        aspace = AnnotationSpace('as_id')
        self.graph.annotation_spaces.add(aspace)
        self.assertEqual(self.graph.annotation_spaces['as_id'], aspace)

    def test_get_region_from_id(self):
        region = Region('1', 'anchor1', 'anchor2')
        self.graph.regions.add(region)
        self.assertEqual(self.graph.regions['1'], region)

    def test_get_region_from_anchors(self):
        region = Region('1', 'anchor1', 'anchor2')
        self.graph.regions.add(region)
        self.assertEqual(self.graph.get_region('anchor1', 'anchor2'), region)

    def test_set_root_not_in_graph(self):
        node = Node('test_node')
        self.assertRaises(ValueError, lambda: setattr(self.graph, 'root', node))

    def test_get_root(self):
        node = Node('test_node')
        self.graph.nodes.add(node)
        self.graph.root = node
        self.assertEqual(self.graph.root, node)

    def test_iter_roots(self):
        node = Node('test_node')
        self.graph.nodes.add(node)
        self.graph.root = node
        self.assertListEqual(list(self.graph.iter_roots()), [node])

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

        self.assertListEqual(list(n1.iter_children()), [n2, n3])
        self.assertListEqual(list(n2.iter_children()), [n1])
        self.assertListEqual(list(n3.iter_children()), [n4])
        self.assertListEqual(list(n4.iter_children()), [])
        self.assertListEqual(list(n1.iter_parents()), [n2])
        self.assertListEqual(list(n2.iter_parents()), [n1])
        self.assertListEqual(list(n3.iter_parents()), [n1])
        self.assertListEqual(list(n4.iter_parents()), [n3])