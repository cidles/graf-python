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
    """
    A set of PyAnnotations.  Each PyAnnotation set has a name (C{Str})
    and a type (C{URI}) and a set of annotations.

    :note : It's should replace the AnnotationSet

    """

    def __init__(self, as_id):
        """Constructor for C{PyAnnotationSpace}

        :param as_id: C{str}
        :param annotations: C{str} of C{PyAnnotation}

        """

        self._as_id = as_id
        self._annotations = []

    def from_as(aSet):
        """Constructs a new C{PyAnnotationSpace} from
        an existing C{PyAnnotationSpace}.

        :param aSet: C{PyAnnotationSpace}
        :return: C{PyAnnotationSpace}

        """

        newAS = PyAnnotationSpace(aSet._as_id)
        for a in aSet.annotations():
            newAS.add_annotation(PyAnnotation.from_annotation(a))
        return newAS

    def __repr__(self):
        return "PyAnnSpace as_id= " + self._as_id

    def add(self, label):
        """Creates a new annotation with specified label, adds it
        to this annotation set, and returns the new annotation.

        :param label: str
        :return: PyAnnotation

        """

        annotation = PyAnnotation(label)
        self.add_annotation(annotation)
        return annotation

    def add_annotation(self, a):
        """Adds a C{PyAnnotation} to the annotations list of
        this C{PyAnnotationSpace}.

        :param a: PyAnnotation

        """

        self._annotations.append(a)
        a._set = self

    def get_annotations_label(self, label):
        """Returns the C{PyAnnotation} with the given label.

        :param label: str
        :return: PyAnnotation

        """

        result = []
        for a in self._annotations:
            if label == a._label:
                result.append(a)
        return result

    def get_annotations(self, label, fs):
        """Returns the C{PyAnnotation} with the given label,
        in the given C{PyFeatureStructure}.

        :param label: str
        :param fs: PyFeatureStructure
        :return: PyFeatureStructure

        """

        result = []
        for a in self._annotations:
            if (label == a.getLabel() 
                            and fs.subsumes(a.getFeatureStructure())):
                result.append(a)
        return result

    def remove_annotation(self, a):
        """Remove the given C{PyAnnotation}.

        :param a: PyAnnotation

        """

        try:
            return self._annotations.remove(a)
        except ValueError:
            print('Error: Annotation not in set')

    def remove_annotations_label(self, label):
        """Remove the C{PyAnnotation} with the given label

        :param label: C{str}

        """

        result = []
        for a in self._annotations:
            if label == a.getLabel():
                result.append(a)
        if len(result) > 0:
            for a in result:
                self._annotations.remove(a)
        return result

    def remove_annotations(self, label, fs):
        """Remove the C{PyAnnotation}s with the given label in
        the given C{PyFeatureStructure}

        :param label: C{str}
        :param fs: C{PyFeatureStructure}

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
