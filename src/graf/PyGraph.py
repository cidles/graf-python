# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

"""
Graph structure backing the ISO GrAF format.
The graph is undirected, composed of C{PyNode}s and C{PyEdge}s, each
backed by a C{list} to maintain the order of the nodes/edges and to
allow for quick traversals, and a hash map so nodes/edges can be found
quickly based on their ID
"""

from PyAnchor import *
from PyAnnotationSet import *
from PyEdge import *
from PyFeature import *
from PyFeatureStructure import *
from PyNode import *
from PyRegion import *
from PyStandoffHeader import *    


class PyGraph:
    def __init__(self):
        """
        Constructor for PyGraph
        """
        self._edgeCount = 0
        self._features = PyFeatureStructure()
        self._nodeSet = {}
        self._edgeSet = {}
        self._regions = {}
        self._annotationSets = {}
        self._content = None
        self._header = PyStandoffHeader()
        self._userObject = None

    def addAnnotationSet(self, set):
        """
        Add given C{PyAnnotationSet} to this C{PyGraph}
        @param set: C{PyAnnotationSet}
        """
        self._annotationSets[set._name] = set
        self._header.addAnnotationSetCreate(set._name, set._type)

    def addASCreate(self, name, type):
        """
        Create C{PyAnnotationSet} from given name, value and 
        add it to this C{PyGraph}
        @param name: C{str}
        @param type: C{str}
        """
        aSet = PyAnnotationSet(name, type)
        self.addAnnotationSet(aSet)
        return aSet

    def addEdge(self, edge):
        """
        Add C{PyEdge} to this C{PyGraph}
        @param edge: C{PyEdge}
        """
        self._edgeSet[edge._id] = edge
        self.updateNode(edge)

    def addEdgeCreate(self, id, fromNode = None , toNode = None):
        """
        Create C{PyEdge} from id, fromNode, toNode and add it to
        this C{PyGraph}
        @param id: C{str}
        @param fromNode: C{PyNode}
        @param toNode: C{PyNode}
        """ 
        if self._nodeSet.get(fromNode.getID()) is None:
            self._nodeSet[fromNode.getID()] = fromNode
        if self._nodeSet.get(toNode.getID()) is None:
            self._nodeSet[toNode.getID()] = toNode
        self._edgeCount += 1
        newEdge = PyEdge(id, fromNode, toNode)
        self._edgeSet[newEdge.getID()] = newEdge
        self.updateNode(newEdge)
        return newEdge
        
    def addEdgeFromTo(self, fromNode, toNode):
        """
        Create C{PyEdge} from fromNode, toNode and add it to 
        this C{PyGraph}
        id is created
        @param fromNode: C{PyNode}
        @param toNode: C{PyNode}
        """
        return self.addEdgeCreate("e" + str(self._edgeCount), 
                                fromNode, toNode)

    def addEdgeToFromID(self, id, fromID, toID):
        """
        Create C{PyEdge} from id, fromID, toID and add it to 
        this C{PyGraph}
        @param id: C{str}
        @param fromID: C{str}
        @param toID: C{str}
        """
        fromNode = self._nodeSet.get(fromID)
        toNode = self._nodeSet.get(toID)
        if fromNode is None or toNode is None:
            return None
        return self.addEdge(id, fromNode, toNode)

    def addFeature(self, name, value):
        self._features.add(name, value)

    def addNode(self, node):
        """
        Add C{PyNode} to this C{PyGraph}
        @param node: C{PyNode} or C{str}
        """
        if isinstance(node, basestring):
            newNode = self._nodeSet.get(node)
            if newNode is None:
                newNode = PyNode(node)
                self._nodeSet[node] = newNode
            return newNode
        else:
            self._nodeSet[node._id] = node

    def addRegion(self, region):
        self._regions[region._id] = region

    def annotationSets(self):
        return self._annotationSets.itervalues()

    def edges(self):
        return self._edgeSet.values()

    def findEdgeFromID(self, id):
        return self._edgeSet.get(id)

    def findEdge(self, fromNode, toNode):
        """
        Search for C{PyEdge} with its fromNode, toNode, either nodes or ids
        @param fromNode: C{PyNode} or C{str}
        @param toNode: C{PyNode} or C{str}
        @return: C{PyEdge}
        """
        if (isinstance(fromNode, basestring) and 
                    isinstance(toNode, basestring)):
            f = self._nodeSet.get(fromNode)
            t = self._nodeSet.get(toNode)
            if f is None or t is None:
                return None
            return findEdge(f, t)
        else:
            for e in self.edges():
                if (e.getFrom().getID() == fromNode.getID() and 
                    e.getTo().getID() == toNode.getID()):
                    return e
            return None

    def findNode(self, id):
        return self._nodeSet.get(id)

    def getAnnotationSet(self, name):
        return self._annotationSets.get(name)

    def getAnnotationSets(self):
        return self._annotationSets.values()

    def getContent(self):
        return self._content

    def getEdgeSetSize(self):
        return len(self._edgeSet)

    def getFeature(self, name):
        return self._features.get(name)

    def getFeatures(self):
        return self._features

    def getHeader(self):
        return self._header

    def getNodeSetSize(self):
        return len(self._nodeSet)

    def getRegion(self, start, end):
        for region in self.regions():
            if (start.compareTo(region.getStart()) == 0 and 
                end.compareTo(region.getEnd()) == 0):
                return region
        return None

    def getRegionFromID(self, id):
        return self._regions.get(id)

    def getRegions(self):
        return self._regions.values()

    def getRoot(self):
        h = self.getHeader()
        roots = h.getRoots()
        if len(roots) == 0:
            return None
        id = roots[0]
        return self._nodeSet.get(id)        

    def getRoots(self):
        roots = []
        h = self.getHeader()
        for id in h.getRoots():
            roots.append(self._nodeSet.get(id))
        return roots

    def getUserObject(self):
        return self._userObject

    def insertEdge(self, e):
        self._edgeSet[e.getID()] = e

    def nodes(self):
        return self._nodeSet.values()

    def regions(self):
        return self._regions.values()

    def removeRegion(self, region):
        if isinstance(region, basestring):
            return self._regions.pop(region, None)
        else: 
            return self._regions.pop(region.getID(), None)

    def roots(self):
        return self.getRoots()

    def setContent(self, content):
        self._content = content

    def setHeader(self, header):
        self._header = header

    def setRoot(self, node):
        self._header.clearRoots()
        self._header.addRoot(node._id) 

    def setUserObject(self, object):
        self._userObject = object

    def updateNode(self, edge):
        edge._fromNode.addOutEdge(edge)
        edge._toNode.addInEdge(edge)

