# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
#         Antonio Lopes <alopes@cidles.eu> (Edited and Updated to
#         Python 3 and added new functionalites)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

from graf.PyLink import *
from graf.PyGraphElement import PyGraphElement

class PyNode(PyGraphElement):
    """
    Class for nodes within a C{PyGraph} instance.
    Each node keeps a list of in-edges and out-edges.
    Each collection is backed by two data structures:
        1. A list (for traversals)
        2. A hash map
    Nodes may also contain one or more C{PyAnnotation} objects.

    """

    def __init__(self, id = ""):
        PyGraphElement.__init__(self, id)
        self._inEdgeList = []
        self._outEdgeList = []
        self._inEdges = {}
        self._outEdges = {}
        self._links = []
        self._annotationRoot = False

    def from_node(node):
        newNode = PyNode(node._id)
        newNode._annotationRoot = node._annotationRoot
        return newNode

    def __repr__(self):
	# Added
        #for inEdge in self._inEdgeList:
        #    print(inEdge)

        #for outEdge in self._inEdgeList:
        #    print(outEdge)

        #for inEdge in self._inEdges:
        #    print(inEdge)

        #for outEdge in self._outEdges:
        #    print(outEdge)

        #for link in self._links:
        #    print(link)

        return "NodeID = " + self._id

    def add_in_edge(self, e):
        self._inEdges[e._id] = e
        self._inEdgeList.append(e)

    def add_link(self, link):
        self._links.append(link)
        for region in link._regions:
            region.add_node(self)
	    # Added
            # Print the region with anchors and nodes
            # Example
            print(region)

    def add_out_edge(self, e):
        self._outEdges[e._id] = e    
        self._outEdgeList.append(e)
    
    def add_region(self, region):
        link = None
        if len(self._links) > 0:
            link = self._links[len(self._links)-1]
        else:
            link = PyLink()
            self._links.append(link)
        link.add_target(region)
        region.add_node(self)
        
    def clear(self):
        self._visited = False
        for e in self._outEdges.values():
            toNode = e.getTo()
            if toNode is not None and toNode.visited():
                toNode.clear()

    def compare_to(self, node):
        if self._id > node._id:
            return 1
        elif self._id < node._id:
            return -1
        else:
            return 0

    def degree(self):
        return len(self._inEdgeList) + len(self._outEdgeList)

    def get_in_edge(self, index):
        if isinstance(index, str):
            return self._inEdges.get(index)
        else:
            if len(self._inEdgeList) <= index:
                return None
            else:
                return self._inEdgeList[index]

    def get_out_edge(self, index):
        if isinstance(index, str):
            return self._outEdges.get(index)
        else:
            if len(self._outEdgeList) <= index:
                return None
            else:
                return self._outEdgeList[index]

    def get_parent(self):
        if len(self._inEdgeList) == 0:
            return None
        else:
            return self._inEdgeList[0].getFrom()

    def in_degree(self):
        return len(self._inEdgeList)

    def out_degree(self):
        return len(self._outEdgeList)
