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
from xml.sax.saxutils import XMLGenerator

from graphs import Graph, Edge, Link, Node
from annotations import Annotation, FeatureStructure
from media import CharAnchor, Region

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
    ANNOTATION_SPACES = "annotationSpaces"
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


class TagWriter(object):
    """Allows a tag to be written using `with` syntax for nesting and `write()` when none is required"""
    __slots__ = ('handler', 'name', 'attribs', 'written')

    def __init__(self, handler, ns, tag, attribs):
        self.written = False
        self.handler = handler
        self.name = (ns, tag)
        self.attribs = self._clean_attribs(attribs, ns)

    @staticmethod
    def _clean_attribs(attribs, ns):
        if not attribs:
            return {}
        res = {}
        for k, v in attribs.items():
            if v is None:
                continue
            if isinstance(k, basestring):
                k = (ns, k)
            res[k] = v
        return res

    def __del__(self):
        if not self.written:
            import sys
            print >> sys.stderr, ('Warning: tag not written: %s' % (self.name,))

    def __enter__(self):
        self.handler.startElementNS(self.name, None, self.attribs)

    def __exit__(self, *args):
        self.written = True
        self.handler.endElementNS(self.name, None)

    def write(self, cdata=None):
        with self:
            if cdata is not None:
                self.handler.characters(cdata)
                 

class GrafRenderer(object):
    """
    Renders a GrAF XML representation that can be read back by an instance
    of L{GraphParser}.

    Version: 1.0.

    """

    def __init__(self, out, constants=Constants):
        """Create an instance of a GrafRenderer.

        """

        out = out if hasattr(out, 'write') else open(out, "w")
        # TODO: use a generator with indents and self-closing tags
        self._gen = XMLGenerator(out, 'utf-8')
        self._g = Constants

    def _tag(self, tag, attribs=None):
        return TagWriter(self._gen, self._g.NAMESPACE, tag, attribs)

    def render_node(self, n):
        """
        Used to render the node elements of the Graph.
        """
        tag = self._tag(self._g.NODE, {
            self._g.ID: n.id,
            self._g.ROOT: 'true' if n.is_root else None,
        })
        with tag:
            for link in n.links:
                self.render_link(link)

        for a in n.annotations:
            self.render_ann(a)

    def render_link(self, link):
        """
        Used to render the link elements of the Graph.
        """
        self._tag(self._g.LINK, {'targets': ' '.join(str(region.id) for region in link)})

    def render_region(self, region):
        """
        Used to render the region elements of the Graph.
        """
        self._tag(self._g.REGION, {
            self._g.ID: region.id,
            self._g.ANCHORS: ' '.join(str(a) for a in region.anchors)
        }).write()

    def render_edge(self, e):
        """
        Used to render the edge elements of the Graph.
        """
        with self._tag(self._g.EDGE, {self._g.FROM: e.from_node.id, self._g.TO: e.to_node.id}):
            for a in e.annotations:
                self.render_ann(a)

    def render_as(self, aSet):
        """
        Used to render the annotation set elements of the Graph.
        """
        with self._tag(self._g.ASET, {self._g.NAME: aSet.name}):
            for a in aSet:
                self.render_ann(a)

    def render_ann(self, a):
        """
        Used to render the annotation elements of the Graph.
        """
        tag = self._tag(self._g.ANNOTATION, {
            'label': a.label, 'ref': a.element.id,
            self._g.ASET: None if a.aspace is None else a.aspace.name
        })
        with tag:
            self.render_fs(a.features)

    def render_fs(self, fs):
        """
        Used to render the feature structure elements of the Graph.
        """
        if not fs:
            return
        with self._tag(self._g.FS, {self._g.TYPE: fs.type}):
            for name, value in fs.items():
                self.render_feature(name, value)

    def render_feature(self, name, value):
        """
        Used to render the features elements of the Graph.
        """
        if hasattr(value, 'items'):
            with self._tag(self._g.FEATURE, {self._g.NAME: name}):
                self.render_fs(value)
        else:
            self._tag(self._g.FEATURE, {self._g.NAME: name, self._g.VALUE: value}).write()

    def write_header(self, g):
        """
        Writes the header tag at the beginning of the XML file.
        """
        header = g.header
        with self._tag(self._g.HEADER):
            self.render_tag_usage(g)
            self.write_header_elements(header)

    def write_header_elements(self, header):
        """
        Helper method for write_header.
        """
        roots = header.roots
        if roots:
            with self._tag(self._g.ROOTS):
                for root in roots:
                    self._tag(self._g.ROOT).write()

        depends_on = header.depends_on
        if depends_on:
            with self._tag(self._g.ROOTS):
                for dependency in depends_on:
                    self._tag(self._g.DEPENDSON, {self._g.TYPE: dependency}).write()

        aspaces = header.annotation_spaces
        if aspaces:
            with self._tag(self._g.ANNOTATION_SPACES):
                for aspace in aspaces:
                    self._tag(self._g.ANNOTATION_SPACE, {self._g.NAME: aspace.name, self._g.TYPE: aspace.type}).write()


    def count_tag_usage(self, g):
        annotations = {}
        for node in g.nodes:
            for a in node.annotations:
                count = annotations.setdefault(a.label, 0)
                annotations[a.label] = count + 1
        return annotations

    def render_tag_usage(self, g):
        annotations = self.count_tag_usage(g)

        with self._tag(self._g.TAGSDECL):
            for k, v in annotations.iteritems():
                self._tag(self._g.TAGUSAGE, {self._g.GI: str(k), self._g.OCCURS: str(v)}).write()

    def render(self, g):
        self._gen.startDocument()
        self._gen.startPrefixMapping(None, self._g.NAMESPACE)
        with self._tag(self._g.GRAPH):
            self.write_header(g)

            # Add any features of the graph
            if g.features is not None:
                self.render_fs(g.features)

            # Render the regions
            for region in sorted(g.regions):
                self.render_region(region)

            # Render the nodes
            nodes = sorted(g.nodes)
            for node in nodes:
                self.render_node(node)

            # Render the edges
            for edge in g.edges:
                self.render_edge(edge)


