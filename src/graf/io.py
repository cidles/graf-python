# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

import sys
import os
import codecs

from xml.sax import make_parser, SAXException
from xml.sax.handler import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.dom import minidom

from xml.etree.ElementTree import Element, SubElement, tostring

from graf.graphs import Graph, Link
from graf.annotations import Annotation, FeatureStructure
from graf.media import CharAnchor, Region

# Set the type of string
if sys.version_info[:2] >= (3, 0):
    string_type = str
else:
    string_type = basestring

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
            if isinstance(k, string_type):
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

        self.out = open(out, "w")

    def render_node(self, n):
        """
        Used to render the node elements of the Graph.
        """

        node = Element('node', {'xml:id': n.id})

        for link in n.links:
            node.append(self.render_link(link))

        return node

    def render_link(self, link):
        """
        Used to render the link elements of the Graph.
        """

        for region in link:
            return Element('link', {'targets': region.id})

    def render_region(self, region):
        """
        Used to render the region elements of the Graph.
        """

        anchors = str(region.anchors[0]) + " " + str(region.anchors[1])

        return Element('region', {'anchors': anchors, 'xml:id': region.id})

    def render_edge(self, e):
        """
        Used to render the edge elements of the Graph.
        """

        return Element('edge', {'from': e.from_node.id,
                                'to': e.to_node.id,
                                'xml:id': str(e.id)})

    def render_ann(self, a):
        """
        Used to render the annotation elements of the Graph.
        """

        annotation = Element('a', {'as': a.label, 'label': a.label,
                                   'ref': a.element.id, 'xml:id': a.id})

        if a.features:
            annotation.append(self.render_fs(a.features))

        return annotation

    def render_fs(self, fs):
        """
        Used to render the feature structure elements of the Graph.
        """

        if not fs:
            return

        if fs.type:
            feature_structure = Element('fs', {'type': fs.type})
        else:
            feature_structure = Element('fs')

        for name, value in fs.items():
            feature_structure.append(self.render_feature(name, value))

        return feature_structure

    def render_feature(self, name, value):
        """
        Used to render the features elements of the Graph.
        """

        feature = Element('f', {'name': name})
        feature.text = value

        return feature

    def write_header(self, g):
        """
        Writes the header tag at the beginning of the XML file.
        """

        header = Element('graph', {'xmlns': 'http://www.xces.org/ns/GrAF/1.0/'})

        header.append(self.write_header_elements(g))

        return header

    def write_header_elements(self, g):
        """
        Helper method for write_header.
        """

        graph_header = Element('graphHeader')

        graph_header.append(self.render_tag_usage(g))

        depends_on = g.header.depends_on
        dependencies = SubElement(graph_header, 'dependencies')
        if depends_on:
            for dependency in depends_on:
                if dependency:
                    SubElement(dependencies, 'dependsOn',
                               {'f.id': dependency})

        aspaces = g.annotation_spaces
        annotation_spaces = SubElement(graph_header, 'annotationSpaces')
        if aspaces:
            for aspace in aspaces:
                SubElement(annotation_spaces, 'annotationSpace',
                           {'as.id': aspace.as_id})

        roots = g.header.roots
        if roots:
            roots_element = SubElement(graph_header, 'roots')
            for root in roots:
                if root:
                    SubElement(roots_element, 'root').text = root

        return graph_header

    def count_tag_usage(self, g):
        annotations = {}
        for node in g.nodes:
            for a in node.annotations:
                count = annotations.setdefault(a.label, 0)
                annotations[a.label] = count + 1
        return annotations

    def render_tag_usage(self, g):
        annotations = self.count_tag_usage(g)

        labels_decl = Element('labelsDecl')

        for k, v in annotations.items():
            SubElement(labels_decl, "labelUsage", {"label": str(k), "occurs": str(v)})

        return labels_decl

    def render(self, g):

        header = self.write_header(g)

        nodes = sorted(g.nodes)

        for node in nodes:
            header.append(self.render_node(node))

            for region in g.regions:
                for region_node in region.nodes:
                    if str(region_node.id) == str(node.id):
                        header.append(self.render_region(region))

            for edge in g.edges:
                if str(edge.to_node.id) == str(node.id):
                    header.append(self.render_edge(edge))

            for a in node.annotations:
                header.append(self.render_ann(a))

        doc = minidom.parseString(tostring(header, encoding="utf-8"))

        self.out.write(doc.toprettyxml())
        self.out.close()


class StandoffHeaderRenderer(object):
    pass

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

        id_ = attribs.get(self._g.ID, None)
        self._cur_annot = Annotation(attribs[self._g.LABEL], id = id_)
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
        self._parsed_deps = None

    def parse(self, stream, graph=None):
        """Parses the XML file at the given path.

        :return: a Graph representing the annotated text in GrAF format
        :rtype: Graph
        """

        def open_file_for_parse(filename):
            if sys.version_info[:2] >= (3, 0):
                return codecs.open(filename, "r", "utf-8")
            else:
                return open(filename, "r")

        def do_parse(stream, graph):
            parser = make_parser()
            handler = GraphHandler(parser, graph, parse_dependency,
                parse_anchor=self._parse_anchor, constants=self._g)
            parser.setContentHandler(handler)
            parser.parse(stream)

        def parse_dependency(name, graph):
            if name in parsed_deps:
                return
            parsed_deps.add(name)
            do_parse(get_dependency(name), graph)

        if not hasattr(stream, 'read'):
            stream = open_file_for_parse(stream)

        parsed_deps = set()

        parsed_files_dict = dict()

        extension = os.path.splitext(stream.name)[1][1:]

        if extension == 'hdr':
            # Read header file
            doc_header = minidom.parse(stream)

            dirname = os.path.dirname(stream.name)

            annotatios_files = doc_header.getElementsByTagName('annotation')

            # Get the files to look for
            for annotation in annotatios_files:
                loc = annotation.getAttribute('loc')
                fid = annotation.getAttribute('f.id')

                if fid in parsed_deps:
                    continue

                if self._get_dep:
                    get_dependency = self._get_dep
                else:
                    header = DocumentHeader(os.path.abspath(os.path.join(dirname, loc)))

                    def get_dependency(name):
                        return open_file_for_parse(header.get_location(name))

                if graph is None:
                    graph = Graph()

                stream = open_file_for_parse(os.path.join(dirname, loc))
                do_parse(stream, graph)
        else:
            if self._get_dep:
                get_dependency = self._get_dep
            else:
                # Default get_dependency is relative to path
                header = DocumentHeader(os.path.abspath(stream.name))
                def get_dependency(name):
                    return open_file_for_parse(header.get_location(name))

            if graph is None:
                graph = Graph()

            do_parse(stream, graph)

        self._parsed_deps = parsed_deps

        return graph


if __name__ == '__main__':
    # Round-trip
    import sys
    graph = GraphParser().parse(sys.argv[1])
    GrafRenderer(sys.stdout).render(graph)
