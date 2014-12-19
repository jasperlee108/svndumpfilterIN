svndumpfilterIN
===============


An implementation of Apache's svndumpfilter that solves some common problems.


## Requirements ##


svndumpfilterIN was developed on a Linux machine using

  * Python 2.6.6
  * nosetests version 1.1.2


##  Usage  ##


**WARNING** Before starting the filter, make sure that the user running it has sufficient permissions to perform svnlook on your
target directory.


    Usage: svndumpfilter.py [OPTIONS] <input_dump> <SUBCOMMAND> [args]



Example Usage:

    sudo python svndumpfilter.py input_name.dump include directory_name -r repo_path -o output_name.dump

Runs the svndumpfilter on `input_name.dump` from `repo_path` to carve out `directory_name`
and save the result to `output_name.dump`.


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

4. Ability to start filtering at any revision.

  Example: You can start filtering at revision 100 if you have already loaded the first 100 previously from
  another dump file.

5. Automatically untangles revisions.

  Example: Whenever you reference an excluded path from an included node-path, you will automatically have the
  excluded data loaded in a prior record.

6. Path matching is done on more than just the top-level.
 
  Example: You can match to `repo/dir1/dir2` which is more than the `repo/dir1/` which is as deep as some filters
  can match to.

7. Added functionality to add dependent directories due to matching at more than the top-level.

  Example: If you match at more than a top-level, you will need to add dependents for paths that are more than 1
  level deep. For example, if you only include `repo/dir1`, you will need to have a node add `repo` before the
  node record that adds `repo/dir1`.

8. Paths to include/exclude can now be read from a file.

  Example: You can now add `--file` to specify a file to read matched paths from.

9. Property tags are added to differentiate dump filter generated items.

  Example: For the property header, a key, `K 23` as `svndumpfilter generated`, is appended with a value, `V 4`
  as `True`.


## Contributing / Issues ##


To file issue reports, use the project's issue tracker on GitHub.

When creating an issue, please provide a sample of the dump file that is creating the problem or provide a method to
reproduce it.

Patches are also welcome to the problems you encounter.




