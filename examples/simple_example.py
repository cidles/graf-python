# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2012 Poio Project
# Author: António Lopes <alopes@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT

from graf.PyNode import PyNode
from graf.PyGraph import PyGraph
from graf.PyEdge import PyEdge
from graf.PyFeature import PyFeature
from graf.PyFeatureStructure import PyFeatureStructure
from graf.PyAnnotation import PyAnnotation
from graf.PyGrafRenderer import PyGrafRenderer

# Create three nodes
node_one = PyNode('node_one')
node_two = PyNode('node_two')
node_three = PyNode('node_three')

# Create the Annotation Graph and set the values
graph = PyGraph()

#Adding the nodes
graph.add_node(node_one)
graph.add_node(node_two)
graph.add_node(node_three)

# Create the edge
edge = PyEdge(node_one, node_three)

# Add an the edge
#graph.add_edge(edge)

# Add Features
feature = PyFeature('another_feature') # Type to write in the strucutre
feature_strct = PyFeatureStructure() # Structure

# Adding two features
# There are two ways to it.
# Use the simple first
# Setting up all the features to the annotation
feature_strct.add('feature1', 'value_1')
feature_strct.add('feature2', 'value_2')

# Setting one value to the defined PyFeature
feature.set_value('value_another')

# Adding the features to annotations
annotation = PyAnnotation('label',feature_strct)
annotation.add_feature(feature)
annotation.add('feature3', 'value_3')

# Adding the annotations to the node
node_one.add_annotation(annotation)

# Rendering the Graph
graf_render = PyGrafRenderer('test.xml') # Change directory
graf_render.render(graph)
