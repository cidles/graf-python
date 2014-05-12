# graf-python: Python GrAF API
#
# Copyright (C) 2014 American National Corpus
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.anc.org/>
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
        self.anchors = list(anchors)
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

    @property
    def end(self):
        return self.anchors[-1]

    @end.setter
    def end(self, val):
        self.anchors[-1] = val

    @property
    def start(self):
        return self.anchors[0]

    @start.setter
    def start(self, val):
        self.anchors[0] = val
