#! /usr/bin/env python

# Simple script to pull a specific revision from a dump file

import argparse


def main():

    parser = argparse.ArgumentParser(description='Dump a revision record from a svn dump file')
    parser.add_argument('-f', '--file', dest='dump_file', required=True, type=str, help='The svn dump file to pull the revision from.')
    parser.add_argument('-r', '--revision', dest='revision', required=True, type=int, help='The revision to pull from the dump file.')
    args = parser.parse_args()
    revision_locator = 'Revision-number: {0}'.format(args.revision)
    with open(args.dump_file, 'r') as fd:
        line = fd.readline()
        buffer = []
        in_revision = False
        while line:
            if in_revision:
                if line.startswith('Revision'):
                    break
                else:
                    buffer.append(line)
            if line.startswith('Revision'):
                if line.startswith(revision_locator):
                    buffer.append(line)
                    in_revision = True
            line = fd.readline()
        print '{0}'.format(''.join(buffer))

if __name__ == '__main__':
    main()
