Parsing GrAF
============

The first step is to initialize the parser:

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
