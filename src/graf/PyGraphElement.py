# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

from PyAnnotationSet import *
from PyFeature import *

class PyGraphElement:
    def __init__(self, id = ""):
        """
        Constructor for C{PyGraphElement}
        @param id: C{str}
        """
        self._id = id
        self._userObject = None
        self._visited = False
        self._annotations = []

    def fromNode(node):
        """
        Constructs a new C{PyGraphElement} from an existing node
        @param node: C{PyNode}
        """
        newGE = PyGraphElement(node.getID())
        for a in node.annotations():
            newGE.addAnnotation(a)
        newGE.setUserObject(node.getUserObject)
        return newGE

    def fromEdge(edge):
        """
        Constructs a new C{PyGraphElement} from an existing edge
        @param edge: C{PyEdge}
        """
        newGE = PyGraphElement(edge.getID())
        for a in edge.annotations():
            newGE.addAnnotations(a)
        newGE.setUserObject(edge.getUserObject())
        return newGE

    def __repr__(self):
        return "PyGraphElement id = " + self._id

    def addAnnotation(self, a):
        self._annotations.append(a)
        a._element = self

    def addAnnotationCreate(self, label):
        """
        Creates an adds an annotation to this C{PyGraphElement}
        @param label: C{str}
        """
        a = PyAnnotation(label)
        self.addAnnotation(a)
        return a

    def annotated(self):
        return not len(self._annotations) == 0

    def clear(self):
        self._visited = False

    def equals(self, o):
        """
        Comparison of two graph elements by ID
        @param o: C{PyGraphElement}
        """
        if not isinstance(o, PyGraphElement) or o == None:
            return False
        else:
            return self._id == o.getID()

    def getAnnotation(self, label = ""):
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

    def getAnnotationFromSet(self, setName, label):#
        result = self.getAnnotation(label)
        if result is None:
            return None
        aSet = result.getAnnotationSet()
        if aSet is None:
            return None
        if not setName == aSet.getName():
            return None
        return result

    def getFeature(self, ann, name):
        a = self.getAnnotation(ann)
        if a is None:
            return None
        return a.getFeature(name)

    def getFeatureFromSet(self, set, ann, name):#
        a = self.getAnnotationFromSet(set, ann)
        if a is not None:
            return a.getFeature(name)
        return None

    def getUserObject(self): #
        return self._userObject

    def setID(self, id): #
        self._id = id

    def setUserObject(self, object): #
        self._userObject = object

    def setVisited(self, visited): #
        self._visited = visited

    def visit(self):
        self._visited = True

    def visited(self):
        return self._visited            

    
    
    
