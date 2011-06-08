#!/usr/bin/env python
import ROOT, rat, SimpleEnergyUtil
# Plots useful to fast path coordination
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>

def PlotNhitRadiusGraph():
	"""Plots the Nhit v radius graph.""" 

	nhitRPlot = SimpleEnergyUtil.ProduceNhitRadiusGraph()
	nhitOrigin = SimpleEnergyUtil.ProduceNhitOriginHistogram()
	c1 = ROOT.TCanvas()
	c1.Divide( 1, 2 )
	c1.cd(1)
	nhitRPlot.Draw("A*")
	c1.cd(2)
	nhitOrigin.Draw()
	raw_input( "Hit Enter to exit." )


if __name__ == '__main__':
	PlotNhitRadiusGraph()
