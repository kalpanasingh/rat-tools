import array
import argparse
import time
import sys

"""
Conversion of TECA Constants from SNO to SNOPLUS Format
Using code from Freija Descamps, PhD
Following Documentation on page 43-44 of SNO-STR-2001-005 (New Format for Time Slope Titles Banks)
Auth: Chris Dock 2015
"""

"""The following lambda expression takes a number and flips bits from r[0] to r[1] excluding r[1]"""
bitflip = lambda n, r: n ^ ((2**(r[1]-r[0])-1)<<(r[0]))

def bitstr(val,bits):
    return (''.join([('1' if (val>>n)&1 else '0') for n in xrange(0,bits)]))[::-1]

def unpack(data,bitsize):
    backwards = ''.join([bitstr(int(val),32) for val in data])
    binstring = ''.join([x[24:31]+x[16:23]+x[7:16]+x[0:7] for x in backwards])
    return [int(binstring[x*bitsize:x*bitsize+bitsize-1],2) for x in xrange(0,len(binstring)/bitsize)]

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

parser = argparse.ArgumentParser(description="Input SNO TECA File")
parser.add_argument("filename",
        help = "Input must be a valid SNO .dat file")
args = parser.parse_args()

with open(args.filename,'r') as f:
    #read in the file
    lines = f.readlines()

    #make sure the file contains the NTimes and NPacked information (and store it)
    ntimes=-1
    npacked=-1
    ntimesFound = False
    j=0
    while j < 100:
        if  "#. Number of time samplings" in lines[j]:
            ntimes = int(lines[j].split()[0])
            npacked = int(lines[j+1].split()[0])
            ntimesFound = True
            break
        j+=1
    if not ntimesFound:
        print "Error: Number of Injected Times wasn't found in the file"
        sys.exit(0)

    #Initialize lists to store unmodified data from the file
    packedwords = [[[0.00 for _ in range(npacked)] for _ in range(4096)] for _ in range(38)]
    unpackedtimes = []#[0.00 for _ in range(ntimes)]
    cardIDs = [[0.0 for _ in range(40)] for _ in range(38)]

    #Loop through the file and pull data into the above lists
    i=0
    a=0
    halfcrate=0
    timesfound = False
    while i < len(lines):
        if "#. Injected Time" in lines[i] and not timesfound:
            i+=1

            unpackedtimes.extend(map(lambda s: s.strip(),lines[i].split()));
            unpackedtimes.extend(map(lambda s: s.strip(),lines[i+1].split()));
            unpackedtimes.extend(map(lambda s: s.strip(),lines[i+2].split()));
            unpackedtimes.extend(map(lambda s: s.strip(),lines[i+3].split()));
            unpackedtimes.extend(map(lambda s: s.strip(),lines[i+4].split()));
            i+=5
            timesfound = True

        if "#.      ---------- Packed" in lines[i]:
            i+=1
            start=i
            cell=0
            while(i < start+4096*3):
                words=[]
                words.extend(map(lambda s: s.strip(),lines[i].split()));
                words.extend(map(lambda s: s.strip(),lines[i+1].split()));
                words.extend(map(lambda s: s.strip(),lines[i+2].split()));
                packedwords[halfcrate][cell]=words
                i+=3
                cell+=1
        if "#.      ----------  Card IDs" in lines[i]:
            i+=1
            start=i
            currentIDs=[]
            while i<start+8:
                currentIDs.extend([int(s[2:],16) for s in lines[i].split()])
                i+=1
            cardIDs[halfcrate]=currentIDs
            halfcrate+=1
        i+=1

#Testing Stuff

print("TIMES")
print("\n\n")
for q in range(len(unpackedtimes)):
    print unpackedtimes[q],
    print "  ",
print("\n PACKED WORDS")
print("\n\n")
for a in range(len(packedwords)):
    print("Half Crate " +str(a+1))
    print("CardIds: "+str(cardIDs[a]))
    print "some adc counts"
    for b in range(3):
        print packedwords[a][b],
        print "\n",
    print "etc etc etc ..... (4096 cells per half crate)"
    print("\n\n\n")




unpackedvoltages = [[[0.00 for _ in range(ntimes)] for _ in range(4096)] for _ in range(38)]
print "\n\n"
print "Unpacking ADC counts"

