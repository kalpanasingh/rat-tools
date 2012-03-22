#!/usr/bin/env python
import string, ROOT, EmissionPDFUtil, sys
# Returns the PDF in ratdb format
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>

def AnalyseFiles( options ):
	""" Output the pdf to the screen in useful ratdb format."""

	pdf = EmissionPDFUtil.ProducePDF()
	startBin = pdf.FindFirstBinAbove( 1e-10 )
	endBin = pdf.FindLastBinAbove( 1e-8 ) # two Mag higher after at least.

    print "{\nname: \"ET1D\","
    print "index: \"%s\"," % options.index
    print "valid_begin : [0, 0],\nvalid_end : [0, 0],"
 	print "time: [",
	for iBin in range( startBin, endBin ):
		tempText = str( pdf.GetXaxis().GetBinCenter( iBin ) )
		sys.stdout.write( tempText + "d, " )
	print "]"
	print "probability: [",
	for iBin in range( startBin, endBin ):
		outText = "" 
		tempText = "%e" % float( pdf.GetBinContent( iBin ) )
		if( tempText.find( "e" ) != -1 ):
			outText = outText + tempText.replace( "e", "d" ) + ", "
		else:
			outText = outText + tempText + "d, "
		sys.stdout.write( outText )
	print "]"
    print "}"
	
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option( "-i", type="string", dest="index", help="RATDB index to place result.", default="" )
    (options, args) = parser.parse_args()
    AnalyseFiles( options )
    
