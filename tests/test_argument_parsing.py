#!/usr/bin/python

import unittest

from UnrealSoundsExtract import produce_parser, INPUT_DEFAULT, OUTPUT_DEFAULT


class TestParseArguments(unittest.TestCase):
    def setUp(self):
        self.parser = produce_parser()
        self.given_input_directory = r'C:\Program Files\Unreal Tournament'
        self.given_output_directory = r'.\output_sounds'

    def test_defaults(self):
        args = self.parser.parse_args([])
        self.assertEqual(args.input, INPUT_DEFAULT)
        self.assertEqual(args.output, OUTPUT_DEFAULT)
        self.assertFalse(args.flatten)

    def test_input_directory_given_a_value(self):
        args = self.parser.parse_args([
            '-i', self.given_input_directory
        ])
        self.assertEqual(args.input, self.given_input_directory)

    def test_output_directory_given_a_value(self):
        args = self.parser.parse_args([
            '-o', self.given_output_directory
        ])
        self.assertEqual(args.output, self.given_output_directory)

    def test_input_and_output_directories(self):
        args = self.parser.parse_args([
            '-i', self.given_input_directory,
            '-o', self.given_output_directory
        ])
        self.assertEqual(args.input, self.given_input_directory)
        self.assertEqual(args.output, self.given_output_directory)

    def test_flatten_on(self):
        args = self.parser.parse_args(['-f'])
        self.assertTrue(args.flatten)
