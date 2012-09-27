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
import codecs

import sys

from graf.PyGraph import *
from graf.PyXML import *
from graf.PyIndentManager import *
from graf.GRAF import *

class PyGrafRenderer:
    """
    Renders a GrAF XML representation that can be read back by an instance
    of L{PyGraphParser}.

    Version: 1.0.

    """

    def __init__(self, filename):
        """Create an instance of a PyGrafRenderer.

        """

        self._xml = PyXML()
        self._indent = PyIndentManager()
        self._FILE = open(filename, "w")
        self._g = GRAF()
        self._VERSION = self._g.VERSION
        self._UTF8 = "UTF-8"
        self._UTF16 = "UTF-16"
        self._encoding = self._UTF8

    def render_node(self, n):
        """Used to render the node elements of the PyGraph.

        """

        self._FILE.write(str(self._indent) + "<" + self._g.NODE + " ")
        self._FILE.write(self._g.ID + "=\"" + n._id + "\"")
        if n._annotationRoot:
            self._FILE.write(" " + self._g.ROOT + "=\"true\"")
        if len(n._links) > 0:
            self._FILE.write( ">" + self._g.EOL)
            self._indent.more()
            for link in n._links:
                self.render_link(link)
            self._indent.less()
            self._FILE.write(str(self._indent) + 
                        "</" + self._g.NODE + ">" + self._g.EOL)
        else:
            self._FILE.write( "/>" + self._g.EOL)

        for a in n._annotations:
            self.render_ann(a)

    def render_link(self, link):
        """Used to render the link elements of the PyGraph.

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

    def render_region(self, region):
        """Used to render the region elements of the PyGraph.

        """

        self._FILE.write(str(self._indent) + "<" + self._g.REGION + " " 
                + self._g.ID + "=\"" + region._id + "\" " 
                + self._g.ANCHORS + "=\"" + self.get_anchors(region)
                + "\"/>" + self._g.EOL)

    def render_edge(self, e):
        """Used to render the edge elements of the PyGraph.

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
                self.render_ann(a)
            self._indent.less()
            self._FILE.write(str(self._indent) + "</" + self._g.EDGE + ">" 
                                     + self._g.EOL)
        else:
            self._FILE.write("/>" + self._g.EOL)

    def render_as(self, aSet):
        """Used to render the annotation set elements of the PyGraph.

        """

        atts = ""
        self.add_attribute(atts, self._g.NAME, aSet.getName())

        self.FILE.write(str(self._indent) + "<" + self._g.ASET 
                        + atts + ">" + self._g.EOL)
        self._indent.more()
        for a in aSet.annotations():
            self.render_ann(a)
        self._indent.less()
        self.FILE.write(str(self._indent) + "</" + self._g.ASET 
                        + ">" + self._g.EOL)

    def render_ann(self, a):
        """Used to render the annotation elements of the PyGraph.

        """

        label = self._xml.encode(a._label)
        self._FILE.write(str(self._indent) + "<" + self._g.ANNOTATION 
                        + " " 
                        + self._xml.attribute("label", label) + " " 
                        + self._xml.attribute("ref", a._element._id))
        set = a._set
        if set is not None:
            try:
                self._FILE.write(" " +
                        self._xml.attribute(self._g.ASET, set._name))
            except :
                self._FILE.write(" " +
                        self._xml.attribute(self._g.ASET, 'graf'))
        
        fs = a._features
        if fs.size() > 0:
            self._FILE.write( ">" + self._g.EOL)
            self._indent.more()
            self.render_fs(fs)
            self._indent.less()
            self._FILE.write(str(self._indent) + "</" 
                            + self._g.ANNOTATION + ">" + self._g.EOL)
        else:
            self._FILE.write("/>" + self._g.EOL)

    def render_fs(self, fs):
        """Used to render the feature structure elements of the PyGraph.

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
            self.render_feature(f)
        self._indent.less()

        self._FILE.write(str(self._indent) + "</" + self._g.FS + ">" 
                            + self._g.EOL)


    def render_feature(self, f):
        """Used to render the features elements of the PyGraph.

        """

        name = f._name
        if f.is_atomic():
            value = f._stringValue
            entry = str(self._indent) + '<' + self._g.FEATURE \
                   + str(' ') + self._g.NAME + '="' + str(name) \
                   + '">' + str(value) + '</'+ self._g.FEATURE \
                   + '>' + self._g.EOL
            self._FILE.write(entry)
        else:
            value = f.getFSValue()
            entry = str(self._indent) + '<' + self._g.FEATURE\
                    + str(' ') + self._g.NAME + '="' + str(name)\
                    + '">' + str(value) + '</'+ self._g.FEATURE\
                    + '>' + self._g.EOL
            self._FILE.write(entry)
            self._indent.more()
            renderFS(value)
            self._indent.less()
            self._FILE.write(str(self._indent) + '</' + self._g.FEATURE
                            + '>' + self._g.EOL)

    def get_anchors(self, region):
        """Gathers the anchors from a region in the PyGraph,
        creates a string listing all of them, separated by spaces.

        """

        buffer = ""
        for a in region.get_anchors():
            buffer = buffer + " " + str(a)
        return buffer[1:len(buffer)]

    def write_open_graph_element(self):
        """Writes the header of the XML file.

        """

        self._FILE.write('<?xml version="1.0" encoding="'
                        + self._encoding + '"?>' + self._g.EOL)
        self._FILE.write(
            '<' + self._g.GRAPH + ' xmlns="' + self._g.NAMESPACE + '"')
        self._FILE.write( '>' + self._g.EOL)

    def add_attribute(self, b, type, value):
        """Adds an attribute to an XML element.

        """

        if value is None:
            return
        b.append(" ")
        b.append(type)
        b.append("=\"")
        b.append(value)
        b.append("\"")

    def write_header(self, g):
        """Writes the header tag at the beginning of the XML file.

        """

        header = g.get_header()
        self._FILE.write(str(self._indent) + "<" + self._g.HEADER 
                        + ">" + self._g.EOL)
        self._indent.more()
        self.render_tag_usage(g)
        self.write_xml(header)
        self._indent.less()
        self._FILE.write(str(self._indent) + "</" + self._g.HEADER 
                        + ">" + self._g.EOL)

    def write_xml(self, header):
        """Helper method for write_header.

        """

        roots = header.get_roots()
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

        dependsOn = header.get_depends_on()
        if len(dependsOn) > 0:
            self._FILE.write(str(self._indent) + "<" 
                            + self._g.DEPENDENCIES + ">" + self._g.EOL)
            self._indent.more()
            self.elements(self._FILE, self._indent, self._g.DEPENDSON, 
                            dependsOn)
            self._indent.less()
            self._FILE.write(str(self._indent) + "</" 
                            + self._g.DEPENDENCIES + ">" + self._g.EOL)

        annotationSets = header.get_annotation_sets()
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
                print(aSet._name)
                print(str(aSet._type))
                self._FILE.write(self._xml.attribute(self._g.TYPE, 
                                     str(aSet._type)))
                self._FILE.write( "/>" + self._g.EOL)
            self._indent.less()
            self._FILE.write(str(self._indent) + "</" 
                    + self._g.ANNOTATION_SETS + ">" + self._g.EOL)


    def elements(self, file, indent, name, uris):
        """Creates XML tags for elements in uris.

        """

        if uris is None:
            return
        for uri in uris:
            self.element(file, indent, name, uri)

    def element(self, file, indent, name, loc):
        """Helper method for elements(), creates an XML tag for an element.

        """

        if loc is None:
            return
        file.write(str(indent) + "<" + name + " " + self._g.TYPE + "=\"" 
                    + loc + "\"/>" + self._g.EOL)

    def count_tag_usage(self, g):
        annotations = {}
        for node in g.nodes():
            for a in node._annotations:
                counter = annotations.get(a._label)
                if counter is None:
                    counter = Counter()
                    annotations[a._label] = counter
                counter.increment()
        return annotations

    def render_tag_usage(self, g):
        annotations = self.count_tag_usage(g)

        self._FILE.write(str(self._indent) + "<" + self._g.TAGSDECL + ">" 
                        + self._g.EOL)
        self._indent.more()
        for k, v in annotations.items():
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
        self.write_open_graph_element()

        self.write_header(g)

        # Add any features of the graph
        fs = g.get_features()
        if fs is not None:
            self.render_fs(fs)

        # Render the regions
        list = g.get_regions()

        if sys.version_info < (3, 0):
            list.sort()

        for region in list:
            self.render_region(region)

        # Render the nodes
        nodes = g.nodes()

        if sys.version_info < (3, 0):
            nodes = sorted(nodes, cmp = PyNode.compare_to)

        for node in nodes:
            self.render_node(node)

        # Render the edges
        for edge in g.edges():
            self.render_edge(edge)

        self._FILE.write( "</graph>" + self._g.EOL)


class Counter:
    def __init__(self):
        self._count = 0

    def __repr__(self):
        return str(self._count)

    def increment(self):
        self._count += 1