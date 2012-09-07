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

from PyAnnotationSet import *
from PyFeature import *

class PyGraphElement:
    """
    Class of edges in PyGraph:

    - Each edge maintains the source (from) C{PyNode} and the destination.
      (to) C{PyNode}.
    - Edges may also contain one or more C{PyAnnotation} objects.

    """

    def __init__(self, id = ""):
        """Constructor for C{PyGraphElement}.

        :param id: C{str}

        """

        self._id = id
        self._userObject = None
        self._visited = False
        self._annotations = []

    def from_node(node):
        """Constructs a new C{PyGraphElement} from an existing node.

        :param node: C{PyNode}

        """

        newGE = PyGraphElement(node.getID())
        for a in node.annotations():
            newGE.add_annotation(a)
        newGE.set_user_object(node.get_user_object)
        return newGE

    def from_edge(edge):
        """Constructs a new C{PyGraphElement} from an existing edge.

        :param edge: C{PyEdge}

        """

        newGE = PyGraphElement(edge.getID())
        for a in edge.annotations():
            newGE.addAnnotations(a)
        newGE.set_user_object(edge.get_user_object())
        return newGE

    def __repr__(self):
        return "PyGraphElement id = " + self._id

    def add_annotation(self, a):
        self._annotations.append(a)
        a._element = self

    def add_annotation_create(self, label):
        """Creates an adds an annotation to this C{PyGraphElement}.

        :param label: C{str}

        """

        a = PyAnnotation(label)
        self.add_annotation(a)
        return a

    def annotated(self):
        return not len(self._annotations) == 0

    def clear(self):
        self._visited = False

    def equals(self, o):
        """Comparison of two graph elements by ID.

        :param o: C{PyGraphElement}

        """

        if not isinstance(o, PyGraphElement) or o == None:
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

    
    
    
