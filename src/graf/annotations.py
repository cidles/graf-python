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

class Annotation:
    """
    A Annotation is the artifcat being annotated.  An annotation is a
    labelled feature structure.  The annotation class/interface also
    provides convenience methods for setting and getting values
    from a feature structure.

    """
    def __init__(self, label, features = FeatureStructure()):
        """Construct a new C{Annotation}.

        :param label: C{str}
        :param features: C{list} of C{Feature} objects
        :param set: this C{Annotation}'s C{AnnotationSet}
        :param element: a C{GraphElement} object

        """

        self._label = label
        self._features = features
        self._set = None
        self._element = None

    def from_annotation(a):
        """Construct a new C{Annotation}.

        :param a: a C{Annotation} object

        """
        return Annotation(a.getLabel(), 
                            FeatureStructure.from_fs(a.getFeatures()))

    def __repr__(self):
        return "Annotation label = " + self._label

    def add(self, name, value):
        """Creates and adda a C{Feature} to this C{Annotation}.

        :param name: name of the C{Feature} to be added
        :param value: value of the C{Feature} to be added

        """

        return self._features.add(name, value)        	

    def add_feature(self, f):
        """Adds the passed C{Feature} to this C{Annotation}.

        :param f: C{Feature} object

        """

        self._features.add_feature(f)

    def features(self):
        """Returns the features.

        :return: C{list} of the C{Feature}s of this C{Annotation}

        """

        return self._features.features()

    def get_feature(self, name):
        """Searches for a C{Feature} in this
        C{Annotation}'s C{list} by name.

        :param name: C{str}
        :return: C{Feature}

        return self._features.get(name)
        """

    def get_feature_value(self, name):
        """Searches for a C{Feature} in this C{Annotation}'s C{list}
        by name, returns that C{Feature}'s value.

        :param: C{str}
        :return: C{str} or None

        """

        f = self.get_feature(name)
        if f is not None and f.is_atomic():
            return f.getStringValue()
        return None


class AnnotationSet:
    """
    A set of Annotations.  Each Annotation set has a name (C{Str})
    and a type (C{URI}) and a set of annotations.

    """

    def __init__(self, name, type):
        """Constructor for C{AnnotationSet}

        :param name: C{str}
        :param type: C{str}
        :param annotations: C{str} of C{Annotation}

        """

        self._name = name
        self._type = type
        self._annotations = []

    def from_as(aSet):
        """Constructs a new C{AnnotationSet} from
        an existing C{AnnotationSet}.

        :param aSet: C{AnnotationSet}
        :return: C{AnnotationSet}

        """

        newAS = AnnotationSet(aSet._name, aSet._type)
        for a in aSet.annotations():
            newAS.add_annotation(Annotation.from_annotation(a))
        return newAS

    def __repr__(self):
        return "AnnSet name= " + self._name + " type= " + self._type

    def add(self, label):
        """Creates a new annotation with specified label, adds it
        to this annotation set, and returns the new annotation.

        :param label: str
        :return: Annotation

        """

        annotation = Annotation(label)
        self.add_annotation(annotation)
        return annotation

    def add_annotation(self, a):
        """Adds a C{Annotation} to the annotations list of
        this C{AnnotationSet}.

        :param a: Annotation

        """

        self._annotations.append(a)
        a._set = self

    def get_annotations_label(self, label):
        """Returns the C{Annotation} with the given label.

        :param label: str
        :return: Annotation

        """

        result = []
        for a in self._annotations:
            if label == a._label:
                result.append(a)
        return result

    def get_annotations(self, label, fs):
        """Returns the C{Annotation} with the given label,
        in the given C{FeatureStructure}.

        :param label: str
        :param fs: FeatureStructure
        :return: FeatureStructure

        """

        result = []
        for a in self._annotations:
            if (label == a.getLabel() 
                            and fs.subsumes(a.getFeatureStructure())):
                result.append(a)
        return result

    def remove_annotation(self, a):
        """Remove the given C{Annotation}.

        :param a: Annotation

        """

        try:
            return self._annotations.remove(a)
        except ValueError:
            print('Error: Annotation not in set')

    def remove_annotations_label(self, label):
        """Remove the C{Annotation} with the given label

        :param label: C{str}

        """

        result = []
        for a in self._annotations:
            if label == a.getLabel():
                result.append(a)
        if len(result) > 0:
            for a in result:
                self._annotations.remove(a)
        return result

    def remove_annotations(self, label, fs):
        """Remove the C{Annotation}s with the given label in
        the given C{FeatureStructure}

        :param label: C{str}
        :param fs: C{FeatureStructure}

        """

        result = []
        for a in self._annotations:
            if (label == a.getLabel() 
                            and fs.subsumes(a.getFeatureStructure())):
                result.append(a)
        if len(result) > 0:
            for a in result:
                self._annotations.remove(a)
        return result

    def size(self):
        return len(self._annotations)


