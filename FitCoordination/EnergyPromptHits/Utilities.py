#!/usr/bin/env python
import ROOT, rat
from array import array
import math
from ROOT import RAT
# Secondary functions and user-defined values for the EnergyPromptHits Coordinator
# Author J Walker - 08/06/2016 <john.walker@liverpool.ac.uk>


ScintEnergy = 2.5 # Use this energy if using a scintillator-filled detector
WaterEnergy = 8.0 # Use this energy if using a water-filled detector
ScintTimeResidualWindow = [0.0, 60.0]
WaterTimeResidualWindow = [-10.0, 8.0]
ScintFiducial = 3500.0
WaterFiducial = 5500.0
ScintSubfiles = 1
WaterSubfiles = 1


# Return the prompt Nhits
def PromptNhits(material):

    # Select which energies and time residual window to use based on the material in the detector
    energy = 0.0
    time_residual_window = []
    subfiles = 0
    if material == "lightwater_sno":
        energy = WaterEnergy
        time_residual_window = WaterTimeResidualWindow
        subfiles = WaterSubfiles
    else:
        energy = ScintEnergy
        time_residual_window = ScintTimeResidualWindow
        subfiles = ScintSubfiles

    # Create histogram
    bins = 0
    bin_min = 0.0
    bin_max = 0.0

    if material == "lightwater_sno":
        bins = 100
        bin_min = 0.0
        bin_max = 20.0
    else:
        bins = 200
        bin_min = 0.0
        bin_max = 600.0

    histogram = ROOT.TH1D("PromptNhits_" + str(int(energy * 1000)), "Prompt Nhits", bins, bin_min, bin_max)

    # Read in ROOT files
    reader = RAT.DU.DSReader(material + "_E=" + str(int(energy * 1000)) + "keV_sf=0.root")

    for sf in xrange(1,subfiles):

        infileName = material + "_E=" + str(int(energy * 1000)) + "keV_sf=" + sf + ".root"
        print infileName

        reader.Add(infileName)

    # Fill appropriate histograms with prompt hits
    for ievent in range(0, reader.GetEntryCount()):
        if ievent % 100 == 0:
            print "PromptNhitsVs:: " + str(ievent) + " : " + str(reader.GetEntryCount())

        ds = reader.GetEntry(ievent)
        light_path = rat.utility().GetLightPathCalculator()
        group_velocity = rat.utility().GetGroupVelocity()
        pmt_info = rat.utility().GetPMTInfo()
        mc = ds.GetMC()

        # Get MC event info
        eventPosition = mc.GetMCParticle(0).GetPosition()
        kineticEnergy = mc.GetMCParticle(0).GetKineticEnergy()

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
            histogram.Fill( promptNhits / kineticEnergy )

    # Calculate histogram mean value
    tolerance = 10
    lowBin = histogram.FindFirstBinAbove(0.0)
    lowBin = lowBin - tolerance
    highBin = histogram.FindLastBinAbove(0.0)
    highBin = highBin + tolerance
    if lowBin < 1:
        lowBin = 1
    if highBin > histogram.GetNbinsX():
        highBin = histogram.GetNbinsX()

    gaussFit = ROOT.TF1("gaus", "gaus", histogram.GetBinCenter(lowBin), histogram.GetBinCenter(highBin))
    histogram.Fit(gaussFit, "RQN")

    return gaussFit.GetParameter(1), histogram


# Return the number of working PMTs at time of coordination
def WorkingPMTs(material):

    # Select which energy to use based on the material in the detector
    energy = 0.0
    if material == "lightwater_sno":
        energy = WaterEnergy
    else:
        energy = ScintEnergy

    totalActiveChannels = 0

    # Read in ROOT files
    reader = RAT.DU.DSReader(material + "_E=" + str(int(energy * 1000)) + "keV_sf=0.root")

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

# Return a Prompt Nhits plot
def PlotPromptNhitsPerMeV(material):

    meanNhits, nhits = PromptNhits(material)

    canvas = ROOT.TCanvas()
    nhits.Draw()
    nhits.GetYaxis().SetTitle("Counts")
    nhits.GetXaxis().SetTitle("Hits / MeV")
    canvas.SaveAs("PromptNhits_"+material+".eps")

    print "Mean prompt Nhits: " + str(meanNhits)

    raw_input("Press 'Enter' to exit")


# Plot the time residuals
def PlotHitTimeResiduals(material):

    # Select which time residual window to use based on the material in the detector
    time_residual_window = []
    subfiles = 0
    energy = 0.0
    time_window = []
    bins = 0
    if material == "lightwater_sno":
        time_residual_window = WaterTimeResidualWindow
        subfiles = WaterSubfiles
        energy = WaterEnergy
        time_window = [-20.0, 40.0]
        bins = 60
    else:
        time_residual_window = ScintTimeResidualWindow
        subfiles = ScintSubfiles
        energy = ScintEnergy
        time_window = [-200.0, 400.0]
        bins = 600

    hit_time_residuals = ROOT.TH1D( "hHitTimeResidualsMC", "Hit time residuals using the MC position", bins, time_window[0], time_window[1] )
    hit_time_residuals.SetDirectory(0)

    # Read in ROOT files
    reader = RAT.DU.DSReader(material + "_P=" + str(int(0.0)) + "mm_E=" + str(int(energy * 1000)) + "keV_sf=0.root")

    for sf in range(1, subfiles):

        infileName = material + "_P=" + str(int(0.0)) + "mm_E=" + str(int(energy * 1000)) + "keV_sf=" + str(int(sf)) + ".root"
        print infileName

        reader.Add(infileName)

    for ievent in range(0, reader.GetEntryCount()):
        if ievent % 100 == 0:
            print "PlotHitTimeResiduals:: " + str(ievent) + " : " + str(reader.GetEntryCount())

        ds = reader.GetEntry(ievent)
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
    hit_time_residuals.GetXaxis().SetTitle("Hit time residual [ns]")
    hit_time_residuals.SetTitle("Hit Time Residuals")
    hit_time_residuals.SetLineColor(ROOT.kBlue+2)

    canvas = ROOT.TCanvas()
    canvas.SetLogy()
    hit_time_residuals.Draw()
    canvas.Update()
    #top = canvas.GetFrame().GetY2()
    #bottom = canvas.GetFrame().GetY1()
    top = canvas.GetUymax()
    bottom = canvas.GetUymin()
    line1 = ROOT.TLine(time_residual_window[0],math.pow(10.0,bottom),time_residual_window[0],math.pow(10.0,top))
    line2 = ROOT.TLine(time_residual_window[1],math.pow(10.0,bottom),time_residual_window[1],math.pow(10.0,top))
    line1.SetLineColor(ROOT.kBlack)
    line2.SetLineColor(ROOT.kBlack)
    line1.SetLineWidth(2)
    line2.SetLineWidth(2)
    line1.Draw()
    line2.Draw()
    canvas.Update()
    canvas.SaveAs("HitTimeResiduals_"+material+".eps")

    raw_input("Press 'Enter' to exit")


# Return the number of working PMTs
def PrintWorkingPMTs(material):

    print "Number of working PMTs: " + str(WorkingPMTs(material))


# Return mean prompt Nhits
def PrintMeanPromptNhitsPerMeV(material):

    print "Mean prompt Nhits per MeV: " + str(PromptNhits(material)[0])



ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(0)
ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
