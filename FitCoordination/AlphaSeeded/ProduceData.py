#!/usr/bin/env python
import os, sys, string, SeededUtilities
# Author K Majumdar - 14/05/2012 <Krishanu.Majumdar@physics.ox.ac.uk>


def ProduceRunMacFiles(options):
	# produces and then runs the required mac files

	# load the basic mac file
	inFile = open("Base.mac", "r")
	rawText = string.Template(inFile.read())
	inFile.close()

	# generate the specific mac files for each particle, with energies and corresponding names given in the Utilities tables
	for index, energy in enumerate(SeededUtilities.Energies):
		if index == 0:
			generator = "/generator/vtx/set alpha 0 0 0 " + str(energy)
			outfile = SeededUtilities.Particles[0]
		elif index == 1:
			generator = "/generator/vtx/set e- 0 0 0 " + str(energy)
			outfile = SeededUtilities.Particles[1]
	
		outText = rawText.substitute(Generator = generator,
									 GeoFile = options.geoFile,
									 ScintMaterial = options.scintMaterial,
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
	ProduceRunMacFiles(options)