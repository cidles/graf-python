# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2012 Poio Project
# Author: António Lopes <alopes@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT

import sys
from graf import Node, Graph, Edge, FeatureStructure, Annotation, GrafRenderer

# Create three nodes
node_one = Node('node_one')
node_two = Node('node_two')
node_three = Node('node_three')

# Create the Annotation Graph and set the values
graph = Graph()

#Adding the nodes
graph.add_node(node_one)
graph.add_node(node_two)
graph.add_node(node_three)

# Create the edge
edge = Edge(node_one, node_three)

# Add an the edge
#graph.add_edge(edge)

# Add Features
feature_strct = FeatureStructure() # Structure

# Adding two features
# There are two ways to it.
# Use the simple first
# Setting up all the features to the annotation
feature_strct['feature1'] = 'value_1'
feature_strct['feature2'] = 'value_2'

# Adding the features to annotations
annotation = Annotation('label', feature_strct)
annotation.features['another_feature'] = 'value_another'
annotation.features['feature3'] = 'value_3'

# Adding the annotations to the node
node_one.add_annotation(annotation)

# Rendering the Graph
graf_render = GrafRenderer(sys.stdout)
graf_render.render(graph)
