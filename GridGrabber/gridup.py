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

###########################################
# File utilities
###########################################
def adler32(filename):
    '''Calculate and return Alder32 checksum of file.
        '''
    import zlib
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

#####################################
#Code for uploading
#####################################

def readin_file(textfile):
    #read in the text file and split up the input into the correct
    #varibles
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

#def get_file_size(filename):
#    size = []
#    i = 0
#    for line in filename:
#        size = os.path.getsize(filename[i])
#        print os.path.getsize(filename[i])
#        i+=1
#    return size

def base_directory(directory):
    #check that one of the offical base directories is used
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

def delete_file(lfc_path):
    input_string = 'lcg-del -a %s' % (lfc_path)
    os.system(input_string)
    return

def grid_file(griddir, directory, path, filename, storage, out_file, \
              remove):
    i = 0
    command = 'lcg-cr'
    gridid = []
    with open(out_file,"w") as f:
        for s in directory:
            se_path = os.path.join(directory[i],path[i],filename[i])
            se_path.strip()
            print se_path
            lfc_path = 'lfn:%s' % os.path.join(griddir,directory[i],path[i],
                                               filename[i])
            print lfc_path
            upfile = filename[i]
            input_string = 'lcg-cr --vo snoplus.snolab.ca --checksum -d %s \
                -P %s -l %s %s'%(storage,se_path,lfc_path,upfile)
            try:
                gridid.append(os.popen(input_string).readlines()[0])
            except:
                if remove:
                    delete_file(lfc_path)
                    try:
                        gridid.append(os.popen(input_string).readlines()[0])
                    except:
                        print "Can not overwrite file"
                        print upfile
                        continue
                    print "Deleted old GRID file and replaced with new file"
                else:
                    print "file already exists"
                    print upfile
                    continue
            str1 = str(filename[i])
            str2 = str(os.stat(filename[i]).st_size)
            str3 = str(gridid[i].rstrip('\n'))
            str4 = str(adler32(filename[i]))
            outline = "%s \t %s \t %s \t %s \n" % (str1,str2,str3,str4)
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
    #if the local file isn't in the same directory as gridup2.py
    #splits the filename away from the path and so can use different
    #paths on grid but the same filename.
    filename = []
    words = []
    for line in filenamepath:
        words.append(line.rstrip('\n').split('/'))
    filename_array = numpy.array(words)
    numberOfFiles = filename_array.shape[0]
    for i in range(numberOfFiles):
        filename.append(filename_array[i][-1])
    return filename

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", dest = 'list', help = "list of files to\
                        upload [in_text.txt]", default='in_text.txt')
    parser.add_argument("-o", dest = 'out', help = "text file produce\
                        with Grid information [Gridid.txt]", default = \
                        'Gridid.txt')
    parser.add_argument("-d", dest = 'dest', help = "storage element on\
                        the GRID 'sehn02.atlas.ualberta.ca'", default =\
                        'sehn02.atlas.ualberta.ca')
    parser.add_argument("-r", dest = 'remove', help = "if the file\
                        already exist should it be overwritten", default\
                        = False)
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
    Directory, Path, FilenamePath = readin_file(args.list)
    Storage = args.dest
    Filename = split_filename(FilenamePath)
    if base_directory(Directory) != True:
        print "not valid base directory"
        exit()
    Out_text = args.out
    Griddir = '/grid/snoplus.snolab.ca'
    Gridid = grid_file(Griddir, Directory, Path, Filename, Storage, \
                       Out_text,args.remove)
    database_file(Directory, Path, Filename, Gridid)
    print Gridid
    
