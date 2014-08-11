#!/usr/bin/env python
import os, sys, string, SeededUtilities
# Author K Majumdar - 14/05/2012 <Krishanu.Majumdar@physics.ox.ac.uk>


def ProduceRunMacFiles(options):
    # produces and then runs the required mac files
    
    # load the basic mac file
    inFile = open("Base.mac", "r")
    rawText = string.Template(inFile.read())
    inFile.close()

    # load any batch options
    batch_params = None
    if options.batch:
        batch_params = {}
        execfile( options.batch, {}, batch_params )

    inFile = open( "batch.sh", "r" )
    rawScriptText = string.Template( inFile.read() )
    inFile.close()

    extraDB = ""
    if options.loadDB:
        extraDB = "/rat/db/load " + options.loadDB
    
    # generate the specific mac files for each particle, with energies and corresponding names given in the Utilities tables
    for index, energy in enumerate(SeededUtilities.Energies):
        if index == 0:
            generator = "/generator/vtx/set alpha 0 0 0 " + str(energy)                        
            outfile = SeededUtilities.Particles[0]
            hadrons = ""
        elif index == 1:
            generator = "/generator/vtx/set e- 0 0 0 " + str(energy)
            outfile = SeededUtilities.Particles[1]
            hadrons = "/PhysicsList/OmitHadronicProcesses true"
            
        outText = rawText.substitute(Generator = generator,
                                     GeoFile = options.geoFile,
                                     ScintMaterial = options.scintMaterial,
                                     OmitHadrons = hadrons,
                                     OutFileName = outfile + ".root",
                                     ExtraDB = extraDB)
            
        outFile = open(outfile + ".mac", "w")
        outFile.write(outText)
        outFile.close()

        print "Running " + outfile + ".mac and generating " + outfile + ".root"
        
        if options.batch:
            # run the macro on a batch system 
            outText = rawScriptText.substitute( Preamble = "\n".join(s for s in batch_params['preamble']),
                                                Cwd = os.environ['PWD'].replace("/.", "/"),
                                                Macro = outfile + ".mac",
                                                Ratenv = batch_params['ratenv'] )
            outFile = open(outfile + ".sh", "w")
            outFile.write(outText)
            outFile.close()
            os.system( batch_params["submit"] + " " + outfile +".sh" )        

        else:
            # run the mac file for the particle
            os.system("rat " + outfile + ".mac")
            
            # delete the particle-specific mac file when running is complete
            os.remove(outfile + ".mac")


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use - location must be absolute or relative to target.", default = "geo/snoplus.geo")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator material.", default = "labppo_scintillator")
    parser.add_option("-p", type = "string", dest = "particle", help = "Particle type - this is not relevant for this coordinator.", default = "")
    parser.add_option("-b", type="string", dest="batch", help="Run in batch mode" )
    parser.add_option("-l", type="string", dest="loadDB", help="Load an extra DB directory")
    (options, args) = parser.parse_args()
    ProduceRunMacFiles(options)
    
