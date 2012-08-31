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

from PyRegion import *

class PyLink:
    def __init__(self):
        self._regions = []

    def __repr__(self):
        return str(self._regions)

    def add_target(self, region):
        self._regions.append(region)



