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
from PyAnnotationSpace import *

class PyStandoffHeader:
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
        aSet = PyAnnotationSet(name, type)
        self._annotationSets[name] = aSet
        return aSet

    # Added AL
    def add_annotation_space(self, aSet):
        self._annotationSpaces[aSet.getName()] = aSet

    # Added AL
    def add_annotation_space_create(self, as_id):
        aSet = PyAnnotationSpace(as_id)
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
            copy = PyAnnotationSet.from_as(aSet)
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
