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

from PyAnnotation import *

class PyAnnotationSpace:

    def __init__(self, as_id):
        self._as_id = as_id
        self._annotations = []

    def from_as(aSet):
        newAS = PyAnnotationSpace(aSet._as_id)
        for a in aSet.annotations():
            newAS.add_annotation(PyAnnotation.from_annotation(a))
        return newAS

    def __repr__(self):
        return "PyAnnSpace as_id= " + self._as_id

    def add(self, label):
        annotation = PyAnnotation(label)
        self.add_annotation(annotation)
        return annotation

    def add_annotation(self, a):
        self._annotations.append(a)
        a._set = self

    def get_annotations_label(self, label):
        result = []
        for a in self._annotations:
            if label == a._label:
                result.append(a)
        return result

    def get_annotations(self, label, fs):
        result = []
        for a in self._annotations:
            if (label == a.getLabel() 
                            and fs.subsumes(a.getFeatureStructure())):
                result.append(a)
        return result


    def remove_annotation(self, a):
        try:
            return self._annotations.remove(a)
        except ValueError:
            print('Error: Annotation not in set')

    def remove_annotations_label(self, label):
        result = []
        for a in self._annotations:
            if label == a.getLabel():
                result.append(a)
        if len(result) > 0:
            for a in result:
                self._annotations.remove(a)
        return result

    def remove_annotations(self, label, fs):
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
