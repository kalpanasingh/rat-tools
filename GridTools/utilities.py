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


def read_grabber_file(filename):
    copy_type = None
    files = []
    sizes = []
    guids = []
    adlers = []
    with open(filename, "r") as fin:
        copy_type = fin.readline().strip()
        if copy_type!="GUID" and copy_type!="SURL":
            raise Exception("Unknown copy type")
        for line in fin.readlines():
            f, s, g, a = line.split()
            files.append(f.strip())
            sizes.append(int(s.strip()))
            guids.append(g.strip())
            adlers.append(a.strip())
    return copy_type, files, sizes, guids, adlers
