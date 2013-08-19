#!/usr/bin/env python
import ROOT, rat
# Useful utility functions
# Author P G Jones - 13/09/2011 <p.jones22@physics.ox.ac.uk>

PosSet = [ 0.0, 2000.0, 4000.0, 5000.0, 5500.0, 5750.0, 5950.0 ]
EnergySet = [ 1.0, 2.0, 3.0, 3.5, 4.0, 5.0 ]

ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(0)
ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetLabelSize( 0.06, "xyz" )
ROOT.gStyle.SetTitleSize( 0.06, "xyz" )
ROOT.gStyle.SetOptStat(0)

def NHitEnergyHistogram( fileName ):
	""" Return [NHit, energy] histogram. """
	nhitHist = ROOT.TH1D( fileName, "NHit", 300, 0.0, 3000.0 )
	energyHist = ROOT.TH1D( fileName, "Energy", 600, 0.0, 6.0 )

	for ds, run in rat.dsreader( fileName ):
		if( ds.GetEVCount() == 0 ):
			continue
		if( ds.GetEV(0).GetFitResult( "energyLookup:scintFitter" ).GetValid() ):
			energyHist.Fill( ds.GetEV(0).GetFitResult( "energyLookup:scintFitter" ).GetVertex(0).GetEnergy() )
			nhitHist.Fill( ds.GetEV(0).GetPMTCalCount() )

	return [nhitHist, energyHist]

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

def NHitEnergyResArray():
	""" Return a 2d array (energy, pos) of [NHit, energy] percentage resolutions. """
	global EnergySet, PosSet
	resultTable = []
	for energy in EnergySet:
		posList = []
		for pos in PosSet:
			fileName = "P%.0fE%.0f.root" % (pos, (energy * 10))
			print fileName
			histos = NHitEnergyHistogram( fileName )
			fitRes = [ FitGauss( x ) for x in histos ]
			posList.append( [ fitRes[0][1] / fitRes[0][0], fitRes[1][1] / fitRes[1][0] ] )
		resultTable.append( posList )
	return resultTable

def Plot():

	global EnergySet, PosSet
	dataArray = NHitEnergyResArray()
	print dataArray
	graphs = []
	graphPoints = []
	for iPos in range( 0, len( PosSet ) ):
		graphs.append( [ ROOT.TGraph(), ROOT.TGraph() ] )
		graphPoints.append(0)
		for iEnergy, energy in enumerate( EnergySet ):
			(graphs[iPos])[0].SetPoint( graphPoints[iPos], energy, (dataArray[iEnergy][iPos])[0] )
			(graphs[iPos])[1].SetPoint( graphPoints[iPos], energy, (dataArray[iEnergy][iPos])[1] )
			graphPoints[iPos] += 1
	c1 = ROOT.TCanvas()
	c1.Divide( 2, len( PosSet ) / 2 )
	for iPad, graph in enumerate( graphs ):
		c1.cd( iPad + 1 )
		graph[0].Draw("A*")
		graph[0].GetYaxis().SetRangeUser( 0.01, 0.1 )
		graph[1].SetMarkerColor( ROOT.kRed )
		graph[1].Draw("*")

	raw_input( "G" )
				
Plot()
