# graf-python: Python GrAF API
#
# Copyright (C) 2014 American National Corpus
# Author: Keith Suderman <suderman@cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik@gmail.com> (Conversion to Python)
# URL: <http://www.anc.org/>
# For license information, see LICENSE.TXT
#

import copy

class Annotation(object):
    """
    An Annotation is the artifact being annotated.  An annotation is a
    labelled feature structure.  The annotation class/interface also
    provides convenience methods for setting and getting values
    from a feature structure.
    """
    __slots__ = ('id', 'label', 'features', 'aspace', 'element')
    _ninsts = -1

    def __init__(self, label, features=None, id=None):
        """Construct a new C{Annotation}.

        :param label: C{str}
        :param features: C{list} of C{Feature} objects

        """

        self.id = id if id is not None else self._next_id()
        self.label = label
        if not isinstance(features, FeatureStructure):
            features = FeatureStructure(items=features)
        self.features = features
        self.aspace = None
        self.element = None

    @classmethod
    def _next_id(cls):
        cls._ninsts += 1
        return 'a-%d' % cls._ninsts

    def __repr__(self):
        return "Annotation(%r, %r)" % (self.label, self.id)

    def __eq__(self, id):
        return self.id == id

    #TODO: perhaps delegate __*item__, etc. methods to features


class AnnotationList(object):
    """
    A collection of Annotations which marks a field on the annotation object indicating its possession.
    """
    __slots__ = ('_elements', '_set_owner')

    def __init__(self, owned_by, owner_field):
        self._elements = []
        self._set_owner = lambda ann: setattr(ann, owner_field, owned_by)

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        return iter(self._elements)

    def __repr__(self):
        return repr(self._elements)

    def add(self, ann):
        """Adds a C{Annotation} to this C{AnnotationSpace}.
        :param a: Annotation
        """

        #if ann not in self._elements:
        self._elements.append(ann)
        self._set_owner(ann)

    def create(self, label):
        """Creates a new annotation with specified label, adds it
        to this annotation set, and returns the new annotation.

        :param label: str
        :return: Annotation

        """
        ann = Annotation(label)
        self.add(ann)
        return ann

    def select(self, label=None, fs=None, aspace=None):
        """Generates Annotation objects having the given label and features
        subsumed by the given FeatureStructure.

        Parameters
        ----------
        label : str
        fs : FeatureStructure
        aspace : an AnnotationSpace name

        Returns
        -------
        gen : generator of Annotation
        """
        filters = self._build_filters(label, fs, aspace)
        return (ann for ann in self._elements if all(fn(ann) for fn in filters))

    def select_not(self, label=None, fs=None, aspace=None):
        """
        Generates those annotations that would not be returned by select() with the same arguments.
        """
        filters = self._build_filters(label, fs, aspace)
        return (ann for ann in self._elements if not all(fn(ann) for fn in filters))

    @staticmethod
    def _build_filters(label=None, fs=None, aspace=None):
        res = []
        if aspace is not None:
            res.append(lambda ann: ann.aspace is not None and ann.aspace.name == aspace)
        if label is not None:
            res.append(lambda ann: ann.label == label)
        if fs is not None:
            res.append(lambda ann: fs.subsumes(ann.features))
        return res

    def get_first(self, label=None, fs=None, aspace=None):
        try:
            return next(self.select(label, fs, aspace))
        except StopIteration:
            raise ValueError('No annotations match those criteria')


class AnnotationSpace(AnnotationList):
    """
    A collection of Annotations.  Each AnnotationSpace has a name (C{Str})
    and a type (C{URI}) and a set of annotations.

    """

    __slots__ = ('as_id')

    def __init__(self, as_id):
        """Constructor for C{AnnotationSpace}

        :param name: C{str}
        :param type: C{str}
        """
        super(AnnotationSpace, self).__init__(self, 'aspace')
        self.as_id = as_id

    def __copy__(self):
        res = AnnotationSpace(self.as_id)
        res.annotations = self.annotations[:]
        return res

    def __repr__(self):
        return "AnnotationSpace(%r)" % (self.as_id)

    def remove(self, ann):
        """Remove the given C{Annotation} object.

        :param a: Annotation
        """
        try:
            return self._elements.remove(ann)
        except ValueError:
            print('Error: Annotation not in set')

    def remove_where(self, label, fs=None):
        """Remove the C{Annotation}s with the given label in
        the given C{FeatureStructure}

        :param label: C{str}
        :param fs: C{FeatureStructure}
        """
        self._elements = list(self.select_not(label, fs))


