# graf-python: Python GrAF API
#
# Copyright (C) 2014 American National Corpus
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.anc.org/>
# For license information, see LICENSE.TXT
#

import sys
import os
import codecs
import datetime
import getpass
import random
from operator import attrgetter

from xml.sax import make_parser, SAXException
from xml.sax.handler import ContentHandler
from xml.dom import minidom


from xml.etree.ElementTree import Element, SubElement, tostring

from graf.graphs import Graph, Link
from graf.annotations import Annotation, FeatureStructure
from graf.media import CharAnchor, Region


class Constants(object):
    """
    A list of constants used in the GrafRenderer
    """
    __slots__ = ()
    VERSION = "1.0"
    NAMESPACE = "http://www.xces.org/ns/GrAF/" + VERSION + "/"
    EOL = "\n"
    #DEFAULT = "DEFAULT"    	
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


class GrafRenderer(object):
    """
    Renders a GrAF XML representation that can be read back by an instance
    of L{GraphParser}.

    Version: 1.0.

    """

    def __init__(self, outputfile):
        """Create an instance of a GrafRenderer.

        """

        self.outputfile = outputfile

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
                                'xml:id': e.id})

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
            SubElement(labels_decl, "labelUsage", {"label": k, "occurs": str(v)})

        return labels_decl

    def render(self, g):

        header = self.write_header(g)

        # render regions
        for region in sorted(g.regions):
            header.append(self.render_region(region))

        # render nodes
        nodes = sorted(g.nodes)
        for node in nodes:
            header.append(self.render_node(node))
            for a in node.annotations:
                header.append(self.render_ann(a))

            # for region in g.regions:
            #     for region_node in region.nodes:
            #         if region_node.id == node.id:
            #             header.append(self.render_region(region))

            # for edge in g.edges:
            #     if edge.to_node.id == node.id:
            #         header.append(self.render_edge(edge))

        # render edges
        for edge in sorted(g.edges, key=lambda e: e.pos
                if e.pos is not None else 0):
            header.append(self.render_edge(edge))

        doc = minidom.parseString(tostring(header, encoding="utf-8"))

        output = open(self.outputfile, "wb")
        output.write(doc.toprettyxml(encoding='utf-8'))
        output.close()


