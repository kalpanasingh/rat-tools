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

from os.path import dirname
#from numpy import array
import numpy

def ReadinFile(textfile):
	directory = []
	file_path = []
	filename = []
	i =0
	words = []
	with open(textfile, 'r') as f:
		data = f.readlines()
		for line in data:
			words.append(line.split('\t'))
			print words[i]
			i+=1
		words_array = numpy.array(words)
		print "array"
		print words_array
		print "end"
		directory = words_array[:,0]
		file_path = words_array[:,1]
		filename = words_array[:,2]
	
	#print words[0]
	#print words[1]
	print directory[0]
	# print directory[1]
	print file_path[0]
#	print file_path[1]
	return directory, file_path, filename

def BaseDirectory(directory):
	i=0
	for entry in directory:
		if directory[i] == "user":
			return True
		elif directory[i] == "sw":
			return True
		elif directory[i] == "snotflow":
			return True
		elif directory[i] == "production_testing":
			return True
		elif directory[i] == "production":
			return True
		elif directory == "nearline":
			return True
		else:
			print "here "
			print directory[i]
			return False
		i+=1

def MakeFolderPath(directory,path,griddir):
	i=0
	for lines in path:
		createfolder = griddir
		words = []
		words.append(path[i].split("/"))
		for column in words:
			  createfolder += "/%s"%words[column]
		    execute('lfc-mkdir', createfolder)
		
		
		#create_path = numpy.fromstring(path[i],dtype=str,sep="/")
		#print create_path
		i+=1
#      lfc_dir = "lfn:/grid/snoplus.snolab.ca/%s/%s/"%(directory[i],path[i])



def GridFile(directory,path,filename):
	print "here"
	i=0
	for s in directory:
		#	lfc_dir = "lfn:/grid/snoplus.snolab.ca/"
		lfc_dir = "lfn:/grid/snoplus.snolab.ca/%s/%s/%s"%(directory[i],path[i],filename[i])
		i+=1
		print lfc_dir


if __name__ == '__main__':
	Textfile = 'in_text.txt'
	Griddir = '/grid/snoplus.snolab.ca/'
	databasedir = ''
	Directory, Path, Filename = ReadinFile(Textfile)
	if BaseDirectory(Directory) != True:
		print "not valid base directory"
		exit()
	MakeFolderPath(Directory, Path, Griddir)
	GridFile(Directory, Path, Filename)
