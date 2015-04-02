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

#import os
#
#def ReadinFile(textfile):
#	directory = []
#	file_path = []
#	filename = []
#	i =0
#	words = []
#	with open(textfile, 'r') as f:
#		data = f.readlines()
#		#print data
#		for line in data:
#			words.append(line.rstrip('\n').split('\t'))
#			print i
#			i+=1
#		directory = words[0]
#		print "dirctory"
#		print directory
#		file_path = words[1]
#		print "file_path"
#		print file_path
#		print "words[1]"
#		print words[1]
#		filename = words[2]
#		print "filename"
#		print filename
#
#	#print words[0]
#	#print "directory"
#	#print directory[0]
#	#print directory[1]
#	#print "filename"
#	#print filename[0]
#	#print filename[1]
#	#print words[1]
#	f.close()
#	return directory, file_path, filename
#
#def BaseDirectory(directory):
#	i=0
#	for entry in directory:
#		if directory[i] == "user":
#			return True
#		elif directory[i] == "sw":
#			return True
#		elif directory[i] == "snotflow":
#			return True
#		elif directory[i] == "production_testing":
#			return True
#		elif directory[i] == "production":
#			return True
#		elif directory == "nearline":
#			return True
#		else:
#			print "here "
#			print directory[i]
#			return False
#		i+=1
#
#def GridFile(directory,Path,filename):
#	print "here"
##	lfc_dir = os.path.join('lfn:/grid/snoplus.snolab.ca/', directory, Path, filename)
##print lfc_dir
#
#if __name__ == '__main__':
#	Textfile = 'in_text.txt'
#	#load the text file with info needed
#	Directory, Path, Filename = ReadinFile(Textfile)
#	print Directory
#	print Path
#	print Filename
#	#check that the base drectory is set correctly
#	if BaseDirectory(Directory) != True:
#		print "not valid base directory"
#		exit()
#	GridFile(Directory, Path, Filename)
##	print Path[0]
##	print Path[1]
from os.path import dirname
from numpy import array
def Readinfile(filename):
	directory = []
	file_path = []
	# row=[]
	#infile = open(filename,"r")
	# lines = infile.readlines()
	# print lines
	
	# for line in infile:
	# row = infile.readline().split("")
	# print line.split(",")
	# print line[0]
	i =0
	words = []
	with open(filename, 'r') as f:
		data = f.readlines()
		
		for line in data:
			words.append(line.split('\t'))
			print words[i]
			i+=1
		words_array = array(words)
		print "array"
		print words_array
		print "end"
		directory = words_array[:,0]
		file_path = words_array[:,1]
				
	
	#print words[0]
	#print words[1]
	print directory[0]
#print directory[1]
	print file_path[0]
#	print file_path[1]



if __name__ == '__main__':
	filename = 'in_text.txt'
	y = Readinfile(filename)
		
