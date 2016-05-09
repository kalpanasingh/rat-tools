#!/usr/bin/env python
import os, sys, string

energyList = [ 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0 ]
numberOfEvents_scintillator = [ 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500 ]
numberOfEvents_water = [ 20000, 10000, 5000, 2000, 1000, 500, 500, 500, 500, 500, 500 ]
# DO NOT include a "0mm" entry in the yPositionList, , since the (y=0mm, z=0mm) point will be covered by the "0mm" entry in the zPositionList
yPositionList = [ 1000, 2000, 3000, 4000, 5000, 5400, 5600, 5800, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500, 8750 ]
zPositionList = [ -8750, -8500, -8250, -8000, -7750, -7500, -7250, -7000, -6750, -6500, -6250, -6000, -5800, -5600, -5400, -5000, -4000, -3000, -2000, -1000, 0, 1000, 2000, 3000, 4000, 5000, 5400, 5600, 5800, 6000 ]


def ProduceRunMacros(options):

	# Load any parameters for running the macros on a Batch system
    batch_params = None
    if options.batch:
        batch_params = {}
        execfile(options.batch, {}, batch_params)
		
    # Load any extra .ratdb files
    extraDB = ""
    if options.loadDB:
        extraDB = "/rat/db/load " + options.loadDB
	
    # Load the basic macro template
    inFile1 = open("Template_Macro.mac", "r")
    rawText1 = string.Template(inFile1.read())
    inFile1.close()
	
    # Load the batch submission script template
    inFile2 = open("Template_Batch.sh", "r")
    rawText2 = string.Template(inFile2.read())
    inFile2.close()

    for energyIndex, energy in enumerate(energyList):
	
        ##################################################
		##### Varying y-position, and setting z to 0 #####
        ##################################################
		
        for yPosition in yPositionList:

            zPosition = 0

            if (options.scintMaterial != "lightwater_sno"):
                numberOfEventsList = list(numberOfEvents_scintillator)
            else:
                numberOfEventsList = list(numberOfEvents_water)
				
            outfileName = options.scintMaterial + "_E=" + str(int(energy * 1000)) + "keV_y=" + str(yPosition) + "mm_z=" + str(zPosition) + "mm"

            generator = "/generator/vtx/set " + str(options.particle) + " 0 0 0 " + str(energy) + "\n" + \
                        "/generator/pos/set 0 " + str(yPosition) + " " + str(zPosition)
            
            outText1 = rawText1.substitute(ExtraDB = extraDB,
                                           GeoFile = options.geoFile, 
                                           ScintMaterial = options.scintMaterial, 
                                           OutFileName = outfileName + ".root", 
                                           Generator = generator,
                                           NumberOfEvents = numberOfEventsList[energyIndex])
            outFile1 = open(outfileName + ".mac", "w")
            outFile1.write(outText1)
            outFile1.close()
			
            outText2 = rawText2.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                           Ratenv = batch_params['ratenv'],
                                           Cwd = os.environ['PWD'].replace("/.", "/"),
                                           RunCommand = "rat " + outfileName + ".mac")
            outFile2 = open(outfileName + ".sh", "w")
            outFile2.write(outText2)
            outFile2.close()

            os.system(batch_params["submit"] + " " + outfileName + ".sh")
			
        ##################################################
		##### Varying z-position, and setting y to 0 #####
        ##################################################
		
        for zPosition in zPositionList:

            yPosition = 0

            outfileName = options.scintMaterial + "_E=" + str( int(energy * 1000) ) + "keV_y=" + str(yPosition) + "mm_z=" + str(zPosition) + "mm"

            generator = "/generator/vtx/set " + str(options.particle) + " 0 0 0 " + str(energy) + "\n" + \
                        "/generator/pos/set 0 " + str(yPosition) + " " + str(zPosition)

            outText1 = rawText1.substitute(ExtraDB = extraDB,
                                           GeoFile = options.geoFile, 
                                           ScintMaterial = options.scintMaterial, 
                                           OutFileName = outfileName + ".root", 
                                           Generator = generator,
                                           NumberOfEvents = numberOfEventsList[energyIndex])
            outFile1 = open(outfileName + ".mac", "w")
            outFile1.write(outText1)
            outFile1.close()
			
            outText2 = rawText2.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                           Ratenv = batch_params['ratenv'],
                                           Cwd = os.environ['PWD'].replace("/.", "/"),
                                           RunCommand = "rat " + outfileName + ".mac")
            outFile2 = open(outfileName + ".sh", "w")
            outFile2.write(outText2)
            outFile2.close()

            os.system(batch_params["submit"] + " " + outfileName + ".sh")


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version="%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the macros in Batch mode")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File - geo/[geometry file], default = snoplus.geo", default = "geo/snoplus.geo")
    parser.add_option("-l", type = "string", dest = "loadDB", help = "Load an extra .ratdb directory")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material, default = labppo_scintillator", default = "labppo_scintillator")
    parser.add_option("-p", type = "string", dest = "particle", help = "Particle type, default = e-", default = "e-")
    (options, args) = parser.parse_args()
    ProduceRunMacros(options)