class AnnotationSpace:
    """
    A set of Annotations.  Each Annotation set has a name (C{Str})
    and a type (C{URI}) and a set of annotations.

    :note : It's should replace the AnnotationSet

    """

    def __init__(self, as_id):
        """Constructor for C{AnnotationSpace}

        :param as_id: C{str}
        :param annotations: C{str} of C{Annotation}

        """

        self._as_id = as_id
        self._annotations = []

    def from_as(aSet):
        """Constructs a new C{AnnotationSpace} from
        an existing C{AnnotationSpace}.

        :param aSet: C{AnnotationSpace}
        :return: C{AnnotationSpace}

        """

        newAS = AnnotationSpace(aSet._as_id)
        for a in aSet.annotations():
            newAS.add_annotation(Annotation.from_annotation(a))
        return newAS

    def __repr__(self):
        return "AnnSpace as_id= " + self._as_id

    def add(self, label):
        """Creates a new annotation with specified label, adds it
        to this annotation set, and returns the new annotation.

        :param label: str
        :return: Annotation

        """

        annotation = Annotation(label)
        self.add_annotation(annotation)
        return annotation

    def add_annotation(self, a):
        """Adds a C{Annotation} to the annotations list of
        this C{AnnotationSpace}.

        :param a: Annotation

        """

        self._annotations.append(a)
        a._set = self

    def get_annotations_label(self, label):
        """Returns the C{Annotation} with the given label.

        :param label: str
        :return: Annotation

        """

        result = []
        for a in self._annotations:
            if label == a._label:
                result.append(a)
        return result

    def get_annotations(self, label, fs):
        """Returns the C{Annotation} with the given label,
        in the given C{FeatureStructure}.

        :param label: str
        :param fs: FeatureStructure
        :return: FeatureStructure

        """

        result = []
        for a in self._annotations:
            if (label == a.getLabel() 
                            and fs.subsumes(a.getFeatureStructure())):
                result.append(a)
        return result

    def remove_annotation(self, a):
        """Remove the given C{Annotation}.

        :param a: Annotation

        """

        try:
            return self._annotations.remove(a)
        except ValueError:
            print('Error: Annotation not in set')

    def remove_annotations_label(self, label):
        """Remove the C{Annotation} with the given label

        :param label: C{str}

        """

        result = []
        for a in self._annotations:
            if label == a.getLabel():
                result.append(a)
        if len(result) > 0:
            for a in result:
                self._annotations.remove(a)
        return result

    def remove_annotations(self, label, fs):
        """Remove the C{Annotation}s with the given label in
        the given C{FeatureStructure}

        :param label: C{str}
        :param fs: C{FeatureStructure}

        """

        result = []
        for a in self._annotations:
            if (label == a.getLabel() 
                            and fs.subsumes(a.getFeatureStructure())):
                result.append(a)
        if len(result) > 0:
            for a in result:
                self._annotations.remove(a)
        return result

    def size(self):
        return len(self._annotations)


class Feature:
    """
    A name/value pair.  The "value" of a C{Feature} may be a string or 
    another Py{FeatureStructure} object.

    """

    def __init__(self, name = None, value = None):
        """Constructor for C{Feature}.

        :param name: C{str}
        :param value: C{str} or C{FeatureStructure}

        """

        self._name = name
        if isinstance(value, basestring):
            self._stringValue = value
            self._fsValue = None
        else: 
            self._fsValue = value
            self._stringValue = None

    def from_feature(f):
        """Constructs a new C{Feature} from an existing C{Feature}.

        :param f: C{Feature}

        """

        newF = Feature(f.getName())
        if f.is_atomic():
            newF._stringValue = f.getStringValue()
            newF._fsValue = None
        else:
            newF._stringValue = None
            newF._fsValue = FeatureStructure(f.getFSValue())
        return newF

    def __repr__(self):
        if self._stringValue is not None:
            return ("FeatureName = " + self._name + " stringValue = " 
                    + self._stringValue)
        else:
            return ("FeatureName = " + self._name + " fsValue = " + 
                    self._fsValue)

    def compare_to(self, f):
        """Compare the values.

        :param f: C{FeatureStructure}

        """

        return cmp(self._name, f.getName())

    def copy(self):
        """Copy this C{FeatureStructure}.

        :return: C{FeatureStructure}

        """

        if self._stringValue is None:
            fs = FeatureStructure(self._fsValue) 
            return Feature(self._name, fs)
        return Feature(self._name, self._stringValue)

    def equals(self, e):
        """Compare the values.

        :param e: C{Feature}
        :return: C{bool}

        """

        result = False
        if isinstance(e, Feature):
            result = self._name == e.getName()
        return result
    
    def get_value(self):
        if self._stringValue is not None:
            return self._stringValue
        return self._fsValue

    def is_atomic(self):
        return self._stringValue is not None

    def set_value(self, value):
        if isinstance(value, basestring):
            self._stringValue = value
            self._fsValue = None
        elif isinstance(value, FeatureStructure):
            self._fsValue = value
            self._stringValue = None
        else: 
            print('Error in set_value(), value must be string or' +
                    ' FeatureStructure object')