dqidlist = [val for element in cardIDs for val in element]
badlist = []#[0 for _ in range(4096) for _ in range(38)]
suspiciouslist = []#[0 for _ in range(4096) for _ in range(38)]
validationlist = []#[0 for _ in range(4096) for _ in range(38)]
fitparslist = []#[0 for _ in range(4) for _ in range(4096) for _ in range(38)]
pointlist = []#[0.0 for _ in range(ntimes) for _ in range(4096) for _ in range(38)]
unpackedtimes=[int(_)/100. for _ in unpackedtimes]
print("unpacked times: "+str(unpackedtimes))
for j in range(len(packedwords)):
    for k in range(len(packedwords[j])):
        print('\n\n')
        print("asdfjkl: "+str(packedwords[j][k][3:]))
        print("ben unpacked: " +str(unpack(packedwords[j][k][3:],12)))
        result = ''
        for l in range(len(packedwords[j][k]))[3:]:
            string= bin(int(packedwords[j][k][l])%(1<<32))[2:]
            string=''.join(['0' for _ in range(32-len(string))])+string
            result+=string
        unpacked = [int(_,2) for _ in list(chunks(result,12))]
        unpacked = unpacked[:len(unpacked)-3]
        #2289 fix
        for m in range(len(unpacked)-4):
            if unpacked[m]==2289 and (m==len(unpacked)-5 or unpacked[m+1]==2289):
                unpacked[m]=-9999
            elif unpacked[m]==2289 and ((m==0 or unpacked[m-1]>2289 or unpacked[m-1]==-9999)
                    or (m==len(unpacked)-5 or unpacked[m+1]<2289)):
                unpacked[m]=-9999
        #Data Points
        points = [_/1. for _ in unpacked[:ntimes]]
        #Cubic Fit Parameters (scaling provided by documentation in SNO-STR-2001-005)
        fitpars = unpacked[len(unpacked)-4:len(unpacked)] #there are three spare words

        for i in range(len(fitpars)):
            fitpars[i]=bin(fitpars[i])[2:]
            fitpars[i]=''.join(['0' for _ in range(12-len(fitpars[i]))])+fitpars[i]
            if fitpars[i][0]=='0':
                fitpars[i] = int(fitpars[i][1:],2)
            else:
                fitpars[i] = -1*(2**11)+int(fitpars[i][1:],2)
        fitpars[0]=fitpars[0]/float(2)
        fitpars[1]=fitpars[1]/float(100)
        fitpars[2]=fitpars[2]/float(10**5)
        fitpars[3]=fitpars[3]/float(10**7)

        #Status Flag Bit Masks
        badflag=bin(int(packedwords[j][k][0])%(1<<32))[2:]
        badflag=''.join(['0' for _ in range(32-len(badflag))])+badflag
        suspiciousflag=bin(int(packedwords[j][k][1])%(1<<32))[2:]
        suspiciousflag=''.join(['0' for _ in range(32-len(suspiciousflag))])+suspiciousflag

        validationflag=bin(int(packedwords[j][k][2])%(1<<32))[2:]
        validationflag=(''.join(['0' for _ in range(32-len(suspiciousflag))])+validationflag)[::-1]

        print('\n\n\n')
        print('unfiltered: '+str(unpacked))
        print('times: '+ str(unpackedtimes))
        print('points: '+str(points))
        print('fitpars: '+str(fitpars))
        print('badflag: '+ str(badflag))
        print('suspiciousflag: '+ str(suspiciousflag))
        print('validationflag: '+ str(validationflag))
        print '\n\n'

        badlist.append(int(suspiciousflag,2)|int(badflag,2))#badflag|suspiciousflag)
        #validationlist.append(validationflag)
        print("\n\n v1: "+validationflag+", v2: "+str(int(validationflag,2)))
        validationlist.append(int(validationflag,2))
        fitparslist.extend(fitpars)
        pointlist.extend(points)
runnum = int(args.filename.split('_')[-3])

with open('./TSLP_'+str(runnum)+'.ratdb','w') as f2:
    f2.write(
"""
////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////
///
/// \\brief   Converted TSLP Titles File output by the ECA for run """
+str(runnum)
+
"""
///
///
////////////////////////////////////////////////////////////////////
{
name: "ECA_TSLP",
run_range : [0, 0],
pass : 0,
""")

    f2.write("\n\n\n tslp_status: "+str(validationlist)+",")
    f2.write("\n tslp_bad: "+str(badlist)+",")
    f2.write("\n tslp_points: "+ str(pointlist)+",")
    f2.write("\n tslp_fitpars: "+str(fitparslist)+",")
    f2.write("\n tslp_dqid: "+str(dqidlist)+",")
    f2.write("\n tslp_times: "+str(unpackedtimes)+",")
    f2.write("\n tslp_ntimes: "+str(ntimes)+",")
    f2.write("\n }")














