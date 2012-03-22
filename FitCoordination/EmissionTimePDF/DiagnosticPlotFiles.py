#!/usr/bin/env python
import ROOT, rat, EmissionPDFUtil
# Plots useful to fast path coordination
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>

def PlotPDF():
	""" Draws the refractive index histograms."""
	pdf = EmissionPDFUtil.ProducePDF()

	c1 = ROOT.TCanvas()
	c1.cd(1)
	pdf.Draw()
	raw_input( "Hit Enter to exit." )


import optparse
if __name__ == '__main__':
	PlotPDF()
