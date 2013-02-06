#!/usr/bin/env python
import os, sys, string


def ProduceRunMacFile( options ):
	"""Produces and then runs the appropriate mac files."""
	inFile = open( "Data_for_PDF.mac", "r" )
	rawText = string.Template( inFile.read() )
	inFile.close()
	outText = rawText.substitute( GeoFile = options.geoFile,
                                      ScintMaterial = options.scintMaterial,
				      Particle = options.particle )
        outFileName = "Data_for_PDF__" + options.scintMaterial + ".mac"
        outFile = open( outFileName, "w" )
        outFile.write( outText )
        outFile.close()
        os.system( "rat " + outFileName )
        os.remove( outFileName )

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option( "-g", type="string", dest="geoFile", help="Geometry File to use, location must be absolute or relative to target.", default="geo/snoplus.geo" )
    parser.add_option( "-s", type="string", dest="scintMaterial", help="Scintillator material.", default="lightwater_sno" )
    parser.add_option( "-p", type="string", dest="particle", help="Particle type.", default="e-" )

    (options, args) = parser.parse_args()
    ProduceRunMacFile( options )
