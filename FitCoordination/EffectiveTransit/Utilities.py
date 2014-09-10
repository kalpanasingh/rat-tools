#!/usr/bin/env python
import ROOT, rat
# Useful secondary functions for the EffectiveTransit Coordinator
# Author P G Jones - 22/05/2011 <p.g.jones@qmul.ac.uk>
#        K Majumdar - 10/09/2014 - Cleanup of Coordinators for new DS

Positions = [0.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0, 5500.0, 5600.0, 5700.0, 5800.0, 5900.0]
 

# Produce the transit time plots (distance vs. time residual and distance vs. transit time) across all positions
def ProducePlots():

    fullPlot = ROOT.TH2D("fullPlot", "Distance vs. Time Residual (no water or AV)", 1200, 0.0, 12000.0, 400, -100.5, 299.5)
    
    for position in Positions:
        infileName = "events_P=" + str(int(position)) + "mm.root"
        UpdatePlot(infileName, fullPlot)

    promptPlot = ROOT.TH1D("promptPlot", "Distance vs Scintillator Transit Time", 1200, 0.0, 12000.0)
    for bin in range(2, 1200):
        yProjection = fullPlot.ProjectionY("yProjection", bin, bin)
        yProjection.SetDirectory(0)
        promptBin = yProjection.GetMaximumBin()
        promptPlot.Fill(fullPlot.GetXaxis().GetBinCenter(bin), fullPlot.GetYaxis().GetBinCenter(promptBin))
    
    return [fullPlot, promptPlot]

	
# Update the Distance vs. Time Residual plot from a single-position rootfile
def UpdatePlot(infileName, fullPlot):

    groupVelocity = rat.utility().GetGroupVelocity()
    lightPath = rat.utility().GetLightPathCalculator()
    pmtInfo = rat.utility().GetPMTInfo()
    
    eventNumber = 0

    for ds, run in rat.dsreader(infileName):
        if eventNumber % 100  == 0:
            print eventNumber
        eventNumber += 1

        mc = ds.GetMC()
        startTime = mc.GetMCParticle(0).GetTime()
        startPosition = mc.GetMCParticle(0).GetPosition()
		
        for pmtIndex in range(0, mc.GetMCPMTCount()):
            mcPMT = mc.GetMCPMT(pmtIndex)
            pmtPosition = pmtInfo.GetPosition(mcPMT.GetPMTID())
			
            # If the event was not near the AV centre, only look at PMTs within 10 degrees angle (forwards and backwards)
            if (startPosition.Mag() > 500.0 and startPosition.Dot(endPosition) < 0.985 and startPosition.Dot(endPosition) > -0.985):
                continue
				
            for peIndex in range(0, mcPMT.GetMCPECount()):
                mcPE = mcPMT.GetMCPE(peIndex)
				
                lightPath.CalcByPosition(startPosition, pmtPosition)
                distInScint = lightPath.GetDistInScint()
                distInAV = lightPath.GetDistInAV()
                distInWater = lightPath.GetDistInWater()
                transitTime = groupVelocity.CalcByDistance(0.0, distInAV, distInWater)
				
                fullPlot.Fill(distInScint, mcPE.GetCreationTime() - startTime - transitTime)

    return


# Draw the Distance vs. Time Residual and Distance vs. Transit Time plots
def DrawPlots():

    histograms = ProducePlots()
	
    c1 = ROOT.TCanvas()
    c1.Divide(1, 2)
    c1.cd(1)
    histograms[0].Draw("COLZ")
    histograms[1].GetXaxis().SetTitle("Distance, mm")
    histograms[1].GetXaxis().SetRangeUser(150.0, 10150.0)
    histograms[1].GetYaxis().SetTitle("Time, ns")
    histograms[1].SetMarkerStyle(5)
    c1.cd(2)
    histograms[1].Draw()
	
    raw_input("Press 'Enter' to exit")

	
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(0)
ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

