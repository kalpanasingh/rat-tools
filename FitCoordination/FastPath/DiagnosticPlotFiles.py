#!/usr/bin/env python
import ROOT, rat, FastPathUtil
# Plots useful to fast path coordination
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>

def PlotRefractiveIndexHistograms():
	""" Draws the refractive index histograms."""
	refractHistos = FastPathUtil.ProduceRefractiveIndexHistograms()
	scintR = refractHistos[0]
	avR = refractHistos[1]
	waterR = refractHistos[2]

	c1 = ROOT.TCanvas()
	c1.Divide( 3, 1 )
	c1.cd(1)
	scintR.Draw()
	c1.cd(2)
	avR.Draw()
	c1.cd(3)
	waterR.Draw()
	raw_input( "Hit Enter to exit." )


import optparse
if __name__ == '__main__':
	PlotRefractiveIndexHistograms()
