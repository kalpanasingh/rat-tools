#!/usr/bin/env python
import ROOT, rat
# Secondary functions and user-defined Values for the EnergyLookup Coordinator
# Author P G Jones - 12/09/2011 <p.g.jones@qmul.ac.uk>
#        K Majumdar - 08/09/2014 - Cleanup of Coordinators for new DS

Positions = [0.0, 2000.0, 4000.0, 5000.0, 5500.0, 5750.0, 5950.0, 6100.0, 6500.0, 7000.0, 7500.0, 8000.0]
ScintEnergies = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]    # Use these energies if using a scintillator-filled detector
WaterEnergies = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]    # Use these energies if using a water-filled detector


# Return a list of Nhits per Position/Energy combination, arranged as the following for "p" positions and "e" energies:
# { Nhits(position[0], energy[0]), Nhits(position[0], energy[1]), ... , Nhits(position[0], energy[e-1], Nhits(position[1], energy[0], ... , Nhits(position[p-1], energy[e-1] }
def NhitsVsPositionEnergy(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies
		
    nHitsTable = []

    for position in Positions:
	
        singlePositionNhitsTable = []
        for energy in energies:
		
            infileName = material + "_P=" + str(int(position)) + "mm_E=" + str(int(energy * 1000)) + "keV"

            Histogram = ROOT.TH1D(infileName, "Nhits", 300, 0.0, 3000.0)

            for ds, run in rat.dsreader(infileName):
                if ds.GetEVCount() == 0:
                    continue
                Histogram.Fill(ds.GetEV(0).GetCalPMTs().GetCount())
		
            tolerance = 10
            lowBin = Histogram.FindFirstBinAbove(0.0)
            lowBin = lowBin - tolerance
            highBin = Hitogram.FindLastBinAbove(0.0)
            highBin = highBin + tolerance
            if lowBin < 1:
                lowBin = 1
            if highBin > Histogram.GetNbinsX():
                highBin = Histogram.GetNbinsX()

            gaussFit = ROOT.TF1("gaus", "gaus", Histogram.GetBinCenter(lowBin), Histogram.GetBinCenter(highBin))
            Histogram.Fit(gaussFit, "RQN")
    
            singlePositionNhitsTable.append(gaussFit.GetParameter(1))
			
            del gaussFit
            del Histogram

        nHitsTable.append(singlePositionNhitsTable)
            
    return nHitsTable
	
	
##### DIAGNOSTIC FUNCTIONS #####

# Return a list of Nhits per Energy/Position combination, arranged as the following for "e" energies and "p" positions:
# { Nhits(energy[0], position[0]), Nhits(energy[0], position[1]), ... , Nhits(energy[0], position[p-1], Nhits(energy[1], position[0], ... , Nhits(energy[e-1], position[p-1] }
def NhitsVsEnergyPosition(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies
		
    nHitsTable = []

    for energy in energies:
	
        singleEnergyNhitsTable = []
        for position in Positions:
		
            infileName = material + "_P=" + str(int(position)) + "mm_E=" + str(int(energy * 1000)) + "keV"

            Histogram = ROOT.TH1D(infileName, "Nhits", 300, 0.0, 3000.0)

            for ds, run in rat.dsreader(infileName):
                if ds.GetEVCount() == 0:
                    continue
                Histogram.Fill(ds.GetEV(0).GetCalPMTs().GetCount())
		
            tolerance = 10
            lowBin = Histogram.FindFirstBinAbove(0.0)
            lowBin = lowBin - tolerance
            highBin = Hitogram.FindLastBinAbove(0.0)
            highBin = highBin + tolerance
            if lowBin < 1:
                lowBin = 1
            if highBin > Histogram.GetNbinsX():
                highBin = Histogram.GetNbinsX()

            gaussFit = ROOT.TF1("gaus", "gaus", Histogram.GetBinCenter(lowBin), Histogram.GetBinCenter(highBin))
            Histogram.Fit(gaussFit, "RQN")
    
            singleEnergyNhitsTable.append(gaussFit.GetParameter(1))
			
            del gaussFit
            del Histogram

        nHitsTable.append(singleEnergyNhitsTable)
            
    return nHitsTable
	

# Return a set of Nhits vs. Position plots (one for each Energy)
def PlotNHitsPerPosition(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    nHitsTable = NhitsVsEnergyPosition(material)
	
    graphsList = []
    for energyIndex, energy in enumerate(energies):
	
        graph = ROOT.TGraph()
        for positionIndex in range(0, len(Positions)):
		
            graph.SetPoint(positionIndex, Positions[positionIndex], nHitsTable[energyIndex][positionIndex])
			
        graph.SetMarkerColor(energyIndex + 2)
        graphsList.append(graph)

    canvas = ROOT.TCanvas()
    canvas.Divide(2, len(energies) / 2)
    for graphIndex, graph in enumerate(graphsList):
        canvas.cd(graphIndex + 1)
        graph.Draw("A*")
        graph.GetYaxis().SetRangeUser(0, 2000)

    raw_input("Press 'Enter' to exit")


# Return a set of Nhits vs. Energy plots (one for each Position)
def PlotNHitsPerEnergy(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies
		
    legend = ROOT.TLegend(0.1, 0.7, 0.3, 0.9)

    nHitsTable = NhitsVsEnergyPosition(material)
	
    graphsList = []
    graphPoints = []
    for positionIndex in range(0, len(Positions)):
	
        graph = ROOT.TGraph()
        graph.SetPoint(0, 0.0, 0.0)
        for energyIndex, energy in enumerate(energies):
		
            graph.SetPoint(energyIndex + 1, energy, nHitsTable[energyIndex][positionIndex])
			
        graph.SetMarkerColor(positionIndex + 2)
        graphsList.append(graph)
		
    canvas = ROOT.TCanvas()
    canvas.Divide(2, len(Positions) / 2)
    for graphIndex, graph in enumerate(graphsList):
        canvas.cd(graphIndex + 1)
        graph.Draw("A*")
        graph.GetYaxis().SetRangeUser(0, 2000)

    raw_input("Press 'Enter' to exit")
	

ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(0)
ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

