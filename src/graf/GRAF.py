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

class GRAF:
    """
    A list of constants used in the GrafRenderer
    """
    def __init__(self):
        self.VERSION = "1.0"
        self.NAMESPACE = "http://www.xces.org/ns/GrAF/" + self.VERSION + "/"
        self.EOL = "\n"
        self.DEFAULT = "DEFAULT"    	
        self.IMPLEMENTATION = "org.xces.graf.api.Implementation"
        self.DEFAULT_IMPLEMENTATION = ("org.xces.graf.impl." + 
                                        "DefaultImplementation")
        self.LANGUAGE = "org.xces.graf.lang"
        self.GRAPH = "graph"
        self.NODESET = "nodeSet"
        self.EDGESET = "edgeSet"
        self.NODE = "node"
        self.EDGE = "edge"
        self.ASET = "as"
        self.ANNOTATION = "a"
        self.FS = "fs"
        self.FEATURE = "f"
        self.REGION = "region"
        self.LINK = "link"
        self.HEADER = "header"
        self.DEPENDENCIES = "dependencies"
        self.PRIMARY_DATA = "primaryData"
        self.BASE_SEGMENTATION = "baseSegmentation"
        self.BASE_ANNOTATION = "baseAnnotation"
        self.DEPENDS_ON = "dependsOn"
        self.REFERENCED_BY = "referencedBy"
        self.EXTERNAL_DOCS = "externalDocumentation"
        self.ANNOTATION_DESC = "annotationDescription"
        self.TAGSDECL = "tagsDecl"
        self.TAGUSAGE = "tagUsage"
        self.ROOTS = "roots"
        self.ROOT = "root"
        self.MEDIA = "media"
        self.MEDIUM = "medium"
        self.ANCHOR_TYPES = "anchorTypes"
        self.ANCHOR_TYPE = "anchorType"
        self.ANNOTATION_SETS = "annotationSets"
        self.ANNOTATION_SET = "annotationSet"
        self.ANNOTATION_SPACE = "annotationSpace"
        self.NAME = "name"
        self.VALUE = "value"
        self.ID = "xml:id"
        self.TYPE = "type"
        self.TYPE_F_ID = "f.id"
        self.AS_ID = "as.id"
        self.START = "start"
        self.END = "end"
        self.FROM = "from"
        self.TO = "to"
        self.ROOT = "root"
        self.LABEL = "label"
        self.ANCHORS = "anchors"
        self.VERSION = "version"
        self.GI = "gi"
        self.OCCURS = "occurs"
        self.LOC = "loc"
        self.LAYER = "layer"
        self.REF = "ref"
        self.ASET = "as"
        self.TARGETS = "targets"
        self.MEDIA = "media"
        self.DEFAULT = "default"