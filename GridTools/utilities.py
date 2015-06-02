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

import zlib
import logging


def get_adler32(filename):
    logging.info("In utilities.get_adler32")
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
    logging.info("In utilities.readin_file")
    directory = []
    file_path = []
    filename = []
    words = []
    with open(textfile, 'r') as f:
        data = f.readlines()
        for line in data:
            line = line.translate(None, '\n\t ')
            words.append(line.split(','))
        directory, file_path, filename = zip(*words)
    logging.info("directory = %s", directory)
    logging.info("file_path = %s", file_path)
    logging.info("filename = %s", filename)
    return directory, file_path, filename


def split_filename(filenamepath):
    # if the local file isn't in GridTools
    # splits the filename away from the path and so can use different
    # paths on grid but the same filename.
    logging.info("In utilities.split_filename")
    filename = []
    words = []
    word = []
    for line in filenamepath:
        words.append(line.rstrip('\n').split('/'))
    numberOfFiles = len(words)
    print numberOfFiles
    for i in range(numberOfFiles):
        filename.append(words[i][-1])
    logging.info(filename)
    return filename
