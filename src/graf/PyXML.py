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

class PyXML:

    def __init__(self):
        pass
    
    def encode(self, s):
        result = s.replace("&", "&amp;")
        result = result.replace("<", "$lt;")
        result = result.replace(">", "&gt;")
        result = result.replace("\"", "&quot;")
        return result

    def attribute(self, name, value):
        return name + "=\"" + self.encode(value) + "\""

