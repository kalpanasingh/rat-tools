#!/usr/bin/env python
import ROOT, rat, EffectiveTransitTimeUtil
# Plots useful to fast path coordination
# Author P G Jones - 20/07/2011 <p.jones22@physics.ox.ac.uk>

def PlotDistVTime():
	""" Draws the Distance v timing plot."""
	#c2 = ROOT.TCanvas()
	#c2.cd()
	#profile = EffectiveTransitTimeUtil.ProduceProfile()
	#profile.Draw()

	histograms = EffectiveTransitTimeUtil.ProduceFullPDFs()
	c1 = ROOT.TCanvas()
	c1.Divide( 2, 1 )
	c1.cd(1)
	histograms[0].Draw( "COLZ" )
	c1.cd(2)
	histograms[1].GetXaxis().SetTitle( "Distance [mm]" )
	histograms[1].GetXaxis().SetRangeUser( 150.0, 10150.0 )
	histograms[1].GetYaxis().SetTitle( "Time [ns]" )
	histograms[1].SetMarkerStyle( 5 )
	histograms[1].Draw()
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
	PlotDistVTime()
