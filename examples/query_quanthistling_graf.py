
# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2012 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

"""
This example scripts writes all heads and translations of a dictionary to a
tab-separated output file.

The data is published by the QuantHistLing project
(http://www.quanthistling.info/). To run the example, please download and
extract the GrAF/XML files of the source "Thiesen, Wesley & Thiesen, Eva. 1998.
Diccionario Bora—Castellano Castellano—Bora" which are available here:

http://www.quanthistling.info/data/downloads/xml/thiesen1998.zip

"""

import graf

# create parser
parser = graf.GraphParser()
g = parser.parse("dict-thiesen1998-25-339-dictinterpretation.xml")

# open file for output
f = codecs.open("heads_with_translations_thiesen1998.txt", "w", "utf-8")

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

# close the output file
f.close()