# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

"""
An annotation graph is a directed graph that represents an annotation of
arbitrary and application dependent size. A graph may cover a sentence,
paragraph, document, or entire corpus. However, to keep processing feasible
graphs are typically relatively small (sentences say) and then combined into
larger graphs as needed.
"""

import sys
import datetime
import getpass
import random

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

from graf.annotations import FeatureStructure, AnnotationList, AnnotationSpace

# Set the type of string
if sys.version_info[:2] >= (3, 0):
    string_type = str
else:
    string_type = basestring


class IdDict(dict):
    __slots__ = ('_id_field',)

    def __init__(self, data=(), field='id'):
        dict.__init__(self, data)
        self._id_field = field

    def add(self, obj):
        self[getattr(obj, self._id_field)] = obj

    def __iter__(self):
        if hasattr(self, 'itervalues'):
            return self.itervalues()
        elif hasattr(self, 'values'):
            return iter(self.values())

    def __contains__(self, obj):
        return dict.__contains__(self, getattr(obj, self._id_field, obj))


class GraphEdges(IdDict):
    __slots__ = ()

    def add(self, obj):
        IdDict.add(self, obj)
        obj.from_node.out_edges.add(obj)
        obj.to_node.in_edges.add(obj)


class GraphNodes(IdDict):
    __slots__ = ('_order',)

    def __init__(self):
        IdDict.__init__(self)
        self._order = list()

    def add(self, obj):
        """Adds the given node or creates one with the given id"""
        if isinstance(obj, string_type):
            obj = Node(obj)
        IdDict.add(self, obj)
        self._order.append(obj.id)
        return obj

    def get_or_create(self, id):
        if id in self:
            return self[id]
        else:
            return self.add(id)

    def iter_ordered(self):
        for id in self._order:
            yield self[id]


class GraphASpaces(IdDict):
    __slots__ = ('_add_hook',)

    def __init__(self, add_hook):
        IdDict.__init__(self, field='as_id')
        self._add_hook = add_hook

    def add(self, obj):
        IdDict.add(self, obj)
        self._add_hook(obj)

    def create(self, as_id):
        res = AnnotationSpace(as_id)
        self.add(res)
        return res


class Graph(object):
    """
    Class of Graph.
    """

    def __init__(self):
        """
        Constructor for Graph.
        """
        self.features = FeatureStructure()
        self.nodes = GraphNodes()
        self._top_edge_id = 0
        self.edges = GraphEdges()
        self.regions = IdDict()
        self.content = None
        self.header = GraphHeader()
        self.annotation_spaces = GraphASpaces(self.header.add_annotation_space)

        # List that will contain additional/extra information
        # to the graph source/origins
        self.additional_information = {}

    def create_edge(self, from_node=None, to_node=None, id=None):
        """Create C{Edge} from id, from_node, to_node and add it to
        this C{Graph}.

        :param id: C{str}
        :param from_node: C{Node}
        :param to_node: C{Node}

        """
        if not hasattr(from_node, 'id'):
            from_node = self.nodes[from_node]
        if from_node.id not in self.nodes:
            self.nodes.add(from_node)

        if not hasattr(to_node, 'id'):
            to_node = self.nodes[to_node]
        if to_node.id not in self.nodes:
            self.nodes.add(to_node)

        if id is None:
            while id is None or id in self.edges:
                id = 'e%d' % self._top_edge_id
                self._top_edge_id += 1
        res = Edge(id, from_node, to_node)

        #if not res in self.edges.values():
        self.edges.add(res)

        return res

    def find_edge(self, from_node, to_node):
        """Search for C{Edge} with its from_node, to_node, either nodes or ids.

        :param from_node: C{Node} or C{str}
        :param to_node: C{Node} or C{str}
        :return: C{Edge} or None
        """
        # resolve ids to nodes if necessary
        if not isinstance(from_node, Node):
            from_node = self.nodes[from_node]
        if not isinstance(to_node, Node):
            to_node = self.nodes[to_node]

        if len(from_node.out_edges) < len(to_node.in_edges):
            for edge in from_node.out_edges:
                if edge.to_node == to_node:
                    return edge
        else:
            for edge in to_node.in_edges:
                if edge.from_node == from_node:
                    return edge
        return None

    def get_element(self, id):
        if id in self.nodes:
            return self.nodes[id]
        return self.edges[id]

    def get_region(self, *anchors):
        for region in self.regions:
            if region.anchors == anchors:
                return region
        return None

    def _get_root(self):
        try:
            if sys.version_info[:2] >= (3, 0):
                return self.iter_roots().__next__()
            else:
                return self.iter_roots().next()
        except StopIteration:
            return None

    def _set_root(self, node):
        # FIXME: how should this interact with node.is_root
        self.header.clear_roots()
        if node.id not in self.nodes:
            raise ValueError('The new root node is not in the graph: %r' % node)
        self.header.roots.append(node.id)

    root = property(_get_root, _set_root)

    def iter_roots(self):
        return (self.nodes[id] for id in self.header.roots)


