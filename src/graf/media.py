# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

# Note: Python Anchor objects:
# * are immutable
# * provide __lt__, __eq__, __add__ and __sub__
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

    def __lt__(self, other):
        if len(self.anchors) == len(other.anchors):
            return self.anchors < other.anchors
        return len(self.anchors) < len(other.anchors) # TODO: work out correct behaviour

    def __eq__(self, other):
        if not isinstance(other, Region) or other is None:
            return False
        return self.anchors == other.anchors

    def _get_end(self):
        return self.anchors[-1]
    def _set_end(self, val):
        self.anchors[-1] = val
    end = property(_get_end, _set_end)
    
    def _get_start(self):
        return self.anchors[0]
    def _set_start(self, val):
        self.anchors[0] = val
    start = property(_get_start, _set_start)
    
