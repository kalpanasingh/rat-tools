#!/usr/bin/env python
#####################
#
# gridup2.py
#
# For use to upload to the grid with
# correct file naming
#
# For uploading files
#
# Author: David Auty
#         <auty@ualberta.ca>
#
#####################

import os
import sys
import re
import numpy
import argparse

sys.path.insert(0,'../GridGrabber')
import grid
#import database

#####################################
#Code for uploading
#####################################

def readin_file(textfile):
    directory = []
    file_path = []
    filename = []
    i = 0
    words = []
    with open(textfile, 'r') as f:
        data = f.readlines()
        for line in data:
            words.append(line.rstrip('\n').split('\t'))
            i+=1
        words_array = numpy.array(words)
        if words_array.shape[1] == 3:
            storage = 'sehn02.atlas.ualberta.ca'
        elif words_array.shape[1] == 4:
            storage == words_array[:, 3]
        else:
            print "Not correct number of inputs"
            print "should be:"
            str1 = repr("<base directory> \t <path> \t <file> \t")
            str2 = ("and optional <storage endpoint>)")
            str3 = "%s %s" % (str1,str2)
            print str3
            sys.exit()
            return 0
        directory = words_array[:, 0]
        file_path = words_array[:, 1]
        filename = words_array[:, 2]
    return directory, file_path, filename, storage

def base_directory(directory):
    i=0
    for entry in directory:
        if directory[i] == 'user':
	    return True
        elif directory[i] == 'sw':
            return True
        elif directory[i] == 'snotflow':
            return True
        elif directory[i] == 'production_testing':
            return True
	elif directory[i] == 'production':
            return True
        elif directory == 'nearline':
            return True
        else:
	    print directory[i]
            return False
        i += 1

def grid_file(griddir, directory, path, filename, storage):
    i = 0
    command = 'lcg-cr'
    gridid = {}
    for s in directory:
        se_path = os.path.join(directory[i],path[i],filename[i])
        se_path.strip()
        print se_path
        lfc_path = 'lfn:%s' % os.path.join(griddir,directory[i],path[i],
                                           filename[i])
        print lfc_path
        upfile = filename[i]
        inputstring = 'lcg-cr --vo snoplus.snolab.ca --checksum -d %s \
        -P %s -l %s %s'%(storage,se_path,lfc_path,upfile)
        gridid[i] = os.popen(inputstring).readlines()
        i += 1
    return gridid

def database_file(directory, path, filename, gridid):
    prod_data_doc = None
		#    prod_data_doc = document.ProdDataDocument.new_doc(db=self.job_doc.db, module=self._name,pass_number=self._pass, run=self._run, rat_version=self.job_doc.get_rat_version())
	#database.connect_db("couch.snopl.us", None, test)
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l",dest="list", help="list of files to upload\
                        [in_text.txt",default="in_text.txt")
    args = parser.parse_args()
    if not grid.proxy_time():
        print "Need to generate a grid proxy"
        if not grid.proxy_create():
            print "Proxy successfully created"
        else:
            str1 = "Unable to create proxy; try 'voms-proxy-init --voms"
            str2 = "snoplus.snolab.ca' in shell"
            str3 = "%s %s" % (str1,str2)
            print str3
            sys.exit()
    Directory, Path, Filename, Storage = readin_file(args.list)
    if base_directory(Directory) != True:
        print "not valid base directory"
        exit()
    Griddir = '/grid/snoplus.snolab.ca'
    Gridid = grid_file(Griddir, Directory, Path, Filename, Storage)
    database_file(Directory, Path, Filename, Gridid)
    print Gridid