class GraphElement(object):
    """
    Class of edges in Graph:

    - Each edge maintains the source (from) C{Node} and the destination.
      (to) C{Node}.
    - Edges may also contain one or more C{Annotation} objects.

    """

    def __init__(self, id=""):
        """Constructor for C{GraphElement}.

        :param id: C{str}

        """
        self.id = id
        self.visited = False
        self.annotations = AnnotationList(self, 'element')

    def __repr__(self):
        return "GraphElement id = " + self.id

    @property
    def is_annotated(self):
        return bool(self.annotations)

    def clear(self):
        self.visited = False

    def __eq__(self, other):
        """Comparison of two graph elements by ID.

        :param o: C{GraphElement}
        """

        if other is None:
            return False
        return type(self) is type(other) and self.id == other.id

    def visit(self):
        self.visited = True


class EdgeList(object):
    """An append-only structure with O(1) lookup by id or order-index"""

    __slots__ = ('_by_ind', '_by_id')

    def __init__(self):
        self._by_ind = []
        self._by_id = {}

    def add(self, edge):
        self._by_id[edge.id] = edge
        self._by_ind.append(edge)

    def __iter__(self):
        return iter(self._by_ind)

    def __len__(self):
        return len(self._by_ind)

    def __getitem__(self, sl):
        """
        Returns the edge corresponding to the specified slice/index or raises an IndexError.
        If the given value is not a slice or int, returns the edge with the given id, or raises a KeyError
        """
        # should ID lookup have preference??
        if isinstance(sl, (int, slice)):
            return self._by_ind[sl]
        return self._by_id[sl]

    def __contains__(self, edge):
        if hasattr(edge, 'id'):
            edge = edge.id
        return edge in self._by_id

    def ids(self):
        return self._by_id.keys()


class Node(GraphElement):
    """
    Class for nodes within a C{Graph} instance.
    Each node keeps a list of in-edges and out-edges.
    Each collection is backed by two data structures:
    1. A list (for traversals)
    2. A hash map
    Nodes may also contain one or more C{Annotation} objects.

    """

    def __init__(self, id=""):
        GraphElement.__init__(self, id)
        self.in_edges = EdgeList()
        self.out_edges = EdgeList()
        self.links = []

    def __repr__(self):
        return "NodeID = " + self.id

    def __lt__(self, other):
        return self.id < other.id

    # Relationship to media

    def add_link(self, link):
        self.links.append(link)
        self._add_regions(link)

    def _add_regions(self, regions):
        for region in regions:
            region.nodes.append(self)

    def add_region(self, region):
        """Adds the given region to the first link for this node"""
        if self.links:
            self.links[0].append(region)
            self._add_regions((region,))
        else:
            self.add_link(Link((region,)))

    # Relationship within graph

    def iter_parents(self):
        for edge in self.in_edges:
            res = edge.from_node
            if res is not None:
                yield res

    @property
    def parent(self):
        try:
            if sys.version_info[:2] >= (3, 0):
                return self.iter_parents().__next__()
            else:
                return self.iter_parents().next()
        except StopIteration:
            raise AttributeError('%r has no parents' % self)

    def iter_children(self):
        for edge in self.out_edges:
            res = edge.to_node
            if res is not None:
                yield res

    def clear(self):
        """Clears this node's visisted status and those of all visited descendents"""
        self.visited = False

        for child in self.iter_children():
            if child.visited:
                child.clear()

    @property
    def degree(self):
        return len(self.in_edges) + len(self.out_edges)


