#!/usr/bin/env python
import ROOT, rat
from array import array
import math
# Secondary functions and user-defined values for the EnergyPromptLookup Coordinator
# Author J Walker - 22/05/2015 <john.walker@liverpool.ac.uk>
# Revision history: 2015-07-08 J. Walker: Increasing width of prompt hits histogram

Positions = [0.0, 200.0, 400.0, 600.0, 800.0, 1000.0, 1200.0, 1400.0, 1600.0, 1800.0, 2000.0, 2200.0, 2400.0, 2600.0, 2800.0, 3000.0, 3200.0, 3400.0, 3600.0, 3800.0, 4000.0, 4200.0, 4400.0, 4600.0, 4800.0, 5000.0, 5200.0, 5400.0, 5600.0, 5800.0, 6000.0, 6200.0, 6400.0, 6600.0, 6800.0, 7000.0, 7200.0, 7400.0, 7600.0, 7800.0, 8000.0]
ScintEnergies = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0] # Use these energies if using a scintillator-filled detector
WaterEnergies = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0] # Use these energies if using a water-filled detector

# Number of bins and bin limits for u.r
uDotrBins = 40
uDotrLimitValues = []
for i in range(0,uDotrBins):
    binMin = -1.0 + (i*2.0/uDotrBins)
    uDotrLimitValues.append(binMin)
uDotrLimitValues.append(1.0)

