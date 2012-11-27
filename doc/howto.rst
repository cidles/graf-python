**********************
How To Use GrAF-Python
**********************

This is the documentation for Graf-Python Libary.

Introduction
============  

This document has as presupposition explation the some functions of the Graf-Python Library such as the parsing of GrAF files.

To use the GrAF-Python Library is important to know that the files must use the GrAF ISO standards. Thoses need to follow some rules because of the dependencies between the nodes and the rest of the elements like annotations, regions and edges. The header file (.hdr) in the GrAF ISO standard is the file that contain the relevant information about the GrAF. The information passes by the author, date of creation and all the relevant data. The important parts of that file are the annotations and the primary file. The annotations are the dependent files to create all the nodes, edges, feature and everything needed to the GrAF. The primary file is the raw file that has the words that are the values of the nodes.

To know more about GrAF and GrAF ISO standards you can consult:
GrAF-wiki (http://www.americannationalcorpus.org/graf-wiki)
GrAF ISO standards (http://www.iso.org/iso/catalogue_detail.htm?csnumber=37326)

The writing of the files to GrAF ISO can be done with the Poio API Library (https://github.com/cidles/poio-api). Check the documentation in the documentation page (http://cidles.github.com/poio-api/howto.html).

Parsing GrAF
============

The first step is to initialize the variable:

.. code-block:: python

	gparser = GraphParser()

Like it was said before to parse a file or it is a header file (extension .hdr) or it is one of the dependent files (file with the suffix e.g. 'file-verb.xml'). The file must be open with the UTF-8 encode.

.. code-block:: python

	file = 'file.hdr'
        file_stream = codecs.open(file, 'r', 'utf-8')

The last step is to call the parser:

.. code-block:: python

        graph = gparser.parse(file_stream)

Now we have a GrAF object and it is possible to verify the nodes, regions, edges and their respectives annotations.

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
