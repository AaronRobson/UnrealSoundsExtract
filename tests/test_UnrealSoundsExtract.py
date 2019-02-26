#!/usr/bin/python

import unittest
import os.path

import UnrealSoundsExtract as ute


class TestMakeFormatString(unittest.TestCase):
    def setUp(self):
        self.givenExtractorFilepath = os.path.join('.', 'System', 'UCC')

    def test_sub_folder(self):
        given = ute.MakeFormatString(
            extractorFilepath=self.givenExtractorFilepath,
            subFolderPerCollectionFile=True)
        actual = self.givenExtractorFilepath + \
            ' batchexport {0} sound wav "{1}{0}"'
        self.assertEqual(given, actual)

    def test_no_sub_folder(self):
        given = ute.MakeFormatString(
            extractorFilepath=self.givenExtractorFilepath,
            subFolderPerCollectionFile=False)
        actual = self.givenExtractorFilepath + \
            ' batchexport {0} sound wav "{1}"'
        self.assertEqual(given, actual)
