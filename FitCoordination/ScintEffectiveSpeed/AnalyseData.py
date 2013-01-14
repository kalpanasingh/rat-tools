#!/usr/bin/env python
# Analyses the data and prints the results to screen in ratdb format
# Author I Coulter - 09/11/2012
import string
import ROOT
import ScintEffectiveSpeedUtil

def AnalyseData( options ):
    """ Run over the produced data and output the results in ratdb format."""
    histograms = ScintEffectiveSpeedUtil.ProduceAllData()
    # Fit a straight line
    endRange = histograms[1].FindLastBinAbove( 1.0 )
    linearFit = ROOT.TF1( "quad", "[0] + [1]*x", -1000.0, 1000.0 )#histograms[1].GetXaxis().GetBinCenter( endRange ) )
    histograms[1].Fit( linearFit, "r" )
    # Print the results
    print "{\nname: \"EFFECTIVE_VELOCITY\","
    print "index: \"%s\"," % options.index
    print "valid_begin : [0, 0],\nvalid_end : [0, 0],"
    print "ScintVg: %.2fd," % linearFit.GetParameter( 0 )
    print "AVVg: 1.93109181500140664d+02,"
    print "WaterVg: 2.17554021555098529d+02,"
    print "Offset: 0.6d,"
    print "}"

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option( "-i", type="string", dest="index", help="RATDB index to place result.", default="" )
    (options, args) = parser.parse_args()
    AnalyseData( options )
    
