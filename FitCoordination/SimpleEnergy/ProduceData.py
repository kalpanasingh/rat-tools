#!/usr/bin/env python
import os, sys, string
# Author P G Jones - 22/05/2011 <p.g.jones@qmul.ac.uk>
#        K Majumdar - 08/09/2014 - Cleanup of Coordinators for new DS


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

    # Load the batch submission script template
    inFile2 = open("Template_Batch.sh", "r")
    rawText2 = string.Template(inFile2.read())
    inFile2.close()

    # Load the macro
    inFile1 = open("Template_Macro.mac", "r")
    rawText1 = string.Template(inFile1.read())
    inFile1.close()
	
    outText1 = rawText1.substitute(ExtraDB = extraDB, 
                                   GeoFile = options.geoFile,
                                   ScintMaterial = options.scintMaterial,
                                   Particle = options.particle)
    outFile1 = open("events_E=1MeV.mac", "w")
    outFile1.write(outText1)
    outFile1.close()
	
    print "Running events_E=1MeV.mac and generating events_E=1MeV.root"
	            
    # Run the macro on a Batch system
    if options.batch:
        outTextTe2 = rawText2.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                         Ratenv = batch_params['ratenv'],
                                         Cwd = os.environ['PWD'].replace("/.", "/"),
                                         RunCommand = "rat events_E=1MeV.mac")
        outFileTe2 = open("events_E=1MeV.sh", "w")
        outFileTe2.write(outTextTe2)
        outFileTe2.close()

        os.system(batch_params["submit"] + " events_E=1MeV.sh")
				
    # Else run the macro locally on an interactive machine				
    else:
        os.system("rat events_E=1MeV.mac")
        # delete the macro when running is complete
        os.remove("events_E=1MeV.mac")

		
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the macro in Batch mode")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use - location relative to rat/data/, default = geo/snoplus.geo", default = "geo/snoplus.geo")
    parser.add_option("-l", type = "string", dest = "loadDB", help = "Load an extra .ratdb directory")
    parser.add_option("-p", type = "string", dest = "particle", help = "Particle type to use (see generator documentation for available particles), default = 'e-'", default = "e-")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = labppo_scintillator", default = "labppo_scintillator")
    (options, args) = parser.parse_args()
    ProduceRunMacros(options)

