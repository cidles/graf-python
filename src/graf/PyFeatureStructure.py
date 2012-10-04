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

from graf.PyAnchor import *

class PyFeatureStructure:
    """
    A list of C{PyFeature}s indexed by name.

    """

    def __init__(self, type = None):
        """Constructor for C{PyFeatureStructure}.

        :param type: C{str}

        """

        self._type = type
        self._elements = {}

    def from_fs(fs):
        """Constructs a new C{PyFeatureStructure} from input.

        :param fs: C{PyFeatureStructure}

        """

        newFS = PyFeatureStructure(fs.getType())
        for f in fs.features():
            newF = None
            if f.is_atomic():
                newF = PyFeature(f.getName(), f.getStringValue())
            else:
                copy = PyFeatureStructure.from_fs(f.getFSValue())
                newF = PyFeature(f.getName(), copy)
            newFS._elements[f.getName()] = newF
        return newFS

    def __repr__(self):
        return "FeatureStructureType = " + self._type

    def copy(self):
        return PyFeatureStructure.from_fs(self)

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
                result = PyFeature(name)
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
            fs = PyFeatureStructure()
            f = PyFeature(head, fs)
            self.add_feature(f)

        return fs.find_loop(tail, create)


    def add(self, name, value):
        """Creates a new feature and adds it to this
        C{PyFeatureStructure}'s list of elements.

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
        if isinstance(element, str):
            return self._elements.pop(element, None) != None
        else:
            return self._elements.pop(element.getName(), None) != None

    def equals(self, o):
        if not isinstance(o, PyFeatureStructure):
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
        result = PyFeatureStructure.from_fs(self)

        # Add all the features from fs to the result
        for f1 in fs.features():
            f2 = result.get(f1.getName())
            if f2 == None:
                result.add_feature(PyFeature.from_feature(f1))
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

from graf.PyFeature import *


