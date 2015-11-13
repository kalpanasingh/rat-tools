#!/usr/bin/env python
import ROOT, rat
from array import array
import math
from ROOT import RAT
# Secondary functions and user-defined values for the EnergyPromptLookup Coordinator
# Author J Walker - 22/05/2015 <john.walker@liverpool.ac.uk>
# Revision history: 2015-07-08 J. Walker: Increasing width of prompt hits histogram
# Revision history: 2015-09-30 J. Walker: Modifying to allow for scintillator material
#                                         Added function to plot hit time residuals
#                                         Output number of working PMTs at time of coordination


Positions = [0.0, 200.0, 400.0, 600.0, 800.0, 1000.0, 1200.0, 1400.0, 1600.0, 1800.0, 2000.0, 2200.0, 2400.0, 2600.0, 2800.0, 3000.0, 3200.0, 3400.0, 3600.0, 3800.0, 4000.0, 4200.0, 4400.0, 4600.0, 4800.0, 5000.0, 5200.0, 5400.0, 5600.0, 5800.0, 6000.0, 6200.0, 6400.0, 6600.0, 6800.0, 7000.0, 7200.0, 7400.0, 7600.0, 7800.0, 8000.0]
ScintEnergies = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0] # Use these energies if using a scintillator-filled detector
WaterEnergies = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0] # Use these energies if using a water-filled detector
ScintTimeResidualWindow = [0.0, 30.0]
WaterTimeResidualWindow = [-10.0, 8.0]
ScintSubfiles = 10
WaterSubfiles = 20


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

    # Select which energies and time residual window to use based on the material in the detector
    energies = []
    time_residual_window = []
    if material == "lightwater_sno":
        energies = WaterEnergies
        time_residual_window = WaterTimeResidualWindow
    else:
        energies = ScintEnergies
        time_residual_window = ScintTimeResidualWindow

    nhitsTable = []
    histograms = []

    # Read in ROOT files
    reader = RAT.DU.DSReader(material + "_P=" + str(int(0.0)) + "mm_E=" + str(int(energies[0] * 1000)) + "keV_sf=0.root")

    for energy in energies:

        if energy == energies[0]:
            continue

        infileName = material + "_P=" + str(int(0.0)) + "mm_E=" + str(int(energy * 1000)) + "keV_sf=0.root"
        print infileName

        reader.Add(infileName)

    # Create vector of histograms
    bins = 0
    bin_min = 0.0
    bin_max = 0.0

    if material == "lightwater_sno":
        bins = 150
        bin_min = 0.0
        bin_max = 300.0
    else:
        bins = 2500
        bin_min = 0.0
        bin_max = 5000.0
    for energy in energies:
        histograms.append(ROOT.TH1D("PromptNhits_" + str(int(energy * 1000)), "Prompt Nhits", bins, bin_min, bin_max))

    # Fill appropriate histograms with prompt hits
    for ievent in range(0, reader.GetEntryCount()):
        if ievent % 100 == 0:
            print "PromptNhitsVsEnergy:: " + str(ievent) + " : " + str(reader.GetEntryCount())

        ds = reader.GetEntry(ievent)
        light_path = rat.utility().GetLightPathCalculator()
        group_velocity = rat.utility().GetGroupVelocity()
        pmt_info = rat.utility().GetPMTInfo()
        mc = ds.GetMC()
        kineticEnergy = mc.GetMCParticle(0).GetKineticEnergy()

        # Get MC event info
        eventPosition = mc.GetMCParticle(0).GetPosition()

        # Loop through events
        for iev in range(0, ds.GetEVCount()):
            if iev != 0:
                continue
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

                if timeResidual > time_residual_window[0] and timeResidual < time_residual_window[1]:
                    promptNhits += 1;

            # Fill with number of prompt Nhits
            histograms[energies.index(round(kineticEnergy,1))].Fill( promptNhits )

    # Fill list with histogram mean values
    for Histogram in histograms:
        tolerance = 10
        lowBin = Histogram.FindFirstBinAbove(0.0)
        lowBin = lowBin - tolerance
        highBin = Histogram.FindLastBinAbove(0.0)
        highBin = highBin + tolerance
        if lowBin < 1:
            lowBin = 1
        if highBin > Histogram.GetNbinsX():
            highBin = Histogram.GetNbinsX()

        gaussFit = ROOT.TF1("gaus", "gaus", Histogram.GetBinCenter(lowBin), Histogram.GetBinCenter(highBin))
        Histogram.Fit(gaussFit, "RQN")

        # Store mean prompt Nhits in table
        nhitsTable.append(gaussFit.GetParameter(1))

        del gaussFit

    return nhitsTable, histograms


