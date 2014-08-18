#!/usr/bin/env python
# Run rat and produce data for each effective speed
# Author I T Coulter - 5/12/2012
import os
import sys
import string
import ScintEffectiveSpeedUtil

def ProduceRunMacFile( options ):
    """Produces and then runs the appropriate mac files."""

    batch_params = None
    if options.batch:
        batch_params = {}
        execfile( options.batch, {}, batch_params )
        
    inFile = open( "Base.mac", "r" )
    rawText = string.Template( inFile.read() )
    inFile.close()

    inFile = open( "batch.sh", "r" )
    rawScriptText = string.Template( inFile.read() )
    inFile.close()

    extraDB = ""
    if options.loaddb:
        extraDB = "/rat/db/load " + options.loaddb

    for speed in ScintEffectiveSpeedUtil.transitTime:
        outText = rawText.substitute( Speed = str( "%.0f" % speed ),
                                      GeoFile = options.geoFile,
                                      ScintMaterial = options.scintMaterial,
                                      Particle = options.particle,
                                      ExtraDB = extraDB)
        outFileName = "scintFit_%.0f.mac" % speed
        outFile = open( outFileName, "w" )
        outFile.write( outText )
        outFile.close()

        if options.batch:
            outText = rawScriptText.substitute( Preamble = "\n".join(s for s in batch_params['preamble']),
                                                Cwd = os.environ['PWD'].replace("/.", "/"),
                                                Macro = outFileName,
                                                Ratenv = batch_params['ratenv'] )
            outScriptName = "scintFit_%.0f.sh" % speed
            outScript = open( outScriptName, "w" )
            outScript.write( outText )
            outScript.close()
            os.system( batch_params["submit"] + " " + outScriptName )
        else:
            os.system( "rat " + outFileName )
            os.remove( outFileName )
    
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option( "-g", type="string", dest="geoFile", help="Geometry File to use, location must be absolute or relative to target.", default="geo/snoplus.geo" )
    parser.add_option( "-s", type="string", dest="scintMaterial", help="Scintillator material.", default="labppo_scintillator" )
    parser.add_option( "-p", type="string", dest="particle", help="Particle type.", default="e-" )
    parser.add_option( "-b", type="string", dest="batch", help="Run in batch mode" )
    parser.add_option( "-l", type="string", dest="loaddb", help="Load additional database directory" )
    (options, args) = parser.parse_args()

    ProduceRunMacFile( options )
    
            
