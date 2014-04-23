#!/usr/bin/env python
import os, sys, string, Utilities
# Author K Majumdar - 02/04/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


def ProduceRunMacros(options):
    # Load the basic macro template
    inFile1 = open("Template_Macro.mac", "r")
    rawText1 = string.Template(inFile1.read())
    inFile1.close()
	
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

                print "Running " + outfileName + ".mac and generating " + outfileName + ".root"
	            os.system("rat " + outfileName + ".mac")

		        # delete the macro when running is complete
	            os.remove(outfileName + ".mac")


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version="%prog 1.0")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use, location must be absolute or relative to target.", default = "geo/snoplus.geo")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator material.", default = "labppo_scintillator")
    parser.add_option("-p", type = "string", dest = "particle", help = "Particle type - this is not relevant for this coordinator.", default = "")
    (options, args) = parser.parse_args()
    ProduceRunMacros(options)

