# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

from PyAnchor import *
from PyNode import *

class PyRegion:
    """
    The area in the text file being annotated.  A region is defined 
    by a sequence of C{PyAnchor} objects
    """

    def __init__(self, id, anchors=None):
        """
        Constructor for C{PyRegion}
        @param id: C{str}
        @param anchors: C{list} of C{PyAnchor}
        """
        self._id = id
        self._nodes = []
        if anchors is None:
            self._anchors = [] 
        elif len(anchors) < 2:
            #add exception
            print "Regions must be bound by at least two anchors"
        else:
            self._anchors = anchors

    def fromRegion(region):
        return PyRegion(region._id, region._anchors)

    def fromStartEnd(id, start, end):
        return PyRegion(id, [start, end])

    def __repr__(self):
        return "RegionID = " + self._id
    
    def add(self, offset):
        self._anchors = [anchor.add(offset) for anchor in self._anchors]

    def addAnchor(self, anchor):
        self._anchors.append(anchor)

    def addNode(self, node):
        if not node in self._nodes:
            self._nodes.append(node)
        
    def compareTo(self, region):
        thisSize = len(self._anchors)
        regionSize = region.getNumAnchors()
        ##better alg?
        if thisSize != regionSize:
            return thisSize - regionSize

        if thisSize == 2:
            result = self.getStart().compareTo(region.getStart())
            if result != 0:
                return result

            return region.getEnd().compareTo(self.getEnd()) 
        
        #python iterator?
        tempIndex = 0
        regionAnchors = region.getAnchors()

        for anchor, regionAnchor in zip(self._anchors, regionAnchors):
            result = thisAnchor.compareTo(regionAnchor)
            if result != 0:
                return result
        return 0

    def equals(self, object):
        if not isinstance(object, PyRegion) or object is None:
            return False
        return self.compareTo(object) == 0


    def getAnchor(self, index):
        if index < 0 or index > (len(self._anchors)-1):
            return None
        return self._anchors[index]

    def getAnchors(self):
        #need to make this unmodifiable
        new_anchors = list(self._anchors)
        return new_anchors
        
    def getEnd(self):
        return self._anchors[len(self._anchors)-1]
    
    def getNumAnchors(self):
        return len(self._anchors)
    
    def getStart(self):
        return self._anchors[0]
    
    def removeAnchor(self, anchor):
        self._anchors.remove(anchor)

    def setAnchor(self, index, anchor):
        """
        Sets the anchors at the given index
        """
        if index < 0 or len(self._anchors) <= index:
            print "Index out of bounds"
            return None
        self._anchors[index] = anchor

    def setAnchors(self, anchors):
        """
        Sets the list of anchors that bounds the region
        """
        self._anchors = anchors

    def setEnd(self, anchor):
        self.setAnchor(len(self._anchors) - 1, anchor)

    def setStart(self, anchor):
        self.setAnchor(0, anchor)

    def subtract(self, offset):
        [anchor.subtract(offset) for anchor in self._anchors]



