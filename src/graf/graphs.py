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
An annotation graph is a directed graph that represents an annotation of
arbitrary and application dependent size. A graph may cover a sentence,
paragraph, document, or entire corpus. However, to keep processing feasible
graphs are typically relatively small (sentences say) and then combined into
larger graphs as needed.
"""

import sys

from graf.annotations import FeatureStructure, AnnotationList, AnnotationSpace

# Set the type of string
if sys.version_info[:2] >= (3, 0):
    string_type = str
else:
    string_type = basestring

class IdDict(dict):
    __slots__ = ('_id_field',)
    def __init__(self, data=(), field='id'):
        dict.__init__(self, data)
        self._id_field = field

    def add(self, obj):
        self[getattr(obj, self._id_field)] = obj

    def __iter__(self):
        if hasattr(self, 'itervalues'):
            return self.itervalues()
        elif hasattr(self, 'values'):
            return iter(self.values())

    def __contains__(self, obj):
        return dict.__contains__(self, getattr(obj, self._id_field, obj))


class GraphEdges(IdDict):
    __slots__ = ()

    def add(self, obj):
        IdDict.add(self, obj)
        obj.from_node.out_edges.add(obj)
        obj.to_node.in_edges.add(obj)


class GraphNodes(IdDict):
    __slots__ = ()

    def add(self, obj):
        """Adds the given node or creates one with the given id"""
        if isinstance(obj, string_type):
            obj = Node(obj)
        IdDict.add(self, obj)
        return obj

    def get_or_create(self, id):
        if id in self:
            return self[id]
        else:
            return self.add(id)


class GraphASpaces(IdDict):
    __slots__ = ('_add_hook',)
    def __init__(self, add_hook):
        IdDict.__init__(self, field='as_id')
        self._add_hook = add_hook

    def add(self, obj):
        IdDict.add(self, obj)
        self._add_hook(obj)

    def create(self, as_id):
        res = AnnotationSpace(as_id)
        self.add(res)
        return res


class Graph(object):
    """
    Class of Graph.
    """

    def __init__(self):
        """
        Constructor for Graph.
        """
        self.features = FeatureStructure()
        self.nodes = GraphNodes()
        self._top_edge_id = 0
        self.edges = GraphEdges()
        self.regions = IdDict()
        self.content = None
        self.header = StandoffHeader()
        self.annotation_spaces = GraphASpaces(self.header.add_annotation_space)

    def create_edge(self, from_node=None, to_node=None, id=None):
        """Create C{Edge} from id, from_node, to_node and add it to
        this C{Graph}.

        :param id: C{str}
        :param from_node: C{Node}
        :param to_node: C{Node}

        """
        if not hasattr(from_node, 'id'):
            from_node = self.nodes[from_node]
        if from_node.id not in self.nodes:
            self.nodes.add(from_node)

        if not hasattr(to_node, 'id'):
            to_node = self.nodes[to_node]
        if to_node.id not in self.nodes:
            self.nodes.add(to_node)

        if id is None:
            while id is None or id in self.edges:
                id = 'e%d' % self._top_edge_id
                self._top_edge_id += 1
        res = Edge(id, from_node, to_node)
        self.edges.add(res)
        return res

    def find_edge(self, from_node, to_node):
        """Search for C{Edge} with its from_node, to_node, either nodes or ids.

        :param from_node: C{Node} or C{str}
        :param to_node: C{Node} or C{str}
        :return: C{Edge} or None
        """
        # resolve ids to nodes if necessary
        if not isinstance(from_node, Node):
            from_node = self.nodes[from_node]
        if not isinstance(to_node, Node):
            to_node = self.nodes[to_node]

        if len(from_node.out_edges) < len(to_node.in_edges):
            for edge in from_node.out_edges:
                if edge.to_node == to_node:
                    return edge
        else:
            for edge in to_node.in_edges:
                if edge.from_node == from_node:
                    return edge
        return None

    def get_element(self, id):
        if id in self.nodes:
            return self.nodes[id]
        return self.edges[id]

    def get_region(self, *anchors):
        for region in self.regions:
            if region.anchors == anchors:
                return region
        return None

    def _get_root(self):
        try:
            if sys.version_info[:2] >= (3, 0):
                return self.iter_roots().__next__()
            else:
                return self.iter_roots().next()
        except StopIteration:
            return None
    def _set_root(self, node):
        # FIXME: how should this interact with node.is_root
        self.header.clear_roots()
        if node.id not in self.nodes:
            raise ValueError('The new root node is not in the graph: %r' % node)
        self.header.roots.append(node.id)
    root = property(_get_root, _set_root)

    def iter_roots(self):
        return (self.nodes[id] for id in self.header.roots)



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
        self.id = id
        self.visited = False
        self.annotations = AnnotationList(self, 'element')

    def __repr__(self):
        return "GraphElement id = " + self.id

    @property
    def is_annotated(self):
        return bool(self.annotations)

    def clear(self):
        self.visited = False

    def __eq__(self, other):
        """Comparison of two graph elements by ID.

        :param o: C{GraphElement}
        """

        if other is None:
            return False
        return type(self) is type(other) and self.id == other.id

    def visit(self):
        self.visited = True


class EdgeList(object):
    """An append-only structure with O(1) lookup by id or order-index"""

    __slots__ = ('_by_ind', '_by_id')

    def __init__(self):
        self._by_ind = []
        self._by_id = {}

    def add(self, edge):
        self._by_id[edge.id] = edge
        self._by_ind.append(edge)

    def __iter__(self):
        return iter(self._by_ind)

    def __len__(self):
        return len(self._by_ind)

    def __getitem__(self, sl):
        """
        Returns the edge corresponding to the specified slice/index or raises an IndexError.
        If the given value is not a slice or int, returns the edge with the given id, or raises a KeyError
        """
        # should ID lookup have preference??
        if isinstance(sl, (int, slice)):
            return self._by_ind[sl]
        return self._by_id[sl]

    def __contains__(self, edge):
        if hasattr(edge, 'id'):
            edge = edge.id
        return edge in self._by_id

    def ids(self):
        return self._by_id.keys()


class Node(GraphElement):
    """
    Class for nodes within a C{Graph} instance.
    Each node keeps a list of in-edges and out-edges.
    Each collection is backed by two data structures:
    1. A list (for traversals)
    2. A hash map
    Nodes may also contain one or more C{Annotation} objects.

    """

    def __init__(self, id=""):
        GraphElement.__init__(self, id)
        self.in_edges = EdgeList()
        self.out_edges = EdgeList()
        self.links = []

    def __repr__(self):
        return "NodeID = " + self.id

    def __lt__(self, other):
        return self.id < other.id

    # Relationship to media

    def add_link(self, link):
        self.links.append(link)
        self._add_regions(link)

    def _add_regions(self, regions):
        for region in regions:
            region.nodes.append(self)

    def add_region(self, region):
        """Adds the given region to the first link for this node"""
        if self.links:
            self.links[0].append(region)
            self._add_regions((region,))
        else:
            self.add_link(Link((region,)))

    # Relationship within graph

    def iter_parents(self):
        for edge in self.in_edges:
            res = edge.from_node
            if res is not None:
                yield res

    @property
    def parent(self):
        try:
            if sys.version_info[:2] >= (3, 0):
                return self.iter_parents().__next__()
            else:
                return self.iter_parents().next()
        except StopIteration:
            raise AttributeError('%r has no parents' % self)

    def iter_children(self):
        for edge in self.out_edges:
            res = edge.to_node
            if res is not None:
                yield res
        
    def clear(self):
        """Clears this node's visisted status and those of all visited descendents"""
        self.visited = False

        for child in self.iter_children():
            if child.visited:
                child.clear()

    @property
    def degree(self):
        return len(self.in_edges) + len(self.out_edges)


