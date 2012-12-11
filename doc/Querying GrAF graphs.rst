Querying GrAF graphs
====================

For a real-world example how to use the GrAF API in Python we will use data from the project "`Quantitative Historical Linguistics <http://www.quanthistling.info/>`_". The project publishes data as GrAF/XML files that are ready to use with the parser. Here we will use the XML files of the dictionary "`Thiesen, Wesley & Thiesen, Eva. 1998. Diccionario Bora—Castellano Castellano—Bora <http://www.quanthistling.info/data/source/thiesen1998/dictionary-25-339.html>`_", which are available as a ZIP package:

http://www.quanthistling.info/data/downloads/xml/thiesen1998.zip

Download and extract the files to a local folder. The following example code will extract all head and translation annotations from the XML files and write them into a separate, tab-separated text file.

First, create a parser object and parse the file "dict-thiesen1998-25-339-dictinterpretation.xml" that you extracted from the ZIP file:

.. code-block:: python

    import graf

    gparser = graf.GraphParser()
    g = parser.parse("dict-thiesen1998-25-339-dictinterpretation.xml")

This will parse the file and all its dependencies into a GrAF object that we can query now. In this case the only dependency is the file "dict-thiesen1998-25-339-entries.xml" that contains regions of dictionary entries that link to the basic data file, and annotations for each of those dictionary entries. We will use the entry nodes to find each "head" and "translation" annotation that are linked to the entry nodes via edges in the graph.

Next, open the output file:

.. code-block:: python

    f = codecs.open("heads_with_translations_thiesen1998.txt", "w", "utf-8")

Then you may loop through all the nodes in the graph. For each node that has a label ending in "entry" we will follow all the edges. The edges that have label "head" or "translation" link to the annotations nodes we want to extract:

.. code-block:: python

    # loop through all nodes in the graph
    for (node_id, node) in g.nodes.items():
        heads = []
        translations = []

        # if the node is a dictionary entry...
        if node_id.endswith("entry"):

            # loop thropugh all edges that are connected
            # to the entry
            for e in node.out_edges:
                # if the edge has a label "head"...
                if e.annotations.get_first().label == "head":
                    # get the "head" annotation string
                    heads.append(e.to_node.annotations.get_first().features.get_value("substring"))

                # if the edge has a label "translation"...
                elif e.annotations.get_first().label == "translation":
                    # get the "translation" annotation string
                    translations.append(e.to_node.annotations.get_first().features.get_value("substring"))
            # write all combinations of heads and translations
            # to the output file
            for h in heads:
                for t in translations:
                    f.write(u"{0}\t{1}\n".format(h, t))

This will write heads and translations to the file, separated by a tab. Don't forget to close the file in the end:

.. code-block:: python

    f.close()

The complete script is available in the Github repository of graf-python:

https://github.com/cidles/graf-python/blob/master/examples/query_quanthistling_graf.py
