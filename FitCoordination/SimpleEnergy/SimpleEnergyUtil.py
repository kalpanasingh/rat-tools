#!/usr/bin/env python
import string, ROOT, rat
# Useful utility functions
# Author P G Jones - 07/06/2011 <p.jones22@physics.ox.ac.uk>

def ProduceNhitRadiusGraph():
	"""Produces a Nhit versus mc radius plot."""

	plotPoint = 0
	nhitRadiusPlot = ROOT.TGraph()
	for ds in rat.dsreader( "E1MeV.root" ):
		mc = ds.GetMC()
		if( ds.GetEVCount() == 0 ):
			continue
		ev = ds.GetEV(0)
		# Fill the Plot
		nhitRadiusPlot.SetPoint( plotPoint, mc.GetMCParticle(0).GetPos().Mag(), ev.GetPMTCalCount() )
		plotPoint = plotPoint + 1

	return nhitRadiusPlot


def ProduceNhitOriginHistogram():
	"""Histogram the origin mc events."""

	nhitOriginHisto = ROOT.TH1D( "NhitOrigin", "NhitOrigin", 200, 300, 500 )
	for ds in rat.dsreader( "E1MeV.root" ):
		mc = ds.GetMC()
		if( ds.GetEVCount() == 0 ):
			continue
		ev = ds.GetEV(0)
		# Fill the Plot
		if( mc.GetMCParticle(0).GetPos().Mag() < 10 ):
			nhitOriginHisto.Fill( ev.GetPMTCalCount() )

	return nhitOriginHisto
