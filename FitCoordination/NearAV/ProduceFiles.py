#!/usr/bin/env python
import os, sys, string
# Author P G Jones - 13/03/2011 <p.jones22@physics.ox.ac.uk>


def ProduceRunMacFile():
	"""Produces and then runs the appropriate mac files."""
	inFile = open( "Electron3MeV.mac", "r" )
	rawText = string.Template( inFile.read() )
	inFile.close()
	for pos in sorted( [5000] + range( 5400, 6100, 100 ) ):
		outText = rawText.substitute( SourcePos = str( pos ) )
		outFileName = "Electron3MeV_" + str(pos) + ".mac"
		outFile = open( outFileName, "w" )
		outFile.write( outText )
		outFile.close()
		os.system( "rat " + outFileName )
		os.remove( outFileName )

if __name__ == '__main__':
	ProduceRunMacFile()
