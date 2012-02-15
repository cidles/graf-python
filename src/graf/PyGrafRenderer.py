# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

import sys

from PyGraph import *
from PyXML import *
from PyIndentManager import *
from GRAF import *

"""
Renders a GrAF XML representation that can be read back by an instance 
of L{PyGraphParser}
version: 1.0
"""

class PyGrafRenderer:
    def __init__(self, filename):
        """
        Create an instance of a PyGrafRenderer
        """
        self._xml = PyXML()
        self._indent = PyIndentManager()
        self._FILE = open(filename, "w")
        self._g = GRAF()
        self._VERSION = self._g.VERSION
        self._UTF8 = "UTF-8"
        self._UTF16 = "UTF-16"
        self._encoding = self._UTF8

    def renderNode(self, n):
        """
        Used to render the node elements of the PyGraph
        """
        self._FILE.write(str(self._indent) + "<" + self._g.NODE + " ")
        self._FILE.write(self._g.ID + "=\"" + n._id + "\"")
        if n._annotationRoot:
            self._FILE.write(" " + self._g.ROOT + "=\"true\"")
        if len(n._links) > 0:
            self._FILE.write( ">" + self._g.EOL)
            self._indent.more()
            for link in n._links:
                self.renderLink(link)
            self._indent.less()
            self._FILE.write(str(self._indent) + 
                        "</" + self._g.NODE + ">" + self._g.EOL)
        else:
            self._FILE.write( "/>" + self._g.EOL)

        for a in n._annotations:
            self.renderAnn(a)

    def renderLink(self, link):
        """
        Used to render the link elements of the PyGraph
        """
        targets = ""
        if len(link._regions) == 0:
            return
        for link in link._regions:
            targets = targets + " " + link._id
        targets = targets[1:len(targets)]
        self._FILE.write(str(self._indent) + "<" + self._g.LINK + " " 
                + self._xml.attribute("targets", targets) + "/>" + 
                self._g.EOL)

    def renderRegion(self, region):
        """
        Used to render the region elements of the PyGraph
        """
        self._FILE.write(str(self._indent) + "<" + self._g.REGION + " " 
                + self._g.ID + "=\"" + region._id + "\" " 
                + self._g.ANCHORS + "=\"" + self.getAnchors(region)
                + "\"/>" + self._g.EOL)

    def renderEdge(self, e):
        """
        Used to render the edge elements of the PyGraph
        """
        self._FILE.write(str(self._indent) + "<" + self._g.EDGE + " " 
                + self._g.ID 
                + "=\"" + e._id + "\" " + self._g.FROM + "=\"" 
                + e._fromNode._id + "\" " + self._g.TO + "=\"" 
                + e._toNode._id + "\"")

        if e.annotated():
            self._FILE.write(">" + self._g.EOL)
            self._indent.more()
            for a in e.annotations():
                self.renderAnn(a)
            self._indent.less()
            self._FILE.write(str(self._indent) + "</" + self._g.EDGE + ">" 
                                     + self._g.EOL)
        else:
            self._FILE.write("/>" + self._g.EOL)

    def renderAS(self, aSet):
        """
        Used to render the annotation set elements of the PyGraph
        """
        atts = ""
        self.addAttribute(atts, self._g.NAME, aSet.getName())

        self.FILE.write(str(self._indent) + "<" + self._g.ASET 
                        + atts + ">" + self._g.EOL)
        self._indent.more()
        for a in aSet.annotations():
            self.renderAnn(a)
        self._indent.less()
        self.FILE.write(str(self._indent) + "</" + self._g.ASET 
                        + ">" + self._g.EOL)

    def renderAnn(self, a):
        """
        Used to render the annotation elements of the PyGraph
        """
        label = self._xml.encode(a._label)
        self._FILE.write(str(self._indent) + "<" + self._g.ANNOTATION 
                        + " " 
                        + self._xml.attribute("label", label) + " " 
                        + self._xml.attribute("ref", a._element._id))
        set = a._set
        if set is not None:
            self._FILE.write(" " + 
                    self._xml.attribute(self._g.ASET, set._name))
        
        fs = a._features
        if fs.size() > 0:
            self._FILE.write( ">" + self._g.EOL)
            self._indent.more()
            self.renderFS(fs)
            self._indent.less()
            self._FILE.write(str(self._indent) + "</" 
                            + self._g.ANNOTATION + ">" + self._g.EOL)
        else:
            self._FILE.write("/>" + self._g.EOL)

    def renderFS(self, fs):
        """
        Used to render the feature structure elements of the PyGraph.
        """
        if fs.size() == 0:
            return
        type = fs._type #
        self._FILE.write(str(self._indent) + "<" + self._g.FS)
        if type is not None:
            self._FILE.write(" " + self._g.TYPE + "=\"" + type + "\">")
        self._FILE.write( ">" + self._g.EOL)
        self._indent.more()
        for f in fs.features():
            self.renderFeature(f)
        self._indent.less()

        self._FILE.write(str(self._indent) + "</" + self._g.FS + ">" 
                            + self._g.EOL)


    def renderFeature(self, f):
        """
        Used to render the features elements of the PyGraph
        """
        name = f._name
        if f.isAtomic():
            value = f._stringValue
            self._FILE.write(str(self._indent) + "<" + self._g.FEATURE 
                    + " " 
                    + self._g.NAME + "=\"" + name + "\" " 
                    + self._g.VALUE + "=\"" + self._xml.encode(value) 
                    + "\"/>" + self._g.EOL)
        else:
            value = f.getFSValue()
            self._FILE.write(str(self._indent) + "<" + self._g.FEATURE 
                            + " " 
                            + self._g.NAME + "=\"" + name + "\">" 
                            + self._g.EOL)
            self._indent.more()
            renderFS(value)
            self._indent.less()
            self._FILE.write(str(self._indent) + "</" + self._g.FEATURE 
                            + ">" + self._g.EOL)

    def getAnchors(self, region):
        """
        Gathers the anchors from a region in the PyGraph, 
        creates a string listing
        all of them, separated by spaces
        """
        buffer = ""
        for a in region.getAnchors():
            buffer = buffer + " " + a.toString()
        return buffer[1:len(buffer)]

    def writeOpenGraphElement(self):
        """
        Writes the header of the XML file
        """
        self._FILE.write("<?xml version=\"1.0\" encoding=\"" 
                        + self._encoding + "\"?>" + self._g.EOL)
        self._FILE.write(
            "<" + self._g.GRAPH + " xmlns=\"" + self._g.NAMESPACE + "\"")
        self._FILE.write( ">" + self._g.EOL)

    def addAttribute(self, b, type, value):
        """
        Adds an attribute to an XML element
        """
        if value is None:
            return
        b.append(" ")
        b.append(type)
        b.append("=\"")
        b.append(value)
        b.append("\"")

    def writeHeader(self, g):
        """
        Writes the header tag at the beginning of the XML file
        """
        header = g.getHeader()
        self._FILE.write(str(self._indent) + "<" + self._g.HEADER 
                        + ">" + self._g.EOL)
        self._indent.more()
        self.renderTagUsage(g)
        self.writeXML(header)
        self._indent.less()
        self._FILE.write(str(self._indent) + "</" + self._g.HEADER 
                        + ">" + self._g.EOL)

    def writeXML(self, header):
        """
        Helper method for writeHeader
        """
        roots = header.getRoots()
        if len(roots) > 0:
            self._FILE.write(str(self._indent) + "<" + self._g.ROOTS + ">" 
                                     + self._g.EOL)
            self._indent.more()
            for root in roots:
                self._FILE.write(str(self._indent) + "<" + self._g.ROOT 
                                + ">")
                self._FILE.write(root)
                self._FILE.write( "</" + self._g.ROOT + ">" + self._g.EOL)
            self._indent.less()
            self._FILE.write(str(self._indent) + "</" + self._g.ROOTS 
                            + ">" + self._g.EOL)

        dependsOn = header.getDependsOn()
        if len(dependsOn) > 0:
            self._FILE.write(str(self._indent) + "<" 
                            + self._g.DEPENDENCIES + ">" + self._g.EOL)
            self._indent.more()
            self.elements(self._FILE, self._indent, self._g.DEPENDSON, 
                            dependsOn)
            self._indent.less()
            self._FILE.write(str(self._indent) + "</" 
                            + self._g.DEPENDENCIES + ">" + self._g.EOL)

        annotationSets = header.getAnnotationSets()
        if len(annotationSets) > 0:
            self._FILE.write(str(self._indent) + "<" 
                    + self._g.ANNOTATION_SETS + ">" + self._g.EOL)
            self._indent.more()
            for aSet in annotationSets:
                self._FILE.write(str(self._indent) + "<" 
                                + self._g.ANNOTATION_SET + " ")
                self._FILE.write(self._xml.attribute(self._g.NAME, 
                                aSet._name))
                self._FILE.write(" ")
                print aSet._name
                print str(aSet._type)
                self._FILE.write(self._xml.attribute(self._g.TYPE, 
                                     str(aSet._type)))
                self._FILE.write( "/>" + self._g.EOL)
            self._indent.less()
            self._FILE.write(str(self._indent) + "</" 
                    + self._g.ANNOTATION_SETS + ">" + self._g.EOL)


    def elements(self, file, indent, name, uris):
        """
        Creates XML tags for elements in uris
        """
        if uris is None:
            return
        for uri in uris:
            self.element(file, indent, name, uri)

    def element(self, file, indent, name, loc):
        """
        Helper method for elements(), creates an XML tag for an element
        """
        if loc is None:
            return
        file.write(str(indent) + "<" + name + " " + self._g.TYPE + "=\"" 
                    + loc + "\"/>" + self._g.EOL)

    def countTagUsage(self, g):
        annotations = {}
        for node in g.nodes():
            for a in node._annotations:
                counter = annotations.get(a._label)
                if counter is None:
                    counter = Counter()
                    annotations[a._label] = counter
                counter.increment()
        return annotations

    def renderTagUsage(self, g):
        annotations = self.countTagUsage(g)

        self._FILE.write(str(self._indent) + "<" + self._g.TAGSDECL + ">" 
                        + self._g.EOL)
        self._indent.more()
        for k, v in annotations.iteritems():
            self._FILE.write(str(self._indent) + "<" 
                            + self._g.TAGUSAGE + " " 
                            + self._g.GI + "=\"" + str(k) + "\" " 
                            + self._g.OCCURS + "=\"" + str(v) + "\"/>" 
                            + self._g.EOL)
        self._indent.less()
        self._FILE.write(str(self._indent) + "</" + self._g.TAGSDECL 
                        + ">" + self._g.EOL)

    def close(self):
        self._FILE.close()

    def render(self, g):
        self.writeOpenGraphElement()

        self.writeHeader(g)

        """ add any features of the graph """
        fs = g.getFeatures()
        if fs is not None:
            self.renderFS(fs)

        """ render the regions """
        list = g.getRegions()
        list.sort()
        for region in list:
            self.renderRegion(region)

        """ render the nodes """
        nodes = g.nodes()
        nodes = sorted(nodes, cmp = PyNode.compareTo)
        for node in nodes:
            self.renderNode(node)

        """ render the edges """
        for edge in g.edges():
            self.renderEdge(edge)

        self._FILE.write( "</graph>" + self._g.EOL)


class Counter:
    def __init__(self):
        self._count = 0

    def __repr__(self):
        return str(self._count)

    def increment(self):
        self._count += 1
    
