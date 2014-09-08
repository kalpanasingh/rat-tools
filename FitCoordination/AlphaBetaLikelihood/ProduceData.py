#!/usr/bin/env python
import os, sys, string, Utilities
# Author E Marzece - 13/03/2014 <marzece@sas.upenn.edu>
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
    
    particleNames = Utilities.ParticleNames[options.particle]
     
    # Generate the specific macro for each particle.  The Po212 is done 3 times (one for each possible pulse shape).
    for particleIndex, particle in enumerate(particleNames):
	
        for pulseIndex, pulseDescription in enumerate(Utilities.ParticlePulseDict[particle]):
		
            outfileName = particle + pulseDescription

            if str(particle) == "Te130":
                vertex = "/generator/vtx/set 2beta " + str(particle) + " 0 1"
                hadrons = "/rat/physics_list/OmitHadronicProcesses true" 
            else:
                vertex = "/generator/vtx/set backg " + str(particle)
                hadrons = ""

            # If it is a Po21X and there is a non-default pulse shape, then add that shape to the macro
            if pulseIndex != 0 and pulseDescription != "": 
                timeConstant = "/rat/db/set OPTICS[" + str(options.scintMaterial) + "] SCINTWAVEFORMalpha_value1 [ " + str(Utilities.PulseTimeConstants[pulseDescription]) + "]"
                pulseRatio = "/rat/db/set OPTICS[" + str(options.scintMaterial) + "] SCINTWAVEFORMalpha_value2 [ " + str(Utilities.PulseTimeRatios[pulseDescription]) + "]"
            else:
                timeConstant = ""
                pulseRatio = ""     

            outText1 = rawText1.substitute(Hadrons = hadrons,
                                           ExtraDB = extraDB,
                                           GeoFile = options.geoFile,
                                           ScintMaterial = options.scintMaterial,
                                           PulseLengthTimeConstant = timeConstant,
                                           PulseLengthRatio = pulseRatio,
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
    parser.add_option("-p", type = "string", dest = "particle", help = "Desired Isotope - either 212 or 214", default = "")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = labppo_scintillator", default = "labppo_scintillator")
    (options, args) = parser.parse_args()
    if options.particle == "212" or options.particle == "214": 
        ProduceRunMacros(options)
    else:
        print "You must specify if you want to generate PDFs for Bi212 or Bi214.  This can be done by adding the option -p IsotopeNumber to your command."

