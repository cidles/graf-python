Parsing GrAF
============

The first step is to initialize the parser:

.. code-block:: python

    import graf
    gparser = graf.GraphParser()

 You can then directly pass the filename of the GrAF header to the parser:

.. code-block:: python

    graph = gparser.parse("filename.hdr")

The parser then collects all the dependencies from this header. You might also pass the file name of any GrAF/XML file to the parser. The parser then loads all files that are dependencies of that file as described in its header.

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
