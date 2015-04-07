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
import subprocess
import numpy

#####################################
#Code for uploading
#####################################

def ReadinFile(textfile):
	directory = []
	file_path = []
	filename = []
	i =0
	words = []
	with open(textfile, 'r') as f:
		data = f.readlines()
		for line in data:
			words.append(line.rstrip('\n').split('\t'))
			print words[i]
			i+=1
		words_array = numpy.array(words)
		print "array"
		print words_array
		print "end"
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

def BaseDirectory(directory):
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
			print "here "
			print directory[i]
			return False
		i+=1

def GridFile(griddir,directory,path,filename,storage):
	print "here"
	i=0
	for s in directory:
		se_path = '%s/%s/%s'%(directory[i],path[i],filename[i])
		print se_path
		se_path.strip()
		print se_path
		lfc_path = 'lfn:%s/%s/%s/%s'%(griddir,directory[i],path[i],filename[i])
		upfile = filename[i]
		inputstring = 'lcg-cr --vo snoplus.snolab.ca --checksum -d sehn02.atlas.ualberta.ca -P %s -l %s %s'%(se_path,lfc_path,upfile)
		os.system(inputstring)
		i+=1
		print inputstring


if __name__ == '__main__':
	Textfile = 'in_text.txt'
	Griddir = '/grid/snoplus.snolab.ca'
	Directory, Path, Filename, Storage = ReadinFile(Textfile)
	if BaseDirectory(Directory) != True:
		print "not valid base directory"
		exit()
	GridFile(Griddir, Directory, Path, Filename, Storage)
