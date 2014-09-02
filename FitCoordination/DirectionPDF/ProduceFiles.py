#!/usr/bin/env python
import os, sys, string


def ProduceRunMacFile( options ):
    """Produces and then runs the appropriate mac files."""
    if options.batch:
        print "Batch mode not required for this FitCoordinator"
    extraDB = ""
    if options.loadDB:
        extraDB = "/rat/db/load " + options.loadDB

    inFile = open( "Data_for_PDF.mac", "r" )
    rawText = string.Template( inFile.read() )
    inFile.close()
    outText = rawText.substitute( GeoFile = options.geoFile,
                                  ScintMaterial = options.scintMaterial,
                                  Particle = options.particle,
                                  ExtraDB = extraDB)
    outFileName = "Data_for_PDF__" + options.scintMaterial + ".mac"
    outFile = open( outFileName, "w" )
    outFile.write( outText )
    outFile.close()
    os.system( "rat " + outFileName )
#    os.remove( outFileName )

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option( "-g", type="string", dest="geoFile", help="Geometry File to use, location must be absolute or relative to target.", default="geo/snoplus_water.geo" )
    parser.add_option( "-s", type="string", dest="scintMaterial", help="Scintillator material.", default="lightwater_sno" )
    parser.add_option( "-p", type="string", dest="particle", help="Particle type.", default="e-" )
    parser.add_option( "-b", type="string", dest="batch", help="Run in batch mode" )
    parser.add_option( "-l", type="string", dest="loadDB", help="Load an extra DB directory")
    (options, args) = parser.parse_args()
    ProduceRunMacFile( options )
