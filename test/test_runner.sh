#! /bin/bash

# Program versions
NEW_VERSION="../svndumpfilter.py"
ORIG_VERSION="./svndumpfilter_orig.py"

# Repositories
REPO_PATH="../repos/python"

# Test signatures
EMPTY_REVS="empty_revs"
NODES_EMPTY_REVS="nodes_empty_revs"
MERGEINFO_REVS="mergeinfo"

# Input dump files
EMPTY_REVS_DUMP="test_${EMPTY_REVS}_dump"
NODES_EMPTY_REVS_DUMP="test_${NODES_EMPTY_REVS}_dump"
MERGEINFO_REVS_DUMP="test_${MERGEINFO_REVS}_dump"

# Output dump files
FILTERED_EMPTY_REVS_DUMP="${EMPTY_REVS}_filtered_dump"
FILTERED_NODES_EMPTY_REVS_DUMP="${NODES_EMPTY_REVS}_filtered_dump"
FILTERED_MERGEINFO_REVS_DUMP="${MERGEINFO_REVS}_filtered_dump"

# Filter execution output files
FILTERED_EMPTY_REVS_OUTPUT="${EMPTY_REVS}_filtered_dump.out"
FILTERED_NODES_EMPTY_REVS_OUTPUT="${NODES_EMPTY_REVS}_filtered_dump.out"
FILTERED_MERGEINFO_REVS_OUTPUT="${MERGEINFO_REVS}_filtered_dump.out"

# Tests
TEST_EMPTY_REVS_REMOVED="Test filtered dump with empty revisions only (removed)"
TEST_EMPTY_REVS_PRESERVED="Test filtered dump with empty revisions only (preserved)"
TEST_EMPTY_REVS_PRESERVED_NO_RENUMBER="Test filtered dump with empty revisions only (preserved), stop renumbering"
TEST_NON_EXISTING_EXCLUDED_NODE_EMPTY_REVS_REMOVED="Test filtered dump with empty revisions (removed), non-existing node (excluded)"
TEST_NON_EXISTING_EXCLUDED_NODE_EMPTY_REVS_PRESERVED="Test filtered dump with empty revisions (preserved), non-existing node (excluded)"
TEST_EXISTING_EXCLUDED_NODE_EMPTY_REVS_REMOVED="Test filtered dump with empty revisions (removed), existing node (excluded)"
TEST_EXISTING_INCLUDED_NODE_EMPTY_REVS_REMOVED="Test filtered dump with empty revisions (removed), existing node (included)"
TEST_MERGEINFO_REMOVAL="Test filtered dump of svn:mergeinfo properties"

# Test empty revisions dump
echo "STARTING: ${TEST_EMPTY_REVS_REMOVED}"

${ORIG_VERSION} -o ${FILTERED_EMPTY_REVS_DUMP}.orig -r ${REPO_PATH} ${EMPTY_REVS_DUMP} exclude foo >& ${FILTERED_EMPTY_REVS_OUTPUT}.orig
if [ $? -ne 0 ]; then
   echo "Original dump filtered execution failed. See command output ${FILTERED_EMPTY_REVS_OUTPUT}.orig"
   exit 1
fi
${NEW_VERSION} -o ${FILTERED_EMPTY_REVS_DUMP} -r ${REPO_PATH} ${EMPTY_REVS_DUMP} exclude foo >& ${FILTERED_EMPTY_REVS_OUTPUT}
if [ $? -ne 0 ]; then
   echo "New dump filtered execution failed. See command output ${FILTERED_EMPTY_REVS_OUTPUT}"
   exit 1
fi
diff ${FILTERED_EMPTY_REVS_DUMP}.orig ${FILTERED_EMPTY_REVS_DUMP} >& diff.out
if [ $? -ne 0 ]; then
   echo "FAILED:   ${TEST_EMPTY_REVS_REMOVED}"
   echo "Original and new filtered dump files are not the same"
   echo "Diff of dump files: diff.out"
   echo "Original filtered dump file: ${FILTERED_EMPTY_REVS_DUMP}.orig"
   echo "New filtered dump file: ${FILTERED_EMPTY_REVS_DUMP}"
   exit 1
fi
echo "PASSED:   ${TEST_EMPTY_REVS_REMOVED}"
   
# Test empty revisions dump, empty revisions preserved
echo "STARTING: ${TEST_EMPTY_REVS_PRESERVED}"

