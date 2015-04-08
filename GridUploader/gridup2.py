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
    i =0
    words = []
    with open(textfile, 'r') as f:
        data = f.readlines()
        for line in data:
            words.append(line.rstrip('\n').split('\t'))
            i+=1
        words_array = numpy.array(words)
        directory = words_array[:,0]
        file_path = words_array[:,1]
        filename = words_array[:,2]
        if words_array.shape[1] == 3:
            storage = 'sehn02.atlas.ualberta.ca'
        elif words_array.shape[1] == 4:
						storage == words_array[:,3]
        else:
						print "Not correct number of inputs\n"
						print "should be\n base directory \t path \t file \t and optional storage endpoint "
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
        i+=1

def grid_file(griddir,directory,path,filename,storage):
    i=0
    command = 'lcg-cr'
    for s in directory:
        se_path = '%s/%s/%s'%(directory[i],path[i],filename[i])
        se_path.strip()
        lfc_path = 'lfn:%s/%s/%s/%s'%(griddir,directory[i],path[i],filename[i])
        upfile = filename[i]
        inputstring = 'lcg-cr --vo snoplus.snolab.ca --checksum -d %s -P %s -l %s %s'%(storage,se_path,lfc_path,upfile)
        args = ['--vo', 'snoplus.snolab.ca', '--checksum', '-d', storage, '-P', se_path, '-l', lfc_path, upfile]
        #rtc, out, err = execute(command, args)
        # os.system(inputstring)
        gridid = os.popen(inputstring).readlines()
        i+=1
        # print inputstring
    return gridid

def database_file(directory,path,filename,gridid):
    prod_data_doc = None
		#    prod_data_doc = document.ProdDataDocument.new_doc(db=self.job_doc.db, module=self._name,pass_number=self._pass, run=self._run, rat_version=self.job_doc.get_rat_version())
	#database.connect_db("couch.snopl.us", None, test)
    return 0


if __name__ == '__main__':
    Textfile = 'in_text.txt'
    Griddir = '/grid/snoplus.snolab.ca'
    if not grid.proxy_time():
        print "Need to generate a grid proxy"
        if not grid.proxy_create():
            print "Proxy successfully created"
        else:
             print "Unable to create proxy; try 'voms-proxy-init --voms snoplus.snolab.ca' in shell"
             sys.exit()
    Directory, Path, Filename, Storage = readin_file(Textfile)
    if base_directory(Directory) != True:
        print "not valid base directory"
        exit()
    Gridid = grid_file(Griddir, Directory, Path, Filename, Storage)
    database_file(Directory,Path,Filename,Gridid)
    print Gridid
