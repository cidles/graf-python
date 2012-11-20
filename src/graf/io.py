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
from xml.dom import minidom

from graphs import Graph, Link
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
    HEADER = "graphHeader"
    DEPENDENCIES = "dependencies"
    PRIMARY_DATA = "primaryData"
    BASE_SEGMENTATION = "baseSegmentation"
    BASE_ANNOTATION = "baseAnnotation"
    DEPENDS_ON = "dependsOn"
    REFERENCED_BY = "referencedBy"
    EXTERNAL_DOCS = "externalDocumentation"
    ANNOTATION_DESC = "annotationDescription"
    TAGSDECL = "labelsDecl"
    TAGUSAGE = "labelUsage"
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
        # TODO: use a generator with indents
        try:
            # For Python >= 3.2
            self._gen = XMLGenerator(out, 'utf-8', short_empty_elements=True)
        except TypeError:
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
        self._tag(self._g.LINK, {'targets': ' '.join(str(region.id) for region in link)}).write()

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
            self.write_header_elements(graph, header)

    def write_header_elements(self, graph, header):
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

        aspaces = graph.annotation_spaces
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
            for k, v in annotations.items():
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


class SAXHandler(ContentHandler):
    ERR_MODE_RAISE = 'error'
    ERR_MODE_IGNORE = 'ignore'

    def __init__(self, handler_map, error_mode=ERR_MODE_RAISE):
        self._tag_stack = []
        self._start_handlers = {}
        self._end_handlers = {}
        self._char_handlers = {}
        for tag, fns in handler_map.items():
            if fns is None:
                fns = (None, None, None)
            elif callable(fns):
                fns = (fns, None, None)
            elif len(fns) == 2:
                fns = (fns[0], fns[1], None)
            fns = [self._ignore if fn is None else fn for fn in fns]
            start, end, char = fns

            self._start_handlers[tag] = start
            self._end_handlers[tag] = end
            self._char_handlers[tag] = char

        self._error_mode = error_mode

    @staticmethod
    def _ignore(*args, **kwargs):
        pass

    def startElement(self, name, attrs):
        try:
            fn = self._start_handlers[name]
        except KeyError:
            if self._error_mode == self.ERR_MODE_IGNORE:
                fn = self._ignore
            else:
                raise SAXException('No start handler for tag {0!r}'.format(name))  # FIXME: better exception
        self._tag_stack.append(name)
        fn(attrs)

    def endElement(self, name):
        try:
            fn = self._end_handlers[name]
        except KeyError:
            if self._error_mode == self.ERR_MODE_IGNORE:
                fn = self._ignore
            else:
                raise SAXException('No end handler for tag {0!r}'.format(name))  # FIXME: better exception
        fn()
        assert self._tag_stack.pop() == name

    def characters(self, ch):
        name = self._tag_stack[-1]
        try:
            fn = self._char_handlers[name]
        except KeyError:
            if self._error_mode == self.ERR_MODE_IGNORE:
                fn = self._ignore
            else:
                raise SAXException('No characters handler for tag {0!r}'.format(name))  # FIXME: better exception
        fn(ch)


