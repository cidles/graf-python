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
import os
from xml.sax import make_parser, SAXException
from xml.sax.handler import ContentHandler

from graphs import Graph, Edge, Link, Node
from annotations import Annotation

class Constants(object):
    """
    A list of constants used in the GrafRenderer
    """
    __slots__ = ()
    VERSION = "1.0"
    NAMESPACE = "http://www.xces.org/ns/GrAF/" + VERSION + "/"
    EOL = "\n"
    DEFAULT = "DEFAULT"    	
    IMPLEMENTATION = "org.xces.graf.api.Implementation"
    DEFAULT_IMPLEMENTATION = "org.xces.graf.impl.DefaultImplementation"
    LANGUAGE = "org.xces.graf.lang"
    GRAPH = "graph"
    NODESET = "nodeSet"
    EDGESET = "edgeSet"
    NODE = "node"
    EDGE = "edge"
    ASET = "as"
    ANNOTATION = "a"
    FS = "fs"
    FEATURE = "f"
    REGION = "region"
    LINK = "link"
    HEADER = "header"
    DEPENDENCIES = "dependencies"
    PRIMARY_DATA = "primaryData"
    BASE_SEGMENTATION = "baseSegmentation"
    BASE_ANNOTATION = "baseAnnotation"
    DEPENDS_ON = "dependsOn"
    REFERENCED_BY = "referencedBy"
    EXTERNAL_DOCS = "externalDocumentation"
    ANNOTATION_DESC = "annotationDescription"
    TAGSDECL = "tagsDecl"
    TAGUSAGE = "tagUsage"
    ROOTS = "roots"
    ROOT = "root"
    MEDIA = "media"
    MEDIUM = "medium"
    ANCHOR_TYPES = "anchorTypes"
    ANCHOR_TYPE = "anchorType"
    ANNOTATION_SETS = "annotationSets"
    ANNOTATION_SET = "annotationSet"
    ANNOTATION_SPACE = "annotationSpace"
    NAME = "name"
    VALUE = "value"
    ID = "xml:id"
    TYPE = "type"
    TYPE_F_ID = "f.id"
    AS_ID = "as.id"
    START = "start"
    END = "end"
    FROM = "from"
    TO = "to"
    ROOT = "root"
    LABEL = "label"
    ANCHORS = "anchors"
    VERSION = "version"
    GI = "gi"
    OCCURS = "occurs"
    LOC = "loc"
    LAYER = "layer"
    REF = "ref"
    ASET = "as"
    TARGETS = "targets"
    MEDIA = "media"
    DEFAULT = "default"


class XML(object):

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


class IndentManager(object):
    def __init__(self):
        self._indent = "    "

    def __repr__(self):
        return self._indent

    def more(self):
        self._indent += "    "

    def less(self):
        self._indent = self._indent[0:len(self._indent)-4]


class DocumentHeader(object):

    def __init__(self, path):
        self._basename = ""
        self._dir = ""
        self._annotationMap = {}
        self.set_basepath(path)

    def set_basepath(self, filename):
        if filename.endswith(".anc") or filename.endswith(".txt"):
            self._basename = filename[0:len(filename)-4]
            return
        elif filename.endswith(".xml"):
            n = filename.rfind('-')
            if n > 0:
                self._basename = filename[0:n]
                return
        self._basename = filename

    def load(self, file):
        pass

    def get_location(self, type):
        if len(self._annotationMap) != 0:
            return self._annotationMap.get(type)
        if self._basename != None:
            return self._basename + '-' + type + ".xml"
        return None

                 
