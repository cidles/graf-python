# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

from PyRegion import *

class PyLink:
    def __init__(self):
        self._regions = []

    def __repr__(self):
        return str(self._regions)

    def addTarget(self, region):
        self._regions.append(region)



