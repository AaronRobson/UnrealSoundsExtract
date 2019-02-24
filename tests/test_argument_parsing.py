#!/usr/bin/python

import unittest

from UnrealSoundsExtract import produce_parser


class TestParseArguments(unittest.TestCase):
    def setUp(self):
        self.parser = produce_parser()
        self.given_input_directory = r'C:\Program Files\Unreal Tournament'
        self.given_output_directory = r'.\output_sounds'

    def test_input_directory(self):
        args = self.parser.parse_args([
            '-i', self.given_input_directory
        ])
        self.assertEqual(args.input, self.given_input_directory)

    def test_input_and_output_directories(self):
        args = self.parser.parse_args([
            '-i', self.given_input_directory,
            '-o', self.given_output_directory
        ])
        self.assertEqual(args.input, self.given_input_directory)
        self.assertEqual(args.output, self.given_output_directory)

    def test_flatten_on(self):
        args = self.parser.parse_args([
            '-i', self.given_input_directory,
            '-f',
        ])
        self.assertTrue(args.flatten)

    def test_flatten_off(self):
        args = self.parser.parse_args([
            '-i', self.given_input_directory,
        ])
        self.assertFalse(args.flatten)
