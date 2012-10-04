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
The graph is undirected, composed of C{Node}s and C{Edge}s, each
backed by a C{list} to maintain the order of the nodes/edges and to
allow for quick traversals, and a hash map so nodes/edges can be found
quickly based on their ID
"""

from annotations import FeatureStructure, AnnotationSpace, Annotation

class Graph(object):
    """
    Class of Graph.

    """

    def __init__(self):
        """Constructor for Graph.

        """

        self._edgeCount = 0
        self._features = FeatureStructure()
        self._nodeSet = {}
        self._edgeSet = {}
        self._regions = {}
        self._annotationSets = {}
        self._annotationSpaces = {} # Added AL
        self._content = None
        self._header = StandoffHeader()
        self._userObject = None

    def add_annotation_set(self, set):
        """Add given C{AnnotationSet} to this C{Graph}.

        :param set: C{AnnotationSet}

        """

        self._annotationSets[set._name] = set
        self._header.add_annotation_set_create(set._name, set._type)

    def add_as_create(self, name, type):
        """Create C{AnnotationSet} from given name, value and
        add it to this C{Graph}.

        :param name: C{str}
        :param type: C{str}

        """

        aSet = AnnotationSet(name, type)
        self.add_annotation_set(aSet)
        return aSet

    # Added AL
    def add_annotation_space(self, set):
        """Add given C{AnnotationSpace} to this C{Graph}.

        :param set: C{AnnotationSpace}

        """

        self._annotationSpaces[set._as_id] = set
        self._header.add_annotation_space_create(set._as_id)

    # Added AL
    def add_aspace_create(self, as_id):
        """Create C{AnnotationSpace} from given name, value and
        add it to this C{Graph}.

        :param name: C{str}
        :param type: C{str}

        """

        aSet = AnnotationSpace(as_id)
        self.add_annotation_space(aSet)
        return aSet

    def add_edge(self, edge):
        """Add C{Edge} to this C{Graph}.

        :param edge: C{Edge}

        """

        self._edgeSet[edge._id] = edge
        self.update_node(edge)

    def add_edge_create(self, id, fromNode = None , toNode = None):
        """Create C{Edge} from id, fromNode, toNode and add it to
        this C{Graph}.

        :param id: C{str}
        :param fromNode: C{Node}
        :param toNode: C{Node}

        """

        if self._nodeSet.get(fromNode.getID()) is None:
            self._nodeSet[fromNode.getID()] = fromNode
        if self._nodeSet.get(toNode.getID()) is None:
            self._nodeSet[toNode.getID()] = toNode
        self._edgeCount += 1
        newEdge = Edge(id, fromNode, toNode)
        self._edgeSet[newEdge.getID()] = newEdge
        self.update_node(newEdge)
        return newEdge
        
    def add_edge_from_to(self, fromNode, toNode):
        """Create C{Edge} from fromNode, toNode and add it to
        this C{Graph} id is created.

        :param fromNode: C{Node}
        :param toNode: C{Node}

        """

        return self.add_edge_create("e" + str(self._edgeCount),
                                fromNode, toNode)

    def add_edgeToFromID(self, id, fromID, toID):
        """Create C{Edge} from id, fromID, toID and add it to
        this C{Graph}.

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
        """Add C{Node} to this C{Graph}.

        :param node: C{Node} or C{str}

        """

        if isinstance(node, str):
            newNode = self._nodeSet.get(node)
            if newNode is None:
                newNode = Node(node)
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
        """Search for C{Edge} with its fromNode, toNode, either nodes or ids.

        :param fromNode: C{Node} or C{str}
        :param toNode: C{Node} or C{str}
        :return: C{Edge}

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

class GraphElement(object):
    """
    Class of edges in Graph:

    - Each edge maintains the source (from) C{Node} and the destination.
      (to) C{Node}.
    - Edges may also contain one or more C{Annotation} objects.

    """

    def __init__(self, id = ""):
        """Constructor for C{GraphElement}.

        :param id: C{str}

        """

        self._id = id
        self._userObject = None
        self._visited = False
        self._annotations = []

    def from_node(node):
        """Constructs a new C{GraphElement} from an existing node.

        :param node: C{Node}

        """

        newGE = GraphElement(node.getID())
        for a in node.annotations():
            newGE.add_annotation(a)
        newGE.set_user_object(node.get_user_object)
        return newGE

    def from_edge(edge):
        """Constructs a new C{GraphElement} from an existing edge.

        :param edge: C{Edge}

        """

        newGE = GraphElement(edge.getID())
        for a in edge.annotations():
            newGE.addAnnotations(a)
        newGE.set_user_object(edge.get_user_object())
        return newGE

    def __repr__(self):
        return "GraphElement id = " + self._id

    def add_annotation(self, a):
        self._annotations.append(a)
        a.element = self

    def add_annotation_create(self, label):
        """Creates an adds an annotation to this C{GraphElement}.

        :param label: C{str}

        """

        a = Annotation(label)
        self.add_annotation(a)
        return a

    def annotated(self):
        return not len(self._annotations) == 0

    def clear(self):
        self._visited = False

    def equals(self, o):
        """Comparison of two graph elements by ID.

        :param o: C{GraphElement}

        """

        if not isinstance(o, GraphElement) or o == None:
            return False
        else:
            return self._id == o.getID()

    def get_annotation(self, label = ""):
        if label == "":
            if len(self._annotations) == 0:
                return None
            else:
                return self._annotations[0]
        else:
            for a in self._annotations:
                if label == a.getLabel():
                    return a
            return None

    def get_annotation_from_set(self, setName, label):#
        result = self.get_annotation(label)
        if result is None:
            return None
        aSet = result.get_annotation_set()
        if aSet is None:
            return None
        if not setName == aSet.getName():
            return None
        return result

    def get_feature(self, ann, name):
        a = self.get_annotation(ann)
        if a is None:
            return None
        return a.get_feature(name)

    def get_feature_from_set(self, set, ann, name):#
        a = self.get_annotation_from_set(set, ann)
        if a is not None:
            return a.get_feature(name)
        return None

    def get_user_object(self): #
        return self._userObject

    def set_id(self, id): #
        self._id = id

    def set_user_object(self, object): #
        self._userObject = object

    def set_visited(self, visited): #
        self._visited = visited

    def visit(self):
        self._visited = True

    def visited(self):
        return self._visited            


class Node(GraphElement):
    """
    Class for nodes within a C{Graph} instance.
    Each node keeps a list of in-edges and out-edges.
    Each collection is backed by two data structures:
        1. A list (for traversals)
        2. A hash map
    Nodes may also contain one or more C{Annotation} objects.

    """

    def __init__(self, id = ""):
        GraphElement.__init__(self, id)
        self._inEdgeList = []
        self._outEdgeList = []
        self._inEdges = {}
        self._outEdges = {}
        self._links = []
        self._annotationRoot = False

    def from_node(node):
        newNode = Node(node._id)
        newNode._annotationRoot = node._annotationRoot
        return newNode

    def __repr__(self):
        return "NodeID = " + self._id

    def add_in_edge(self, e):
        self._inEdges[e._id] = e
        self._inEdgeList.append(e)

    def add_link(self, link):
        self._links.append(link)
        for region in link._regions:
            region.add_node(self)

    def add_out_edge(self, e):
        self._outEdges[e._id] = e    
        self._outEdgeList.append(e)
    
    def add_region(self, region):
        link = None
        if len(self._links) > 0:
            link = self._links[len(self._links)-1]
        else:
            link = Link()
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
        if isinstance(index, basestring):
            return self._inEdges.get(index)
        else:
            if len(self._inEdgeList) <= index:
                return None
            else:
                return self._inEdgeList[index]

    def get_out_edge(self, index):
        if isinstance(index, basestring):
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


class Edge(GraphElement):
    """
    Class of edges in Graph:
    - Each edge maintains the source (from) C{Node} and the destination.
      (to) C{Node}.
    - Edges may also contain one or more C{Annotation} objects.

    """

    def __init__(self, id, fromNode = None, toNode = None):
        """C{Edge} Constructor.

        :param id: C{str}
        :param fromNode: C{Node}
        :param toNode: C{Node}

        """

        GraphElement.__init__(self, id)
        self._fromNode = fromNode
        self._toNode = toNode

    def from_edge(e):
        """C{Edge} Constructor from an existing C{Edge}.

        :param e: C{Edge}

        """

        return Edge(e._id, e._fromNode, e._toNode)

    def __repr__(self):
        return "Edge id = " + self._id


class Link(object):
    def __init__(self):
        self._regions = []

    def __repr__(self):
        return str(self._regions)

    def add_target(self, region):
        self._regions.append(region)


class StandoffHeader(object):
    def __init__(self):
        self._annotationSets = {}
        self._annotationSpaces = {}
        self._dependsOn = []
        self._roots = []

    def __repr__(self):
        return "StandoffHeader"

    def add_annotation_set(self, aSet):
        self._annotationSets[aSet.getName()] = aSet

    def add_annotation_set_create(self, name, type):
        aSet = AnnotationSet(name, type)
        self._annotationSets[name] = aSet
        return aSet

    # Added AL
    def add_annotation_space(self, aSet):
        self._annotationSpaces[aSet.getName()] = aSet

    # Added AL
    def add_annotation_space_create(self, as_id):
        aSet = AnnotationSpace(as_id)
        self._annotationSpaces[as_id] = aSet
        return aSet

    def add_dependency(self, type, location):
        self._dependsOn.append(type)

    def add_root(self, id):
        self._roots.append(id)

    def clear_roots(self):
        del self._roots[:]

    def copy(self, header):
        self._dependsOn = list(header.get_depends_on())
        self._roots = list(header.get_roots())
        del self._annotationSets[:]
        for aSet in header.get_annotation_sets():
            copy = AnnotationSet.from_as(aSet)
            self._annotationSets[copy.getName()] = copy

    def get_annotation_set(self, name):
        return self._annotationSets.get(name)

    def get_annotation_sets(self):
        return list(self._annotationSets.values())

    # Added AL
    def get_annotation_space(self, as_id):
        return self._annotationSpaces.get(as_id)

    # Added AL
    def get_annotation_spaces(self):
        return list(self._annotationSpaces.values())

    def get_depends_on(self):
        return self._dependsOn

    def get_roots(self):
        return self._roots

    def remove_root(self, id):
        self._roots.remove(id)

    def set_depends_on(self, dependsOn):
        self._dependsOn = dependsOn


