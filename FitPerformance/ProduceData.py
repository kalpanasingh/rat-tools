#!/usr/bin/env python
import os, sys, string
# Author P G Jones - 13/03/2011 <p.jones22@physics.ox.ac.uk>

def ProduceRunFiles( baseFile, level ):
	"""Produces and then runs the appropriate mac files."""
	level = int( level )
	if( level == 0 or level > 2 ):
		print "Position Varying Run..."
		ProduceRunPosElectronFiles( baseFile )
	if( level == 1 or level > 2 ):
		print "Near AV Position Varying Run..."
		ProduceRunPosElectronFiles( baseFile, True )
	if( level == 2 or level > 2 ):
		print "Energy Varying Run..."
		ProduceRunFillElectronFiles( baseFile )
	print "Finished"


def ProduceRunPosElectronFiles( baseFile, nearAV = False ):
	"""Produces and runs the mac files varying by electron position,
	whilst keeping the energy at 3MeV."""

	# Load the raw Base file
	inFile = open( baseFile, "r" )
	rawText = string.Template( inFile.read() )
	inFile.close()

	posSet = []
	if( nearAV == False ):
		posSet = [ 0.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0, 6000.0 ]
	else:
		posSet = [ 5500.0, 5600.0, 5700.0, 5800.0, 5900.0 ]

	for pos in posSet:
		# Set the generator text first
		generator = "/generator/add combo gun:point\n" + \
					"/generator/vtx/set e- 0 0 0 3.0\n" + \
					"/generator/pos/set 0 %.0f 0" % pos 
		# Create the correct file
		outFileName = "P%.0f" % pos
		outText = rawText.substitute( Generator = generator, OutFileName = outFileName + ".root" ) # Not upper/lower case first letter...
		outFile = open( outFileName + ".mac", "w" )
		outFile.write( outText )
		outFile.close()
		# Now run it
		print "Running " + outFileName
		os.system( "rat -s 10 " + outFileName + ".mac" )
		# Now delete the temporary mac file
		os.remove( outFileName + ".mac" )
		

def ProduceRunFillElectronFiles( baseFile ):
	"""Produces and runs the mac files varying by electron energy,
	whilst filling the av volume."""

	# Load the raw Base file
	inFile = open( baseFile, "r" )
	rawText = string.Template( inFile.read() )
	inFile.close()

	for energy in [ 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0 ]:
		# Set the generator text first
		generator = "/generator/add combo gun:fill\n" + \
					"/generator/vtx/set e- 0 0 0 " + str( energy ) + "\n" + \
					"/generator/pos/set 0 0 0"
		# Create the correct file
		outFileName = "E%.0f" % (energy * 10)
		outText = rawText.substitute( Generator = generator, OutFileName = outFileName + ".root" ) # Not upper/lower case first letter...
		outFile = open( outFileName + ".mac", "w" )
		outFile.write( outText )
		outFile.close()
		# Now run it
		print "Running " + outFileName
		os.system( "rat -s 10 " + outFileName + ".mac" )
		# Now delete the temporary mac file
		os.remove( outFileName + ".mac" )

import optparse
if __name__ == '__main__':
	parser = optparse.OptionParser( usage = "usage: %prog [options] baseFile", version="%prog 1.0" )
	(options, args) = parser.parse_args()

	if( len( args ) == 1 ):
		ProduceRunFiles( args[0], 3 )
	if( len( args ) == 2 ):
		ProduceRunFiles( args[0], args[1] )
