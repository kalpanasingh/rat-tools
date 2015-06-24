import array
import argparse
import time
import sys

"""
Conversion of DQXX Constants from SNO to SNOPLUS Format
Using logic from a SNO macro written by Gabriel Orebi Gann, PhD
Auth: Chris Dock 2015
"""

"""The following lambda expression takes a number and flips bits from r[0] to r[1] excluding r[1]"""
def listdouble(l,n):
    if n==0:
	return l
    return listdouble(l,n-1)+listdouble(l,n-1)


parser = argparse.ArgumentParser(description="Input SNO DQXX File")
parser.add_argument("filename",
        help = "Input must be a valid SNO .dat file")
args = parser.parse_args()
titles = []
dqids=[]
dqchwords=[]
dqcrwords=[]
for i in range(0,39):
    titles.append([])
with open(args.filename,'r') as f:
    #read in the file (there are 39 titles - 19 for dqcr and dqch and 1 for dqid
    lines = f.readlines()
    # break into title files 
    t=0
    for line in lines:
        titles[t].append(line)
	if "End of Title" in line: 
	    t+=1
    #remove headers
    for k in range(0,len(titles)):
	for i in range(0,len(titles[k])):
	    if 'End of Standard Database Header' in titles[k][i]:
		titles[k]=titles[k][i+1:]
		break
    #extract dqids
    dqidtitle = titles[38]
    dqidtitle = filter(lambda x: x[0:2]=='#x',dqidtitle)
    dqidtitle = map(lambda x: x.replace('#','0').replace('\r\n',''),dqidtitle)
    dqids = ' '.join(dqidtitle).split()
    #extract dqch and dqcr
    for i in range(0,38):
	titles[i] = filter(lambda x: x[0:2]=='#x',titles[i])
        titles[i] = map(lambda x: x.replace('#','0').replace('\r\n',''),titles[i])
	if i%2==0: #DQCH
	    temp_dqchwords = ' '.join(titles[i]).split()
	    dqchwords.extend(temp_dqchwords)
	else: #DQCR
	    temp_dqcrwords = ' '.join(titles[i]).split()
    	    dqcrwords.extend(temp_dqcrwords)
runnum = int(args.filename.split('_')[-1][:-4])
print("run # is "+str(runnum))
with open('./PMT_DQXX0'+str(runnum)+'.ratdb','w') as f2:
    f2.write(
"""
////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////
///
/// \\brief   Converted DQXX Titles File output by the ECA for run """
+str(runnum)
+
"""
///
///
////////////////////////////////////////////////////////////////////
{
type: "PMT_DQXX",
version: 1,
run_range: [0,0],
pass : 0,
production : false,
timestamp: "",
comment : "",

cratestatus_n100: 0,
cratestatus_n20: 0,
cratestatus_esumL: 0,
cratestatus_esumH: 0,
cratestatus_owlN: 0,
cratestatus_owlEL: 0,
cratestatus_owlEH: 0,

""")

    f2.write("\n dqch: "+str(dqchwords).replace('\'','')+",")
    f2.write("\n dqcr: "+str(dqcrwords).replace('\'','')+",")
    f2.write("\n dqid: "+str(dqids).replace('\'','')+",")
    f2.write("\n }")