class DocumentHeader(object):

    def __init__(self, path):
        self._basename = ""
        self._dir = ""
        self._annotationMap = {}
        self.set_basepath(path)

    def set_basepath(self, filename):
        if filename.endswith(".anc") or filename.endswith(".txt"):
            self._basename = filename[0:-4]
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


class GraphParser(ContentHandler):
    """
    Used to parse the GrAF XML representation and construct the instance 
    of C{Graph} objects.

    version: 1.0.

    """

    def __init__(self, constants=Constants, anchor_cls=CharAnchor):
        """Create a new C{GraphParser} instance.

        """

        self._anchor_cls = anchor_cls
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
            self._graph.add_edge(Edge(edge.id, from_node, to_node))
    
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
                region = self._graph.regions[target]
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
            self._current_node.is_root = True

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
        sets = self._graph.annotation_spaces
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
        sets = self._graph.annotation_spaces
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
            self._current_annotation.features= fs
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
                anchor = self._anchor_cls(t)
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
        # FIXME: is this logic correct?
        if self._f_stack:
            fs = self._fs_stack.pop()
            if self._f_stack:
                name, value = self._f_stack.pop()
                self._f_stack.append((name, fs))


    def feature_start(self, attrs):
        """ Used to parse start features elements in the XML representation.

        """

        name = attrs.getValue(self._g.NAME)

        # In the new MASC version the values aren't attributes
        # any more. So with this way the value is granted
        try:
            value = attrs.getValue(self._g.VALUE)
        except KeyError:
            value = attrs.getValueByQName(self._g.NAME)

        self._f_stack.append((name, value))

    def feature_end(self):
        """Used to parse end features elements in the XML representation.

        """

        key, value = self._f_stack.pop()
        try:
            fs = self._fs_stack[-1]
        except IndexError:
            raise SAXException("Unable to attach feature %r to a feature structure" % key)
        fs[key] = value
    
    def as_start(self, attrs):
        """ Used to parse start <as/ ...> elements in the XML representation.

        """

        type = attrs.getValue(self._g.TYPE)
        if type is None:
            raise SAXException("No type specified for as element.")
        else:
            self._current_annotation_set = self._graph.annotation_spaces[type]

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
            self._node_map[node.id] = node

        for edge in dependency.edges():
            id = edge.id
            from_id = edge.from_node.id
            to_id = edge.to_node.id
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
