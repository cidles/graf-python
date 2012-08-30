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

    def from_region(region):
        return PyRegion(region._id, region._anchors)

    def from_start_end(id, start, end):
        return PyRegion(id, [start, end])

    def __repr__(self):
        return "RegionID = " + self._id
    
    def add(self, offset):
        self._anchors = [anchor.add(offset) for anchor in self._anchors]

    def add_anchor(self, anchor):
        self._anchors.append(anchor)

    def add_node(self, node):
        if not node in self._nodes:
            self._nodes.append(node)
        
    def compare_to(self, region):
        thisSize = len(self._anchors)
        regionSize = region.get_num_anchors()
        ##better alg?
        if thisSize != regionSize:
            return thisSize - regionSize

        if thisSize == 2:
            result = self.get_start().compare_to(region.get_start())
            if result != 0:
                return result

            return region.get_end().compare_to(self.get_end())
        
        #python iterator?
        tempIndex = 0
        regionAnchors = region.get_anchors()

        for anchor, regionAnchor in zip(self._anchors, regionAnchors):
            result = thisAnchor.compare_to(regionAnchor)
            if result != 0:
                return result
        return 0

    def equals(self, object):
        if not isinstance(object, PyRegion) or object is None:
            return False
        return self.compare_to(object) == 0


    def get_anchor(self, index):
        if index < 0 or index > (len(self._anchors)-1):
            return None
        return self._anchors[index]

    def get_anchors(self):
        #need to make this unmodifiable
        new_anchors = list(self._anchors)
        return new_anchors
        
    def get_end(self):
        return self._anchors[len(self._anchors)-1]
    
    def get_num_anchors(self):
        return len(self._anchors)
    
    def get_start(self):
        return self._anchors[0]
    
    def remove_anchor(self, anchor):
        self._anchors.remove(anchor)

    def set_anchor(self, index, anchor):
        """
        Sets the anchors at the given index
        """
        if index < 0 or len(self._anchors) <= index:
            print "Index out of bounds"
            return None
        self._anchors[index] = anchor

    def set_anchors(self, anchors):
        """
        Sets the list of anchors that bounds the region
        """
        self._anchors = anchors

    def set_end(self, anchor):
        self.set_anchor(len(self._anchors) - 1, anchor)

    def set_start(self, anchor):
        self.set_anchor(0, anchor)

    def subtract(self, offset):
        [anchor.subtract(offset) for anchor in self._anchors]



