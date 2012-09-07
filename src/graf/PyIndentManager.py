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

class PyIndentManager:
    def __init__(self):
        self._indent = "    "

    def __repr__(self):
        return self._indent

    def more(self):
        self._indent += "    "

    def less(self):
        self._indent = self._indent[0:len(self._indent)-4]


