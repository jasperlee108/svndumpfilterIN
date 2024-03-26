from dataclasses import dataclass
from difflib import diff_bytes, unified_diff
from pathlib import Path, PurePath
from tempfile import NamedTemporaryFile
import unittest

from ..svndumpfilter import parse_dump


class ParseDumpTestCase(unittest.TestCase):
    # Set up structure equivalent to parsed options in main program to pass on to filtering routine
    @dataclass
    class OPTIONS:
        drop_empty: bool = True
        renumber_revs: bool = True
        strip_merge: bool = False
        quiet: bool = False
        start_revision: int = None
        scan: bool = False
        file: str = None
        repo: str = '../repos/python'
        debug: bool = False

    # Directory location of test dumpfiles and expected filtered dump files
    DUMPFILE_DIRECTORY = PurePath(Path(__file__).resolve().parent, 'data')

    def setUp(self):
        super().setUp()
        self.DEFAULT_OPTIONS = self.OPTIONS(True, True, False, False, None, False, None, '../repos/python', False)

    def filtered_dumpfile_differences(self, expected_dumpfile, filtered_dumpfile):
        """ Compute difference between the expected filtered dumpfile and the filtered dumpfile.

            The dumpfiles are split based on newlines and differences are returned
            as unified diffs

        """
        expected_dumpfile_lines = open(expected_dumpfile, '+rb').read().split(b'\n')
        filtered_dumpfile_lines = open(filtered_dumpfile, '+rb').read().split(b'\n')

        diff_generator = diff_bytes(unified_diff,
                                    expected_dumpfile_lines,
                                    filtered_dumpfile_lines,
                                    fromfile=b'Expected Filtered Dump',
                                    tofile=b'Actual Filtered Dump')
        diff = b''
        for diff_line in diff_generator:
            diff += diff_line

        return diff

    def test_only_empty_revisions_removed(self):
        """ Test filtering dump file with only empty revisions removes them """
        input_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'test_empty_revs_dump')
        expected_filtered_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'expected_empty_revs_removed_filtered_dump')
        opt = self.OPTIONS()

        with NamedTemporaryFile() as filtered_output_file:
            parse_dump(input_dumpfile, filtered_output_file.name, ['foo'], False, opt)
            diff = self.filtered_dumpfile_differences(expected_filtered_dumpfile, filtered_output_file.name)
        self.assertEqual(b'', diff)

    def test_only_empty_revisions_preserved(self):
        """ Test filtering dump file with only empty revisions preserving them """
        input_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'test_empty_revs_dump')
        expected_filtered_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'expected_empty_revs_preserved_filtered_dump')
        opt = self.OPTIONS()
        opt.drop_empty = False

        with NamedTemporaryFile() as filtered_output_file:
            parse_dump(input_dumpfile, filtered_output_file.name, ['foo'], False, opt)
            diff = self.filtered_dumpfile_differences(expected_filtered_dumpfile, filtered_output_file.name)
        self.assertEqual(b'', diff)

    def test_only_empty_revisions_preserved_stop_renumbering(self):
        """ Test filtering dump file with only empty revisions preserving them and stop re-numbering"""
        input_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'test_empty_revs_dump')
        expected_filtered_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'expected_empty_revs_preserved_stop_renumbering_filtered_dump')
        opt = self.OPTIONS()
        opt.drop_empty = False
        opt.renumber_revs = False

        with NamedTemporaryFile() as filtered_output_file:
            parse_dump(input_dumpfile, filtered_output_file.name, ['foo'], False, opt)
            diff = self.filtered_dumpfile_differences(expected_filtered_dumpfile, filtered_output_file.name)
        self.assertEqual(b'', diff)

    def test_non_existing_excluded_node_empty_with_revisions_removed(self):
        """ Test filtering dump file with nodes and empty revisions, exclude non-existing node, remove empty revisions """
        input_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'test_nodes_empty_revs_dump')
        expected_filtered_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'expected_non_existing_node_excluded_empty_revs_removed')
        opt = self.OPTIONS()

        with NamedTemporaryFile() as filtered_output_file:
            parse_dump(input_dumpfile, filtered_output_file.name, ['foo'], False, opt)
            diff = self.filtered_dumpfile_differences(expected_filtered_dumpfile, filtered_output_file.name)
        self.assertEqual(b'', diff)

    def test_non_existing_excluded_node_empty_with_revisions_preserved(self):
        """ Test filtering dump file with nodes and empty revisions, exclude non-existing node, preserve empty revisions """
        input_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'test_nodes_empty_revs_dump')
        expected_filtered_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'expected_non_existing_node_excluded_empty_revs_preserved')
        opt = self.OPTIONS()
        opt.drop_empty = False

        with NamedTemporaryFile() as filtered_output_file:
            parse_dump(input_dumpfile, filtered_output_file.name, ['foo'], False, opt)
            diff = self.filtered_dumpfile_differences(expected_filtered_dumpfile, filtered_output_file.name)
        self.assertEqual(b'', diff)

    def test_existing_excluded_node_empty_with_revisions_removed(self):
        """ Test filtering dump file with nodes and empty revisions, exclude existing node, remove empty revisions """
        input_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'test_nodes_empty_revs_dump')
        expected_filtered_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'expected_existing_node_excluded_empty_revs_removed')
        opt = self.OPTIONS()

        with NamedTemporaryFile() as filtered_output_file:
            parse_dump(input_dumpfile, filtered_output_file.name, ['python/trunk/Doc/Makefile'], False, opt)
            diff = self.filtered_dumpfile_differences(expected_filtered_dumpfile, filtered_output_file.name)
        self.assertEqual(b'', diff)

    def test_existing_included_node_empty_with_revisions_removed(self):
        """ Test filtering dump file with nodes and empty revisions, include existing node, remove empty revisions """
        input_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'test_nodes_empty_revs_dump')
        expected_filtered_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'expected_existing_node_included_empty_revs_removed')
        opt = self.OPTIONS()

        with NamedTemporaryFile() as filtered_output_file:
            parse_dump(input_dumpfile, filtered_output_file.name, ['python/trunk/Doc/README'], True, opt)
            diff = self.filtered_dumpfile_differences(expected_filtered_dumpfile, filtered_output_file.name)
        self.assertEqual(b'', diff)

    def test_merginfo_properties_removal_no_renumbering(self):
        """ Test filtering dump file with to ensure mergeinfo properties are removed and stop renumbering"""
        input_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'test_mergeinfo_dump')
        expected_filtered_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'expected_mergeinfo_removed_no_renumber')
        opt = self.OPTIONS()
        opt.strip_merge = True
        opt.renumber_revs = False

        with NamedTemporaryFile() as filtered_output_file:
            parse_dump(input_dumpfile, filtered_output_file.name, ['foo'], False, opt)
            diff = self.filtered_dumpfile_differences(expected_filtered_dumpfile, filtered_output_file.name)
        self.assertEqual(b'', diff)

    def test_large_binary_file_include(self):
        """ Test correctly including large files (greater then the read buffer) and filtering others """
        input_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'test_include_large_file_dump')
        expected_filtered_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'expected_include_large_file_dump')
        opt = self.OPTIONS()

        with NamedTemporaryFile() as filtered_output_file:
            parse_dump(input_dumpfile, filtered_output_file.name, ['python/trunk/Include'], True, opt)
            diff = self.filtered_dumpfile_differences(expected_filtered_dumpfile, filtered_output_file.name)
        print(diff)
        self.assertEqual(b'', diff)

    def test_empty_revs_message(self):
        """ Test correctly filtering empty revs with a custom message """
        input_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'test_nodes_empty_revs_dump')
        expected_filtered_dumpfile = PurePath(self.DUMPFILE_DIRECTORY, 'expected_existing_node_excluded_empty_revs_message')
        opt = self.OPTIONS()

        opt.renumber_revs = False
        with NamedTemporaryFile() as filtered_output_file:
            parse_dump(input_dumpfile, filtered_output_file.name, ['python/trunk/Doc/README'], False, opt)
            diff = self.filtered_dumpfile_differences(expected_filtered_dumpfile, filtered_output_file.name)
        self.assertEqual(b'', diff)