class GraphHandler(SAXHandler):
    def __init__(self, parser, graph, parse_dependency, parse_anchor=CharAnchor, constants=Constants):
        SAXHandler.__init__(self, {
            constants.GRAPH: (None, self.graph_end),
            # Header
            constants.DEPENDENCIES: None,
            constants.DEPENDS_ON: self.dependency_handle,
            constants.ANNOTATION_SPACES: None,
            constants.ANNOTATION_SPACE: self.aspace_handle,
            constants.ANNOTATION_SETS: None,
            constants.ANNOTATION_SET: self.aspace_handle,
            constants.ROOTS: None,
            constants.ROOT: (None, None, self.root_chars),
            constants.HEADER: None,
            constants.TAGSDECL: None,
            constants.TAGUSAGE: None,
            # Media
            constants.REGION: self.region_handle,
            # Graph
            constants.NODE: (self.node_start, self.node_end),
            constants.LINK: self.link_handle,
            constants.EDGE: self.edge_handle,
            # Annotations
            constants.ANNOTATION: (self.annot_start, self.annot_end),
            constants.ASET: (self.aspace_enter, self.aspace_exit),
            constants.FS: (self.fs_start, self.fs_end),
            constants.FEATURE: (self.feature_start, self.feature_end, self.feature_chars),
        })

        self._parser = parser
        self.graph = graph
        self._g = constants
        self._parse_dependency = parse_dependency
        self._parse_anchor = parse_anchor

        self._cur_node = None
        self._delayed_links = []

        self._cur_annot = None
        self._fs_stack = []
        self._feat_name_stack = []
        self._aspace_stack = []

    # === Header ===

    def dependency_handle(self, attribs):
        # In MASC version 1 in the graph header on
        # <dependencies>
        #   <dependsOn type="seg"/>
        # </dependencies>
        # Now in MASC version 3 the depencies here
        # changed to
        # <dependsOn f.id="seg"/>

        try:
            type = attribs[self._g.TYPE_F_ID]
        except KeyError:
            type = attribs[self._g.TYPE]

        self._parse_dependency(type, self.graph)

    def aspace_handle(self, attribs):
        as_id = attribs[self._g.AS_ID]

        if as_id not in self.graph.annotation_spaces:
            self.graph.annotation_spaces.create(as_id)

    def root_chars(self, node_id):
        node = self.graph.nodes.get_or_create(node_id)
        self.graph.root = node

    # === Media ===

    def region_handle(self, attribs):
        anchors = attribs[self._g.ANCHORS]
        region = Region(attribs[self._g.ID], *[self._parse_anchor(anchor) for anchor in anchors.split()])
        self.graph.regions.add(region)

    # === Graph ===

    def node_start(self, attribs):
        assert self._cur_node is None
        self._cur_node = self.graph.nodes.get_or_create(attribs[self._g.ID])
        self._cur_node.is_root = attribs.get(self._g.ROOT, False) == "true"

    def node_end(self):
        self._cur_node = None

    def link_handle(self, attribs):
        self._delayed_links.append((self._cur_node, attribs[self._g.TARGETS]))

    def edge_handle(self, attribs):
        self.graph.create_edge(attribs[self._g.FROM], attribs[self._g.TO], attribs[self._g.ID])

    def graph_end(self):
        # Create links waiting for regions
        for node, targets in self._delayed_links:
            node.add_link(Link(self.graph.regions[target] for target in targets.split()))

    # === Annotations ===

    def annot_start(self, attribs):
        assert self._cur_annot is None
        aspace = attribs.get(self._g.ASET, None)
        if aspace is None:
            aspace = self._aspace_stack[-1]
        else:
            aspace = self.graph.annotation_spaces[aspace]

        self._cur_annot = Annotation(attribs[self._g.LABEL])
        element = self.graph.get_element(attribs[self._g.REF])
        element.annotations.add(self._cur_annot)
        aspace.add(self._cur_annot)

    def annot_end(self):
        self._cur_annot = None

    def fs_start(self, attribs):
        type_ = attribs.get(self._g.TYPE, None)
        if self._fs_stack:
            fs = FeatureStructure(type_)
            self._fs_stack[-1][self._feat_name_stack[-1]] = fs
            self._fs_stack.append(fs)
        else:
            self._cur_annot.features.type = type_
            self._fs_stack.append(self._cur_annot.features)

    def fs_end(self):
        self._fs_stack.pop()

    def feature_start(self, attribs):
        name = attribs.get(self._g.NAME)

        try:
            value = attribs.get(self._g.VALUE)
        except KeyError:
            value = ""

        # In the new MASC version the values aren't attributes
        # any more. So with this way the value is granted
        # ??FIXME?????????????????????????????????????????????
        # if value is None:
        #     value = attrs.getValueByQName(self._g.NAME)

        self._feat_name_stack.append(name)
        self._fs_stack[-1][name] = value

    def feature_end(self):
        self._feat_name_stack.pop()

    def feature_chars(self, value):
        name = self._feat_name_stack[-1]
        self._fs_stack[-1][name] = value

    def aspace_enter(self, attribs):
        self._aspace_stack.append(self.graph.annotation_spaces[attribs[self._g.NAME]])

    def aspace_exit(self):
        self._aspace_stack.pop()


def ignore_dependency(name):
    pass


class GraphParser(object):
    """
    Used to parse the GrAF XML representation and construct the instance 
    of C{Graph} objects.

    version: 1.0.

    """

    def __init__(self, get_dependency=None, parse_anchor=CharAnchor, constants=Constants):
        self._g = constants
        self._get_dep = get_dependency
        self._parse_anchor = parse_anchor

    def parse(self, stream, graph=None):
        """Parses the XML file at the given path.

        :return: a Graph representing the annotated text in GrAF format
        :rtype: Graph
        """
        def do_parse(stream, graph):
            parser = make_parser()
            handler = GraphHandler(parser, graph, parse_dependency, parse_anchor=self._parse_anchor, constants=self._g)
            parser.setContentHandler(handler)
            parser.parse(stream)

        def parse_dependency(name, graph):
            if name in parsed_deps:
                return
            parsed_deps.add(name)
            do_parse(get_dependency(name), graph)

        if not hasattr(stream, 'read'):
            stream = open(stream)

        parsed_deps = set()

        # Read header file
        doc_header = minidom.parse(stream)


        la = os.path.dirname(stream.name)

        annotatios_files = doc_header.getElementsByTagName('annotation')

        # Get the files to look for
        for annotation in annotatios_files:
            loc = annotation.getAttribute('loc') # File name
            fid = annotation.getAttribute('f.id') # File id

            if self._get_dep:
                get_dependency = self._get_dep
            else:
                # Default get_dependency is relative to path
                #header = DocumentHeader(os.path.abspath(stream.name))
                header = DocumentHeader(os.path.abspath(la+'/'+loc))
                def get_dependency(name):
                    #return open(header.get_location(name))
                    return open(la+'/'+loc)

            if graph is None:
                graph = Graph()

            print(la)
            do_parse(la+'/'+loc, graph)

        return graph


if __name__ == '__main__':
    # Round-trip
    import sys
    graph = GraphParser().parse(sys.argv[1])
    GrafRenderer(sys.stdout).render(graph)
