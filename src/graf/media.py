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

# Note: Python Anchor objects:
# * are immutable
# * provide __cmp__, __add__ and __sub__
# * may be initialised given a string representation

CharAnchor = int

class Region(object):
    """
    The area in the text file being annotated.  A region is defined 
    by a sequence of anchor values.

    """
    __slots__ = ('id', 'nodes', 'anchors')

    def __init__(self, id, *anchors):
        """Constructor for C{Region}.

        :param id: C{str}
        :param anchors: C{list} of C{Anchor}

        """

        self.id = id
        self.nodes = []
        self.anchors = anchors
        if len(anchors) == 1:
            raise ValueError('Regions must be defined by at least 2 anchors')

    def __repr__(self):
        return "RegionID = " + self.id

    def __iadd__(self, offset):
        for i in range(len(self.anchors)):
            self.anchors[i] += offset

    def __isub__(self, offset):
        for i in range(len(self.anchors)):
            self.anchors[i] -= offset

    def __cmp__(self, other):
        return (len(self.anchors) - len(other.anchors)) or cmp(self.anchors, other.anchors)

    def __eq__(self, other):
        if not isinstance(other, Region) or other is None:
            return False
        return not cmp(self, other)
        
    @property
    def end(self):
        return self.anchors[-1]
    
    @property
    def start(self):
        return self.anchors[0]
