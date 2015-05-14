#!/usr/bin/env python
#####################
#
# utilities.py
#
# Common functions that are used
# for many GridTools
#
#
#
# Author: David Auty
#         <auty@ualberta.ca>
#
#####################

import numpy
import os
import zlib

def get_adler32(filename):
    '''Calculate and return Alder32 checksum of file.
    '''
    block = 32 * 1024 * 1024
    val = 1
    f = open(filename, 'rb')
    while True:
        line = f.read(block)
        if len(line) == 0:
            break
        val = zlib.adler32(line, val)
        if val < 0:
            val += 2**32
    f.close()
    return hex(val)[2:10].zfill(8).lower()

def readin_file(textfile):
    # read in the text file and split up the input into the correct
    # varibles
    directory = []
    file_path = []
    filename = []
    words = []
    with open(textfile, 'r') as f:
        data = f.readlines()
        for line in data:
            line = line.translate(None, '\n\t ')
            words.append(line.split(','))
        words_array = numpy.array(words)
        if words_array.shape[1] != 3:
            print "Not correct number of inputs"
            print "should be:"
            print repr("<base directory>,<remote path>,<local file>")
            print "you have used inputs"
            print words_array.shape[1]
            sys.exit()
            return 0
        directory = words_array[:, 0]
        file_path = words_array[:, 1]
        filename = words_array[:, 2]
    return directory, file_path, filename

def delete_file(lfc_path):
    input_string = 'lcg-del -a %s' % (lfc_path)
    os.system(input_string)
    return

def delete_folder(lfc_path):
    input_string = 'lcg-del -d %s' % (lfc_path)
    os.system(input_string)
    return