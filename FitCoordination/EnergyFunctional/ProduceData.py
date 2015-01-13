#!/usr/bin/env python
import os, sys, string, Utilities
# Author K Majumdar - 09/01/2015 <Krishanu.Majumdar@physics.ox.ac.uk>


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
	
    # Loop over the fit parameters to be calculated (each one needs a separate set of events)
    for i in range(len(Utilities.parameters)):
	
        # Check what kind of parameter this loop is for, based on the parameter index "i"
        # If "internal energyCoeffs" (i = 0), check what material has been set and load the correct energies
		# If "external energyCoeffs" (i = 1), set material to always be water, and load the correct energies
		# If "radialCoeffs" (i = 2), load the correct energies
		# If "zCoeffs" (i = 3), load the correct energies
        if (i == 0):
            material = options.scintMaterial

            if (material == "lightwater_sno"):
                energyList = list(Utilities.energies_energyCoeffs_water)
            else:
                energyList = list(Utilities.energies_energyCoeffs_scintillator)
        elif (i == 1):
            material = "lightwater_sno"
            energyList = list(Utilities.energies_energyCoeffs_water)
        elif (i == 2):
            material = options.scintMaterial
            energyList = list(Utilities.energies_radiusCoeffs)
        else:
            material = options.scintMaterial
            energyList = list(Utilities.energies_zCoeffs)
            
        # For each parameter, simulate the correct number of events at each energy (5 files per energy per parameter)
        for energyIndex, energy in enumerate(energyList):

            for p in range (1, 6):

                outfileName = "electrons_" + Utilities.parameters[i] + "_" + str(int(energy * 1000)) + "keV_" + Utilities.positionTypes[i] + "_part" + str(p)
				
                # For the z-function, need to fill 3 separate volumes (inner_av, av and water), so need 3 separate position generator lines
                positionLine = ""
                if (i != 3):
                    positionLine += "/generator/pos/set " + Utilities.positionArgs[i] + "\n"
                else:
                    for positionIndex in range(3, len(Utilities.positionArgs)):
                        positionLine += "/generator/pos/set " + Utilities.positionArgs[positionIndex] + "\n"			

                outText1 = rawText1.substitute(ExtraDB = extraDB,
                                               GeoFile = options.geoFile,
                                               ScintMaterial = material,
                                               FileName = outfileName + ".root",
                                               PositionType = Utilities.positionTypes[i],
                                               Energy = energy,
                                               PositionArg = positionLine)
                outFile1 = open(outfileName + ".mac", "w")
                outFile1.write(outText1)
                outFile1.close()

                print "Running " + outfileName + ".mac and generating " + outfileName + ".root"
	            
                # Run the macro on a Batch system
                if options.batch:
                    outText2 = rawText2.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                                   Ratenv = batch_params['ratenv'],
                                                   Cwd = os.environ['PWD'].replace("/.", "/"),
                                                   RunCommand = "rat " + outfileName + ".mac")
                    outFile2 = open(outfileName + ".sh", "w")
                    outFile2.write(outText2)
                    outFile2.close()

                    os.system(batch_params["submit"] + " " + outfileName + ".sh")
				
                # Else run the macro locally on an interactive machine				
                else:
                    os.system("rat " + outfileName + ".mac")
                    # delete the macro when running is complete
                    os.remove(outfileName + ".mac")


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the macros in Batch mode")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use - location relative to rat/data/, default = geo/snoplus.geo", default = "geo/snoplus.geo")
    parser.add_option("-l", type = "string", dest = "loadDB", help = "Load an extra .ratdb directory")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = labppo_scintillator", default = "labppo_scintillator")
    (options, args) = parser.parse_args()
    ProduceRunMacros(options)