# Return the position/direction dependent scale factor distribution, arranged as the following for "c" u.r's and "r" radiis:
# { S(u.r[0],radius[0]), S(u.r[0],radius[1]), ... , S(u.r[0],radius[r-1]), ...,
# S(u.r[c-1],radius[0]), S(u.r[c-1],radius[1]), ... , S(u.r[c-1],radius[r-1]) }
def PositionDirectionScaleFactor(material):

    # Select which time residual window to use based on the material in the detector
    time_residual_window = []
    subfiles = 0
    energy = 0.0
    if material == "lightwater_sno":
        time_residual_window = WaterTimeResidualWindow
        subfiles = WaterSubfiles
        energy = 5.0
    else:
        time_residual_window = ScintTimeResidualWindow
        subfiles = ScintSubfiles
        energy = 2.5

    # Calculate edges of position bins
    lowBins = [Positions[0]-(Positions[1]-Positions[0])/2]
    for i in range(1,len(Positions)):
        lowBins.append( (Positions[i-1]+Positions[i])/2 )
    lowBins.append( Positions[-1]+(Positions[-1]-Positions[-2])/2 )
    lowBinsArray = array('d',lowBins)

    HistogramTotal = ROOT.TH2D("Total", "Total", len(Positions), lowBinsArray, uDotrBins, -1.0, 1.0)
    HistogramPrompt = ROOT.TH2D("Prompt", "Prompt", len(Positions), lowBinsArray, uDotrBins, -1.0, 1.0)

    # Read in ROOT files
    reader = RAT.DU.DSReader(material + "_P=" + str(int(Positions[0])) + "mm_E=" + str(int(energy * 1000)) + "keV_sf=0.root")

    for position in Positions:
        for sf in range(0, subfiles):

            if position == Positions[0] and sf == 0:
                continue

            infileName = material + "_P=" + str(int(position)) + "mm_E=" + str(int(energy * 1000)) + "keV_sf=" + str(int(sf)) + ".root"
            print infileName

            reader.Add(infileName)

    for ievent in range(0, reader.GetEntryCount()):
        if ievent % 100 == 0:
            print "PositionDirectionScaleFactor:: " + str(ievent) + " : " + str(reader.GetEntryCount())

        ds = reader.GetEntry(ievent)
        light_path = rat.utility().GetLightPathCalculator()
        group_velocity = rat.utility().GetGroupVelocity()
        pmt_info = rat.utility().GetPMTInfo()
        mc = ds.GetMC()

        # Get MC event info
        eventPosition = mc.GetMCParticle(0).GetPosition()
        eventDirection = mc.GetMCParticle(0).GetMomentum().Unit()

        # Loop through events
        for iev in range(0, ds.GetEVCount()):
            if iev != 0:
                continue
            ev = ds.GetEV( iev )
            calibratedPMTs = ev.GetCalPMTs()

            # Check fit worked and positions close
            if False in (ev.DefaultFitVertexExists(), ev.GetDefaultFitVertex().ContainsPosition(), ev.GetDefaultFitVertex().ValidPosition(), ev.GetDefaultFitVertex().ContainsTime(), ev.GetDefaultFitVertex().ValidTime()):
                continue # Didn't fit successfully
            positionDiff = eventPosition - ev.GetDefaultFitVertex().GetPosition()
            if positionDiff.Mag() > 1000.0:
                continue # Position fit outside tolerace

            # If at centre radial magnitude is zero so fill first bin
            if abs(eventPosition.Mag()-0.0)<0.01 or abs(eventPosition.Mag()-8000.0)<0.01:
                HistogramTotal.Fill( eventPosition.Mag(), -1.0 )
            else:
                if material == "lightwater_sno":
                    HistogramTotal.Fill( eventPosition.Mag(), eventPosition.Unit().Dot(eventDirection) )
                else:
                    HistogramTotal.Fill( eventPosition.Mag(), eventPosition.CosTheta() )

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
                if timeResidual > time_residual_window[0] and timeResidual < time_residual_window[1]:
                    if abs(eventPosition.Mag()-0.0) < 0.01 or abs(eventPosition.Mag()-8000.0) < 0.01:
                        HistogramPrompt.Fill( eventPosition.Mag(), -1.0 )
                    else:
                        if material == "lightwater_sno":
                            HistogramPrompt.Fill( eventPosition.Mag(), eventPosition.Unit().Dot(eventDirection) )
                        else:
                            HistogramPrompt.Fill( eventPosition.Mag(), eventPosition.CosTheta() )

    # Calculate average prompt Nhits, if up to 8000mm set edge to same value (low statistics) and scale by value at centre
    HistogramPrompt.Divide(HistogramTotal)
    centre_value = HistogramPrompt.GetBinContent(1,1)
    edge_value = HistogramPrompt.GetBinContent(len(Positions),1)
    if Positions[-1] == 8000.0:
        for i in range(1, uDotrBins+1):
            HistogramPrompt.SetBinContent(len(Positions),i,edge_value)
    HistogramPrompt.Scale(1.0/centre_value)
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


