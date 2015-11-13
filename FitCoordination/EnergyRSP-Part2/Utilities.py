#!/usr/bin/env python
import ROOT, rat
from array import array
import math
from ROOT import RAT
# Secondary functions and user-defined values for the EnergyRSP-Part2 Coordinator
# Author J Walker - 28/09/2015 <john.walker@liverpool.ac.uk>

ScintEnergies = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0] # Use these energies if using a scintillator-filled detector
WaterEnergies = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0] # Use these energies if using a water-filled detector


# Return a list of predicted Cerenkov photons per Energy, and the associated histogram, arranged as the following for "e" energies:
# The predicted number of Cerenkov photons calculated by EnergyRSP fitter
# { nCerPhotons(energy[0]), nCerPhotons(energy[1]), ... , nCerPhotons(energy[e-1]) }
def PredictedNCerenkovVsEnergy(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    nPhotonsTable = []
    histograms = []

    # Read in ROOT files
    reader = RAT.DU.DSReader(material + "_E=" + str(int(energies[0] * 1000)) + "keV.root")

    for energy in energies:

        if energy == energies[0]:
            continue

        infileName = material + "_E=" + str(int(energy * 1000)) + "keV.root"
        print infileName

        reader.Add(infileName)

    # Create vector of histograms
    for energy in energies:
        histograms.append(ROOT.TH1D("Nphotons_" + str(int(energy * 1000)), "Nphotons", 150, 0.0, 15000.0))

    # Fill appropriate histograms with predicted Cerenkov photons
    for ievent in range(0, reader.GetEntryCount()):
        if ievent % 100 == 0:
            print "PredictedNCerenkovVsEnergy:: " + str(ievent) + " : " + str(reader.GetEntryCount())

        ds = reader.GetEntry(ievent)
        mc = ds.GetMC()
        kineticEnergy = mc.GetMCParticle(0).GetKineticEnergy()

        for iev in range(0, ds.GetEVCount()):
            if iev != 0:
                continue # throw away retriggers
            ev = ds.GetEV(iev)
            if not ev.DefaultFitVertexExists() or not ev.GetDefaultFitVertex().ContainsPosition() or not ev.GetDefaultFitVertex().ValidPosition() or not ev.GetDefaultFitVertex().ContainsDirection() or not ev.GetDefaultFitVertex().ValidDirection():
                continue  # didn't fit succesfully
            # Fitter must have reconstructed inside AV
            if ev.GetDefaultFitVertex().GetPosition().Mag() < 6005.0:
                histograms[energies.index(kineticEnergy)].Fill(ev.GetFitResult("energyRSP:waterFitter").GetFOM("nCerPhotons"))

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

        nPhotonsTable.append(gaussFit.GetParameter(1))

        del gaussFit

    return nPhotonsTable, histograms


##### DIAGNOSTIC FUNCTIONS #####

# Return a predicted NCerenkov vs. Energy plot
def PlotMeanPredictedNCerenkovVsEnergy(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    legend = ROOT.TLegend(0.1, 0.7, 0.3, 0.9)

    nPhotonsTable = PredictedNCerenkovVsEnergy(material)[0]

    graph = ROOT.TGraph()
    for energyIndex, energy in enumerate(energies):
        graph.SetPoint(energyIndex, energy, nPhotonsTable[energyIndex])

    canvas = ROOT.TCanvas()
    graph.Draw("A*")
    graph.GetYaxis().SetTitle("Predicted Cerenkov photons")
    graph.GetXaxis().SetTitle("Energy [MeV]")
    canvas.SaveAs("MeanPredictedNCerenkovVsEnergy.eps")
    canvas.SaveAs("MeanPredictedNCerenkovVsEnergy.root")

    raw_input("Press 'Enter' to exit")

# Return a set of predicted NCerenkov distribution plots (one for each Energy)
def PlotPredictedNCerenkovPerEnergy(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    histList = PredictedNCerenkovVsEnergy(material)[1]

    canvas = ROOT.TCanvas("canvas","canvas",600,900)
    canvas.Divide(2, int(math.ceil(len(energies)/2.0)))
    for histIndex, hist in enumerate(histList):
        canvas.cd(histIndex + 1)
        hist.Draw()
    canvas.SaveAs("PredictedNCerenkovPerEnergy.eps")
    canvas.SaveAs("PredictedNCerenkovPerEnergy.root")

    raw_input("Press 'Enter' to exit")


ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(0)
ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
