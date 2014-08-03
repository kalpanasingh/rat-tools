#!/usr/bin/env python
# Run rat and produce data for each position in the posSet
# Author P G Jones - 13/03/2011 <p.jones22@physics.ox.ac.uk>
import os
import sys
import string
import EffectiveTransitTimeUtil

def ProduceRunMacFile( options ):
    """Produces and then runs the appropriate mac files."""
    inFile = open( "Base.mac", "r" )
    rawText = string.Template( inFile.read() )
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

    for pos in EffectiveTransitTimeUtil.posSet:
        outText = rawText.substitute( SourcePos = str( "%.0f" % pos ),
                                      GeoFile = options.geoFile,
                                      ScintMaterial = options.scintMaterial,
                                      Particle = options.particle,
                                      ExtraDB = extraDB )
        outFileName = "P%.0f.mac" % pos
        outFile = open( outFileName, "w" )
        outFile.write( outText )
        outFile.close()

        print "Running " + outfile + ".mac and generating " + outfile + ".root"

        if options.batch:
            # run the macro on a batch system 
            outText = rawScriptText.substitute( Preamble = "\n".join(s for s in batch_params['preamble']),
                                                Cwd = os.environ['PWD'].replace("/.", "/"),
                                                Macro = outFileName,
                                                Ratenv = batch_params['ratenv'] )
            outScriptName = "P%.0f.sh" % pos
            outFile = open(outScriptName, "w")
            outFile.write(outText)
            outFile.close()
            os.system( batch_params["submit"] + " " + outScriptName )

        else:
            # run the mac file for the particle
            os.system( "rat " + outFileName )
            os.remove( outFileName )
    
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option( "-g", type="string", dest="geoFile", help="Geometry File to use, location must be absolute or relative to target.", default="geo/snoplus.geo" )
    parser.add_option( "-s", type="string", dest="scintMaterial", help="Scintillator material.", default="labppo_scintillator" )
    parser.add_option( "-p", type="string", dest="particle", help="Particle type.", default="e-" )
    parser.add_option( "-b", type="string", dest="batch", help="Run in batch mode" )
    parser.add_option( "-l", type="string", dest="loadDB", help="Load an extra DB directory")
    (options, args) = parser.parse_args()
    ProduceRunMacFile( options )
    
            
