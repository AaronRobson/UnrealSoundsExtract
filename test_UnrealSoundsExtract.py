#!/usr/bin/python

import unittest

import UnrealSoundsExtract as ute


class TestMakeFormatString(unittest.TestCase):

    def test_sub_folder(self):
        given = ute.MakeFormatString(makeSubFolderForEachCollectionFile=True)
        actual = 'UCC batchexport {0} sound wav "{1}{0}"'
        self.assertEqual(given, actual)

    def test_no_sub_folder(self):
        given = ute.MakeFormatString(makeSubFolderForEachCollectionFile=False)
        actual = 'UCC batchexport {0} sound wav "{1}"'
        self.assertEqual(given, actual)


if __name__ == "__main__":
    unittest.main()
