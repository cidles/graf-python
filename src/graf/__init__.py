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

"""
The GrAF API is used by the ISO GrAF corpus reader (masc.py)
to parse the MASC Corpus.  Each text file in the corpus is accompanied
by a series of xml files that store annotation information for that
text file.  So, to parse the annotations we must first construct the
GrAF representation of the file, and then retrieve the annotations.
"""

from graf.media import Region
from graf.annotations import Annotation, AnnotationSpace, FeatureStructure
from graf.graphs import Edge, Graph, Node, Link, StandoffHeader
from graf.io import GraphParser, GrafRenderer
from graf.util import *


__all__ = [
    'Annotation',
    'AnnotationSpace',
    'Edge',
    'FeatureStructure',
    'GrafRenderer',
    'Graph'
    'GraphParser',
    'Link',
    'Node',
    'Region',
    'StandoffHeader',
]