${ORIG_VERSION} -k -o ${FILTERED_EMPTY_REVS_DUMP}.orig -r ${REPO_PATH} ${EMPTY_REVS_DUMP} exclude foo >& ${FILTERED_EMPTY_REVS_OUTPUT}.orig
if [ $? -ne 0 ]; then
   echo "Original dump filtered execution failed. See command output ${FILTERED_EMPTY_REVS_OUTPUT}.orig"
   exit 1
fi
${NEW_VERSION} -k -o ${FILTERED_EMPTY_REVS_DUMP} -r ${REPO_PATH} ${EMPTY_REVS_DUMP} exclude foo >& ${FILTERED_EMPTY_REVS_OUTPUT}
if [ $? -ne 0 ]; then
   echo "New dump filtered execution failed. See command output ${FILTERED_EMPTY_REVS_OUTPUT}"
   exit 1
fi
diff ${FILTERED_EMPTY_REVS_DUMP}.orig ${FILTERED_EMPTY_REVS_DUMP} >& diff.out
if [ $? -ne 0 ]; then
   echo "FAILED:   ${TEST_EMPTY_REVS_PRESERVED}"
   echo "Original and new filtered dump files are not the same"
   echo "Diff of dump files: diff.out"
   echo "Original filtered dump file: ${FILTERED_EMPTY_REVS_DUMP}.orig"
   echo "New filtered dump file: ${FILTERED_EMPTY_REVS_DUMP}"
   exit 1
fi
echo "PASSED:   ${TEST_EMPTY_REVS_PRESERVED}"
   
# Test empty revisions dump, empty revisions preserved, stop renumbering
echo "STARTING: ${TEST_EMPTY_REVS_PRESERVED_NO_RENUMBER}"

${ORIG_VERSION} -k -s -o ${FILTERED_EMPTY_REVS_DUMP}.orig -r ${REPO_PATH} ${EMPTY_REVS_DUMP} exclude foo >& ${FILTERED_EMPTY_REVS_OUTPUT}.orig
if [ $? -ne 0 ]; then
   echo "Original dump filtered execution failed. See command output ${FILTERED_EMPTY_REVS_OUTPUT}.orig"
   exit 1
fi
${NEW_VERSION} -k -s -o ${FILTERED_EMPTY_REVS_DUMP} -r ${REPO_PATH} ${EMPTY_REVS_DUMP} exclude foo >& ${FILTERED_EMPTY_REVS_OUTPUT}
if [ $? -ne 0 ]; then
   echo "New dump filtered execution failed. See command output ${FILTERED_EMPTY_REVS_OUTPUT}"
   exit 1
fi
diff ${FILTERED_EMPTY_REVS_DUMP}.orig ${FILTERED_EMPTY_REVS_DUMP} >& diff.out
if [ $? -ne 0 ]; then
   echo "FAILED:   ${TEST_EMPTY_REVS_PRESERVED_NO_RENUMBER}"
   echo "Original and new filtered dump files are not the same"
   echo "Diff of dump files: diff.out"
   echo "Original filtered dump file: ${FILTERED_EMPTY_REVS_DUMP}.orig"
   echo "New filtered dump file: ${FILTERED_EMPTY_REVS_DUMP}"
   exit 1
fi
echo "PASSED:   ${TEST_EMPTY_REVS_PRESERVED_NO_RENUMBER}"
   
# Test node and empty revisions dump, empty revisions removed, non-existing node excluded 
echo "STARTING: ${TEST_NON_EXISTING_EXCLUDED_NODE_EMPTY_REVS_REMOVED}"

${ORIG_VERSION} -o ${FILTERED_NODES_EMPTY_REVS_DUMP}.orig -r ${REPO_PATH} ${NODES_EMPTY_REVS_DUMP} exclude foo >& ${FILTERED_NODES_EMPTY_REVS_OUTPUT}.orig
if [ $? -ne 0 ]; then
   echo "Original dump filtered execution failed. See command output ${FILTERED_NODES_EMPTY_REVS_OUTPUT}.orig"
   exit 1
fi
${NEW_VERSION} -o ${FILTERED_NODES_EMPTY_REVS_DUMP} -r ${REPO_PATH} ${NODES_EMPTY_REVS_DUMP} exclude foo >& ${FILTERED_NODES_EMPTY_REVS_OUTPUT}
if [ $? -ne 0 ]; then
   echo "New dump filtered execution failed. See command output ${FILTERED_NODES_EMPTY_REVS_OUTPUT}"
   exit 1
