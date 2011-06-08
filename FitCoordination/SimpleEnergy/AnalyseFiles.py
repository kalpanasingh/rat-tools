#!/usr/bin/env python
import string, ROOT, SimpleEnergyUtil
# Analyses the files to determine the Nhit to MeV ratio
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>

def AnalyseFiles():
	""" Determine the Nhit to MeV ratio, then the dependence near the AV."""

	nhitRPlot = SimpleEnergyUtil.ProduceNhitRadiusGraph()
	nhitOrigin = SimpleEnergyUtil.ProduceNhitOriginHistogram()
	# Fit gaussian to origin nhits
	originFit = ROOT.TF1( "gaus", "gaus", 300.0, 500.0 )
	nhitOrigin.Fit( originFit )
	# Fit a straight line to nit R plot
	avNhitFit = ROOT.TF1( "linear", "[0] + [1]*x", 5000.0, 6000.0 )
	nhitRPlot.Fit( avNhitFit )
	# Print the results
	print "nhit_per_mev: %.2fd," % originFit.GetParameter( 1 )
	print "nhit_intercept: %.2fd," % avNhitFit.GetParameter( 0 )
	print "nhit_gradient: %.6fd," % avNhitFit.GetParameter( 1 )

if __name__ == '__main__':
	AnalyseFiles()