class Edge(GraphElement):
    """
    Class of edges in Graph:
    - Each edge maintains the source (from) C{Node} and the destination.
    (to) C{Node}.
    - Edges may also contain one or more C{Annotation} objects.

    """

    def __init__(self, id, from_node=None, to_node=None):
        """C{Edge} Constructor.

        :param id: C{str}
        :param from_node: C{Node}
        :param to_node: C{Node}

        """
        GraphElement.__init__(self, id)
        self.from_node = from_node
        self.to_node = to_node

    def __repr__(self):
        return "Edge id = " + self.id


class Link(list):
    """
    Link objects are used to associate nodes in the graph with the
    regions of the graph they annotate. Links are almost like edges except a
    link is a relation between a node and a region rather than a relation
    between two nodes. A node make be linked to more than one region.
    """
    # Inherits all functionality from builtin list
    __slots__ = ()

    def __init__(self, vals=()):
        super(Link, self).__init__(vals)


class GraphHeader(object):
    """
    Class that represents the graphHeader of each
    GrAF file.

    """

    def __init__(self):
        self.annotation_spaces = {}
        self.depends_on = []
        self.roots = []

    def __repr__(self):
        return "GraphHeader"

    def add_annotation_space(self, aspace):
        self.annotation_spaces[aspace.as_id] = aspace

    def add_dependency(self, type):
        self.depends_on.append(type)

    def clear_roots(self):
        del self.roots[:]


