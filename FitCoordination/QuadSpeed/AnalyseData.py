#!/usr/bin/env python
# Analyses the data and prints the results to screen in ratdb format
# Author I Coulter - 09/11/2012
import string
import ROOT
import QuadSpeedUtil

def AnalyseData( options ):
    """ Run over the produced data and output the results in ratdb format."""
    histograms = QuadSpeedUtil.ProduceAllData()
    # Fit a straight line
    endRange = histograms[1].FindLastBinAbove( 1.0 )
    linearFit = ROOT.TF1( "quad", "[0] + [1]*x", -1000.0, 1000.0 )#histograms[1].GetXaxis().GetBinCenter( endRange ) )
    histograms[1].Fit( linearFit, "r" )
    # Print the results
    print "{\nname: \"QUAD_FIT\","
    print "index: \"%s\"," % options.index
    print "valid_begin : [0, 0],\nvalid_end : [0, 0],\n"
    print "light_speed: %.2fd,  // Effective overall speed of light" % linearFit.GetParameter( 0 )
    print "num_points: 4000,      // Max points generated in quadcloud"
    print "limit_points: 20000,   // Number of attempts to generate points"
    print "calc_time: 1,       // Whether to calcuate the reconstructed time"
    print "calc_errors: 1,     // Whether to compute errors on time & position"
    print "}"

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option( "-i", type="string", dest="index", help="RATDB index to place result.", default="" )
    (options, args) = parser.parse_args()
    AnalyseData( options )
    
