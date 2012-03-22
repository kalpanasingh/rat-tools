#!/usr/bin/env python
import os, sys, string
# Author P G Jones - 13/03/2011 <p.jones22@physics.ox.ac.uk>


def ProduceRunMacFile( options ):
	"""Produces and then runs the appropriate mac files."""
	inFile = open( "Electron3MeV.mac", "r" )
	rawText = string.Template( inFile.read() )
	inFile.close()
	for pos in sorted( [5000] + range( 5400, 6100, 100 ) ):
		outText = rawText.substitute( SourcePos = str( pos ),
                                      GeoFile = options.geoFile,
                                      ScintMaterial = options.scintMaterial )
		outFileName = "Electron3MeV_" + str(pos) + ".mac"
		outFile = open( outFileName, "w" )
		outFile.write( outText )
		outFile.close()
		os.system( "rat " + outFileName )
		os.remove( outFileName )

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option( "-g", type="string", dest="geoFile", help="Geometry File to use, location must be absolute or relative to target.", default="geo/snoplus.geo" )
    parser.add_option( "-s", type="string", dest="scintMaterial", help="Scintillator material.", default="scintillator" )
    (options, args) = parser.parse_args()
	ProduceRunMacFile( options )
