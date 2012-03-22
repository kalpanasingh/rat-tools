#!/usr/bin/env python
import os, sys, string, ROOT, rat, NearAVUtil
# Analyses the files to determine the window, ratio cut, ratio m, ratio c.
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>

def AnalyseFiles( options ):
	""" Main function which determines the window, ratio m and c, first and then the ratio
	cut."""
	# Ratio window is calculated using events near the AV (>5400mm)
	averageHistograms = []
	for pos in sorted( range( 5400, 6100, 100 ) ):
		fileName = "Electron3MeV_" + str(pos) + ".root"
		print "Extracting " + fileName
		averageHistograms.append( NearAVUtil.ProduceTimeCorrectedAverageHistogram( fileName ) )

	bestWindow = FindBestWindow( averageHistograms )

	# The ratio is calculated using events away from the AV (<5400mm)
	fileName = "Electron3MeV_5000.root"
	histograms = NearAVUtil.ProduceTimeCorrectedHistograms( fileName )
	bestRatio = FindBestRatioCut( histograms, bestWindow[0], bestWindow[1] )

    print "{\nname: \"FIT_NEAR_AV\","
    print "index: \"%s\",\n" % options.index
    print "valid_begin : [0, 0],\nvalid_end : [0, 0],"
        
	print "region_start: %.2fd," % bestWindow[0]
	print "region_end: %.2fd," % bestWindow[1]
	print "ratio_m: %.2fd," % bestWindow[2]
	print "ratio_c: %.2fd," % bestWindow[3]
	print "ratio_cut: %.2fd," % bestRatio[0]
    print "}"

def FindBestWindow( histograms ):
	""" Finds the best window for the NearAV method. The best window is the one with the largest
	negative gradient of dRatio by dPosition i.e. the window with the largest position discrimination."""
	starts = []
	ends = []
	gradients = []
	intercepts = []
	for windowStart in range( 255, 350 ):
		for windowEnd in range( windowStart + 1, 400 ):
			ratios = NearAVUtil.ProduceEventRatios( histograms, windowStart, windowEnd )
			# Now plot these ratios such that a root fit can be used
			ratioPlot = ROOT.TGraph()
			for index, ratio in enumerate( ratios ):
				ratioPlot.SetPoint( index, 5400.0 + index * 100, ratio )

			# Fit a straight line
			ratioFit = ROOT.TF1( "linear", "[0] + [1]*x", 0.0, 1.0 )
			ratioPlot.Fit( ratioFit )
			# Need a has fit worked check, good Fval/deg?

			starts.append( windowStart )
			ends.append( windowEnd )
			intercepts.append( ratioFit.GetParameter( 0 ) )
			gradients.append( ratioFit.GetParameter( 1 ) )

	minIndex = gradients.index( min( gradients ) )
	return [ starts[minIndex], ends[minIndex], 1.0 / gradients[minIndex], -intercepts[minIndex] / gradients[minIndex] ] # Note ratio m is dPos by dRatio

def FindBestRatioCut( histograms,
					  windowStart,
					  windowEnd ):
	""" Find the best ratio cut for the nearAV method. The best ratio is cut is the ratio which
	doesn't cut any event that are away from the AV. """
	ratioPlot = ROOT.TH1D( "ratioPlot", "ratioPlot", 100, 0.0, 1.0 )
	ratios = NearAVUtil.ProduceEventRatios( histograms, windowStart, windowEnd )
	for ratio in ratios:
		ratioPlot.Fill( ratio )

	# Now fit a guassian to it
	ratioFit = ROOT.TF1( "gaus", "gaus", 0.0, 1.0 )
	ratioPlot.Fit( ratioFit )
	return [ ratioFit.GetParameter( 1 ) - 3.0 * ratioFit.GetParameter( 2 ), ratioFit.GetParameter( 1 ), ratioFit.GetParameter( 2 ) ]

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option( "-i", type="string", dest="index", help="RATDB index to place result.", default="" )
    (options, args) = parser.parse_args()
	AnalyseFiles( options )
