svndumpfilterIN
===============


An implementation of Apache's svndumpfilter that solves some common problems.


## Requirements ##

Latest version of svndumpfilterIN was updated on:

  * Python 3.9.18
  * Pytest 8.0.0
  * Ubuntu 20.04.06 LTS


##  Usage  ##


**WARNING** Before starting the filter, make sure that the user running it has sufficient permissions to perform svnlook on your
target directory.


    Usage: svndumpfilter.py [OPTIONS] <input_dump> <SUBCOMMAND> [args]



Example Usage:

    sudo python3 svndumpfilter.py input_name.dump include directory_name -r repo_path -o output_name.dump

Runs the svndumpfilter on `input_name.dump` from `repo_path` to carve out `directory_name`
and save the result to `output_name.dump`.

See also `python3 svndumpfilter.py --help`.

## Implementation ##


The filter relies on svnlook to pull excluded files/directories that are eventually moved into included
directories.


## Features ##


1. Drops empty revision record when all node records are excluded from revision

  Example : You have a revision record, but all the paths are for excluded directories.
  The result is that the node record will not show up in the final dump file.

2. Renumbers revisions based on revisions that were dropped.

  Example: There are 5 revisions and 3 revisions are empty because all their node records are for excluded paths.
  You will have an output dump file with 2 revisions, numbered Revision 1 and Revision 2.

3. Scan-only mode where a quick scan of the dump file is done to detect whether untangling repositories will be
necessary.

  Example of untangling: You have a node record that has a `copyfrom-path` that refers to an excluded directory.
  You will need to untangle this by retrieving information about the file that you are copying from and add
  it to a prior node record.

4. Ability to strip `svn:mergeinfo` properties.

  Example: You can strip svn:mergeinfo properties. Svnadmin tries to resolve merge info from `svn:mergeinfo` properties,
  and in case of heavy filtering they are broken because of the dropped revisions. Such dumps cause svnadmin to fail import. 

  Arguments: `-x`, `--strip-mergeinfo`.

5. Ability to start filtering at any revision.

  Example: You can start filtering at revision 100 if you have already loaded the first 100 previously from
  another dump file.

6. Automatically untangles revisions.

  Example: Whenever you reference an excluded path from an included node-path, you will automatically have the
  excluded data loaded in a prior record.

7. Path matching is done on more than just the top-level.
 
  Example: You can match to `repo/dir1/dir2` which is more than the `repo/dir1/` which is as deep as some filters
  can match to.

7. Added functionality to add dependent directories due to matching at more than the top-level.

  Example: If you match at more than a top-level, you will need to add dependents for paths that are more than 1
  level deep. For example, if you only include `repo/dir1`, you will need to have a node add `repo` before the
  node record that adds `repo/dir1`.

9. Paths to include/exclude can now be read from a file.

  Example: You can now add `--file` to specify a file to read matched paths from.

10. Property tags are added to differentiate dump filter generated items.

  Example: For the property header, a key, `K 23` as `svndumpfilter generated`, is appended with a value, `V 4`
  as `True`.


## Contributing / Issues ##


To file issue reports, use the project's issue tracker on GitHub.

When creating an issue, please provide a sample of the dump file that is creating the problem or provide a method to
reproduce it.

PRs are also welcome to the problems you encounter.

### <u>For development it is recommended use the following set up:</u> ###
   1. Use python version 3.10.13
   2. Set up a virtual environment:

          % cd <your_git_workspace>
          % python3 -m venv venv
          % source venv/bin/activate

      See [Virtual Environment and Packages](https://docs.python.org/3/tutorial/venv.html)
      for more details.
   3. Use pytest for running unit tests. To set up
      (once in your virutal environment):

          % pip install pytest

      See the [pytest documentation](https://docs.pytest.org/en) for more details.
   4. Use pycodestyle for adherence to style guidelines. To set up
      (once in your virutal environment):

          % pip install pycodestyle

      See the [pycodestyle documentation](https://pycodestyle.pycqa.org/en/latest/)
      for more details.

    5. Use Bandit to locate common secuity issues. To set up 
       (once in your virtual environment):
          % pip install bandit

      See the [Bandit documentation](https://bandit.readthedocs.io/en/latest/)
      for more details.

### <u>Prior to submitting a PR please:</u> ###
   1. Check your changes adhere to style guidelines by ensuring
      the following passes with no complaints:

          % pycodestyle *.py 

   2. Add unit test(s) to test_svndumpfilter.py demonstrating the
      problem and fix in your patch.
   3. Ensure all unit tests pass using pytest:

          % pytest test

   4. Ensure no security issues have been introduced using Bandit:

          % bandit --ini tox.ini --exclude ./venv -r 

### <u>GitHub actions:</u> ###

   * The above prior requirements for submitting a PR will also be
     checked by an equivalent set of GitHub actions

### <u>Svndump format:</u> ###

   * The most useful documentation on the [svndump format](https://svn.apache.org/repos/asf/subversion/trunk/notes/dump-load-format.txt) can be on the 
     [Apache Subversion Server](https://svn.apache.org/)




