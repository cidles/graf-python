# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

from graf.PyGraphElement import PyGraphElement

class PyEdge(PyGraphElement):
    """
    Class of edges in PyGraph:
    
    - Each edge maintains the source (from) C{PyNode} and the destination.
      (to) C{PyNode}. 
    - Edges may also contain one or more C{PyAnnotation} objects.
    
    """

    def __init__(self, id, fromNode = None, toNode = None):
        """C{PyEdge} Constructor.
        
        :param id: C{str}
        :param fromNode: C{PyNode}
        :param toNode: C{PyNode}
        
        """
        
        PyGraphElement.__init__(self, id)
        self._fromNode = fromNode
        self._toNode = toNode

    def from_edge(e):
        """C{PyEdge} Constructor from an existing C{PyEdge}.
        
        :param e: C{PyEdge}
        
        """
        return PyEdge(e._id, e._fromNode, e._toNode)

    def __repr__(self):
        return "Edge id = " + self._id