class StandoffHeader(object):
    """
    Class that represents the primary data document header.
    The construction of the file is based in the
    ISO 24612.

    """

    def __init__(self, version = "1.0.0", **kwargs):
        """Class's constructor.

        Parameters
        ----------
        version : str
            Version of the document header file.
        filedesc : ElementTree
            Element with the description of the file.
        profiledesc : ElementTree
            Element with the description of the source file.
        datadesc : ElementTree
            Element with the description of the annotations.

        """

        self._kwargs = kwargs
        
        self.version = version
        self.filedesc = self._get_key_value('fileDesc')
        self.profiledesc = self._get_key_value('profilDesc')
        self.datadesc = self._get_key_value('dataDesc')

    def create_element(self):
        """Create an Element Tree.

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
                                  "version": self.version,
                                  "creator": getpass.getuser(),
                                  "date.created": pubDate})

        filedesc = self.filedesc.create_element()
        profiledesc = self.profiledesc.create_element()
        datadesc = self.datadesc.create_element()

        profiledesc.append(datadesc.getchildren()[0])
        profiledesc.append(datadesc.getchildren()[1])

        documentheader.append(filedesc)
        documentheader.append(profiledesc)

        return documentheader

    def __repr__(self):
        return "StandoffHeader"

    def _get_key_value(self, key):
        if key == 'fileDesc':
            return FileDesc()
        if key == 'profilDesc':
            return ProfileDesc()
        if key == 'dataDesc':
            return DataDesc(None)

        return None
    
    def write_file_header(self, outputfile):
        """Write primary data document header.

        Parameters
        ----------
        outputfile : str
            Path of the outputfile.

        """

        documentheader = self.create_element()

        file = open(outputfile, 'wb')
        doc = minidom.parseString(tostring(documentheader, encoding="utf-8"))
        file.write(doc.toprettyxml(indent='  ', encoding='utf-8'))
        file.close()

    def update_header(self, filename):
        """Updated the documentheader element every time
        something change in a existing file.

        Parameters
        ----------
        filename : str
            Path of the filename.

        """

        pass

    def add_revision(self):
        pass


class FileDesc(object):
    """
    Class that represents the descriptions of the file
    containing the primary data document.

    """

    def __init__(self, **kwargs):
        """Class's constructor.

        Parameters
        ----------
        titlestmt : str
            Name of the file containing the primary data
            document.
        extent : dict
            Size of the resource. The keys are 'count' -
            Value expressing the size. And 'unit' - Unit
            in which the size of the resource is expressed.
            Both keys are mandatory.
        title : str
            Title of the primary data document.
        author : dict
            Author of the primary data document. The keys
            are 'age' and 'sex'.
        source : dict
            Source from which the primary data was obtained.
            The keys are 'type' - Role or type the source
            with regard to the document. And 'source'. Both
            keys are mandatory.
        distributor : str
            Distributor of the primary data (if different
            from source).
        publisher : str
            Publisher of the source.
        pubAddress : str
            Address of publisher.
        eAddress : dict
            Email address, URL, etc. of publisher. The keys
            are 'email' and 'type' - Type of electronic
            address, such as email or URL. Both keys are
            mandatory.
        pubDate : str
            Date of original publication. Should use the
            ISO 8601 format YYYY-MM-DD.
        idno : dict
            Identification number for the document. The keys
            are 'number' and 'type' - Type of the identification
            number (e.g. ISBN). Both keys are mandatory.
        pubName : str
            Name of the publication in which the primary data was
            originally published (e.g. journal in which it appeared).
        documentation : str
            PID where documentation concerning the data may be found.

        """

        self._kwargs = kwargs

        self.titlestmt = self._get_key_value('titlestmt')
        self.extent = self._get_key_value('extent')
        self.title = self._get_key_value('title')
        self.author = self._get_key_value('author')
        self.source = self._get_key_value('source')
        self.distributor = self._get_key_value('distributor')
        self.publisher = self._get_key_value('publisher')
        self.pubAddress = self._get_key_value('pubAddress')
        self.eAddress = self._get_key_value('eAddress')
        self.pubDate = self._get_key_value('pubDate')
        self.idno = self._get_key_value('idno')
        self.pubName = self._get_key_value('pubName')
        self.documentation = self._get_key_value('documentation')

    def create_element(self):
        """Create an Element Tree.

        Returns
        -------
        fileDesc : ElementTree
            Element with the descriptions of the primary file.

        """

        fileDesc = Element('fileDesc')

        titleStmt = SubElement(fileDesc, 'titleStmt')
        SubElement(titleStmt, 'title').text = self.titlestmt

        if self.extent:
            SubElement(fileDesc, 'extent', {"unit": self.extent['unit'],
                                            "count": self.extent['count']})

        sourceDesc = SubElement(fileDesc, "sourceDesc")

        if self.title:
            SubElement(sourceDesc, 'title').text = self.title

        if self.author:
            if 'age' in self.author:
                aut = {"age": self.author['age']}
            if 'sex' in self.author:
                aut = {"sex": self.author['sex']}

            SubElement(sourceDesc, "author", aut).text = self.author['name']

        if self.source:
            SubElement(sourceDesc, "source",
                       {"type": self.source['type']}).text = self.source['source']

        if self.distributor:
            SubElement(sourceDesc, "distributor").text = self.distributor

        if self.publisher:
            SubElement(sourceDesc, "publisher").text = self.publisher

        if self.pubAddress:
            SubElement(sourceDesc, "pubAddress").text = self.pubAddress

        if self.eAddress:
            SubElement(sourceDesc, "eAddress",
                       {"type": self.eAddress['type']}).text = self.eAddress['email']

        if self.pubDate:
            SubElement(sourceDesc, "pubDate", {"iso8601": self.pubDate})

        if self.idno:
            SubElement(sourceDesc, "idno",
                       {"type": self.idno['type']}).text = self.idno['number']

        if self.pubName:
            SubElement(sourceDesc, "pubName",
                       {"type": self.pubName['type']}).text = self.pubName['text']

        if self.documentation:
            SubElement(sourceDesc, "documentation").text = self.documentation

        return fileDesc

    def __repr__(self):
        return "FileDesc"

    def _get_key_value(self, key):
        if key in self._kwargs:
            return self._kwargs[key]

        return None


class ProfileDesc(object):
    """
    Class that represents the descriptions of the file
    containing the primary data document.

    """

    def __init__(self, **kwargs):
        """Class's constructor.

        Parameters
        ----------
        catRef : str
            One or more categories defined in the resource
            header.
        subject : str
            Topic of the primary data.
        domain : str
            Primary domain of the data.
        subdomain : str
            Subdomain of the data.
        languages : array_like
            Array that contains the codes of the language(s)
            of the primary data. The code should be in the
            ISO 639.
        participants : array_like
            Array that contains the participants in an
            interaction. Each person is a dict element and
            the keys are 'age', 'sex', 'role' and 'id' -
            Identifier for reference from annotation documents.
            The 'id' key is mandatory.
        settings : array_like
            Array that contains the settings within which a
            language interaction takes place. Each settings is
            a dictionary and the keys are 'who', 'time', 'activity'
            and 'locale'.

        """

        self._kwargs = kwargs

        self.languages = self._get_key_value('languages')
        self.catRef = self._get_key_value('catRef')
        self.subject = self._get_key_value('subject')
        self.domain = self._get_key_value('domain')
        self.subdomain = self._get_key_value('subdomain')
        self.participants = self._get_key_value('participants')
        self.settings = self._get_key_value('settings')

    def create_element(self):
        """Create an Element Tree.

        Returns
        -------
        profileDesc : ElementTree
            Element with the descriptions of the source file.

        See Also
        --------
        add_language, add_participant, add_setting

        """

        profileDesc = Element("profileDesc")

        if self.languages:
            langUsage = SubElement(profileDesc, "langUsage")

            for language in self.languages:
                SubElement(langUsage, "language", {"iso639": language})

        if self.catRef:
            textClass = SubElement(profileDesc, "textClass",
                                   {"catRef": self.catRef})

            if self.subject:
                subject_el = SubElement(textClass, "subject")
                subject_el.text = self.subject

            if self.domain:
                domain = SubElement(textClass, "domain")
                domain.text = self.domain

            if self.subdomain:
                subdomain = SubElement(textClass, "subdomain")
                subdomain.text = self.subdomain

        if self.participants:
            particDesc = SubElement(profileDesc, "particDesc") # Required

            for participant in self.participants:
                SubElement(particDesc, "person", participant)

        if self.settings:
            settingDesc = SubElement(profileDesc, "settingDesc")

            for sett in self.settings:
                setting = SubElement(settingDesc, "setting",
                                     {"who": sett['who']})

                time = SubElement(setting, "time")
                time.text = sett['time']

                activity = SubElement(setting, "activity")
                activity.text = sett['activity']

                locale = SubElement(setting, "locale")
                locale.text = sett['locale']

        return profileDesc

    def __repr__(self):
        return "ProfileDesc"

    def add_language(self, language_code):
        """This method is responsible to add the
        annotations to the list of languages.

        The language list in this class will
        represents the language(s) that the
        primary data use.

        Parameters
        ----------
        language_code : str
            ISO 639 code(s) for the language(s) of the primary data.

        """

        self.languages.append(language_code)

    def add_participant(self, id, age=None, sex=None, role=None):
        """This method is responsible to add the
        annotations to the list of participants.

        The parcipant list in this class will
        represents participants in an interaction
        with the data manipulated in the files pointed
        by the header.

        A participant is a person in this case and it's
        important and required to give the id.

        Parameters
        ----------
        id : str
            Identifier for reference from annotation documents.
        age : int
            Age of the speaker.
        role : str
            Role of the speaker in the discourse.
        sex : str
            One of male, female, unknown.

        """

        participant = {'id': id}

        if age:
            participant['age'] = age
        if sex:
            participant['sex'] = sex
        if role:
            participant['role'] = role

        self.participants.append(participant)

    def add_setting(self, who, time, activity, locale):
        """This method is responsible to add the
        annotations to the list of settings.

        The setting list in this class will
        represents the setting or settings
        within which a language interaction takes
        place, either as a prose description or a
        series of setting elements.

        A setting is a particular setting in which
        a language interaction takes place.

        Parameters
        ----------
        who : str
            Reference to person IDs involved in this interaction.
        time : str
            Time of the interaction.
        activity : str
            What a participant in a language interaction is doing
            other than speaking.
        locale : str
            Place of the interaction, e.g. a room, a restaurant,
            a park bench.

        """

        self.settings.append({'who': who, 'time': time, 'activity': activity,
                              'locale': locale})

    def _get_key_value(self, key):
        if key in self._kwargs:
            return self._kwargs[key]

        return None


class DataDesc(object):
    """
    Class that represents the annotations to the document associated
    with the primary data document this header describes.

    """

    def __init__(self, primaryData):
        """Class's constructor.

        Parameters
        ----------
        primaryData : dict
            Provides the location of the primary data
            document. The keys are 'loc' - relative
            path or PID of the primary data document,
            'loctype' - Indicates whether the primary
            data path is a fully specified path (PID)
            or a path relative to the location of
            this header file, the default is 'relative',
            the other option is 'URL'. The other key is
            'f.id' - File type via reference to definition
            in the resource header. All keys are mandatory.

        """

        self.primaryData = primaryData
        self.annotations_list = None

    def create_element(self):
        """Create an Element Tree.

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

        SubElement(dataDesc, "primaryData", self.primaryData)

        annotations = SubElement(dataDesc, "annotations")

        for ann in self.annotations_list:
            SubElement(annotations, "annotation", ann)

        return dataDesc

    def __repr__(self):
        return "DataDesc"

    def add_annotation(self, loc, fid, loctype="relative"):
        """This method is responsible to add the
        annotations to the list of annotations.

        The annotations list in this class will
        represents the documents associated with
        the primary data document that this header
        will describe.

        Parameters
        ----------
        loc : str
            Relative path or PID of the annotation document.
        fid : str
            File type via reference to definition in the resource header.
        loctype : str
            Indicates whether the path is a fully specified path or a
            path relative to the header file.


        """

        if self.annotations_list is None:
            self.annotations_list = []

        value = {'loc': loc, 'loctype': loctype, 'f.id': fid}

        if value not in self.annotations_list:
            self.annotations_list.append({'loc': loc, 'loctype': loctype,
                                          'f.id': fid})


