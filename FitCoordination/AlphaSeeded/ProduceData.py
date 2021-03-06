#!/usr/bin/env python
import os, sys, string, Utilities
# Author K Majumdar - 14/05/2012 <Krishanu.Majumdar@physics.ox.ac.uk>
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

    # Load the basic macro template
    inFile1 = open("Template_Macro.mac", "r")
    rawText1 = string.Template(inFile1.read())
    inFile1.close()
	
    # Load the batch submission script template
    inFile2 = open("Template_Batch.sh", "r")
    rawText2 = string.Template(inFile2.read())
    inFile2.close()
    
    # Generate the specific macro for each particle, with energies and corresponding names given in the Utilities tables
    for index, energy in enumerate(Utilities.Energies):
        if index == 0:
            vertex = "/generator/vtx/set alpha 0 0 0 " + str(energy)                        
            outfileName = Utilities.Particles[0]
            hadrons = ""
        elif index == 1:
            vertex = "/generator/vtx/set e- 0 0 0 " + str(energy)
            outfileName = Utilities.Particles[1]
            hadrons = "/rat/physics_list/OmitHadronicProcesses true"
            
        outText1 = rawText1.substitute(Hadrons = hadrons,
                                       ExtraDB = extraDB,
                                       GeoFile = options.geoFile,
                                       ScintMaterial = options.scintMaterial,
                                       FileName = outfileName + ".root",
                                       Vertex = vertex)
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
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = labppo_scintillator", default = "labppo_scintillator")
    (options, args) = parser.parse_args()
    ProduceRunMacros(options)
    
