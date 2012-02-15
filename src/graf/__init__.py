# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

"""
The PyGrAF API is used by the ISO GrAF corpus reader (masc.py)
to parse the MASC Corpus.  Each text file in the corpus is accompanied
by a series of xml files that store annotation information for that
text file.  So, to parse the annotations we must first construct the
GrAF representation of the file, and then retrieve the annotations.
"""

from api import *
from util import *

from PyGraphParser import *


__all__ = [
    'GRAF',
    'PyAnchor', 
    'PyAnnotation',
    'PyAnnotationObj',
    'PyAnnotationSet',
    'PyDocumentHeader',
    'PyEdge',
    'PyFeature',
    'PyFeatureStructure',
    'PyGrafRenderer',
    'PyGraph'
    'PyGraphParser',
    'PyIndentManager',
    'PyLink',
    'PyNode',
    'PyRegion',
    'PyStandoffHeader',
    'PyXML',]
