import unittest

from ..svndumpfilter import MatchFiles, add_dependents


DUMP_VERSIONS = [2, 3]


class PathMethodTestCase(unittest.TestCase):

    def path_match_exclude(self, expected, excluded):
        """
        Returns true if path is included.
        """
        check = MatchFiles(False)
        for item in excluded:
            check.add_to_matches(item)
        for path, result in iter(expected.items()):
            self.assertEqual(check.is_included(path), result)
        return True

    def path_match_include(self, expected, included):
        """
        Returns true if path is included.
        """
        check = MatchFiles(True)
        for item in included:
            check.add_to_matches(item)
        for path, result in iter(expected.items()):
            self.assertEqual(check.is_included(path), result)

    def test_path_include_1(self):
        """
        Tests path inclusion with a 1-level inclusion parameter.
        """
        expected = {"exclude_me": False, "exclude_me/file1.txt": False, "include_me": True,
                    "include_me/file1.txt": True, "include_me/exclude_me/file1.txt": True,
                    "include_me/exclude_me": True, "exclude_me/include_me": False}
        included = ["include_me"]
        self.path_match_include(expected, included)

    def test_path_include_2(self):
        """
        Tests path inclusion with a 2-level inclusion parameter.
        """
        expected = {"foon": False, "foo": False, "foo/boon": False, "foo/boon/file1.txt": False,
                    "foo/bar": True, "foo/bar/file1.txt": True, "foon/bar": False,
                    "foon/var/file.txt": False, "bar": False}
        included = ["foo/bar"]
        self.path_match_include(expected, included)

    def test_path_exclude_1(self):
        """
        Tests path exclusion with a 1-level exclusion parameter.
        """
        expected = {"exclude_me": False, "exclude_me/file1.txt": False, "include_me": True,
                    "include_me/file1.txt": True, "include_me/exclude_me/file1.txt": True,
                    "include_me/exclude_me": True, "exclude_me/include_me": False}
        excluded = ["exclude_me"]
        self.path_match_exclude(expected, excluded)

    def test_path_exclude_2(self):
        """
        Tests path exclusion with a 2-level exclusion parameter.
        """
        expected = {"foon": True, "foo": True, "foo/boon": True, "foo/boon/file1.txt": True,
                    "foo/bar": False, "foo/bar/file1.txt": False, "foon/bar": True,
                    "foon/var/file.txt": True, "bar": True}
        excluded = ["foo/bar"]
        self.path_match_exclude(expected, excluded)

    def test_add_dependents_1(self):
        """
        Path coconut/branches is added.
        """
        for dump_version in DUMP_VERSIONS:
            check = MatchFiles(True)
            check.add_to_matches("coconut/branches")
            check.add_to_matches("User")
            to_write = []
            add_dependents(to_write, check.matches, dump_version)
            actual_paths = [node.head["Node-path"] for node in to_write]
            expected_paths = ["coconut"]
            self.assertEqual(actual_paths, expected_paths)

    def test_add_dependents_2(self):
        """
        Nothing has been added.
        """
        for dump_version in DUMP_VERSIONS:
            check = MatchFiles(True)
            to_write = []
            add_dependents(to_write, check.matches, dump_version)
            actual_paths = [node.head["Node-path"] for node in to_write]
            expected_paths = []
            self.assertEqual(actual_paths, expected_paths)

    def test_add_dependents_3(self):
        """
        Path coconut/branches is added.
        Path coconut/branches/testname is added.
        Path test/testme/test3 is added.
        Path test is added.
        Path whoop/whoo/woon is added.
        """
        for dump_version in DUMP_VERSIONS:
            check = MatchFiles(True)
            check.add_to_matches("coconut/branches")
            check.add_to_matches("coconut/branches/testname")
            check.add_to_matches("test/testme/test3")
            check.add_to_matches("test")
            check.add_to_matches("whoop/whoo/woon")
            to_write = []
            add_dependents(to_write, check.matches, dump_version)
            actual_paths = [node.head["Node-path"] for node in to_write]
            expected_paths = ["whoop", "coconut", "whoop/whoo"]
            self.assertEqual(set(actual_paths), set(expected_paths))
