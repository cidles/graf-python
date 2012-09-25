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

from graf.PyFeatureStructure import *

class PyAnnotation:
    """
    A PyAnnotation is the artifcat being annotated.  An annotation is a
    labelled feature structure.  The annotation class/interface also
    provides convenience methods for setting and getting values
    from a feature structure.

    """
    def __init__(self, label, features = PyFeatureStructure()):
        """Construct a new C{PyAnnotation}.

        :param label: C{str}
        :param features: C{list} of C{PyFeature} objects
        :param set: this C{PyAnnotation}'s C{PyAnnotationSet}
        :param element: a C{PyGraphElement} object

        """

        self._label = label
        self._features = features
        self._set = None
        self._element = None

    def from_annotation(a):
        """Construct a new C{PyAnnotation}.

        :param a: a C{PyAnnotation} object

        """
        return PyAnnotation(a.getLabel(), 
                            PyFeatureStructure.from_fs(a.getFeatures()))

    def __repr__(self):
        return "Annotation label = " + self._label

    def add(self, name, value):
        """Creates and adda a C{PyFeature} to this C{PyAnnotation}.

        :param name: name of the C{PyFeature} to be added
        :param value: value of the C{PyFeature} to be added

        """

        return self._features.add(name, value)        	

    def add_feature(self, f):
        """Adds the passed C{PyFeature} to this C{PyAnnotation}.

        :param f: C{PyFeature} object

        """

        self._features.add_feature(f)

    def features(self):
        """Returns the features.

        :return: C{list} of the C{PyFeature}s of this C{PyAnnotation}

        """

        return self._features.features()

    def get_feature(self, name):
        """Searches for a C{PyFeature} in this
        C{PyAnnotation}'s C{list} by name.

        :param name: C{str}
        :return: C{PyFeature}

        return self._features.get(name)
        """

    def get_feature_value(self, name):
        """Searches for a C{PyFeature} in this C{PyAnnotation}'s C{list}
        by name, returns that C{PyFeature}'s value.

        :param: C{str}
        :return: C{str} or None

        """

        f = self.get_feature(name)
        if f is not None and f.is_atomic():
            return f.getStringValue()
        return None
