# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

from PyEdge import *
from PyLink import *
from PyGraphElement import PyGraphElement


class PyNode(PyGraphElement):
    """
    Class for nodes within a C{PyGraph} instance.
    Each node keeps a list of in-edges and out-edges.
    Each collection is backed by two data structures:
        1. A list (for traversals)
        2. A hash map
    Nodes may also contain one or more C{PyAnnotation} objects
    """

    def __init__(self, id = ""):
        PyGraphElement.__init__(self, id)
        self._inEdgeList = []
        self._outEdgeList = []
        self._inEdges = {}
        self._outEdges = {}
        self._links = []
        self._annotationRoot = False

    def fromNode(node):
        newNode = PyNode(node._id)
        newNode._annotationRoot = node._annotationRoot
        return newNode

    def __repr__(self):
        return "NodeID = " + self._id

    def addInEdge(self, e):
        self._inEdges[e._id] = e
        self._inEdgeList.append(e)

    def addLink(self, link):
        self._links.append(link)
        for region in link._regions:
            region.addNode(self)

    def addOutEdge(self, e):
        self._outEdges[e._id] = e    
        self._outEdgeList.append(e)
    
    def addRegion(self, region):
        link = None
        if len(self._links) > 0:
            link = self._links[len(self._links)-1]
        else:
            link = PyLink()
            self._links.append(link)
        link.addTarget(region)
        region.addNode(self)
        
    def clear(self):
        self._visited = False
        for e in self._outEdges.values():
            toNode = e.getTo()
            if toNode is not None and toNode.visited():
                toNode.clear()

    def compareTo(self, node):
        if self._id > node._id:
            return 1
        elif self._id < node._id:
            return -1
        else:
            return 0

    def degree(self):
        return len(self._inEdgeList) + len(self._outEdgeList)

    def getInEdge(self, index):
        if isinstance(index, basestring):
            return self._inEdges.get(index)
        else:
            if len(self._inEdgeList) <= index:
                return None
            else:
                return self._inEdgeList[index]

    def getOutEdge(self, index):
        if isinstance(index, basestring):
            return self._outEdges.get(index)
        else:
            if len(self._outEdgeList) <= index:
                return None
            else:
                return self._outEdgeList[index]

    def getParent(self):
        if len(self._inEdgeList) == 0:
            return None
        else:
            return self._inEdgeList[0].getFrom()

    def inDegree(self):
        return len(self._inEdgeList)

    def outDegree(self):
        return len(self._outEdgeList)
