**********************
How To Use GrAF-Python
**********************

Introduction
============  

This document explains some functions of the graf-python library such as the parsing of GrAF files.

To use the graf-python library is important to know that the files must use the GrAF ISO standards. Thoses need to follow some rules because of the dependencies between the nodes and the rest of the elements like annotations, regions and edges. The header file (.hdr) in the GrAF ISO standard is the file that contain the relevant information about the GrAF. The information passes by the author, date of creation and all the relevant data. The important parts of that file are the annotations and the primary file. The annotations are the dependent files to create all the nodes, edges, feature and everything needed to the GrAF. The primary file is the raw file that has the words that are the values of the nodes.

To know more about GrAF and GrAF ISO standards you can consult:
GrAF-wiki (http://www.americannationalcorpus.org/graf-wiki)
GrAF ISO standards (http://www.iso.org/iso/catalogue_detail.htm?csnumber=37326)

Parsing GrAF
============

The first step is to initialize the variable:

.. code-block:: python

    import graf
	gparser = graf.GraphParser()

Like it was said before to parse a file or it is a header file (extension .hdr) or it is one of the dependent files (file with the suffix e.g. 'file-verb.xml'). You can directly pass the filename to the parser:

.. code-block:: python

    graph = gparser.parse("filename.hdr")

Alternativily the parser also accepts and open file stream. Now we have a GrAF object and it is possible to verify the nodes, regions, edges and their respectives annotations.

.. code-block:: python

        # Checking the nodes
	for node in graph.nodes():
		print(node)

        # Checking the regions
	for region in graph.regions():
		print(region)

        # Checking the edges
	for edge in graph.edges():
		print(edge)