class GrafRenderer(object):
    """
    Renders a GrAF XML representation that can be read back by an instance
    of L{GraphParser}.

    Version: 1.0.

    """

    def __init__(self, out, constants=Constants):
        """Create an instance of a GrafRenderer.

        """

        self._xml = XML()
        self._indent = IndentManager()
        self._FILE = out if hasattr(out, 'write') else open(out, "w")
        self._g = Constants
        self._VERSION = self._g.VERSION
        self._UTF8 = "UTF-8"
        self._UTF16 = "UTF-16"
        self._encoding = self._UTF8

    def render_node(self, n):
        """Used to render the node elements of the Graph.

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
        """Used to render the link elements of the Graph.

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
        """Used to render the region elements of the Graph.

        """

        self._FILE.write(str(self._indent) + "<" + self._g.REGION + " " 
                + self._g.ID + "=\"" + region._id + "\" " 
                + self._g.ANCHORS + "=\"" + self.get_anchors(region)
                + "\"/>" + self._g.EOL)

    def render_edge(self, e):
        """Used to render the edge elements of the Graph.

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
        """Used to render the annotation set elements of the Graph.

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
        """Used to render the annotation elements of the Graph.

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
            self.render_fs(fs)
            self._indent.less()
            self._FILE.write(str(self._indent) + "</" 
                            + self._g.ANNOTATION + ">" + self._g.EOL)
        else:
            self._FILE.write("/>" + self._g.EOL)

    def render_fs(self, fs):
        """Used to render the feature structure elements of the Graph.

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
        """Used to render the features elements of the Graph.

        """

        name = f._name
        if f.is_atomic():
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

    def get_anchors(self, region):
        """Gathers the anchors from a region in the Graph,
        creates a string listing all of them, separated by spaces.

        """

        buffer = ""
        for a in region.get_anchors():
            buffer = buffer + " " + a.toString()
        return buffer[1:len(buffer)]

    def write_open_graph_element(self):
        """Writes the header of the XML file.

        """

        self._FILE.write("<?xml version=\"1.0\" encoding=\"" 
                        + self._encoding + "\"?>" + self._g.EOL)
        self._FILE.write(
            "<" + self._g.GRAPH + " xmlns=\"" + self._g.NAMESPACE + "\"")
        self._FILE.write( ">" + self._g.EOL)

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
        self.write_open_graph_element()

        self.write_header(g)

        # Add any features of the graph
        fs = g.get_features()
        if fs is not None:
            self.render_fs(fs)

        # Render the regions
        list = g.get_regions()
        list.sort()
        for region in list:
            self.render_region(region)

        # Render the nodes
        nodes = g.nodes()
        nodes = sorted(nodes, cmp = Node.compare_to)
        for node in nodes:
            self.render_node(node)

        # Render the edges
        for edge in g.edges():
            self.render_edge(edge)

        self._FILE.write( "</graph>" + self._g.EOL)


class Counter(object):
    def __init__(self):
        self._count = 0

    def __repr__(self):
        return str(self._count)

    def increment(self):
        self._count += 1


