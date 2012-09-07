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

"""
Graph structure backing the ISO GrAF format.
The graph is undirected, composed of C{PyNode}s and C{PyEdge}s, each
backed by a C{list} to maintain the order of the nodes/edges and to
allow for quick traversals, and a hash map so nodes/edges can be found
quickly based on their ID
"""

from PyAnnotationSet import *
from PyEdge import *
from PyNode import *
from PyStandoffHeader import *

class PyGraph:
    """
    Class of PyGraph.

    """

    def __init__(self):
        """Constructor for PyGraph.

        """

        self._edgeCount = 0
        self._features = PyFeatureStructure()
        self._nodeSet = {}
        self._edgeSet = {}
        self._regions = {}
        self._annotationSets = {}
        self._annotationSpaces = {} # Added AL
        self._content = None
        self._header = PyStandoffHeader()
        self._userObject = None

    def add_annotation_set(self, set):
        """Add given C{PyAnnotationSet} to this C{PyGraph}.

        :param set: C{PyAnnotationSet}

        """

        self._annotationSets[set._name] = set
        self._header.add_annotation_set_create(set._name, set._type)

    def add_as_create(self, name, type):
        """Create C{PyAnnotationSet} from given name, value and
        add it to this C{PyGraph}.

        :param name: C{str}
        :param type: C{str}

        """

        aSet = PyAnnotationSet(name, type)
        self.add_annotation_set(aSet)
        return aSet

    # Added AL
    def add_annotation_space(self, set):
        """Add given C{PyAnnotationSpace} to this C{PyGraph}.

        :param set: C{PyAnnotationSpace}

        """

        self._annotationSpaces[set._as_id] = set
        self._header.add_annotation_space_create(set._as_id)

    # Added AL
    def add_aspace_create(self, as_id):
        """Create C{PyAnnotationSpace} from given name, value and
        add it to this C{PyGraph}.

        :param name: C{str}
        :param type: C{str}

        """

        aSet = PyAnnotationSpace(as_id)
        self.add_annotation_space(aSet)
        return aSet

    def add_edge(self, edge):
        """Add C{PyEdge} to this C{PyGraph}.

        :param edge: C{PyEdge}

        """

        self._edgeSet[edge._id] = edge
        self.update_node(edge)

    def add_edge_create(self, id, fromNode = None , toNode = None):
        """Create C{PyEdge} from id, fromNode, toNode and add it to
        this C{PyGraph}.

        :param id: C{str}
        :param fromNode: C{PyNode}
        :param toNode: C{PyNode}

        """

        if self._nodeSet.get(fromNode.getID()) is None:
            self._nodeSet[fromNode.getID()] = fromNode
        if self._nodeSet.get(toNode.getID()) is None:
            self._nodeSet[toNode.getID()] = toNode
        self._edgeCount += 1
        newEdge = PyEdge(id, fromNode, toNode)
        self._edgeSet[newEdge.getID()] = newEdge
        self.update_node(newEdge)
        return newEdge
        
    def add_edge_from_to(self, fromNode, toNode):
        """Create C{PyEdge} from fromNode, toNode and add it to
        this C{PyGraph} id is created.

        :param fromNode: C{PyNode}
        :param toNode: C{PyNode}

        """

        return self.add_edge_create("e" + str(self._edgeCount),
                                fromNode, toNode)

    def add_edgeToFromID(self, id, fromID, toID):
        """Create C{PyEdge} from id, fromID, toID and add it to
        this C{PyGraph}.

        :param id: C{str}
        :param fromID: C{str}
        :param toID: C{str}

        """

        fromNode = self._nodeSet.get(fromID)
        toNode = self._nodeSet.get(toID)
        if fromNode is None or toNode is None:
            return None
        return self.add_edge(id, fromNode, toNode)

    def add_feature(self, name, value):
        self._features.add(name, value)

    def add_node(self, node):
        """Add C{PyNode} to this C{PyGraph}.

        :param node: C{PyNode} or C{str}

        """

        if isinstance(node, str):
            newNode = self._nodeSet.get(node)
            if newNode is None:
                newNode = PyNode(node)
                self._nodeSet[node] = newNode
            return newNode
        else:
            self._nodeSet[node._id] = node

    def add_region(self, region):
        self._regions[region._id] = region

    def annotation_sets(self):
        return self._annotationSets.itervalues()

    # Added AL
    def annotation_spaces(self):
        return self._annotationSpaces.itervalues()

    def edges(self):
        return self._edgeSet.values()

    def find_edge_from_id(self, id):
        return self._edgeSet.get(id)

    def find_edge(self, fromNode, toNode):
        """Search for C{PyEdge} with its fromNode, toNode, either nodes or ids.

        :param fromNode: C{PyNode} or C{str}
        :param toNode: C{PyNode} or C{str}
        :return: C{PyEdge}

        """

        if (isinstance(fromNode, str) and
                    isinstance(toNode, str)):
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

    def find_node(self, id):
        return self._nodeSet.get(id)

    def get_annotation_set(self, name):
        return self._annotationSets.get(name)

    def get_annotation_sets(self):
        return self._annotationSets.values()

    # Added AL
    def get_annotation_space(self, as_id):
        return self._annotationSpaces.get(as_id)

    # Added AL
    def get_annotation_spaces(self):
        return self._annotationSpaces.values()

    def get_content(self):
        return self._content

    def get_edge_set_size(self):
        return len(self._edgeSet)

    def get_feature(self, name):
        return self._features.get(name)

    def get_features(self):
        return self._features

    def get_header(self):
        return self._header

    def get_node_set_size(self):
        return len(self._nodeSet)

    def get_region(self, start, end):
        for region in self.regions():
            if (start.compare_to(region.get_start()) == 0 and
                end.compare_to(region.get_end()) == 0):
                return region
        return None

    def get_region_from_id(self, id):
        return self._regions.get(id)

    def get_regions(self):
        return self._regions.values()

    def get_root(self):
        h = self.get_header()
        roots = h.get_roots()
        if len(roots) == 0:
            return None
        id = roots[0]
        return self._nodeSet.get(id)        

    def get_roots(self):
        roots = []
        h = self.get_header()
        for id in h.get_roots():
            roots.append(self._nodeSet.get(id))
        return roots

    def get_user_object(self):
        return self._userObject

    def insert_edge(self, e):
        self._edgeSet[e.getID()] = e

    def nodes(self):
        return self._nodeSet.values()

    def regions(self):
        return self._regions.values()

    def remove_region(self, region):
        if isinstance(region, str):
            return self._regions.pop(region, None)
        else: 
            return self._regions.pop(region.getID(), None)

    def roots(self):
        return self.get_roots()

    def set_content(self, content):
        self._content = content

    def set_header(self, header):
        self._header = header

    def set_root(self, node):
        self._header.clear_roots()
        self._header.add_root(node._id)

    def set_user_object(self, object):
        self._userObject = object

    def update_node(self, edge):
        edge._fromNode.add_out_edge(edge)
        edge._toNode.add_in_edge(edge)