fi
diff ${FILTERED_NODES_EMPTY_REVS_DUMP}.orig ${FILTERED_NODES_EMPTY_REVS_DUMP} >& diff.out
if [ $? -ne 0 ]; then
   echo "FAILED:   ${TEST_NON_EXISTING_EXCLUDED_NODE_EMPTY_REVS_REMOVED}"
   echo "Original and new filtered dump files are not the same"
   echo "Diff of dump files: diff.out"
   echo "Original filtered dump file: ${FILTERED_NODES_EMPTY_REVS_DUMP}.orig"
   echo "New filtered dump file: ${FILTERED_NODES_EMPTY_REVS_DUMP}"
   exit 1
fi
echo "PASSED:   ${TEST_NON_EXISTING_EXCLUDED_NODE_EMPTY_REVS_REMOVED}"

# Test node and empty revisions dump, empty revisions preserved, non-existing node excluded 
echo "STARTING: ${TEST_NON_EXISTING_EXCLUDED_NODE_EMPTY_REVS_PRESERVED}"

${ORIG_VERSION} -k -o ${FILTERED_NODES_EMPTY_REVS_DUMP}.orig -r ${REPO_PATH} ${NODES_EMPTY_REVS_DUMP} exclude foo >& ${FILTERED_NODES_EMPTY_REVS_OUTPUT}.orig
if [ $? -ne 0 ]; then
   echo "Original dump filtered execution failed. See command output ${FILTERED_NODES_EMPTY_REVS_OUTPUT}.orig"
   exit 1
fi
${NEW_VERSION} -k -o ${FILTERED_NODES_EMPTY_REVS_DUMP} -r ${REPO_PATH} ${NODES_EMPTY_REVS_DUMP} exclude foo >& ${FILTERED_NODES_EMPTY_REVS_OUTPUT}
if [ $? -ne 0 ]; then
   echo "New dump filtered execution failed. See command output ${FILTERED_NODES_EMPTY_REVS_OUTPUT}"
   exit 1
fi
diff ${FILTERED_NODES_EMPTY_REVS_DUMP}.orig ${FILTERED_NODES_EMPTY_REVS_DUMP} >& diff.out
if [ $? -ne 0 ]; then
   echo "FAILED:   ${TEST_NON_EXISTING_EXCLUDED_NODE_EMPTY_REVS_PRESERVED}"
   echo "Original and new filtered dump files are not the same"
   echo "Diff of dump files: diff.out"
   echo "Original filtered dump file: ${FILTERED_NODES_EMPTY_REVS_DUMP}.orig"
   echo "New filtered dump file: ${FILTERED_NODES_EMPTY_REVS_DUMP}"
   exit 1
fi
echo "PASSED:   ${TEST_NON_EXISTING_EXCLUDED_NODE_EMPTY_REVS_PRESERVED}"

# Test node and empty revisions dump, empty revisions removed, existing node excluded 
echo "STARTING: ${TEST_EXISTING_EXCLUDED_NODE_EMPTY_REVS_REMOVED}"

${ORIG_VERSION} -o ${FILTERED_NODES_EMPTY_REVS_DUMP}.orig -r ${REPO_PATH} ${NODES_EMPTY_REVS_DUMP} exclude python/trunk/Doc/Makefile >& ${FILTERED_NODES_EMPTY_REVS_OUTPUT}.orig
if [ $? -ne 0 ]; then
   echo "Original dump filtered execution failed. See command output ${FILTERED_NODES_EMPTY_REVS_OUTPUT}.orig"
   exit 1
fi
${NEW_VERSION} -o ${FILTERED_NODES_EMPTY_REVS_DUMP} -r ${REPO_PATH} ${NODES_EMPTY_REVS_DUMP} exclude python/trunk/Doc/Makefile >& ${FILTERED_NODES_EMPTY_REVS_OUTPUT}
if [ $? -ne 0 ]; then
   echo "New dump filtered execution failed. See command output ${FILTERED_NODES_EMPTY_REVS_OUTPUT}"
   exit 1
