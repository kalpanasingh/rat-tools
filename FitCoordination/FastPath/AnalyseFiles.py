#!/usr/bin/env python
import string, ROOT, rat, FastPathUtil
# Analyses the files to determine the travel times in each media
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>

def AnalyseFiles():
	""" Analyses and finds the minimum effective refractive index for each media
	at 400 +- 10nm."""

	refractHistos = FastPathUtil.ProduceRefractiveIndexHistograms()
	scintR = refractHistos[0]
	avR = refractHistos[1]
	waterR = refractHistos[2]
	print "scintR: %.3fd," % scintR.GetXaxis().GetBinCenter( scintR.GetMaximumBin() )
	print "avR: $.3fd," % avR.GetXaxis().GetBinCenter( avR.GetMaximumBin() )
	print "waterR: %0.3fd," % waterR.GetXaxis().GetBinCenter( waterR.GetMaximumBin() )
				
if __name__ == '__main__':
	AnalyseFiles()