class FeatureStructure:
    """
    A list of C{Feature}s indexed by name.

    """

    def __init__(self, type = None):
        """Constructor for C{FeatureStructure}.

        :param type: C{str}

        """

        self._type = type
        self._elements = {}

    def from_fs(fs):
        """Constructs a new C{FeatureStructure} from input.

        :param fs: C{FeatureStructure}

        """

        newFS = FeatureStructure(fs.getType())
        for f in fs.features():
            newF = None
            if f.is_atomic():
                newF = Feature(f.getName(), f.getStringValue())
            else:
                copy = FeatureStructure.from_fs(f.getFSValue())
                newF = Feature(f.getName(), copy)
            newFS._elements[f.getName()] = newF
        return newFS

    def __repr__(self):
        return "FeatureStructureType = " + self._type

    def copy(self):
        return FeatureStructure.from_fs(self)

    def size(self):
        return len(self._elements)

    def find(self, name, create=True):
        """Removes '/' chars at start or end of name
        so it is not done repeatedly during recursive search.

        :param name: C{str}
        :param create: C{bool}

        """

        length = len(name)
        if name[0] == '/':
            name = name[1:length]
        if name[length-1] == '/':
            name = name[0:length-1]
        #find_loop does the real work
        return self.find_loop(name, create)

    def find_loop(self, name, create):
        slash = name.find('/')
        if slash < 0:
            result = self._elements.get(name)
            if result == None and create:
                result = Feature(name)
                self.add_feature(result)
            return result

        head = name[0:slash]
        tail = name[slash+1:len(name)]
        f = self._elements.get(head)
        fs = None
        if f != None:
            if f.is_atomic():
                return None
            fs = f.getFSValue()
        else:
            if not create:
                return None
            fs = FeatureStructure()
            f = Feature(head, fs)
            self.add_feature(f)

        return fs.find_loop(tail, create)


    def add(self, name, value):
        """Creates a new feature and adds it to this
        C{FeatureStructure}'s list of elements.

        :param name: C{str}
        :param value: C{str}

        """

        f = self.find(name, True)
        f.set_value(value)
        return f


    def add_feature(self, f):
        self._elements[f._name] = f

    def get(self, name):
        return self.find(name, False)

    def iterator(self):
        return self._elements.itervalues()

    def features(self):
        return self._elements.values()

    def remove(self, element):
        if isinstance(element, basestring):
            return self._elements.pop(element, None) != None
        else:
            return self._elements.pop(element.getName(), None) != None

    def equals(self, o):
        if not isinstance(o, FeatureStructure):
            return False
        return self._type == o.getType()

    def subsumes(self, fs2):
        for f1 in self.features():
            f2 = fs2.get(f1.getName())
            if f2 == None:
                print('f2 == None')
                return False
            if f1.is_atomic():
                if not f2.is_atomic():
                    print('f1 is_atomic, fs is not atomic')
                    return False
                f1Value = f1.getStringValue()
                f2Value = f2.getStringValue()
                if not f1Value == f2Value:
                    print('f1Value != fsValue')
                    return False
            # This feature value is present in fs2
            else:
                if f2.is_atomic():
                    print('feature value is present, fs is atomic')
                    return False
                # Get the feature structures that form the values
                # of these features and check them
                f1fs = f1.getFSValue()
                f2fs = f2.getFSValue()
                if not f1fs.subsumes(f2fs):
                    print('f1fs does not subsume f2fs')
                    return False
        return True

    def unify(self, fs):
        fsType = fs.getType()
        if (self._type == None or fsType == None) and self._type !=fsType:
            #One, but not both, of the types are None
            return None
        if self._type != None:
            #fsType must be non-None
            if self._type != fsType:
                return None

        # make a copy of this feature structure
        result = FeatureStructure.from_fs(self)

        # Add all the features from fs to the result
        for f1 in fs.features():
            f2 = result.get(f1.getName())
            if f2 == None:
                result.add_feature(Feature.from_feature(f1))
            else:
                # A feature with the same name is already present in the result.
                # If this is an atomic feature the values must match or unification fails
                if f1.is_atomic() and f2.is_atomic():
                    fVal = f1.getStringValue()
                    f2Val = f2.getStringValue()
                    if not fVal == f2Val:
                        return None
                elif f1.is_atomic() or f2.is_atomic():
                    # They are not both atomic (handled above) so unification also fails
                    return None
                else:
                    # they are both feature structures so see if they unify
                    f1fs = f1.getFSValue()
                    f2fs = f2.getFSValue()
                    u = f1fs.unify(f2fs)
                    if u == None:
                        return None
                    # They do unify, so add the unified structure to the result
                    result.add(f1.getName(), u)
        return result