class StandoffHeaderRenderer(object):

    def __init__(self, outputfile):
        self.outputfile = outputfile

    def render_documentheader(self, standoffheader):
        """Create the documentHeader Element.

        Returns
        -------
        documentheader : ElementTree
            Primary element of the primary data document header.

        """

        now = datetime.datetime.now()
        pubDate = now.strftime("%Y-%m-%d")

        documentheader = Element('documentHeader',
                                 {"xmlns": "http://www.xces.org/ns/GrAF/1.0/",
                                  "xmlns:xlink": "http://www.w3.org/1999/xlink",
                                  "docId": "PoioAPI-" + str(random.randint(1, 1000000)),
                                  "version": standoffheader.version,
                                  "creator": getpass.getuser(),
                                  "date.created": pubDate})

        filedesc = self.render_filedesc(standoffheader.filedesc)
        profiledesc = self.render_profiledesc(standoffheader.profiledesc)
        datadesc = self.render_datadesc(standoffheader.datadesc)

        profiledesc.append(datadesc.getchildren()[0])
        profiledesc.append(datadesc.getchildren()[1])

        documentheader.append(filedesc)
        documentheader.append(profiledesc)

        return documentheader

    def render_filedesc(self, filedesc):
        """Create an fileDesc Element.

        Returns
        -------
        fileDesc : ElementTree
            Element with the descriptions of the primary file.

        """

        fileDesc = Element('fileDesc')

        titleStmt = SubElement(fileDesc, 'titleStmt')
        SubElement(titleStmt, 'title').text = filedesc.titlestmt

        if filedesc.extent:
            SubElement(fileDesc, 'extent', {"unit": filedesc.extent['unit'],
                                            "count": filedesc.extent['count']})

        sourceDesc = SubElement(fileDesc, "sourceDesc")

        if filedesc.title:
            SubElement(sourceDesc, 'title').text = filedesc.title

        if filedesc.author:
            if 'age' in filedesc.author:
                aut = {"age": filedesc.author['age']}
            if 'sex' in filedesc.author:
                aut = {"sex": filedesc.author['sex']}

            SubElement(sourceDesc, "author", aut).text = filedesc.author['name']

        if filedesc.source:
            SubElement(sourceDesc, "source",
                       {"type": filedesc.source['type']}).text = filedesc.source['source']

        if filedesc.distributor:
            SubElement(sourceDesc, "distributor").text = filedesc.distributor

        if filedesc.publisher:
            SubElement(sourceDesc, "publisher").text = filedesc.publisher

        if filedesc.pubAddress:
            SubElement(sourceDesc, "pubAddress").text = filedesc.pubAddress

        if filedesc.eAddress:
            SubElement(sourceDesc, "eAddress",
                       {"type": filedesc.eAddress['type']}).text = filedesc.eAddress['email']

        if filedesc.pubDate:
            SubElement(sourceDesc, "pubDate", {"iso8601": filedesc.pubDate})

        if filedesc.idno:
            SubElement(sourceDesc, "idno",
                       {"type": filedesc.idno['type']}).text = filedesc.idno['number']

        if filedesc.pubName:
            SubElement(sourceDesc, "pubName",
                       {"type": filedesc.pubName['type']}).text = filedesc.pubName['text']

        if filedesc.documentation:
            SubElement(sourceDesc, "documentation").text = filedesc.documentation

        return fileDesc
    
    def render_profiledesc(self, profiledesc):
        """Create an profileDesc Element.

        Returns
        -------
        profileDesc : ElementTree
            Element with the descriptions of the source file.

        See Also
        --------
        add_language, add_participant, add_setting

        """

        profileDesc = Element("profileDesc")

        if profiledesc.languages:
            langUsage = SubElement(profileDesc, "langUsage")

            for language in profiledesc.languages:
                SubElement(langUsage, "language", {"iso639": language})

        if profiledesc.catRef:
            textClass = SubElement(profileDesc, "textClass",
                                   {"catRef": profiledesc.catRef})

            if profiledesc.subject:
                subject_el = SubElement(textClass, "subject")
                subject_el.text = profiledesc.subject

            if profiledesc.domain:
                domain = SubElement(textClass, "domain")
                domain.text = profiledesc.domain

            if profiledesc.subdomain:
                subdomain = SubElement(textClass, "subdomain")
                subdomain.text = profiledesc.subdomain

        if profiledesc.participants:
            particDesc = SubElement(profileDesc, "particDesc") # Required

            for participant in profiledesc.participants:
                SubElement(particDesc, "person", participant)

        if profiledesc.settings:
            settingDesc = SubElement(profileDesc, "settingDesc")

            for sett in profiledesc.settings:
                setting = SubElement(settingDesc, "setting",
                                     {"who": sett['who']})

                time = SubElement(setting, "time")
                time.text = sett['time']

                activity = SubElement(setting, "activity")
                activity.text = sett['activity']

                locale = SubElement(setting, "locale")
                locale.text = sett['locale']

        return profileDesc

    def render_datadesc(self, datadesc):
        """Create an dataDesc Element.

        Returns
        -------
        dataDesc : ElementTree
            Element with the descriptions of the annotation
            files.

        See Also
        --------
        add_annotation

        """

        dataDesc = Element("dataDesc")

        SubElement(dataDesc, "primaryData", datadesc.primaryData)

        annotations = SubElement(dataDesc, "annotations")

        for ann in datadesc.annotations_list:
            SubElement(annotations, "annotation", ann)

        return dataDesc

    def render_revisiondesc(self, revisiondesc):
        """Create an revisionDesc Element.

        Returns
        -------
        revisionDesc : ElementTree
            Element with the revisions of the changes in
            the file.

        See Also
        --------
        add_change

        """

        revisionDesc = Element("revisionDesc")

        if revisiondesc.changes is not None:
            for ch in revisiondesc.changes:
                change = SubElement(revisionDesc, "change")

                changeDate = SubElement(change, "changeDate")
                changeDate.text = ch['changedate']

                respName = SubElement(change, "respName")
                respName.text = ch['resp']

                item = SubElement(change, "item")
                item.text = ch['item']

        return revisionDesc

    def render(self, standoffheader):
        """Write primary data document header.

        Parameters
        ----------
        outputfile : str
            Path of the outputfile.

        """

        documentheader = self.render_documentheader(standoffheader)

        doc = minidom.parseString(tostring(documentheader, encoding="utf-8"))

        output = open(self.outputfile, "wb")
        output.write(doc.toprettyxml(encoding='utf-8'))
        output.close()