class GraphParser(ContentHandler):
    """
    Used to parse the GrAF XML representation and construct the instance 
    of C{Graph} objects.

    version: 1.0.

    """

    def __init__(self, constants=Constants):
        """Create a new C{GraphParser} instance.

        """

        self._parser = make_parser()
        self._parser.setContentHandler(self)
        self._g = Constants
        self._annotation_set_map = {}
        self._annotation_space_map = {} # Added AL
        self._buffer = ""
        self._current_annotation = None
        self._current_annotation_set = None
        self._current_fs = None
        self._current_node = None
        self._edge_annotations = [] # pairs?
        self._edges = []
        self._fs_stack = []
        self._f_stack = []
        self._graph = None
        self._header = None
        self._node_map = {}
        self._parent_dir = None ###
        self._parsed = [] 
        self._relations = []
        self._root_id = ""
        self._root_element = 0


    def parse(self, file, parsed = None):
        """Parses the XML file at the given path.

        :return: a Graph representing the annotated text in GrAF format
        :rtype: Graph

        """

        if parsed is None:
            parsed = []
        #print "parsing " + file
        delete_header = False
        if self._header is None:
            self._header = DocumentHeader(os.path.abspath(file))
            delete_header = True

        self._parsed = parsed
        FILE = open(file, 'r')
        self._parser.parse(FILE)
        result = self._graph

        self._graph = None

        if delete_header:
            self._header = None

        FILE.close()
        return result

    def startElement(self, name, attrs):
        """Processes the opening xml tags, according to their type.
        It's a method from ContentHandler class.

        """
        if name == self._g.GRAPH:
            self.graph_start(attrs)
        elif name == self._g.NODE:
            self.node_start(attrs)
        elif name == self._g.EDGE:
            self.edge_start(attrs)
        elif name == self._g.ANNOTATION:
            self.ann_start(attrs)
        elif name == self._g.ASET:
            self.as_start(attrs)
        elif name == self._g.REGION:
            self.region_start(attrs)
        elif name == self._g.LINK:
            self.link_start(attrs)
        elif name == self._g.DEPENDS_ON:
            self.depends_on_start(attrs)
        elif name == self._g.ANNOTATION_SET:
            self.annotation_set_start(attrs)
        elif name == self._g.ANNOTATION_SPACE:
            self.annotation_space_start(attrs)
        elif name == self._g.ROOT:
            self.root_start(attrs)

        elif name == self._g.FS:
            self.fs_start(attrs)
        elif name == self._g.FEATURE:
            self.feature_start(attrs)
        else:
            pass

    def characters(self, ch):
        """Processes any characters within the xml file.
        It's a method from ContentHandler class.

        """

        # Check for root node
        if self._root_element == 1:
            self._buffer += ch
    
    def endElement(self, name):
        """ Processes the end xml tags, according to their type.
        It's a method from ContentHandler class.

        """

        if name == self._g.GRAPH:
            self.graph_end()
        elif name == self._g.NODE:
            self.node_end()
        elif name == self._g.ANNOTATION:
            self.ann_end()
        elif name == self._g.ASET:
            self.as_end()
        elif name == self._g.EDGE:
            pass
        elif name == self._g.FS:
            self.fs_end()
        elif name == self._g.FEATURE:
            self.feature_end()
        elif name == self._g.ROOT:
            self.root_end()

    def graph_start(self, attrs):
        """Executes when the parser encounters the begin graph tag
        Initializes the data structures used to construct the graph.
        The element attributes are added to the new graph as features.

        """

        del self._edges[:]
        del self._fs_stack[:]
        self._node_map.clear()
        self._current_node = None
        self._root_id = None
        del self._relations[:]
        self._graph = Graph()
        n = attrs.getLength() - 1
        # Remove it when tested
        # This is never used with any of the MASC Versions
        # name = attrs.getQName(i)
        # Gives error to each version
        #for i in range(0, n):
        #    attrs.getQName(i)
        #    name = attrs.getQName(i)
        #    value = attrs.getValue(i)
        #    if self._g.ROOT == name:
        #        self._root_id = value
        #    elif self._g.VERSION != name:
        #        self._graph.add_feature(name, value)

    def graph_end(self):
        """Executes when the parser encounters the end graph tag.
        Sets the root node and adds all the edges to the graph.
        Neither of these tasks can be safely performed until all nodes
        have been added.

        """

        # Create and add the edges
        for edge in self._edges:
            from_node = self._node_map.get(edge._from)
            to_node = self._node_map.get(edge._to)
            self._graph.add_edge(Edge(edge._id, from_node, to_node))
    
        # Add annotations to any edges
        for s, a in self._edge_annotations:
            e = self._graph.find_edge(s)
            if e is None:
                raise SAXException("Could not find graph element with ID " 
                                + s)
            e.add_annotation(a)

        # Link nodes to regions
        for n, s in self._relations:
            link = Link()
            for target in s.split():
                region = self._graph.get_region_from_id(target)
                if region is not None:
                    link.add_target(region)
            n.add_link(link)

        if self._root_id is not None:
            root = self._graph.find_node(self._root_id)
            if root is None:
                raise SAXException("Root node with ID " + self._root_id 
                        + " was not found in the graph.")
            self._graph.set_root(root)


    def node_start(self, attrs):
        """ Used to parse the node start tag.
        Creates a new self._current_node, of type Node.

        """

        id = attrs.getValue(self._g.ID)
        isRoot = attrs.get(self._g.ROOT) ##?
        self._current_node = Node(id)

        if isRoot is not None and "true" is isRoot:
            self._current_node._annotationRoot = True

        self._node_map[id] = self._current_node

    def node_end(self):
        """ Adds the current_node to the graph being constructed and
        sets self._current_node to None.

        """

        self._graph.add_node(self._current_node)
        self._current_node = None


    def annotation_set_start(self, attrs):
        """ Used to parse <annotationSet .../> elements in the XML
        representation.

        """

        name = attrs.getValue(self._g.NAME)
        type = attrs.getValue(self._g.TYPE)
        sets = self._graph.get_annotation_sets()
        for set in sets:
            if set._name == name:
                if set._type != type:
                    raise SAXException("Annotation set type mismatch for " 
                            				+ name)
                self._annotation_set_map[name] = set
                return
        a_set = self._graph.add_as_create(name, type)
        self._annotation_set_map[name] = a_set

    # Added AL
    def annotation_space_start(self, attrs):
        """ Used to parse <annotationSpace .../> elements in the XML
        representation.

        """

        as_id = attrs.getValue(self._g.AS_ID)
        sets = self._graph.get_annotation_sets()
        for set in sets:
            if set._as_id == as_id:
                if set._type != type:
                    raise SAXException("Annotation set type mismatch for "
                    + as_id)
                self._annotation_space_map[as_id] = set
                return
        a_set = self._graph.add_aspace_create(as_id)
        self._annotation_space_map[as_id] = a_set

    def ann_start(self, attrs):
        label = attrs.getValue(self._g.LABEL)
        self._current_annotation = Annotation(label)

        if label is None:
            SAXException("Required attribute " + self._g.LABEL + 
                    " missing on annotation")

        node_id = attrs.getValue(self._g.REF)
        if node_id is None:
            raise SAXException("Annotation is not associate with a node")
        set_name = attrs.get(self._g.ASET)
        if set_name is not None:
            a_set = self._annotation_set_map.get(set_name)
            if a_set is None:
                a_set = self._annotation_space_map.get(set_name)
            elif a_set is None:
                raise SAXException("Unknown annotation set name "
                + set_name)
            self._current_annotation._set = a_set
            a_set.add_annotation(self._current_annotation)

        if self._current_annotation_set is not None:
            self._current_annotation_set.add_annotation(
                                                self._current_annotation)
            self._current_annotation.setAnnotationSet(
                                                self.current_annotation_set)

        node = self._node_map.get(node_id)
        if node is None:
            # Assume it belongs to an edge
            self._edge_annotations.append((node_id, 
                                    self._current_annotation))
        else:
            node.add_annotation(self._current_annotation)

    def ann_end(self):
        if len(self._fs_stack) != 0:
            fs = self._fs_stack.pop()
            self._current_annotation._features= fs
        self._current_annotation = None

    def edge_start(self, attrs):
        """Used to parse edge elements in the XML representation.
        Edge information is stored and the edges are added after
        all nodes/spans have been parsed.

        """

        from_id = attrs.getValue(self._g.FROM)
        to_id = attrs.getValue(self._g.TO)
        id = attrs.getValue(self._g.ID)
        self._edges.append(EdgeInfo(id, from_id, to_id))

    def region_start(self, attrs):
        """Used to pare the region elements in the XML representation.
        A tolkenizer is used to separate the anchors listed in the XML tag,
        and a new Anchor instance is created for each one.
        A Region instance is then created with the id from the
        XML tag and added to the graph.

        """

        id = attrs.getValue(self._g.ID)
        att = attrs.getValue(self._g.ANCHORS)
        tokenizer = att.split()
        if len(tokenizer) < 2:
            raise SAXException("Invalid number of anchors for the regions")
        anchors = []
        for t in tokenizer:
            anchor = None
            try:
                anchor = Anchor(t)
            except:
                raise SAXException("Unable to create an anchor for " + t)

            anchors.append(anchor)

        try:
            region = Region(id, anchors)
            self._graph.add_region(region)
        except:
            raise SAXException("Could not add the region to the graph")

    def fs_start(self, attrs):
        """ Used to parse <fs> elements in the XML representation.

        """

        type = attrs.get(self._g.TYPE)
        fs = FeatureStructure(type)
        self._fs_stack.append(fs)

    def fs_end(self):
        """Used to parse </fs> elements in the XML representation.

        """

        if len(self._f_stack) != 0:
            fs = self._fs_stack.pop()
            if len(self._f_stack) -1 >= 0:
                f = self._f_stack[len(self._f_stack)-1]
                f.set_value(fs)


    def feature_start(self, attrs):
        """ Used to parse start features elements in the XML representation.

        """

        name = attrs.getValue(self._g.NAME)

        # In the new MASC version the values aren't attributes
        # any more. So with this way the value is granted
        try:
            value = attrs.getValue(self._g.VALUE)
        except KeyError as inst:
            value = attrs.getValueByQName(self._g.NAME)

        f = Feature(name)

        if value is not None:
            f.set_value(value)

        self._f_stack.append(f)

    def feature_end(self):
        """Used to parse end features elements in the XML representation.

        """

        f = self._f_stack.pop()
        n = len(self._fs_stack)-1
        if n < 0:
            fs = None
        else:
            fs = self._fs_stack[len(self._fs_stack)-1]
        if fs is None:
            SAXException("Unable to attach feature to a feature structure:" 
                        + " " + f.getName())
        fs.add_feature(f)

    
    def as_start(self, attrs):
        """ Used to parse start <as/ ...> elements in the XML representation.

        """

        type = attrs.getValue(self._g.TYPE)
        if type is None:
            raise SAXException("No type specified for as element.")
        else:
            self._current_annotation_set = self._graph.get_annotation_set(
                                                                    type)

    def as_end(self):
        """ Used to parse end /as> elements in the XML representation.

        """

        self._current_annotation_set = None

    def link_start(self, attrs):
        """Used to parse link elements in the XML representation.

        """

        links = attrs.getValue(self._g.TARGETS)
        self._relations.append((self._current_node, links))

    def depends_on_start(self, attrs):
        """Used to parse dependsOn elements in the XML representation.
        Finds other XML annotation files on which depend the current
        XML file. Parses the dependency files and adds the resulting graph
        to the current graph.

        """

        # In MASC version 1 in the graph header on
        # <dependencies>
        #   <dependsOn type="seg"/>
        # </dependencies>
        # Now in MASC version 3 the depencies here
        # changed to
        # <dependsOn f.id="seg"/>

        try:
            type = attrs.getValue(self._g.TYPE)
        except Exception as inst:
            try:
                type = attrs.getValue(self._g.TYPE_F_ID)
            except Exception as inst:
                print(inst)

        if type is None:
            raise SAXException("No annotation type defined")

        if type in self._parsed:
            return

        self._parsed.append(type)


        path = self._header.get_location(type)
        if path is None:
            raise SAXException("Unable to get path for dependency of type"
                                 + " " + type)

        parser = GraphParser()
        dependency = parser.parse(path, self._parsed)

        for a_set in dependency.annotation_sets():
            self._graph.add_annotation_set(a_set)

        for node in dependency.nodes():
            self._graph.add_node(node)
            self._node_map[node._id] = node

        for edge in dependency.edges():
            id = edge._id
            from_id = edge.getFrom()._id
            to_id = edge.getTo()._id
            e = self._graph.add_edgeToFromID(id, from_id, to_id)
            for a in edge.annotations():
                e.add_annotation(Annotation.from_annotation(a))

        for region in dependency.regions():
            self._graph.add_region(region)


    def root_start(self, attrs):
        """Used to parse start root elements in the XML representation.
        The root characters are processed by the characters() method and
        stored in self._buffer.

        self._root_element is a flag indicating the presence of a root.

        """

        self._buffer = ""
        self._root_element = 1

    def root_end(self):
        """Used to parse end root elements in the XML representation.

        """

        self._root_id = self._buffer
        self._buffer = ""
        self._root_element = 0


class EdgeInfo(object):
    """
    Used to store information about edges when parsing the GrAF XML
    representation.

    """

    def __init__(self, id = "", fromID = "", toID = ""):
        self._id = id
        self._from = fromID
        self._to = toID
