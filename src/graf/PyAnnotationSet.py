# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

from PyAnnotation import *

class PyAnnotationSet:
    """
    A set of PyAnnotations.  Each PyAnnotation set has a name (C{Str})
    and a type (C{URI}) and a set of annotations.
    """
    def __init__(self, name, type):
        """
        Constructor for C{PyAnnotationSet}
        @param name: C{str}
        @param type: C{str}
        @param annotations: C{str} of C{PyAnnotation}
        """
        self._name = name
        self._type = type
        self._annotations = []

    def fromAS(aSet):
        """
        Constructs a new C{PyAnnotationSet} from 
        an existing C{PyAnnotationSet}
        @param aSet: C{PyAnnotationSet}
        @return: C{PyAnnotationSet}
        """
        newAS = PyAnnotationSet(aSet._name, aSet._type)
        for a in aSet.annotations():
            newAS.addAnnotation(PyAnnotation.fromAnnotation(a))
        return newAS

    def __repr__(self):
        return "PyAnnSet name= " + self._name + " type= " + self._type

    def add(self, label):
        """
        Creates a new annotation with specified label, adds it 
        to this annotation set, and returns the new annotation
        @param label: C{str}
        @return: C{PyAnnotation}
        """
        annotation = PyAnnotation(label)
        self.addAnnotation(annotation)
        return annotation

    def addAnnotation(self, a):
        """
        Adds a C{PyAnnotation} to the annotations list of 
        this C{PyAnnotationSet}
        @param a: C{PyAnnotation}
        """
        self._annotations.append(a)
        a._set = self

    def getAnnotationsLabel(self, label):
        """
        Returns the C{PyAnnotation} with the given label
        @param label: C{str}
        @return: C{PyAnnotation}
        """
        result = []
        for a in self._annotations:
            if label == a._label:
                result.append(a)
        return result

    def getAnnotations(self, label, fs):
        """
        Returns the C{PyAnnotation} with the given label, 
        in the given C{PyFeatureStructure}
        @param label: C{str}
        @param fs: C{PyFeatureStructure}
        return: C{PyFeatureStructure}
        """
        result = []
        for a in self._annotations:
            if (label == a.getLabel() 
                            and fs.subsumes(a.getFeatureStructure())):
                result.append(a)
        return result


    def removeAnnotation(self, a):
        """
        Remove the given C{PyAnnotation}
        @param a: C{PyAnnotation}
        """
        try:
            return self._annotations.remove(a)
        except ValueError:
            print "Error: Annotation not in set"

    def removeAnnotationsLabel(self, label):
        """
        Remove the C{PyAnnotation} with the given label
        @param label: C{str}
        """
        result = []
        for a in self._annotations:
            if label == a.getLabel():
                result.append(a)
        if len(result) > 0:
            for a in result:
                self._annotations.remove(a)
        return result

    def removeAnnotations(self, label, fs):
        """
        Remove the C{PyAnnotation}s with the given label in 
        the given C{PyFeatureStructure}
        @param label: C{str}
        @param fs: C{PyFeatureStructure}
        """
        result = []
        for a in self._annotations:
            if (label == a.getLabel() 
                            and fs.subsumes(a.getFeatureStructure())):
                result.append(a)
        if len(result) > 0:
            for a in result:
                self._annotations.remove(a)
        return result

    def size(self):
        return len(self._annotations)