class RevisonDesc():
    """
    Class that represents the changes made in a specific
    of the primary data document header.

    """

    def __init__(self, changes=None):
        """Class's constructor.

        Parameters
        ----------
        changes : array_like
            Array that contains a list of changes. Each
            change is a dictionary. The keys are
            'changedate', 'respname' and 'item': All keys
            are mandatory.

        """

        self.changes = changes

    def create_element(self):
        """Create an Element Tree.

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

        if self.changes is not None:
            for ch in self.changes:
                change = SubElement(revisionDesc, "change")

                changeDate = SubElement(change, "changeDate")
                changeDate.text = ch['changedate']

                respName = SubElement(change, "respName")
                respName.text = ch['resp']

                item = SubElement(change, "item")
                item.text = ch['item']

        return revisionDesc

    def __repr__(self):
        return "RevisonDesc"

    def add_change(self, changedate, respname, item):
        """This method is responsible to add the
        annotations to the list of changes.

        The changes list in this class will
        represents the information about a
        particular change made to the document.

        Parameters
        ----------
        changedate : str
            Date of the change in ISO 8601 format.
        responsible : str
            Identification of the person responsible for the change.
        item : str
            Description of the change.

        """

        self.changes.append({'changedate': changedate,
                             'respname': respname, 'item': item})