#!/usr/bin/env python
import os, sys, string, Utilities, rat
from ROOT import RAT
# Author I T Coulter - 9/11/2012 <icoulter@hep.upenn.edu>
#        K Majumdar - 11/09/2014 - Cleanup of Coordinators for new DS


def ProduceRunMacros(options):

    # First, check if the material is new or not
    db = RAT.DB.Get()
    db.LoadAll(os.environ["GLG4DATA"], "*QUAD*.ratdb")
    if options.loadDB:
        db.LoadAll(options.loadDB, "*.ratdb")
    link = db.GetLink("QUAD_FIT", options.scintMaterial)
    try:
        link.GetD("light_speed")
    except:
        defaultMaterial = True
        print "Running for a new material"
    else:
        defaultMaterial = False
        print "Found database index for", options.scintMaterial

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

    # Choose particle energy based on the material
    energy = "3.0"
    if options.scintMaterial == "lightwater_sno":
        energy = "8.0"
		
    # Generate the specific macro for each speed given in the Utilities table
    for speed in Utilities.Speeds:

        outfileName = "quadFit_" + str(int(speed)) 

        if defaultMaterial:
            speedString = "QUAD_FIT light_speed %s" % speed
        else:
            speedString = "QUAD_FIT[%s] light_speed %s" % (options.scintMaterial, speed)

        outText1 = rawText1.substitute(ExtraDB = extraDB,
                                       GeoFile = options.geoFile,
                                       ScintMaterial = options.scintMaterial,
                                       SpeedDB = speedString,
                                       FileName = outfileName + ".root",
                                       Particle = options.particle,
                                       Energy = energy)
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
			
            os.system( batch_params["submit"] + " " + outfileName +".sh" )        
				
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
    parser.add_option("-p", type = "string", dest = "particle", help = "Particle type to use (see generator documentation for available particles), default = 'e-'", default = "e-")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = labppo_scintillator", default = "labppo_scintillator")
    (options, args) = parser.parse_args()
    ProduceRunMacros(options)

