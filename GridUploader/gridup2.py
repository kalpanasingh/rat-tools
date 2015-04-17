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
try:
    import argparse
except:
    raise ImportError("argparse not availbel; python version needs to \
                      be 2.7+")
sys.path.insert(0,'../GridGrabber')
import grid
import database

#####################################
#Code for uploading
#####################################

def readin_file(textfile):
    directory = []
    file_path = []
    filename = []
    storage = []
    i = 0
    words = []
    with open(textfile, 'r') as f:
        data = f.readlines()
        for line in data:
            line = line.translate(None,'\n\t ')
            words.append(line.split(','))
            i+=1
        words_array = numpy.array(words)
        if words_array.shape[1] == 3:
            storage = 'sehn02.atlas.ualberta.ca'
        elif words_array.shape[1] == 4:
            storage = words_array[:, 3]
        else:
            print "Not correct number of inputs"
            print "should be:"
            str1 = repr("<base directory>,<path>,<file>")
            str2 = ("and optional ,<storage endpoint>)")
            str3 = "%s %s" % (str1,str2)
            print str3
            print "you have used"
            for j in words_array:
                print str(words_array[j])
            sys.exit()
            return 0
        #print (words_array)
        directory = words_array[:, 0]
        file_path = words_array[:, 1]
        filename = words_array[:, 2]
    print "next line storage"
    print storage
    return directory, file_path, filename, storage

#def get_file_size(filename):
#    size = []
#    i = 0
#    for line in filename:
#        size = os.path.getsize(filename[i])
#        print os.path.getsize(filename[i])
#        i+=1
#    return size

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
    gridid = []
    with open("Gridid.txt","w") as f:
        for s in directory:
            se_path = os.path.join(directory[i],path[i],filename[i])
            se_path.strip()
            print se_path
            lfc_path = 'lfn:%s' % os.path.join(griddir,directory[i],path[i],
                                           filename[i])
            print lfc_path
            upfile = filename[i]
            inputstring = 'lcg-cr --vo snoplus.snolab.ca --checksum -d %s \
            -P %s -l %s %s'%(storage[i],se_path,lfc_path,upfile)
            #gridid[i] = os.popen(inputstring).readlines()
            gridid.append(os.popen(inputstring).readlines()[0])
            str1 = str(filename[i])
            # str2 = str(size[i])
            str3 = str(gridid[i])
            outline = "%s \t %s" % (str1,str3)
            f.write(outline)
            i += 1
    f.close()
    return gridid

def database_file(directory, path, filename, gridid):
    prod_data_doc = None
		#    prod_data_doc = document.ProdDataDocument.new_doc(db=self.job_doc.db, module=self._name,pass_number=self._pass, run=self._run, rat_version=self.job_doc.get_rat_version())
	#database.connect_db("couch.snopl.us", None, test)
    return 0

def split_filename(filenamepath):
    filename = []
    words = []
    for line in filenamepath:
        words.append(line.rstrip('\n').split('/'))
        print words
    filename_array = numpy.array(words)
    numberOfFiles = filename_array.shape[0]
    for i in range(numberOfFiles):
        filename.append(filename_array[i][-1])
    print filename
    return filename

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l",dest="list", help="list of files to upload\
                        [in_text.txt]",default="in_text.txt")
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
    Directory, Path, FilenamePath, Storage = readin_file(args.list)
    Filename = split_filename(FilenamePath)
    if base_directory(Directory) != True:
        print "not valid base directory"
        exit()
    #Size = get_file_size(Filename)
    #print Size
    Griddir = '/grid/snoplus.snolab.ca'
    Gridid = grid_file(Griddir, Directory, Path, Filename, Storage)
    database_file(Directory, Path, Filename, Gridid)
    print Gridid
    
