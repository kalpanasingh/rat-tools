# This program reads in SNO gain or timewalk PCA files and converts them to
# RAT PMTCALIB.ratdb or TW_PMTCALIB.ratdb files
# F Descamps aug 2012
# v1 brute force my way through it!


import array
import argparse

def bitflip(n,range):
    bitfliplen = range[1]-range[0]
    return n ^ ((2**bitfliplen-1) << (range[0])) # XOR(n,leftshift(power(2,range[1]-range[0])-1,range[0])

parser = argparse.ArgumentParser()
parser.add_argument("filename",
        help="Input must be a SNO gpca or wpca2 .dat file")
args = parser.parse_args()
f = open(args.filename, 'r')

#Check the type of input file
if "gpca" in args.filename:
    print "Squeezing old SNO gain calibration constants into new RAT format..."

     # Make the table for the gain values
    table= [ [ [ [ 0.00 for i in range(7) ] for j in range(32) ] for h in range(16) ] for g in range(19) ] #7 x 32 x 16 x 19 table, all zeros
     # We will need to keep track of hhp_min, hhp_max and hhp_mean ourselves
     # since this is not part of the  old SNO file
    hhp_min = 9999.0
    hhp_max = -9999.0
    hhp_mean = 0
    counter =0
    for line in f:
        for item in line.split("\s"): #white space characters (space, indent, enter, etc)
            if "#.   Crate" in item:
                j= int(item.split() [-1].strip()) #last character in the last w
                i= int(item.split() [-3].strip())
                for x in range(0,32):
                    linenow=f.next()
                    h=int(linenow.split() [-1].strip())
                    for y in range(3,10):
                        table[i][j][h][y-3]=float(linenow.split() [-y].strip())
                        if y-3==3 and table[i][j][h][y-3]!=-9999 and table[i][j][h][y-3]!=0.0:
                            hhp_mean += table[i][j][h][y-3]
                            counter +=1
                            if table[i][j][h][y-3]<hhp_min:
                                hhp_min = table[i][j][h][y-3]
                            if table[i][j][h][y-3]>hhp_max:
                                hhp_max = table[i][j][h][y-3]
    hhp_mean = hhp_mean/counter
     # The table is now filled according to table[crate][card][channel][values]
     # print this neatly out out to a RAT .ratdb file
     # Get the old runnumber from the input filename and
     # add it to the output filename
    runnumber=args.filename.split('_')[-3]
    outfilename="PMTCALIB_%i.ratdb" %int(runnumber)
    f = open(outfilename, 'w')
     # Now we have to loop over the table 8 times.. ugh
    f.write('{\n name: "PMTCALIB",\n run_range: [0,0], \n pass : 0, \n')
    f.write('\n mean_hhp : ')
    f.write(str(hhp_mean))
    f.write(',\n min_hhp : ')
    f.write(str(hhp_min))
    f.write(',\n max_hhp : ')
    f.write(str(hhp_max))
    f.write(',\n')

    f.write('\n tube_status : [ ')
    for x in range(0,19):
        for y in range(0,16):
            for z in range(0,32):
                f.write(str(int(table[x][y][z][6])))
                f.write('.00, ')
    f.write('],\n \n QHS_threshold : [ ')
    for x in range(0,19):
        for y in range(0,16):
            for z in range(0,32):
                f.write(str(table[x][y][z][5]))
                f.write(', ')
    f.write('],\n \n QHS_peak : [ ')
    for x in range(0,19):
        for y in range(0,16):
            for z in range(0,32):
                f.write(str(table[x][y][z][4]))
                f.write(', ')
    f.write('],\n \n QHS_hhp : [ ')
    for x in range(0,19):
        for y in range(0,16):
            for z in range(0,32):
                f.write(str(table[x][y][z][3]))
                f.write(', ')
    f.write('],\n \n QHL_threshold : [ ')
    for x in range(0,19):
        for y in range(0,16):
            for z in range(0,32):
                f.write(str(table[x][y][z][2]))
                f.write(', ')
    f.write('],\n \n QHL_peak : [ ')
    for x in range(0,19):
        for y in range(0,16):
            for z in range(0,32):
                f.write(str(table[x][y][z][1]))
                f.write(', ')
    f.write('],\n \n QHL_hhp : [ ')
    for x in range(0,19):
        for y in range(0,16):
            for z in range(0,32):
                f.write(str(table[x][y][z][0]))
                f.write(', ')
    f.write('],\n }')

elif "wpca2" in args.filename:
    print "Squeezing old SNO timewalk calibration constants into new RAT format..."
 #make the tables for the timewalk binary values
    temptable= [ [ [ [ 0.00 for i in range(13) ]
        for j in range(32) ]
        for h in range(16) ]
        for g in range(19) ]
    table= [ [ [ [ 0.00 for i in range(13) ]
        for j in range(32) ]
        for h in range(16) ]
        for g in range(19) ]
    for line in f:
        for item in line.split("\s"):
            if "#.   Crate" in item:
                j= int(item.split() [-1].strip())
                i= int(item.split() [-3].strip())
                print("Crate: "+str(j)+"Card: "+str(i))
                for x in range(0,32):
                    firstlinenow=f.next()
                    h=int(firstlinenow.split() [-1].strip())
                    print("temptable length: "+str(len(temptable[i][j][h])))
                    print(firstlinenow)
                    for l in range(3,10):
                        print("l: "+str(l))
                        temptable[i][j][h][l-3]=firstlinenow.split() [-l].strip()
                    secondlinenow=f.next()
                    print(secondlinenow)
                    for k in range(1,7):
                        temptable[i][j][h][k+6]=secondlinenow.split() [-k].strip()

# Now re-organise the information correctly
    for x in range(0,19):
        for y in range(0,16):
            for z in range(0,32):
                table[x][y][z][0]=temptable[x][y][z][6]
                table[x][y][z][1]=temptable[x][y][z][5]
                table[x][y][z][2]=temptable[x][y][z][4]
                table[x][y][z][3]=temptable[x][y][z][3]
                table[x][y][z][4]=temptable[x][y][z][2]
                table[x][y][z][5]=temptable[x][y][z][1]
                table[x][y][z][6]=temptable[x][y][z][0]

                table[x][y][z][7]=temptable[x][y][z][12]
                table[x][y][z][8]=temptable[x][y][z][11]
                table[x][y][z][9]=temptable[x][y][z][10]
                table[x][y][z][10]=temptable[x][y][z][9]
                table[x][y][z][11]=temptable[x][y][z][8]
                table[x][y][z][12]=temptable[x][y][z][7]

 # Write to outputfile
    runnumber=args.filename.split('_')[-3]
    outfilename="PCATW_%i.ratdb" %int(runnumber)
    f = open(outfilename, 'w')
     # Write, write, write!
     # Now we have to loop over the table.. ugh
    f.write('{\n name: "PCA_TW",\n run_range: [0,0], \n tw_npoints : 10, \n is_sno : 1, \n \n twinter : [ ')
    for x in range(0,19):
        for y in range(0,16):
            for z in range(0,32):
                for k in range(2,13):
                    a=int(table[x][y][z][k])
                    b = bitflip(a,(0,1))
                    # print "a: {0:b}\nb: {1:b}".format(a,b)
                    f.write(str(b))
                    f.write(', ')
    f.write('],\n \n PCATW_status : [ ')
    for x in range(0,19):
        for y in range(0,16):
            for z in range(0,32):
                f.write(str(table[x][y][z][0]))
                f.write(', ')
    f.write('],\n }')
else:
    print "I am unsure what to do with this file. Please supply either a SNO gpca or wpca2 file..."

