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

########################
#read in the data
from os.path import dirname
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
		directory = words[0]
		file_path = words[1]
		
		
	print words[0]
	print words[1]
	print directory[0]
	print directory[1]
	print file_path[0]
	print file_path[1]

			
    
if __name__ == '__main__':
    filename = 'in_text.txt'
    y = Readinfile(filename)
