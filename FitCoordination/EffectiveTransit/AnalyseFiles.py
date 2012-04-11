#!/usr/bin/env python
import string, ROOT, EffectiveTransitTimeUtil
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>

def AnalyseFiles( options ):

        histograms = EffectiveTransitTimeUtil.ProduceFullPDFs()
        # Fit a straight line
        endRange = histograms[1].FindLastBinAbove( 1.0 )
        linearFit = ROOT.TF1( "quad", "[0] + [1]*x", 0.0, 10000.0 )#histograms[1].GetXaxis().GetBinCenter( endRange ) )
        histograms[1].Fit( linearFit, "r" )
        # Print the results
        print "{\nname: \"FIT_EFFECTIVE_TRANSIT\","
        print "index: \"%s\"," % options.index
        print "valid_begin : [0, 0],\nvalid_end : [0, 0],"
        print "Intercept: %.2fd," % linearFit.GetParameter( 0 )
        print "Speed: %.2fd," % float( 1.0 / linearFit.GetParameter( 1 ) )
#print "Variation: %.2f" % float(
        print "}"

import optparse
if __name__ == '__main__':
        parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
        parser.add_option( "-i", type="string", dest="index", help="RATDB index to place result.", default="" )
        (options, args) = parser.parse_args()
        AnalyseFiles( options )
        
