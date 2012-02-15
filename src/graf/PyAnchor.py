# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

class PyAnchor:
    """
    Class for the PyAnchor elements of a PyGraph.
    These are used to represent character offsets in a region of text.
    Each PyAnchor contains an offset, which is a number (int) that 
    corresponds to a character position in a text file
    """
    def __init__(self, offset = 0):
        self._offset = offset

    def __repr__(self):
        return "AnchorOffset = " + str(self._offset)

    def toString(self):
        return str(self._offset)

    def add(self, delta):
        #TODO: add outofbounds check
        self._offset += delta

    def addAnchor(self, a):
        self._offset += a._offset

    def addFromAnchor(self, a):
        self._offset += a._offset

    def subtract(self, delta):
        self._offset = self._offset - delta
        return self._offset

    def subtractFromAnchor(self, a):
        self._offset = self._offset - a.getOffset()
        return self._offset

    def compareTo(self, a):
        if self._offset == a._offset:
            return 0
        elif self._offset < a._offset:
            return -1
        return 1        

    def equals(self, a):
        if isinstance(a, PyAnchor):
            return self._offset == a._offset()
        return False
    
    def getOffset(self):
        return self._offset



