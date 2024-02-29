Contains gzip'ed svnrdump results of the python source code revisions 1 -> 89071
split into 2 files. To restore to original form on Linux:
   % cat pydumpa* > python.dump.gz
   % gzip -d python.dump.gz
   %  md5sum python.dump 
   3c65f4a7268fb989b7e63b1b72623047  python.dump

Should you encounter the following error when importing the dumpfile into a new
repository:
    svnadmin: E14001: Dump stream contains a malformed header (with no ':') at '* Dumped revision 0.
It can be fixed with:
    % grep --binary-files=text -v '^* Dumped revision' python.dump > python.dump.cleaned
