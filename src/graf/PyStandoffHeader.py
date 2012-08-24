# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

from graf import PyAnnotationSpace

class PyStandoffHeader:

    def __init__(self):
        self._annotationSets = {}
        self._dependsOn = []
        self._roots = []

    def __repr__(self):
        return "StandoffHeader"

    def add_annotation_set(self, aSet):
        self._annotationSets[aSet.getName()] = aSet

    def add_annotation_set_create(self, name, type):
        aSet = PyAnnotationSpace(name, type)
        self._annotationSets[name] = aSet
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
            copy = PyAnnotationSpace.from_as(aSet)
            self._annotationSets[copy.getName()] = copy

    def get_annotation_set(self, name):
        return self._annotationSets.get(name)

    def get_annotation_sets(self):
        return list(self._annotationSets.values())

    def get_depends_on(self):
        return self._dependsOn

    def get_roots(self):
        return self._roots

    def remove_root(self, id):
        self._roots.remove(id)

    def set_depends_on(self, dependsOn):
        self._dependsOn = dependsOn