class GrAFXMLValidator(object):

    def __init__(self):
        try:
            from lxml import etree

            xsd_header = os.path.join(os.path.dirname(__file__), "..",
                                      "..", "xsd", "GrAF_DocumentHeader.xsd")
            xsd_annotation = os.path.join(os.path.dirname(__file__), "..",
                                          "..", "xsd", "GrAF_StandoffAnnotation.xsd")

            self.header_xmlschema = etree.XMLSchema(etree.parse(xsd_header))
            self.annotation_xmlschema = etree.XMLSchema(etree.parse(xsd_annotation))

            self.import_validator = True
        except :
            self.import_validator = False

    def validate_xml(self, context, header=False, annotation=False):

        if self.import_validator:
            from lxml import etree

            if header:
                validator = self.header_xmlschema
            elif annotation:
                validator = self.annotation_xmlschema

            doc = etree.fromstring(context)

            validator.assert_(doc)

class DocumentHeader(object):

    def __init__(self, path):
        self._basename = ""
        self._dir = ""
        self._annotationMap = {}
        self.set_basepath(path)

    def set_basepath(self, filename):
        if filename.endswith(".txt"):
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
            return self._annotationMap[type]
        if self._basename is not None:
            #return self._basename + ".xml"
            if type.startswith('f.'):
                type = type[2:]
            return self._basename + '-' + type + ".xml"
        return None

    def add_type(self, type, loc):
        self._annotationMap[type] = loc


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
        self._default_aspace_id = None

    # === Header ===

    def dependency_handle(self, attribs):
        try:
            type = attribs[self._g.TYPE_F_ID]
        except KeyError:
            type = attribs[self._g.TYPE]

        self._parse_dependency(type, self.graph)

    def aspace_handle(self, attribs):
        as_id = attribs[self._g.AS_ID]
        is_default = attribs.get(self._g.DEFAULT, False) == "true"

        if as_id not in self.graph.annotation_spaces:
            self.graph.annotation_spaces.create(as_id)

        if is_default:
            self._default_aspace_id = as_id

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
            if len(self._aspace_stack) > 0:
                aspace = self._aspace_stack[-1]
            elif self._default_aspace_id:
                aspace = self.graph.annotation_spaces[self._default_aspace_id]
        else:
            aspace = self.graph.annotation_spaces[aspace]

        id_ = attribs.get(self._g.ID, None)
        self._cur_annot = Annotation(attribs[self._g.LABEL], id=id_)
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
        self.graf_validator = GrAFXMLValidator()

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
            filename = stream.name
            context = stream.read()
            #self.graf_validator.validate_xml(context, annotation="True")

            parser = make_parser()
            handler = GraphHandler(parser, graph, parse_dependency,
                                   parse_anchor=self._parse_anchor,
                                   constants=self._g)
            parser.setContentHandler(handler)
            parser.parse(filename)

        def parse_dependency(name, graph):
            if name in parsed_deps:
                return
            parsed_deps.add(name)
            do_parse(get_dependency(name), graph)

        if not hasattr(stream, 'read'):
            stream = open_file_for_parse(stream)

        parsed_deps = set()
        extension = os.path.splitext(stream.name)[1][1:]

        if extension == 'hdr':
            context = stream.read()
            #self.graf_validator.validate_xml(context, header=True)

            doc_header = minidom.parseString(context)
            dirname = os.path.dirname(stream.name)

            if self._get_dep:
                get_dependency = self._get_dep
            else:
                header = DocumentHeader(stream.name)
                for annotation in doc_header.getElementsByTagName('annotation'):
                    loc = annotation.getAttribute('loc')
                    fid = annotation.getAttribute('f.id')
                    header.add_type(fid, loc)

                def get_dependency(name):
                    return open_file_for_parse(os.path.join(dirname, header.get_location(name)))


            for annotation in doc_header.getElementsByTagName('annotation'):
                loc = annotation.getAttribute('loc')
                fid = annotation.getAttribute('f.id')

                if fid in parsed_deps:
                    continue

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