fi
diff ${FILTERED_NODES_EMPTY_REVS_DUMP}.orig ${FILTERED_NODES_EMPTY_REVS_DUMP} >& diff.out
if [ $? -ne 0 ]; then
   echo "FAILED:   ${TEST_EXISTING_EXCLUDED_NODE_EMPTY_REVS_REMOVED}"
   echo "Original and new filtered dump files are not the same"
   echo "Diff of dump files: diff.out"
   echo "Original filtered dump file: ${FILTERED_NODES_EMPTY_REVS_DUMP}.orig"
   echo "New filtered dump file: ${FILTERED_NODES_EMPTY_REVS_DUMP}"
   exit 1
fi
echo "PASSED:   ${TEST_EXISTING_EXCLUDED_NODE_EMPTY_REVS_REMOVED}"

# Test node and empty revisions dump, empty revisions removed, existing node included
echo "STARTING: ${TEST_EXISTING_INCLUDED_NODE_EMPTY_REVS_REMOVED}"

${ORIG_VERSION} -o ${FILTERED_NODES_EMPTY_REVS_DUMP}.orig -r ${REPO_PATH} ${NODES_EMPTY_REVS_DUMP} include python/trunk/Doc/README >& ${FILTERED_NODES_EMPTY_REVS_OUTPUT}.orig
if [ $? -ne 0 ]; then
   echo "Original dump filtered execution failed. See command output ${FILTERED_NODES_EMPTY_REVS_OUTPUT}.orig"
   exit 1
fi
${NEW_VERSION} -o ${FILTERED_NODES_EMPTY_REVS_DUMP} -r ${REPO_PATH} ${NODES_EMPTY_REVS_DUMP} include python/trunk/Doc/README >& ${FILTERED_NODES_EMPTY_REVS_OUTPUT}
if [ $? -ne 0 ]; then
   echo "New dump filtered execution failed. See command output ${FILTERED_NODES_EMPTY_REVS_OUTPUT}"
   exit 1
fi
diff ${FILTERED_NODES_EMPTY_REVS_DUMP}.orig ${FILTERED_NODES_EMPTY_REVS_DUMP} >& diff.out
if [ $? -ne 0 ]; then
   echo "FAILED:   ${TEST_EXISTING_INCLUDED_NODE_EMPTY_REVS_REMOVED}"
   echo "Original and new filtered dump files are not the same"
   echo "Diff of dump files: diff.out"
   echo "Original filtered dump file: ${FILTERED_NODES_EMPTY_REVS_DUMP}.orig"
   echo "New filtered dump file: ${FILTERED_NODES_EMPTY_REVS_DUMP}"
   exit 1
fi
echo "PASSED:   ${TEST_EXISTING_INCLUDED_NODE_EMPTY_REVS_REMOVED}"

# Test svn:mergeinfo properties removal
echo "STARTING: ${TEST_MERGEINFO_REMOVAL}"

${ORIG_VERSION} -x -s -o ${FILTERED_MERGEINFO_REVS_DUMP}.orig -r ${REPO_PATH} ${MERGEINFO_REVS_DUMP} exclude foo >& ${FILTERED_MERGEINFO_REVS_OUTPUT}.orig
if [ $? -ne 0 ]; then
   echo "Original dump filtered execution failed. See command output ${FILTERED_MERGEINFO_REVS_OUTPUT}.orig"
   exit 1
fi
${NEW_VERSION} -x -s -o ${FILTERED_MERGEINFO_REVS_DUMP} -r ${REPO_PATH} ${MERGEINFO_REVS_DUMP} exclude foo >& ${FILTERED_MERGEINFO_REVS_OUTPUT}
if [ $? -ne 0 ]; then
   echo "New dump filtered execution failed. See command output ${FILTERED_MERGEINFO_REVS_OUTPUT}"
   exit 1
fi
diff ${FILTERED_MERGEINFO_REVS_DUMP}.orig ${FILTERED_MERGEINFO_REVS_DUMP} >& diff.out
if [ $? -ne 0 ]; then
   echo "FAILED:   ${TEST_MERGEINFO_REMOVAL}"
   echo "Original and new filtered dump files are not the same"
   echo "Diff of dump files: diff.out"
   echo "Original filtered dump file: ${FILTERED_MERGEINFO_REVS_DUMP}.orig"
   echo "New filtered dump file: ${FILTERED_MERGEINFO_REVS_DUMP}"
   exit 1
fi
echo "PASSED:   ${TEST_MERGEINFO_REMOVAL}"

