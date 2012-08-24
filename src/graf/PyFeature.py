# Natural Language Toolkit: GrAF API
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Keith Suderman <suderman:cs.vassar.edu> (Original API)
#         Stephen Matysik <smatysik:gmail.com> (Conversion to Python)
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

import graf.PyFeatureStructure

class PyFeature:
    """
    A name/value pair.  The "value" of a C{PyFeature} may be a string or 
    another Py{FeatureStructure} object.
    
    """

    def __init__(self, name = None, value = None):
        """Constructor for C{PyFeature}.
        
        :param name: C{str}
        :param value: C{str} or C{PyFeatureStructure}
        
        """
        
        self._name = name
        if isinstance(value, str):
            self._stringValue = value
            self._fsValue = None
        else: 
            self._fsValue = value
            self._stringValue = None

    def from_feature(f):
        """Constructs a new C{PyFeature} from an existing C{PyFeature}.
        
        :param f: C{PyFeature}
        
        """
        
        newF = PyFeature(f.getName())
        if f.is_atomic():
            newF._stringValue = f.getStringValue()
            newF._fsValue = None
        else:
            newF._stringValue = None
            newF._fsValue = graf.PyFeatureStructure.PyFeatureStructure(f.getFSValue())
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
        
        :param f: C{PyFeatureStructure}
        
        """
        
        return cmp(self._name, f.getName())

    def copy(self):
        """Copy this C{PyFeatureStructure}.
        
        :return: C{PyFeatureStructure}
                
        """
        if self._stringValue is None:
            fs = graf.PyFeatureStructure.PyFeatureStructure(self._fsValue)
            return PyFeature(self._name, fs)
        return PyFeature(self._name, self._stringValue)

    def equals(self, e):
        """Compare the values.
        
        :param e: C{PyFeature}
        :return: C{bool}
        
        """
        
        result = False
        if isinstance(e, PyFeature):
            result = self._name == e.getName()
        return result
    
    def get_value(self):
        if self._stringValue is not None:
            return self._stringValue
        return self._fsValue

    def is_atomic(self):
        return self._stringValue is not None

    def set_value(self, value):
        if isinstance(value, str):
            self._stringValue = value
            self._fsValue = None
        elif isinstance(value, graf.PyFeatureStructure.PyFeatureStructure):
            self._fsValue = value
            self._stringValue = None
        else: 
            print ("Error in set_value(), value must be string or" +
                    " PyFeatureStructure object")