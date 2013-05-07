#!/usr/bin/env python
import os, sys, string, Utilities
# Author K Majumdar - 22/08/2012 <Krishanu.Majumdar@physics.ox.ac.uk>


def ProduceRunMacros(options):
    # produce the macros and submit scripts

    # load the basic macro template
    inFile = open("Template_Macro.mac", "r")
    rawText = string.Template(inFile.read())
    inFile.close()

	# load the basic submit script template
    infile2 = open("Template_Submit.sh", "r")
    rawText2 = string.Template(infile2.read())
    infile2.close()

    # create a new file for submitting all macros simultaneously
    outFile3 = open("SubmitAll.sh", "w")

    # generate the specific macro and submit script for each radius, and add new command to the submitAll script
    for innerpos in Utilities.radius:
	    if (innerpos == 5000):
		    position = "/generator/pos/set 0 0 0 0 0 0 5000 5001"
	    else:
		    position = "/generator/pos/set 0 0 0 0 0 0 " + str(innerpos) + " " + str(innerpos + 99)

	    outfile = "electrons_" + str(innerpos) + "mm"
	    outText = rawText.substitute(GeoFile = options.geoFile,
                                     ScintMaterial = options.scintMaterial,
                                     Position = position,
                                     OutFileName = outfile + ".root")
	    outText2 = rawText2.substitute(envrnLoc = Utilities.envrnLoc,
		                               currentLoc = Utilities.currentLoc,
		                               runCommand = "rat " + outfile + ".mac")

	    outFile = open(outfile + ".mac", "w")
	    outFile.write(outText)
	    outFile.close()

	    outFile2 = open(outfile + ".sh", "w")
	    outFile2.write(outText2)
	    outFile2.close()

	    outFile3.write("qsub " + outfile + ".sh\n")

    outFile3.close()
    
	# send all batch commands at once, and ends the production script
    os.system("source SubmitAll.sh")


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version="%prog 1.0")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use, location must be absolute or relative to target.", default = "geo/snoplus.geo")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator material.", default = "labppo_scintillator")
    parser.add_option("-p", type = "string", dest = "particle", help = "Particle type - this is not relevant for this coordinator.", default = "")
    (options, args) = parser.parse_args()
    ProduceRunMacros(options)