# Return the number of working PMTs at time of coordination
def WorkingPMTs(material):

    if material == "lightwater_sno":
        energy = 5.0
    else:
        energy = 2.5

    totalActiveChannels = 0

    infileName = material + "_P=" + str(int(0.0)) + "mm_E=" + str(int(energy * 1000)) + "keV_sf=0.root"
    print infileName

    reader = RAT.DU.DSReader(infileName)

    for ievent in range(0, reader.GetEntryCount()):
        if ievent != 0:
            continue

        ds = reader.GetEntry(ievent)

        # Get total number of channels
        pmt_info = rat.utility().GetPMTInfo()
        numChannels = pmt_info.GetCount()

        # Find active channels
        channelHardwareStatus = rat.utility().GetChanHWStatus()
        for lcn in range(0, numChannels):
            if pmt_info.GetType( lcn ) != pmt_info.NORMAL:
                continue
            if channelHardwareStatus.IsEnabled():
                if channelHardwareStatus.IsTubeOnline( lcn ):
                    totalActiveChannels = totalActiveChannels + 1

    return totalActiveChannels


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

    nhitsTable = PromptNhitsVsEnergy(material)[0]

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

    # Select which energies and time residual window to use based on the material in the detector
    energies = []
    time_residual_window = []
    if material == "lightwater_sno":
        energies = WaterEnergies
        time_residual_window = WaterTimeResidualWindow
    else:
        energies = ScintEnergies
        time_residual_window = ScintTimeResidualWindow

    histList = PromptNhitsVsEnergy(material)[1]

    canvas = ROOT.TCanvas()
    canvas.Divide(2, int(math.ceil(len(energies)/2.0)))
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
    if material == "lightwater_sno":
        hist.GetYaxis().SetTitle("u.r")
    else:
        hist.GetYaxis().SetTitle("Cos(#theta)")
    canvas.SaveAs("PositionDirectionScaleFactor.eps")

    raw_input("Press 'Enter' to exit")


# Plot the time residuals
def PlotHitTimeResiduals(material):

    energy = 5.0

    infileName = material + "_P=" + str(int(0.0)) + "mm_E=" + str(int(energy * 1000)) + "keV_sf=0.root"
    print infileName

    hit_time_residuals = ROOT.TH1D( "hHitTimeResidualsMC", "Hit time residuals using the MC position", 120, -20.0, 100.0 )
    hit_time_residuals.SetDirectory(0)

    for ds, run in rat.dsreader(infileName):
        # rat.utility().GetLightPath() must be called *after* the rat.dsreader constructor.
        light_path = rat.utility().GetLightPathCalculator()
        group_velocity = rat.utility().GetGroupVelocity()
        pmt_info = rat.utility().GetPMTInfo()
        event_position = ds.GetMC().GetMCParticle(0).GetPosition() # At least 1 is somewhat guaranteed
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)

            # Check fit worked
            if not ev.DefaultFitVertexExists() or not ev.GetDefaultFitVertex().ContainsTime() or not ev.GetDefaultFitVertex().ValidTime():
                continue

            event_time = ev.GetDefaultFitVertex().GetTime()
            calibrated_pmts = ds.GetEV(iev).GetCalPMTs()
            for ipmt in range(0, calibrated_pmts.GetCount()):
                pmt_cal = calibrated_pmts.GetPMT(ipmt)
                light_path.CalcByPosition(event_position, pmt_info.GetPosition(pmt_cal.GetID()))
                inner_av_distance = light_path.GetDistInInnerAV()
                av_distance = light_path.GetDistInAV()
                water_distance = light_path.GetDistInWater()
                transit_time = group_velocity.CalcByDistance(inner_av_distance, av_distance, water_distance) # Assumes 400nm photon
                hit_time_residuals.Fill(pmt_cal.GetTime() - transit_time - event_time)

    hit_time_residuals.GetYaxis().SetTitle("Count per 1 ns bin")
    hit_time_residuals.GetXaxis().SetTitle("Hit time residuals [ns]")
    hit_time_residuals.SetTitle("Hit Time Residuals")

    canvas = ROOT.TCanvas()
    canvas.SetLogy()
    hit_time_residuals.Draw()
    canvas.Update();
    canvas.SaveAs("HitTimeResiduals.eps")

    raw_input("Press 'Enter' to exit")


# Return the number of working PMTs
def PrintWorkingPMTs(material):

    print "Number of working PMTs: " + str(WorkingPMTs(material))


ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(0)
ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
