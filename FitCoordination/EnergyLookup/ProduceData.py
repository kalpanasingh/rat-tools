#!/usr/bin/env python
import os, sys, string, EnergyLookupUtil
# Author P G Jones - 12/09/2011 <p.jones22@physics.ox.ac.uk>

def ProduceRunFiles( options ):
	# Load the raw Base file
	inFile = open( "Base.mac", "r" )
	rawText = string.Template( inFile.read() )
	inFile.close()

	for pos in EnergyLookupUtil.PosSet:
		for energy in EnergyLookupUtil.EnergySet:
			# Set the generator text first
			generator = "/generator/add combo gun:point\n" + \
						"/generator/vtx/set e- 0 0 0 " + str( energy ) + "\n" + \
						"/generator/pos/set 0 %.0f 0" % pos 
			# Create the correct file
			outFileName = "P%.0fE%.0f" % (pos, (energy * 10))
			outText = rawText.substitute( Generator = generator,
                                          GeoFile = options.geoFile,
                                          ScintMaterial = options.scintMaterial,
                                          OutFileName = outFileName + ".root" ) # Note upper/lower case first letter...
			outFile = open( outFileName + ".mac", "w" )
			outFile.write( outText )
			outFile.close()
			# Now run it
			print "Running " + outFileName
			os.system( "rat " + outFileName + ".mac" )
			# Now delete the temporary mac file
			os.remove( outFileName + ".mac" )
		
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option( "-g", type="string", dest="geoFile", help="Geometry File to use, location must be absolute or relative to target.", default="geo/snoplus.geo" )
    parser.add_option( "-s", type="string", dest="scintMaterial", help="Scintillator material.", default="scintillator" )
    (options, args) = parser.parse_args()
    ProduceRunFiles( options )
