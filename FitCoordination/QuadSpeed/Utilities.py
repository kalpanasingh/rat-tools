#!/usr/bin/env python
import ROOT, rat 
# Useful secondary functions for the QuadSpeed Coordinator
# Author I Coulter - 09/11/2012 <icoulter@hep.upenn.edu>
#        K Majumdar - 11/09/2014 - Cleanup of Coordinators for new DS

Speeds = [ 170.0, 175.0, 180.0, 185.0, 190.0, 195.0, 200.0,]
fiducialCut = 5500


# Produce the Radial Bias vs. Effective Speed plots (2D scatter, and a weighted 1D) across all Speeds
def ProducePlots():

    fullPlot = ROOT.TH2D("fullPlot", "Radial Bias vs. Effective Speed", 2000, -1000.0, 1000.0, 150, 100, 250)
    oneDimPlot = ROOT.TH1D("oneDimPlot", "Radial Bias vs. Effective Speed in 1 Dimension", 2000, -1000.0, 1000.0);
    
    for speed in Speeds:
        infileName = "quadFit_" + str(int(speed)) + ".root"
        meanBias = MeanRadialBias(infileName)

        fullPlot.Fill(meanBias, speed)
        oneDimPlot.Fill(meanBias, speed)

    return [fullPlot, oneDimPlot]
	
	
# Find the mean radial bias at a single speed
def MeanRadialBias(infileName):

    biasPlot = ROOT.TH1D("RadialBias", "RadialBias", 200, -1000.0, 1000.0)
    biasFit = ROOT.TF1("biasFit", "gaus", -1000, 1000)
	
    for ds, run in rat.dsreader(infileName):
        if ds.GetEVCount() == 0:
            continue

        startPosition = ds.GetMC().GetMCParticle(0).GetPosition()

        ev = ds.GetEV(0)

        if not ev.FitResultExists("scintFitter"):
            continue
        if not ev.GetFitResult("scintFitter").GetValid():
            continue
        try:
            fitPosition = ev.GetFitResult("quad").GetVertex(0).GetPosition()
            radialBias = (fitPosition - startPosition).Dot(startPosition.Unit())

            if fitPosition.Mag() < fiducialCut:
                biasPlot.Fill(radialBias)
        except:
            pass

    biasPlot.Fit(biasFit)
    return biasFit.GetParameter(1)


# Draw the Radial Bias vs. Effective Speed 2D plot
def DrawPlot():

    histograms = ProducePlots()
	
    histograms[0].Draw("*")
    histograms[0].GetXaxis().SetTitle("Radial Bias, mm")
    histograms[0].GetYaxis().SetTitle("Effective Speed, mm/ns")
    histograms[0].SetMarkerStyle(20)

    raw_input("Press 'Enter' to exit")


ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(0)
ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