class Edge(GraphElement):
    """
    Class of edges in Graph:
    - Each edge maintains the source (from) C{Node} and the destination.
    (to) C{Node}.
    - Edges may also contain one or more C{Annotation} objects.

    """
    def __init__(self, id, from_node=None, to_node=None):
        """C{Edge} Constructor.

        :param id: C{str}
        :param from_node: C{Node}
        :param to_node: C{Node}

        """
        GraphElement.__init__(self, id)
        self.from_node = from_node
        self.to_node = to_node

    def __repr__(self):
        return "Edge id = " + self.id


class Link(list):
    """
    Link objects are used to associate nodes in the graph with the
    regions of the graph they annotate. Links are almost like edges except a
    link is a relation between a node and a region rather than a relation
    between two nodes. A node make be linked to more than one region.
    """
    # Inherits all functionality from builtin list
    __slots__ = ()
    def __init__(self, vals=()):
        super(Link, self).__init__(vals)


class StandoffHeader(object):
    def __init__(self):
        self.annotation_spaces = {}
        self.depends_on = []
        self.roots = []

    def __repr__(self):
        return "StandoffHeader"

    def add_annotation_space(self, aspace):
        self.annotation_spaces[aspace.as_id] = aspace

    def add_dependency(self, type, location):
        self.depends_on.append(type)

    def clear_roots(self):
        del self.roots[:]