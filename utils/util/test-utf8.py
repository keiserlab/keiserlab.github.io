#!/usr/bin/env python
#
# KEISER 2018-06-08
#
# Util to check for non-UTF compliant files (yay Jekyll errors)
#
#import sys
import os

from optparse import OptionParser
import codecs


def testfile(infile):
    # https://stackoverflow.com/questions/3269293/how-to-write-a-check-in-python-to-see-if-file-is-valid-utf-8
    try:
        f = codecs.open(infile, encoding='utf-8', errors='strict')
        for line in f:
            pass
        #sys.exit(os.EX_OK)
    except UnicodeDecodeError:
        print "invalid utf-8: %s" % infile
        return
        #sys.exit(os.EX_SOFTWARE)
    except :
        print "misc err (%s): %s" % (sys.exc_info()[0], infile)
# end testfile

def main(indir):
    if indir.find(".git/") != -1: 
        print indir
        return
    for root, dirs, files in os.walk(indir):
        for f in files:
            testfile(os.path.join(root, f))
        for d in dirs:
            d = os.path.abspath(os.path.join(root, d))
            main(d)


if __name__ == '__main__':
    usage = 'usage: %prog [options] startdir'
    parser = OptionParser(usage)
    options,args = parser.parse_args()

    try:
        arg1, = args
    except:
        parser.error("Incorrect number of arguments")

    main(arg1)
# end __main__