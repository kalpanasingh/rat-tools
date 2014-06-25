#!/usr/bin/env python
import os, sys, string, Utilities
# Author K Majumdar - 25/06/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


def ProduceRunMacros(options):
    # Load the basic macro template
    inFile1 = open("Template_Macro.mac", "r")
    rawText1 = string.Template(inFile1.read())
    inFile1.close()
	
    # load the basic submit script template
    infile2 = open("Template_Submit.sh", "r")
    rawText2 = string.Template(infile2.read())
    infile2.close()

    # create a new file for submitting all macros simultaneously
    outFile3 = open("ProduceData_ShortTime_SubmitScript.sh", "w")

	# Need 5000 events per Parameter per Energy ... go quicker by doing 5 files of 1000 events each
    for energy in Utilities.energies:

        for i in range(len(Utilities.parameters)):

            for p in range (1, 6):
                
                outfileName = "electrons_" + Utilities.parameters[i] + "_" + str(int(energy * 1000)) + "keV_" + Utilities.positionTypes[i] + "_part" + str(p)
                
                outText1 = rawText1.substitute(GeoFile = options.geoFile,
                                               ScintMaterial = options.scintMaterial,
											   FileName = outfileName + ".root",
                                               PositionType = Utilities.positionTypes[i],
                                               Energy = energy,
                                               PositionArg = Utilities.positionArgs[i])
                outFile1 = open(outfileName + ".mac", "w")
                outFile1.write(outText1)
                outFile1.close()
                
                outText2 = rawText2.substitute(envrnLoc = Utilities.envrnLoc,
		                                       currentLoc = Utilities.currentLoc,
		                                       runCommand = "rat " + outfileName + ".mac")
                outFile2 = open(outfileName + ".sh", "w")
                outFile2.write(outText2)
                outFile2.close()
                
                outFile3.write("qsub -l cput=01:59:00 " + outfileName + ".sh\n")

    outFile3.close()

    # send all batch commands at once, and ends the production script
    submitCommand = "source " + Utilities.currentLoc + "/ProduceData_ShortTime_SubmitScript.sh"
    os.system(submitCommand)
		

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version="%prog 1.0")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use - location relative to rat/data/, default = geo/snoplus.geo", default = "geo/snoplus.geo")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = labppo_scintillator", default = "labppo_scintillator")
    (options, args) = parser.parse_args()
    ProduceRunMacros(options)

