#!/usr/bin/env python
#
# KEISER 2018-06-08
#
# Util to check for non-UTF compliant files (yay Jekyll errors)
#
import sys
import os
import codecs
import argparse


def testfile(infile):
    # https://stackoverflow.com/questions/3269293/how-to-write-a-check-in-python-to-see-if-file-is-valid-utf-8
    try:
        f = codecs.open(infile, encoding='utf-8', errors='strict')
        for line in f:
            pass
    except UnicodeDecodeError:
        print(f"invalid utf-8: {infile}")
        return
    except :
        print(f"misc err ({sys.exc_info()[0]}): {infile}")

def main(indir):
    if ".git/" in indir:
        print(indir)
        return
    for root, dirs, files in os.walk(indir):
        for f in files:
            testfile(os.path.join(root, f))
        for d in dirs:
            d = os.path.abspath(os.path.join(root, d))
            main(d)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check for non-UTF compliant files.')
    parser.add_argument('startdir', help='Directory to start checking')
    args = parser.parse_args()

    main(args.startdir)