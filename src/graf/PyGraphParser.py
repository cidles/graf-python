# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

from xml.sax import make_parser, SAXException
from xml.sax.handler import ContentHandler
import os

from PyGraph import *
from GRAF import *
from PyGrafRenderer import *
from PyDocumentHeader import *

class PyGraphParser(ContentHandler):
    """
    Used to parse the GrAF XML representation and construct the instance 
    of C{PyGraph} objects.
    version: 1.0
    """

    def __init__(self):
        """
        Create a new C{PyGraphParser} instance
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
        """
        Parses the XML file at the given path
    
        @return: a PyGraph representing the annotated text in GrAF format
        @rtype: PyGraph
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
        """
        Processes the opening xml tags, according to their type
        """
        if name == self._g.GRAPH:
            self.graphStart(attrs)
        elif name == self._g.NODE:
            self.nodeStart(attrs)
        elif name == self._g.EDGE:
            self.edgeStart(attrs)
        elif name == self._g.ANNOTATION:
            self.annStart(attrs)
        elif name == self._g.ASET:
            self.ASStart(attrs)
        elif name == self._g.REGION:
            self.regionStart(attrs)
        elif name == self._g.LINK:
            self.linkStart(attrs)
        elif name == self._g.DEPENDS_ON:
            self.dependsOnStart(attrs)
        elif name == self._g.ANNOTATION_SET:
            self.annotationSetStart(attrs)
        elif name == self._g.ROOT:
            self.rootStart(attrs)

        elif name == self._g.FS:
            self.fsStart(attrs)
        elif name == self._g.FEATURE:
            self.featureStart(attrs)
        else:
            pass

    def characters(self, ch):
        """
        Processes any characters within the xml file
        """
        #check for root node
        if self._root_element == 1:
            self._buffer += ch
    
    def endElement(self, name):
        """
        Processes the end xml tags, according to their type
        """
        if name == self._g.GRAPH:
            self.graphEnd()
        elif name == self._g.NODE:
            self.nodeEnd()
        elif name == self._g.ANNOTATION:
            self.annEnd()
        elif name == self._g.ASET:
            self.ASEnd()
        elif name == self._g.EDGE:
            pass
        elif name == self._g.FS:
            self.fsEnd()
        elif name == self._g.FEATURE:
            self.featureEnd()
        elif name == self._g.ROOT:
            self.rootEnd()

    def graphStart(self, attrs):
        """
        Executes when the parser encounters the begin graph tag
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
            value = attrs.getValue(i)
            if self._g.ROOT == name:
                self._root_id = value
            elif self._g.VERSION != name:
                self._graph.addFeature(name, value)

    def graphEnd(self):
        """
        Executes when the parser encounters the end graph tag.
        Sets the root node and adds all the edges to the graph. 
        Neither of these tasks can be safely performed until all nodes 
        have been added.
        """
        """Create and add the edges"""
        for edge in self._edges:
            from_node = self._node_map.get(edge._from)
            to_node = self._node_map.get(edge._to)
            self._graph.addEdge(PyEdge(edge._id, from_node, to_node))
    
        """add annotations to any edges"""
        for s, a in self._edge_annotations:
            e = self._graph.findEdge(s)
            if e is None:
                raise SAXException("Could not find graph element with ID " 
                                + s)
            e.addAnnotation(a)

        """link nodes to regions"""
        for n, s in self._relations:
            link = PyLink()
            for target in s.split():
                region = self._graph.getRegionFromID(target)
                if region is not None:
                    link.addTarget(region)
            n.addLink(link)

        if self._root_id is not None:
            root = self._graph.findNode(self._root_id)
            if root is None:
                raise SAXException("Root node with ID " + self._root_id 
                        + " was not found in the graph.")
            self._graph.setRoot(root)


    def nodeStart(self, attrs):
        """
        Used to parse the node start tag.
        Creates a new self._current_node, of type PyNode
        """
        id = attrs.getValue(self._g.ID)
        isRoot = attrs.get(self._g.ROOT) ##?
        self._current_node = PyNode(id)

        if isRoot is not None and "true" is isRoot:
            self._current_node._annotationRoot = True

        self._node_map[id] = self._current_node

    def nodeEnd(self):
        """
        Adds the current_node to the graph being constructed and
        sets self._current_node to None.
        """
        self._graph.addNode(self._current_node)
        self._current_node = None


    def annotationSetStart(self, attrs):
        """
        Used to parse <annotationSet .../> elements in the XML 
        representation.
        """
        name = attrs.getValue(self._g.NAME)
        type = attrs.getValue(self._g.TYPE)
        sets = self._graph.getAnnotationSets()
        for set in sets:
            if set._name == name:
                if set._type != type:
                    raise SAXException("Annotation set type mismatch for " 
                            				+ name)
                self._annotation_set_map[name] = set
                return
        a_set = self._graph.addASCreate(name, type)
        self._annotation_set_map[name] = a_set

    def annStart(self, attrs):
        label = attrs.getValue(self._g.LABEL)
        self._current_annotation = PyAnnotation(label)

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
                raise SAXException("Unknown annotation set name " 
                                    + set_name)
            self._current_annotation._set = a_set
            a_set.addAnnotation(self._current_annotation)

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
            node.addAnnotation(self._current_annotation)

    def annEnd(self):
        if len(self._fs_stack) != 0:
            fs = self._fs_stack.pop()
            self._current_annotation._features= fs
        self._current_annotation = None

    def edgeStart(self, attrs):
        """
        Used to parse edge elements in the XML representation.
        Edge information is stored and the edges are added after 
        all nodes/spans have been parsed.
        """
        from_id = attrs.getValue(self._g.FROM)
        to_id = attrs.getValue(self._g.TO)
        id = attrs.getValue(self._g.ID)
        self._edges.append(EdgeInfo(id, from_id, to_id))

    def regionStart(self, attrs):
        """
        Used to pare the region elements in the XML representation.
        A tolkenizer is used to separate the anchors listed in the XML tag,
        and a new PyAnchor instance is created for each one.  
        A PyRegion instance is then created with the id from the 
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
                anchor = PyAnchor(t)
            except:
                raise SAXException("Unable to create an anchor for " + t)

            anchors.append(anchor)

        try:
            region = PyRegion(id, anchors)
            self._graph.addRegion(region)
        except:
            raise SAXException("Could not add the region to the graph")

    def fsStart(self, attrs):
        """
        Used to parse <fs> elements in the XML representation.
        """
        type = attrs.get(self._g.TYPE)
        fs = PyFeatureStructure(type)
        self._fs_stack.append(fs)
        

    def fsEnd(self):
        """
        Used to parse </fs> elements in the XML representation.
        """
        if len(self._f_stack) != 0:
            fs = self._fs_stack.pop()
            if len(self._f_stack) -1 >= 0:
                f = self._f_stack[len(self._f_stack)-1]
                f.setValue(fs)


    def featureStart(self, attrs):
        """
        Used to parse start features elements in the XML representation.
        """
        name = attrs.getValue(self._g.NAME)
        value = attrs.getValue(self._g.VALUE)
        
        f = PyFeature(name)

        if value is not None:
            f.setValue(value)

        self._f_stack.append(f)

    def featureEnd(self):
        """
        Used to parse end features elements in the XML representation.
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

    
    def ASStart(self, attrs):
        """
        Used to parse start <as/ ...> elements in the XML representation.
        """
        type = attrs.getValue(self._g.TYPE)
        if type is None:
            raise SAXException("No type specified for as element.")
        else:
            self._current_annotation_set = self._graph.getAnnotationSet(
                                                                    type)

    def ASEnd(self):
        """
        Used to parse end /as> elements in the XML representation.
        """
        self._current_annotation_set = None


    def linkStart(self, attrs):
        """
        Used to parse link elements in the XML representation.
        """
        links = attrs.getValue(self._g.TARGETS)
        self._relations.append((self._current_node, links))


    def dependsOnStart(self, attrs):
        """
        Used to parse dependsOn elements in the XML representation.
        Finds other XML annotation files on which depend the current 
        XML file. Parses the dependency files and adds the resulting graph 
        to the current graph
        """
        type = attrs.getValue(self._g.TYPE)
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

        for a_set in dependency.annotationSets():
            self._graph.addAnnotationSet(a_set)

        for node in dependency.nodes():
            self._graph.addNode(node)
            self._node_map[node._id] = node

        for edge in dependency.edges():
            id = edge._id
            from_id = edge.getFrom()._id
            to_id = edge.getTo()._id
            e = self._graph.addEdgeToFromID(id, from_id, to_id)
            for a in edge.annotations():
                e.addAnnotation(PyAnnotation.fromAnnotation(a))

        for region in dependency.regions():
            self._graph.addRegion(region)


    def rootStart(self, attrs):
        """
        Used to parse start root elements in the XML representation.
        The root characters are processed by the characters() method and 
        stored in self._buffer.
        self._root_element is a flag indicating the presence of a root.
        """
        self._buffer = ""
        self._root_element = 1

    def rootEnd(self):
        """
        Used to parse end root elements in the XML representation.
        """
        self._root_id = self._buffer
        self._buffer = ""
        self._root_element = 0


"""
Used to store information about edges when parsing the GrAF XML 
representation.
"""
class EdgeInfo:
    def __init__(self, id = "", fromID = "", toID = ""):
        self._id = id
        self._from = fromID
        self._to = toID
        
            




