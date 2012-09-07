# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2012 Poio Project
# Author: António Lopes <alopes@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT
"""A reader for corpora that consist of documents in
the ISO GrAF format.

All the test use the MASC version 1.0.3
"""


import nltk

class TestMascCorpusReader:

    def test_raw(self):
        """Raise an assertion if can't retrieve the file.

        Return given file(s) as a single string.

        Raises
        ------
        AssertionError
            If can't retrieve a string.

        """

        error_message = 'Fail - Retrieve the file as a string'

        assert(nltk.corpus.masc.raw(), error_message)

    def test_words(self):
        """Raise an assertion if can't retrieve a list of strings
        from a given file.

        Return the given file(s) as a list of words and
        punctuation symbols.

        Raises
        ------
        AssertionError
            If can't retrieve the list of string.

        """

        error_message = 'Fail - Retrieve the list of strings'

        assert(nltk.corpus.masc.words(), error_message)

    def test_sents(self):
        """Raise an assertion if can't retrieve a list of sentences
        from a given file.

        Return the given file(s) as a list of sentences or utterances,
        each encoded as a list of word strings.

        Raises
        ------
        AssertionError
            If can't retrieve the list of sentences.

        """

        error_message = 'Fail - Retrieve the list of sentences'

        assert(nltk.corpus.masc.sents(), error_message)

    def test_paras(self):
        """Raise an assertion if can't retrieve a list of paragraphs
        from a given file.

        Return the given file(s) as a list of paragraphs, each encoded
        as a list of sentences, which are in turn encoded as lists of
        word strings.

        Raises
        ------
        AssertionError
            If can't retrieve the list of strings.

        """

        error_message = 'Fail - Retrieve the list of paragraphs'

        assert(nltk.corpus.masc.paras(), error_message)

    def test_nouns(self):
        """Raise an assertion if can't retrieve a list of nouns
        from a given file.

        Return the given file(s) as a list of nouns.

        Raises
        ------
        AssertionError
            If can't retrieve the list of nouns.

        """

        error_message = 'Fail - Retrieve the list of nouns'

        assert(nltk.corpus.masc.nouns(), error_message)

    def test_verbs(self):
        """Raise an assertion if can't retrieve a list of verbs
        from a given file.

        Return the given file(s) as a list of verbs.

        Raises
        ------
        AssertionError
            If can't retrieve the list of verbs.

        """

        error_message = 'Fail - Retrieve the list of verbs'

        assert(nltk.corpus.masc.verbs(), error_message)

    def test_persons(self):
        """Raise an assertion if can't retrieve a list of persons
        from a given file.

        Return the given file(s) as a list of persons.

        Raises
        ------
        AssertionError
            If can't retrieve the list of persons.

        """

        error_message = 'Fail - Retrieve the list of persons'

        assert(nltk.corpus.masc.persons(), error_message)