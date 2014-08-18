#!/usr/bin/env python
# Run rat and produce data for each effective speed
# Author I T Coulter - 9/11/2012
import os
import sys
import string
import QuadSpeedUtil
import rat

def ProduceRunMacFile( options ):
    """Produces and then runs the appropriate mac files."""

    # load the basic mac file
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

    for speed in QuadSpeedUtil.transitTime:
        # TODO:
        # Load the database and check whether a QUAD_FIT table exists for this material
        # If not, use the default material
        # Currently cannot do this: can't load DB in python
        quad_db = rat.db.get
        transitTimeText = "/rat/db/set QUAD_FIT light_speed %s" % speed
        if not options.default:
            transitTimeText = "/rat/db/set QUAD_FIT[%s] light_speed %s" % ( options.scintMaterial, speed )
        outText = rawText.substitute( Speed = str( "%.0f" % speed ),
                                      GeoFile = options.geoFile,
                                      ScintMaterial = options.scintMaterial,
                                      Particle = options.particle,
                                      TransitTime = transitTimeText,
                                      ExtraDB = extraDB)
        outFileName = "quad_%.0f.mac" % speed
        outFile = open( outFileName, "w" )
        print "MACRO:"
        print outText
        outFile.write( outText )
        outFile.close()

        print "Running " outFileName

        if options.batch:
            # run the macro on a batch system 
            outText = rawScriptText.substitute( Preamble = "\n".join(s for s in batch_params['preamble']),
                                                Cwd = os.environ['PWD'].replace("/.", "/"),
                                                Macro = outfile + ".mac",
                                                Ratenv = batch_params['ratenv'] )
            outScriptName = "quad_%.0f.sh" % speed
            outFile = open(outScriptName, "w")
            outFile.write(outText)
            outFile.close()
            os.system( batch_params["submit"] + " " + outScriptName )

        else:
            # run the macro locally
            os.system( "rat " + outFileName )
            os.remove( outFileName )
    
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option( "-g", type="string", dest="geoFile", help="Geometry File to use, location must be absolute or relative to target.", default="geo/snoplus.geo" )
    parser.add_option( "-s", type="string", dest="scintMaterial", help="Scintillator material.", default="labppo_scintillator" )
    parser.add_option( "-p", type="string", dest="particle", help="Particle type.", default="e-" )
    parser.add_option( "-t", type="string", dest="transitTimes", help="Transit times (accepts a list).",
                       action="callback", callback=QuadSpeedUtil.parse_list_arg)
    parser.add_option("-b", type="string", dest="batch", help="Run in batch mode" )
    parser.add_option("-l", type="string", dest="loadDB", help="Load an extra DB directory")
    (options, args) = parser.parse_args()
    ProduceRunMacFile( options )
    
            
