#!/usr/bin/env python
import os, sys, string, Utilities
# Author K Majumdar - 18/12/2012 <Krishanu.Majumdar@physics.ox.ac.uk>


def ProduceRunMacros(options):
	# produces and then runs the required rat macros

	# load the basic macro template
    inFile = open("Template_Macro.mac", "r")
    rawText = string.Template(inFile.read())
    inFile.close()

	# create the specific macro for each radius, and then run it
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

	    outFile = open(outfile + ".mac", "w")
	    outFile.write(outText)
	    outFile.close()
		
		# run the mac file for the particle
	    print "Running " + outfile + ".mac and generating " + outfile + ".root"
	    os.system("rat " + outfile + ".mac")

		# delete the particle-specific mac file when running is complete
	    os.remove(outfile + ".mac")


import optparse
if __name__ == '__main__':
	parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
	parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use - location must be absolute or relative to target.", default = "geo/snoplus.geo")
	parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator material.", default = "labppo_scintillator")
	parser.add_option("-p", type = "string", dest = "particle", help = "Particle type - this is not relevant for this coordinator.", default = "")
	(options, args) = parser.parse_args()
	ProduceRunMacros(options)