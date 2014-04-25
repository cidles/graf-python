# graf-python: Python GrAF API
#
# Copyright (C) 2014 American National Corpus
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.anc.org/>
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
from graf.graphs import Edge, Graph, Node, Link, GraphHeader, StandoffHeader, \
    FileDesc, ProfileDesc, DataDesc, RevisonDesc
from graf.io import GraphParser, GrafRenderer, StandoffHeaderRenderer
from graf.util import *

__all__ = [
    'Annotation',
    'AnnotationSpace',
    'Edge',
    'FeatureStructure',
    'GrafRenderer',
    'Graph'
    'GraphParser',
    'GraphHeader',
    'Link',
    'Node',
    'Region',
    'StandoffHeader',
    'FileDesc',
    'ProfileDesc',
    'DataDesc',
    'RevisonDesc',
    'StandoffHeaderRenderer',
]
