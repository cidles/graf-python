# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

from PyAnnotationSet import *

class PyStandoffHeader:
    def __init__(self):
        self._annotationSets = {}
        self._dependsOn = []
        self._roots = []

    def __repr__(self):
        return "StandoffHeader"

    def addAnnotationSet(self, aSet):
        self._annotationSets[aSet.getName()] = aSet

    def addAnnotationSetCreate(self, name, type):
        aSet = PyAnnotationSet(name, type)
        self._annotationSets[name] = aSet
        return aSet

    def addDependency(self, type, location):
        self._dependsOn.append(type)

    def addRoot(self, id):
        self._roots.append(id)

    def clearRoots(self):
        del self._roots[:]

    def copy(self, header):
        self._dependsOn = list(header.getDependsOn())
        self._roots = list(header.getRoots())
        del self._annotationSets[:]
        for aSet in header.getAnnotationSets():
            copy = PyAnnotationSet.fromAS(aSet)
            self._annotationSets[copy.getName()] = copy

    def getAnnotationSet(self, name):
        return self._annotationSets.get(name)

    def getAnnotationSets(self):
        return list(self._annotationSets.values())

    def getDependsOn(self):
        return self._dependsOn

    def getRoots(self):
        return self._roots

    def removeRoot(self, id):
        self._roots.remove(id)

    def setDependsOn(self, dependsOn):
        self._dependsOn = dependsOn
