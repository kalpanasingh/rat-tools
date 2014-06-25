#!usr/bin/env python
import string, Utilities, os
# Author K Majumdar - 25/06/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


# returns the parameters for the Functional Form of Energy Reconstruction in the form of a complete RATDB entry
def AnalyseRootFiles(options):
    
    # load the basic submit script template
    infile = open("Template_Submit.sh", "r")
    rawText = string.Template(infile.read())
    infile.close()

    outText = rawText.substitute(envrnLoc = Utilities.envrnLoc,
		                         currentLoc = Utilities.currentLoc,
		                         runCommand = "python AnalyseData.py -i " + options.index)
    outFile = open("AnalyseData_ShortTime_SubmitScript.sh", "w")
    outFile.write(outText)
    outFile.close()

    os.system("qsub -l cput=00:59:00 AnalyseData_ShortTime_SubmitScript.sh")


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)