class FeatureStructure(object):
    """
    A dict of key -> feature, where feature is either a string or another FeatureStructure.
    A FeatureStructure may also have a type.
    When key is a tuple of names, or a string of names joined by '/', it is interpreted as the path to a nested feature structure.
    Additionally, a FeatureStructure defines the operations 'subsumes' and 'unify'.
    """

    __slots__ = ('type', '_elements')

    def __init__(self, type_var=None, items=None):
        """Constructor for C{FeatureStructure}.

        :param type: C{str}

        """
        self.type = type_var
        self._elements = {}
        if items:
            self.update(items)

    def __len__(self):
        return len(self._elements)

    def __repr__(self):
        return "<FeatureStructure(%r) with %d elements>" % (self.type, len(self))

    def __copy__(self):
        res = FeatureStructure(self.type)
        res._elements = self._elements.copy()
        return res

    copy = __copy__

    def __deepcopy__(self):
        res = FeatureStructure(self.type)
        res._elements = copy.deepcopy(self._elements)
        return res

    def __iter__(self):
        return iter(self._elements)

    if hasattr(dict, 'iterkeys'): # Python 2.x
        def iterkeys(self):
            return self._elements.iterkeys()

        def iteritems(self):
            return self._elements.iteritems()

    if hasattr(dict, 'viewkeys'): # Python 2.7+
        def viewkeys(self):
            return self._elements.viewkeys()

        def viewitems(self):
            return self._elements.viewitems()

    def keys(self):
        return self._elements.keys()

    def items(self):
        return self._elements.items()

    def _resolve_fs(self, path, create=False):
        """
        Resolves a list of keys to this or a descendent feature structure.
        """
        fs = self
        for name in path:
            try:
                fs = fs._elements[name]
            except KeyError:
                if create:
                    fs = fs._elements[name] = FeatureStructure()
                else:
                    fs = None
            if not isinstance(fs, FeatureStructure):
                raise KeyError('Could not resolve feature structure for path %r. Got %r' % (path, fs))
        return fs

    def _parse_key(self, key, create=False):
        try:
            key = key.strip('/').split('/')
        except AttributeError:
            # assume key is already list of path elements
            pass
        return self._resolve_fs(key[:-1], create), key[-1]

    def __contains__(self, key):
        try:
            fs, key = self._parse_key(key)
        except KeyError:
            return False
        return key in fs._elements

    def __getitem__(self, key):
        fs, key = self._parse_key(key)
        return fs._elements[key]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def get_fs(self, key):
        """Returns the value corresponding to key if it is a FeatureStructure, and otherwise throws a ValueError"""
        val = self[key]
        if not isinstance(val, FeatureStructure):
            raise ValueError('Value for key %r is not a FeatureStructure' % key)
        return val

    def get_value(self, key):
        """Returns the value corresponding to key but throws a ValueError if it is a FeatureStructure"""
        val = self[key]
        if isinstance(val, FeatureStructure):
            raise ValueError('Value for key %r is a FeatureStructure' % key)
        return val

    def __setitem__(self, key, val):
        fs, key = self._parse_key(key, create=True)
        fs._elements[key] = val

    def setdefault(self, key, default):
        fs, key = self._parse_key(key, create=True)
        return fs._elements.setdefault(key, default)

    def update(self, other):
        if hasattr(other, 'items'):
            other = other.items()
        for key, value in other:
            self[key] = value

    def __delitem__(self, key):
        fs, key = self._parse_key(key)
        del fs._elements[key]

    def pop(self, key, default=None):
        try:
            fs, key = self._parse_key(key)
            return fs._elements.pop(key, default)
        except KeyError:
            return default

    def __eq__(self, other):
        """
        Equivalence is equivalent types (????)
        """
        try:
            return self.type == other.type
        except AttributeError:
            return False

    def subsumes(self, other):
        for key, val in self.items():
            try:
                oval = other._elements[key]
            except KeyError:
                return False
            if isinstance(val, FeatureStructure) and isinstance(oval, FeatureStructure):
                if not val.subsumes(oval):
                    return False
            elif val != oval:
                return False
        return True

    def unify(self, other):
        if self.type != other.type and self.type is not None and other.type is not None:
            raise ValueError('Cannot unify feature structues of different types: %r and %r' % (self.type, other.type))

        res = copy.deepcopy(self)

        for name, oval in other.items():
            if name not in res._elements:
                res._elements[name] = copy.deepcopy(oval)
                continue

            val = res._elements[name]
            if isinstance(val, FeatureStructure) and isinstance(oval, FeatureStructure):
                res._elements[name] = val.unify(oval)
            elif val != oval:
                raise ValueError('Name %r exists but value %r != %r in unification' % (name, val, oval))
        return res
