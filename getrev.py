#! /usr/bin/env python3

# Simple script to pull a specific revision from a dump file

import argparse
import os
import sys


def main():

    parser = argparse.ArgumentParser(description='Dump a revision record from a svn dump file')
    parser.add_argument('-f', '--file', dest='dump_file', required=True, type=str, help='The svn dump file to pull the revision from.')
    parser.add_argument('-r', '--revision', dest='revision', required=True, type=int, help='The revision to pull from the dump file.')
    args = parser.parse_args()
    revision_locator = 'Revision-number: {0}'.format(args.revision)
    with open(args.dump_file, 'rb') as fd:
        line = fd.readline().decode()
        buffer = []
        in_revision = False
        binary = False
        while line:
            if in_revision:
                if binary:
                    buffer.append((binary, line))
                elif line.startswith('Revision'):
                    break
                else:
                    buffer.append((binary, line))
            if not binary and line.startswith('Revision'):
                if line.startswith(revision_locator):
                    buffer.append((binary, line))
                    in_revision = True
            next_line = fd.readline()
            try:
                line = next_line.decode()
                binary = False
            except UnicodeDecodeError:
                line = next_line
                binary = True
        with os.fdopen(sys.stdout.fileno(), 'wb', closefd=False) as stdout:
            for binary, revision_line in buffer:
                if binary:
                    stdout.write(revision_line)
                else:
                    stdout.write(revision_line.encode())
            stdout.flush()


if __name__ == '__main__':
    main()
