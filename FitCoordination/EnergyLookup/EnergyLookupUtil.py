#!/usr/bin/env python
import ROOT, rat
# Useful utility functions
# Author P G Jones - 13/09/2011 <p.jones22@physics.ox.ac.uk>

PosSet = [ 0.0, 2000.0, 4000.0, 5000.0, 5500.0, 5750.0, 5950.0 ]
EnergySet = [ 1.0, 2.0, 3.0, 3.5, 4.0, 5.0 ]

def NhitsHistogram( fileName ):

	nhitHist = ROOT.TH1D( fileName, "Nhit", 300, 0.0, 3000.0 )

	for ds in rat.dsreader( fileName ):
		if( ds.GetEVCount() == 0 ):
			continue
		nhitHist.Fill( ds.GetEV(0).GetPMTCalCount() )

	return nhitHist

def FitGauss( nhitHist ):

	tolerance = 10
	lowBin = nhitHist.FindFirstBinAbove( 0.0 )
	lowBin = lowBin - tolerance
	highBin = nhitHist.FindLastBinAbove( 0.0 )
	highBin = highBin + tolerance
	if( lowBin < 1 ):
		lowBin = 1
	if( highBin > nhitHist.GetNbinsX() ):
		highBin = nhitHist.GetNbinsX()

	fitGauss = ROOT.TF1( "gaus", "gaus", nhitHist.GetBinCenter( lowBin ), nhitHist.GetBinCenter( highBin ) )
	nhitHist.Fit( fitGauss, "rN" )

	return [ fitGauss.GetParameter( 1 ), fitGauss.GetParameter( 2 ) ]

def NhitPerMeVEnergyPos():
	""" Return 2d array (energy, pos) of the nhit per MeV values."""
	global EnergySet, PosSet
	resultTable = []

	for energy in EnergySet:
		posList = []
		for pos in PosSet:
			fileName = "P%.0fE%.0f.root" % (pos, (energy * 10))
			print fileName
			posList.append( FitGauss( NhitsHistogram( fileName ) )[0] )
		resultTable.append( posList )

	return resultTable

def SigmaPerMeVEnergyPos():
	""" Return 2d array (energy, pos) of the nhit per MeV values."""
	global EnergySet, PosSet
	resultTable = []
	
	for energy in EnergySet:
		posList = []
		for pos in PosSet:
			fileName = "P%.0fE%.0f.root" % (pos, (energy * 10))
			print fileName
			posList.append( FitGauss( NhitsHistogram( fileName ) )[1] )
		resultTable.append( posList )
		
	return resultTable

def NhitPerMeVPosEnergy():
	""" Return 2d array (pos, energy) of the nhit per MeV values."""
	global EnergySet, PosSet
	resultTable = []

	for pos in PosSet:
		energyList = []
		for energy in EnergySet:
			fileName = "P%.0fE%.0f.root" % (pos, (energy * 10))
			print fileName
			energyList.append( FitGauss( NhitsHistogram( fileName ) )[0] )
		resultTable.append( energyList )
			
	return resultTable