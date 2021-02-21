#!/usr/bin/python

import unittest
from unittest.mock import patch
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


@patch('os.system', return_value=None)
@patch('UnrealSoundsExtract.GetFilenamesInDirectory', return_value=[])
class TestDoExtraction(unittest.TestCase):
    def setUp(self):
        self.given_input = os.path.join('.')
        self.given_output = os.path.join('.', 'SoundsInWav')
        self.given_flatten = False
        self.expected_sounds_directory = os.path.join(self.given_input, 'Sounds')

    def test_no_files(self, mock_get_filenames_in_directory, mock_os_system):
        with self.assertRaisesRegex(OSError, r'^No Files to Extract from in:'):
            ute.DoExtraction(self.given_input, self.given_output, self.given_flatten)
        mock_get_filenames_in_directory.assert_called_with(self.expected_sounds_directory)
        mock_os_system.assert_not_called()

    def test_multiple_files(self, mock_get_filenames_in_directory, mock_os_system):
        mock_get_filenames_in_directory.return_value = [
            os.path.join(self.expected_sounds_directory, 'abc.uax'),
            os.path.join(self.expected_sounds_directory, 'xyz.uax'),
        ]
        self.assertIsNone(ute.DoExtraction(self.given_input, self.given_output, self.given_flatten))
        mock_get_filenames_in_directory.assert_called_with(self.expected_sounds_directory)
        self.assertEqual(mock_os_system.call_count, 2)
