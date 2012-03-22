#!/usr/bin/env python
import ROOT, rat, NearAVUtil
# Plots useful to calibrating the NearAV method
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>

def PlotAveragedHistograms():
	""" Draws the averaged timed histograms overlaided on the same plot."""
	print "Average Histogram Plotting"
	averageHistograms = []
	posSet = sorted( range( 5400, 6100, 100 ) + [5000] )
	for pos in posSet:
		fileName = "Electron3MeV_" + str(pos) + ".root"
		print "Extracting " + fileName
		averageHistograms.append( NearAVUtil.ProduceTimeCorrectedAverageHistogram( fileName ) )

	l1 = ROOT.TLegend( 0.7, 0.5, 0.9, 0.9 )

	for index, histogram in enumerate( averageHistograms ):
		histogram.SetLineColor( index + 1 )
		l1.AddEntry( histogram, str( posSet[index] ) + "mm", "l" )
		if( index == 0 ):
			histogram.GetXaxis().SetTitle( "PMT Hit Time [ns]" )
			histogram.GetYaxis().SetTitle( "Summed hits per 1ns bin" )
			histogram.Draw()
		else:
			histogram.Draw("SAME")

	l1.Draw()
	raw_input( "Hit Enter to exit." )

def PlotAveragedRatios( windowStart,
						windowEnd ):
	""" Draws the scatter plot of averaged ratio versus position."""
	print "Average Ratio Plotting"
	averageHistograms = []
	positions = sorted( range( 5400, 6100, 100 ) + [5000] )
	for pos in positions:
		fileName = "Electron3MeV_" + str(pos) + ".root"
		print "Extracting " + fileName
		averageHistograms.append( NearAVUtil.ProduceTimeCorrectedAverageHistogram( fileName ) )

	plotPoint = 0
	ratioPlot = ROOT.TGraph()
	ratios = NearAVUtil.ProduceEventRatios( averageHistograms, windowStart, windowEnd )
	for pos, ratio in zip( positions, ratios ):
		ratioPlot.SetPoint( plotPoint, ratio, pos )
		plotPoint = plotPoint + 1

	ratioPlot.Draw("A*")
	raw_input( "Hit Enter to exit." )

def PlotRatios( windowStart,
				windowEnd ):
	""" Draws the scatter plot of ratio versus position."""
	print "Ratio Plotting"
	ratioPlot = ROOT.TGraph()
	plotPoint = 0
	for pos in sorted( range( 5400, 6100, 100 ) + [5000] ):
		fileName = "Electron3MeV_" + str(pos) + ".root"
		print "Extracting " + fileName
		histograms = NearAVUtil.ProduceTimeCorrectedHistograms( fileName )

		ratios = NearAVUtil.ProduceEventRatios( histograms, windowStart, windowEnd )
		for ratio in ratios:
			ratioPlot.SetPoint( plotPoint, pos, ratio )
			plotPoint = plotPoint + 1

	ratioPlot.Draw("A*")
	raw_input( "Hit Enter to exit." )

import optparse
if __name__ == '__main__':
	ROOT.gROOT.SetStyle("Plain")
	ROOT.gStyle.SetCanvasBorderMode(0)
	ROOT.gStyle.SetPadBorderMode(0)
	ROOT.gStyle.SetPadColor(0)
	ROOT.gStyle.SetCanvasColor(0)
	ROOT.gStyle.SetOptTitle(0)
	ROOT.gStyle.SetLabelSize( 0.06, "xyz" )
	ROOT.gStyle.SetTitleSize( 0.06, "xyz" )
	ROOT.gStyle.SetOptStat(0)									

	parser = optparse.OptionParser( usage = "usage: %prog [options] windowStart windowEnd", version="%prog 1.0" )
	parser.add_option( "-a", action="store_true", dest="average", default=False, help="Use averaged histograms?" )
	(options, args) = parser.parse_args()
	if len( args ) != 2:
		PlotAveragedHistograms()
	elif( options.average ):
		PlotAveragedRatios( float( args[0] ), float( args[1] ) )
	else:
		PlotRatios( float( args[0] ), float( args[1] ) )
	