# Return a list of Prompt Nhits per Energy, arranged as the following for "e" energies:
# { Nhits(energy[0]), Nhits(energy[1]), ... , Nhits(energy[e-1]) }
def PromptNhitsVsEnergy(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    nhitsTable = []

    for energy in energies:

        infileName = material + "_P=" + str(int(0.0)) + "mm_E=" + str(int(energy * 1000)) + "keV.root"
        print infileName
        hNhits = ROOT.TH1D(infileName, "Prompt Nhits", 150, 0.0, 300.0)

        for ds, run in rat.dsreader(infileName):
            light_path = rat.utility().GetLightPathCalculator()
            group_velocity = rat.utility().GetGroupVelocity()
            pmt_info = rat.utility().GetPMTInfo()
            mc = ds.GetMC()

            # Get MC event info
            eventPosition = mc.GetMCParticle(0).GetPosition()

            # Loop through events
            for iev in range(0, ds.GetEVCount()):
                ev = ds.GetEV(iev)
                calibratedPMTs = ev.GetCalPMTs();

                # Check fit worked
                if False in (ev.DefaultFitVertexExists(), ev.GetDefaultFitVertex().ContainsPosition(), ev.GetDefaultFitVertex().ValidPosition(), ev.GetDefaultFitVertex().ContainsTime(), ev.GetDefaultFitVertex().ValidTime()):
                    continue

                # Get fitted event time
                eventTime = ev.GetDefaultFitVertex().GetTime()

                promptNhits = 0
                # Loop through calibrated PMTs
                for ipmt in range(0, calibratedPMTs.GetCount()):
                    pmtCal = calibratedPMTs.GetPMT( ipmt )

                    # Calculate time residual
                    light_path.CalcByPosition( eventPosition, pmt_info.GetPosition( pmtCal.GetID() ) )
                    distInInnerAV = light_path.GetDistInInnerAV()
                    distInAV = light_path.GetDistInAV()
                    distInWater = light_path.GetDistInWater()
                    transitTime = group_velocity.CalcByDistance( distInInnerAV, distInAV, distInWater )
                    timeResidual = pmtCal.GetTime() - transitTime - eventTime

                    if timeResidual > -10.0 and timeResidual < 8.0:
                        promptNhits += 1;

                # Fill with number of prompt Nhits
                hNhits.Fill( promptNhits )

        # Fit a Gaussian to the prompt Nhits
        tolerance = 10
        lowBin = hNhits.FindFirstBinAbove(0.0)
        lowBin = lowBin - tolerance
        highBin = hNhits.FindLastBinAbove(0.0)
        highBin = highBin + tolerance
        if lowBin < 1:
            lowBin = 1
        if highBin > hNhits.GetNbinsX():
            highBin = hNhits.GetNbinsX()

        gaussFit = ROOT.TF1("gaus", "gaus", hNhits.GetBinCenter(lowBin), hNhits.GetBinCenter(highBin))
        hNhits.Fit(gaussFit, "RQN")

        # Store mean prompt Nhits in table
        nhitsTable.append(gaussFit.GetParameter(1))

        del gaussFit
        del hNhits

    return nhitsTable

# Return the position/direction dependent scale factor distribution, arranged as the following for "c" u.r's and "r" radiis:
# { S(u.r'[0],radius[0]), S(u.r'[0],radius[1]), ... , S(u.r'[0],radius[r-1]), ...,
# S(u.r'[c-1],radius[0]), S(u.r'[c-1],radius[1]), ... , S(u.r'[c-1],radius[r-1]) }
def PositionDirectionScaleFactor(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    # Calculate edges of position bins
    lowBins = [Positions[0]-(Positions[1]-Positions[0])/2]
    for i in range(1,len(Positions)):
        lowBins.append( (Positions[i-1]+Positions[i])/2 )
    lowBins.append( Positions[-1]+(Positions[-1]-Positions[-2])/2 )
    lowBinsArray = array('d',lowBins)

    HistogramTotal = ROOT.TH2D("Total", "Total", len(Positions), lowBinsArray, uDotrBins, -1.0, 1.0)
    HistogramPrompt = ROOT.TH2D("Prompt", "Prompt", len(Positions), lowBinsArray, uDotrBins, -1.0, 1.0)

    for position in Positions:
        energy = 5.0

        infileName = material + "_P=" + str(int(position)) + "mm_E=" + str(int(energy * 1000)) + "keV.root"
        print infileName

        for ds, run in rat.dsreader(infileName):
            light_path = rat.utility().GetLightPathCalculator()
            group_velocity = rat.utility().GetGroupVelocity()
            pmt_info = rat.utility().GetPMTInfo()
            mc = ds.GetMC()

            # Get MC event info
            eventPosition = mc.GetMCParticle(0).GetPosition()
            eventDirection = mc.GetMCParticle(0).GetMomentum().Unit()

            # Loop through events
            for iev in range(0, ds.GetEVCount()):
                ev = ds.GetEV( iev )
                calibratedPMTs = ev.GetCalPMTs()

                # Check fit worked and positions close
                if False in (ev.DefaultFitVertexExists(), ev.GetDefaultFitVertex().ContainsPosition(), ev.GetDefaultFitVertex().ValidPosition(), ev.GetDefaultFitVertex().ContainsTime(), ev.GetDefaultFitVertex().ValidTime()):
                    continue # Didn't fit successfully
                positionDiff = eventPosition - ev.GetDefaultFitVertex().GetPosition()
                if positionDiff.Mag() > 1000.0:
                    continue # Position fit outside tolerace

                # If at centre radial magnitude is zero so fill first bin
                if position == 0.0:
                    HistogramTotal.Fill( eventPosition.Mag(), -1.0 )
                else:
                    HistogramTotal.Fill( eventPosition.Mag(), eventPosition.Unit().Dot(eventDirection) )

                # Get fitted time
                eventTime = ev.GetDefaultFitVertex().GetTime()

                # Loop through PMTs
                for ipmt in range(0, calibratedPMTs.GetCount()):
                    pmtCal = calibratedPMTs.GetPMT( ipmt )

                    # Calculate time residual
                    light_path.CalcByPosition( eventPosition, pmt_info.GetPosition( pmtCal.GetID() ) )
                    distInInnerAV = light_path.GetDistInInnerAV()
                    distInAV = light_path.GetDistInAV()
                    distInWater = light_path.GetDistInWater()
                    transitTime = group_velocity.CalcByDistance( distInInnerAV, distInAV, distInWater )
                    timeResidual = pmtCal.GetTime() - transitTime - eventTime

                    # Fill if time residual within range
                    if timeResidual > -10.0 and timeResidual < 8.0:
                        if position == 0.0:
                            HistogramPrompt.Fill( eventPosition.Mag(), -1.0 )
                        else:
                            HistogramPrompt.Fill( eventPosition.Mag(), eventPosition.Unit().Dot(eventDirection) )

    # Calculate average prompt Nhits and scale by value at centre
    HistogramPrompt.Divide(HistogramTotal)
    centre_value = HistogramPrompt.GetBinContent(1,1)
    HistogramPrompt.Scale(1/centre_value)
    for i in range(1, uDotrBins+1):
        HistogramPrompt.SetBinContent(1,i,1.0)

    scaleFactor = []
    for binc in range(0, uDotrBins):
        singleUDotrScaleFactor = []
        for binr in range(0, len(Positions)):
            singleUDotrScaleFactor.append(HistogramPrompt.GetBinContent( binr+1, binc+1 ))
        scaleFactor.append(singleUDotrScaleFactor)

    del HistogramPrompt
    del HistogramTotal

    return scaleFactor


##### DIAGNOSTIC FUNCTIONS #####

# Return a Prompt Nhits vs. Energy plot
def PlotMeanPromptNhitsPerEnergy(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    legend = ROOT.TLegend(0.1, 0.7, 0.3, 0.9)

    nhitsTable = PromptNhitsVsEnergy(material)

    graph = ROOT.TGraph()
    for energyIndex, energy in enumerate(energies):
        graph.SetPoint(energyIndex, energy, nhitsTable[energyIndex])

    canvas = ROOT.TCanvas()
    graph.Draw("A*")
    graph.GetYaxis().SetTitle("Mean Prompt Nhits")
    graph.GetXaxis().SetTitle("Energy [MeV]")
    canvas.SaveAs("MeanPromptNhitsPerEnergy.eps")

    raw_input("Press 'Enter' to exit")


# Return a set of Prompt Nhit distribution plots (one for each Energy)
def PlotPromptNhitsPerEnergy(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    histList = []

    for energy in energies:

        infileName = material + "_P=" + str(int(0.0)) + "mm_E=" + str(int(energy * 1000)) + "keV.root"
        print infileName
        hNhits = ROOT.TH1D(infileName, "Nphotons - " + str(energy) + "MeV", 150, 0.0, 300.0)

        for ds, run in rat.dsreader(infileName):
            light_path = rat.utility().GetLightPathCalculator()
            group_velocity = rat.utility().GetGroupVelocity()
            pmt_info = rat.utility().GetPMTInfo()
            mc = ds.GetMC()

            # Get MC event info
            eventPosition = mc.GetMCParticle(0).GetPosition()

            # Loop through events
            for iev in range(0, ds.GetEVCount()):
                ev = ds.GetEV(iev)
                calibratedPMTs = ev.GetCalPMTs();

                # Check fit worked
                if False in (ev.DefaultFitVertexExists(), ev.GetDefaultFitVertex().ContainsPosition(), ev.GetDefaultFitVertex().ValidPosition(), ev.GetDefaultFitVertex().ContainsTime(), ev.GetDefaultFitVertex().ValidTime()):
                    continue

                # Get fitted time
                eventTime = ev.GetDefaultFitVertex().GetTime()

                promptNhits = 0
                # Loop through calibrated PMTs
                for ipmt in range(0, calibratedPMTs.GetCount()):
                    pmtCal = calibratedPMTs.GetPMT( ipmt )

                    # Calculate time residual
                    light_path.CalcByPosition( eventPosition, pmt_info.GetPosition( pmtCal.GetID() ) )
                    distInInnerAV = light_path.GetDistInInnerAV()
                    distInAV = light_path.GetDistInAV()
                    distInWater = light_path.GetDistInWater()
                    transitTime = group_velocity.CalcByDistance( distInInnerAV, distInAV, distInWater )
                    timeResidual = pmtCal.GetTime() - transitTime - eventTime

                    if timeResidual > -10.0 and timeResidual < 8.0:
                        promptNhits += 1;

                # Fill with number of prompt Nhits
                hNhits.Fill( promptNhits )

        # Fit Gaussian to prompt Nhits
        tolerance = 10
        lowBin = hNhits.FindFirstBinAbove(0.0)
        lowBin = lowBin - tolerance
        highBin = hNhits.FindLastBinAbove(0.0)
        highBin = highBin + tolerance
        if lowBin < 1:
            lowBin = 1
        if highBin > hNhits.GetNbinsX():
            highBin = hNhits.GetNbinsX()

        gaussFit = ROOT.TF1("gaus", "gaus", hNhits.GetBinCenter(lowBin), hNhits.GetBinCenter(highBin))

        hNhits.GetXaxis().SetTitle("prompt nhits")

        histList.append([hNhits,gaussFit])

        del gaussFit
        del hNhits

    canvas = ROOT.TCanvas()
    canvas.Divide(2, len(energies) / 2)
    for histIndex, hist in enumerate(histList):
        canvas.cd(histIndex + 1)
        hist[0].Fit(hist[1],"RQN")
        hist[0].Draw()
    canvas.SaveAs("PromptNhitsPerEnergy.eps")

    raw_input("Press 'Enter' to exit")


# Return the position/direction scale factor plot
def PlotPositionDirectionScaleFactor(material):

    scaleFactor = PositionDirectionScaleFactor(material)

    # Calculate edges of position bins
    lowBins = [Positions[0]-(Positions[1]-Positions[0])/2]
    for i in range(1,len(Positions)):
        lowBins.append( (Positions[i-1]+Positions[i])/2 )
    lowBins.append( Positions[-1]+(Positions[-1]-Positions[-2])/2 )
    lowBinsArray = array('d',lowBins)

    hist = ROOT.TH2D("Total", "Total", len(Positions), lowBinsArray, uDotrBins, -1.0, 1.0)

    for uDotrBin in range(0,uDotrBins):
        for radialBin in range(0,len(Positions)):
            hist.SetBinContent( radialBin+1, uDotrBin+1, scaleFactor[uDotrBin][radialBin] )

    hist.SetContour(500);
    canvas = ROOT.TCanvas()
    hist.Draw("colz")
    hist.GetXaxis().SetTitle("|r|")
    hist.GetYaxis().SetTitle("p'.r")
    canvas.SaveAs("PositionDirectionScaleFactor.eps")

    raw_input("Press 'Enter' to exit")


ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(0)
ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
