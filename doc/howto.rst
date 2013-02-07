***************************
Introduction to graf-python
***************************

The library graf-python is a Python implemenation to parse files GrAF/XML files as described in ISO 24612. The parser of the library create an annotation graph from the files. The user may then query the annotation graph via the API of graf-python. This documentation gives some examples how to acccess data and how to transform it for further processing in linguistic and computational libraries like networkX, numpy and NLTK.

**References:**
    * GrAF-wiki (http://www.americannationalcorpus.org/graf-wiki)
    * ISO 24612 (http://www.iso.org/iso/catalogue_detail.htm?csnumber=37326)

GrAF/XML Data Sources
=====================

* MASC: http://www.anc.org/MASC/Home.html
* QuantHistLing: http://www.quanthistling.info/data

How to use the library
======================

.. toctree::
   :maxdepth: 1

   Parsing GrAF
   Querying GrAF graphs
   Translation Graph from GrAF

