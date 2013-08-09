#!/usr/bin/env python

from svndumpfilter import *
from nose.tools import *


def path_match_exclude(expected, excluded):
  """
  Returns true if path is included.
  """
  check = MatchFiles(False)
  for item in excluded:
    check.add_to_matches(item)
  for path, result in expected.iteritems():
    assert check.is_included(path) == result
  return True

def path_match_include(expected, included):
  """
  Returns true if path is included.
  """
  check = MatchFiles(True)
  for item in included:
    check.add_to_matches(item)
  for path, result in expected.iteritems():
    assert check.is_included(path) == result

def test_path_include_1():
  """
  Tests path inclusion with a 1-level inclusion parameter.
  """
  expected = {"exclude_me": False, "exclude_me/file1.txt":False, "include_me":True,
            "include_me/file1.txt":True, "include_me/exclude_me/file1.txt":True,
            "include_me/exclude_me":True, "exclude_me/include_me":False}
  included = ["include_me"]
  path_match_include(expected, included)

def test_path_include_2():
  """
  Tests path inclusion with a 2-level inclusion parameter.
  """
  expected = {"foon":False, "foo": False, "foo/boon":False, "foo/boon/file1.txt":False,
             "foo/bar":True, "foo/bar/file1.txt":True, "foon/bar":False,
             "foon/var/file.txt":False, "bar":False}
  included = ["foo/bar"]
  path_match_include(expected, included)

def test_path_exclude_1():
  """
  Tests path exclusion with a 1-level exclusion parameter.
  """
  expected = {"exclude_me": False, "exclude_me/file1.txt":False, "include_me":True,
            "include_me/file1.txt":True, "include_me/exclude_me/file1.txt":True,
            "include_me/exclude_me":True, "exclude_me/include_me":False}
  excluded = ["exclude_me"]
  path_match_exclude(expected, excluded)

def test_path_exclude_2():
  """
  Tests path exclusion with a 2-level exclusion parameter.
  """
  expected = {"foon":True, "foo": True, "foo/boon": True, "foo/boon/file1.txt":True,
            "foo/bar":False, "foo/bar/file1.txt":False, "foon/bar":True,
            "foon/var/file.txt":True, "bar":True}
  excluded = ["foo/bar"]
  path_match_exclude(expected, excluded)

def test_add_dependents_1():
  """
  Path coconut/branches is added.
  """
  check = MatchFiles(True)
  check.add_to_matches("coconut/branches")
  check.add_to_matches("User")
  to_write = []
  add_dependents(to_write, check.matches)
  actual_paths = [node.head["Node-path"] for node in to_write]
  expected_paths = ["coconut"]
  assert actual_paths == expected_paths

def test_add_dependents_2():
  """
  Nothing has been added.
  """
  check = MatchFiles(True)
  to_write = []
  add_dependents(to_write, check.matches)
  actual_paths = [node.head["Node-path"] for node in to_write]
  expected_paths = []
  assert actual_paths == expected_paths

def test_add_dependents_3():
  """
  Path coconut/branches is added.
  Path coconut/branches/testname is added.
  Path test/testme/test3 is added.
  Path test is added.
  Path whoop/whoo/woon is added.
  """
  check = MatchFiles(True)
  check.add_to_matches("coconut/branches")
  check.add_to_matches("coconut/branches/testname")
  check.add_to_matches("test/testme/test3")
  check.add_to_matches("test")
  check.add_to_matches("whoop/whoo/woon")
  to_write = []
  add_dependents(to_write, check.matches)
  actual_paths = [node.head["Node-path"] for node in to_write]
  expected_paths = ["whoop", "coconut", "whoop/whoo"]
  assert actual_paths == expected_paths
