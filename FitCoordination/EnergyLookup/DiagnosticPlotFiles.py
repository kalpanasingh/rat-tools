#!/usr/bin/env python
import ROOT, rat, EnergyLookupUtil
# Plots useful to Energy Lookup coordination
# Author P G Jones - 13/09/2011 <p.jones22@physics.ox.ac.uk>

def PlotNHitPerPos():
    """ Plot the Nhit per radial position for different energies."""
	c1 = ROOT.TCanvas()
	l1 = ROOT.TLegend( 0.1, 0.7, 0.3, 0.9)
	nhitPerMeVtable = EnergyLookupUtil.NhitPerMeVEnergyPos()
	graphs = []
	for iPad, energy in enumerate( EnergyLookupUtil.EnergySet ):
		graph = ROOT.TGraph()
		for graphPoint in range( 0, len( EnergyLookupUtil.PosSet ) ):
			graph.SetPoint( graphPoint, EnergyLookupUtil.PosSet[graphPoint], nhitPerMeVtable[iPad][graphPoint] )
		graph.SetMarkerColor( iPad + 2 )
		graphs.append( graph )
		l1.AddEntry( graph, str(energy), "P" )

	for iGraph, graph in enumerate( graphs ):
		if iGraph == 0:
			graph.Draw( "A*" )
			graph.GetYaxis().SetRangeUser( 0, 2000 )
		else:
			graph.Draw( "*" )
	l1.Draw()

	raw_input( "Hit Enter to exit." )

def PlotNHitPerMeV():
    """ Plot the Nhit per energy for different radial positions."""
	l1 = ROOT.TLegend( 0.1, 0.7, 0.3, 0.9)
	nhitPerMeVtable = EnergyLookupUtil.NhitPerMeVEnergyPos()
	graphs = []
	graphPoints = []
	for iPos in range( 0, len( EnergyLookupUtil.PosSet ) ):
		graphs.append( ROOT.TGraph() )
		graphPoints.append(0)
		for iEnergy, energy in enumerate( EnergyLookupUtil.EnergySet ):
			graphs[iPos].SetPoint( graphPoints[iPos], energy, nhitPerMeVtable[iEnergy][iPos] )
			graphPoints[iPos] += 1
	c1 = ROOT.TCanvas()
	c1.Divide( 2, len( EnergyLookupUtil.PosSet ) / 2 )
	masterFit = ROOT.TF1( "master", "[0] + [1]*x", 0, 5.5 )
	fits = []
	for iPad, graph in enumerate( graphs ):
		c1.cd( iPad + 1 )
		graph.Draw("A*")
		fits.append( masterFit.Clone( "new" + str(iPad) ) )
		graph.Fit( fits[iPad], "r" )

	raw_input( "Hit Enter to exit." )

ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(0)
ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options]", version="%prog 1.0" )
    parser.add_option( "-e", action="store_true", dest="energy", default=False, help="Plot v energy rather than position?" )
    (options, args) = parser.parse_args()
    if options.energy:
        PlotNHitPerMeV()
    else:
        PlotNHitPerPos()
		
