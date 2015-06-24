#This program reads in SNO ECA pdst files and converts them to RAT PDST.ratdb
#F Descamps Feb 2013

import array
import argparse
import time

start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("filename",help="Input must be a peca .dat file")
args = parser.parse_args()
f = open(args.filename, 'r')

arraySTAT=[ 0.00 for i in range(19*16*32*16)]
arrayQHS=[ 0.00 for i in range(19*16*32*16)]
arrayQHL=[ 0.00 for i in range(19*16*32*16)]
arrayQLX=[ 0.00 for i in range(19*16*32*16)]
arrayTAC=[ 0.00 for i in range(19*16*32*16)]
l=0

for line in f:
   for item in line.split("\s"):
       if "--- Crate" in item:
            j= int(item.split() [-2].strip()) #pattern
            i= int(item.split() [-5].strip()) #crate
            #print i,j
            linenow=f.next()
            for x in range(0,4096):
               linenow=f.next()
               arrayTAC[l]=float(linenow.split() [-1].strip())
               arrayQLX[l]=float(linenow.split() [-2].strip())
               arrayQHL[l]=float(linenow.split() [-3].strip())
               arrayQHS[l]=float(linenow.split() [-4].strip())
               arraySTAT[l]=int(linenow.split() [-5].strip())
             #  printl,arrayQHS[l],arrayQHL[l],arrayQLX[l],arrayTAC[l]
               l=l+1

print("time: "+str(time.time()-start))
# The arrays are now all filled according to
# OFFSET = 5*[(ice-1)*(nchannels*ncards/2) + (ich-1)*(ncards/2) + (jca-1)]  + 1 + N
# Print this out to RAT .ratdb file according to cccc = icell + 16*ichan + 512icard + 8192 icrate
# Get the old runnumber from the input filename and add it to the output filename

runnumber=args.filename.split('_')[-3]
nchannels=32
ncards=16
outfilename="PDST_%i_0.ratdb" %int(runnumber)
f = open(outfilename, 'w')
# Now we have to loop over the table 8 times.. ugh
f.write('{\n type: "ECA_PDST",\n version: 1,\n run_range: [0,0], \n pass : 0, \n production : false, \n timestamp: \"\",\n comment : \"\",\n\n pdst_status: [ ')
# For now, set all the statuswords to zero..
# Need to translate SNO status words into SNO+ ones..
for x in range(0,19):
    for y in range(0,16):
        for z in range(0,32):
           for w in range(0,16):
            f.write('0')
            f.write(',')
f.write('],\n \n ')
f.write('pdst_qhs: [')
for x in range(0,16*16*32*19):
   f.write(str(arrayQHS[x]))
   f.write(',')
f.write('],\n \n ')
f.write('pdst_qhl: [')
for x in range(0,16*16*32*19):
   f.write(str(arrayQHL[x]))
   f.write(',')
f.write('],\n \n ')
f.write('pdst_qlx: [')
for x in range(0,16*16*32*19):
   f.write(str(arrayQLX[x]))
   f.write(',')
f.write('],\n \n ')
f.write('pdst_tac: [')
for x in range(0,16*16*32*19):
   f.write(str(arrayTAC[x]))
   f.write(',')
f.write('],\n \n ')
f.write('pdst_qhswidth: [3.61 : 155648],\n \n ')
f.write('pdst_qhlwidth: [3.61 : 155648],\n \n ')
f.write('pdst_qlxwidth: [3.61 : 155648],\n \n ')
f.write('pdst_tacwidth: [0.0 : 155648],\n \n ')
f.write('pdst_dqid: [')
for x in range(0,19):
    for y in range(0,16):
        for z in range(0,32):
           for w in range(0,16):
            f.write('0')
            f.write(',')
f.write('],\n \n ')
f.write('}')



