# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman:cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik:gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

from xml.sax import make_parser, SAXException
from xml.sax.handler import ContentHandler
import os

from graf.PyGraph import PyGraph
from graf.GRAF import GRAF
from graf.PyDocumentHeader import PyDocumentHeader

class PyGraphParser(ContentHandler):
    """
    Used to parse the GrAF XML representation and construct the instance 
    of C{PyGraph} objects.
    
    version: 1.0.
    
    """

    def __init__(self):
        """Create a new C{PyGraphParser} instance.
        
        """
        
        self._parser = make_parser()
        self._parser.setContentHandler(self)
        self._g = GRAF()
        self._annotation_set_map = {}
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
    
        :return: a PyGraph representing the annotated text in GrAF format
        :rtype: PyGraph
        
        """
        if parsed is None:
            parsed = []
        #print "parsing " + file
        delete_header = False
        if self._header is None:
            self._header = PyDocumentHeader(os.path.abspath(file))
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
        
        """
        
        #check for root node
        if self._root_element == 1:
            self._buffer += ch
    
    def endElement(self, name):
        """Processes the end xml tags, according to their type.
        
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
        self._graph = PyGraph()
        n = attrs.getLength() - 1
        for i in range(0, n):
            name = attrs.getQName(i)
            value = attrs.get_value(i)
            if self._g.ROOT == name:
                self._root_id = value
            elif self._g.VERSION != name:
                self._graph.add_feature(name, value)

    def graph_end(self):
        """Executes when the parser encounters the end graph tag.
        Sets the root node and adds all the edges to the graph. 
        Neither of these tasks can be safely performed until all nodes 
        have been added.
        
        """
        
        """Create and add the edges"""
        for edge in self._edges:
            from_node = self._node_map.get(edge._from)
            to_node = self._node_map.get(edge._to)
            self._graph.add_edge(PyEdge(edge._id, from_node, to_node))
    
        """add annotations to any edges"""
        for s, a in self._edge_annotations:
            e = self._graph.find_edge(s)
            if e is None:
                raise SAXException("Could not find graph element with ID " 
                                + s)
            e.add_annotation(a)

        """link nodes to regions"""
        for n, s in self._relations:
            link = PyLink()
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
        """Used to parse the node start tag.
        Creates a new self._current_node, of type PyNode.
        
        """
        
        id = attrs.get_value(self._g.ID)
        isRoot = attrs.get(self._g.ROOT) ##?
        self._current_node = PyNode(id)

        if isRoot is not None and "true" is isRoot:
            self._current_node._annotationRoot = True

        self._node_map[id] = self._current_node

    def node_end(self):
        """Adds the current_node to the graph being constructed and
        sets self._current_node to None.
        
        """
        
        self._graph.add_node(self._current_node)
        self._current_node = None


    def annotation_set_start(self, attrs):
        """Used to parse <annotationSet .../> elements in the XML 
        representation.
        
        """
        
        name = attrs.get_value(self._g.NAME)
        type = attrs.get_value(self._g.TYPE)
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

    def ann_start(self, attrs):
        label = attrs.get_value(self._g.LABEL)
        self._current_annotation = PyAnnotation(label)

        if label is None:
            SAXException("Required attribute " + self._g.LABEL + 
                    " missing on annotation")

        node_id = attrs.get_value(self._g.REF)
        if node_id is None:
            raise SAXException("Annotation is not associate with a node")
        set_name = attrs.get(self._g.ASET)
        if set_name is not None:
            a_set = self._annotation_set_map.get(set_name)
            if a_set is None:
                raise SAXException("Unknown annotation set name " 
                                    + set_name)
            self._current_annotation._set = a_set
            a_set.add_annotation(self._current_annotation)

        if self._current_annotation_set is not None:
            self._current_annotation_set.addAnnotation(
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
        
        from_id = attrs.get_value(self._g.FROM)
        to_id = attrs.get_value(self._g.TO)
        id = attrs.get_value(self._g.ID)
        self._edges.append(EdgeInfo(id, from_id, to_id))

    def region_start(self, attrs):
        """Used to pare the region elements in the XML representation.
        A tolkenizer is used to separate the anchors listed in the XML tag,
        and a new PyAnchor instance is created for each one.  
        A PyRegion instance is then created with the id from the 
        XML tag and added to the graph.
        
        """
        
        id = attrs.get_value(self._g.ID)
        att = attrs.get_value(self._g.ANCHORS)
        tokenizer = att.split()
        if len(tokenizer) < 2:
            raise SAXException("Invalid number of anchors for the regions")
        anchors = []
        for t in tokenizer:
            anchor = None
            try:
                anchor = PyAnchor(t)
            except:
                raise SAXException("Unable to create an anchor for " + t)

            anchors.append(anchor)

        try:
            region = PyRegion(id, anchors)
            self._graph.add_region(region)
        except:
            raise SAXException("Could not add the region to the graph")

    def fs_start(self, attrs):
        """Used to parse <fs> elements in the XML representation.
        
        """
        
        type = attrs.get(self._g.TYPE)
        fs = PyFeatureStructure(type)
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
        """Used to parse start features elements in the XML representation.
        
        """
        
        name = attrs.get_value(self._g.NAME)
        value = attrs.get_value(self._g.VALUE)
        
        f = PyFeature(name)

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
        fs.addFeature(f)                 

    
    def as_start(self, attrs):
        """Used to parse start <as/ ...> elements in the XML representation.
        
        """
        
        type = attrs.get_value(self._g.TYPE)
        if type is None:
            raise SAXException("No type specified for as element.")
        else:
            self._current_annotation_set = self._graph.get_annotation_set(
                                                                    type)

    def as_end(self):
        """Used to parse end /as> elements in the XML representation.
        
        """
        
        self._current_annotation_set = None


    def link_start(self, attrs):
        """Used to parse link elements in the XML representation.
        
        """
        
        links = attrs.get_value(self._g.TARGETS)
        self._relations.append((self._current_node, links))


    def depends_on_start(self, attrs):
        """Used to parse dependsOn elements in the XML representation.
        Finds other XML annotation files on which depend the current 
        XML file. Parses the dependency files and adds the resulting graph 
        to the current graph.
        """
        
        type = attrs.get_value(self._g.TYPE)
        if type is None:
            raise SAXException("No annotation type defined")

        if type in self._parsed:
            return

        self._parsed.append(type)


        path = self._header.getLocation(type)
        if path is None:
            raise SAXException("Unable to get path for dependency of type"
                                 + " " + type)


        parser = PyGraphParser()
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
            e = self._graph.add_edge_to_from_id(id, from_id, to_id)
            for a in edge.annotations():
                e.add_annotation(PyAnnotation.from_annotation(a))

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


class EdgeInfo:
    """
    Used to store information about edges when parsing the GrAF XML 
    representation.
    
    """
    
    def __init__(self, id = "", fromID = "", toID = ""):
        self._id = id
        self._from = fromID
        self._to = toID
