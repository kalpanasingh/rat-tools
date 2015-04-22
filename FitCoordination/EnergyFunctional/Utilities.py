#!usr/bin/env python
from array import array
import ROOT, rat, math
# Secondary functions and user-defined Values for the Functional Energy Fitter's Coordinator
# Author K Majumdar - 11/01/2015 <Krishanu.Majumdar@physics.ox.ac.uk>

##############################

# List of energies (in MeV) to coordinate the fitter over, depending on the material being used
energies_energyCoeffs_scintillator = [ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 ]
energies_energyCoeffs_water = [ 5.0, 6.0, 7.0, 8.0, 9.0, 10.0 ]
energies_radiusCoeffs = [ 3.0, 4.0, 5.0, 6.0, 7.0, 8.0 ]
energies_zCoeffs = [ 3.0, 4.0, 5.0, 6.0, 7.0, 8.0 ]

# List of parameters in the general formula, together with the position information used to simulate the data for each parameter
parameters = ["EnergyCoeffs_internal", "EnergyCoeffs_external", "RadiusCoeffs", "ZCoeffs"]
positionTypes = ["point", "point", "plane", "fill"]
positionArgs = ["0 0 0", "0 0 0", "0 0 0 0 0 1 8799", "0 0 0", "6006 0 0", "8500 0 0"]

# Number of segments in each of phi and theta for the Segmentor (the default in the Segmentor is 10)
numberOfSegments = 10

# Base filename for the output text and root files
baseFileName = "AnalyseData_Results_"

# Information on the fit functions used to extract the parameters
# As much of the fit information should be defined here, rather than hard-coded into the functions below, to make it easier to change the functions being used if needed
numberOfEnergyCoeffs = 2
energyFitFunction = "pol1"
numberOfRadiusCoeffs_Internal_Low = 3
radiusFitFunction_Internal_Low = "pol2"
radiusFitRange_Internal_Low = [0.0, 3000.0]
numberOfRadiusCoeffs_Internal_Mid = 4
radiusFitFunction_Internal_Mid = "pol3"
radiusFitRange_Internal_Mid = [3000.0, 5300.0]
numberOfRadiusCoeffs_Internal_High = 3
radiusFitFunction_Internal_High = "pol2"
radiusFitRange_Internal_High = [5300.0, 6005.0]
numberOfRadiusCoeffs_External_Low = 3
radiusFitFunction_External_Low = "pol2"
radiusFitRange_External_Low = [6005.0, 7500.0]
numberOfRadiusCoeffs_External_High = 3
radiusFitFunction_External_High = "pol2"
radiusFitRange_External_High = [7500.0, 8800.0]
numberOfZCoeffs = 4
zFitFunction = "pol3"
zFitRange = [-8800.0, 6005.0]


##############################
# Plot the H-Parameter distribution for each energy, followed by the mean H-Parameter vs. energy, for either internal (parameterIndex == 0) or external (parameterIndex == 1) events
def PlotsForEnergyCoeffs(parameterIndex, material):

    if (parameterIndex == 0):

        if (material == "lightwater_sno"):
            energyList = list(energies_energyCoeffs_water)
        else:
            energyList = list(energies_energyCoeffs_scintillator)
    else:
        energyList = list(energies_energyCoeffs_water)
		
    plotFileName = baseFileName + "PlotsForEnergyCoeffs.root"
    plotFile = ROOT.TFile(plotFileName, "UPDATE")

    meanHValues = []

    for energy in energyList:
        singleEnergyHValues = []
        singleEnergyMinHValue = 1000.0
        singleEnergyMaxHValue = 0.0

        for p in range (1, 6):
            fileName = "electrons_" + parameters[parameterIndex] + "_" + str(int(energy * 1000)) + "keV_" + positionTypes[parameterIndex] + "_part" + str(p) + ".root"

            for ds, run in rat.dsreader(fileName):
                if ds.GetEVCount() == 0:
                    continue
                calibratedPMTs = ds.GetEV(0).GetCalPMTs()

                Segmentor = rat.utility().GetSegmentor()
                Segmentor.SetNumberOfDivisions(numberOfSegments)
                rawPMTSegmentIDs = Segmentor.GetSegmentIDs()
                rawPMTSegmentPopulations = Segmentor.GetSegmentPopulations()
                hitPMTSegmentPopulations = [0] * len(rawPMTSegmentPopulations)
                for j in range(0, calibratedPMTs.GetCount()):
                    hitPMTSegmentPopulations[rawPMTSegmentIDs[calibratedPMTs.GetPMT(j).GetID()]] += 1

                hValue = 0.0
                for s in range(len(rawPMTSegmentPopulations)):
                    if (hitPMTSegmentPopulations[s] >= rawPMTSegmentPopulations[s]):
                        correctedHitPMTSegmentPopulation = rawPMTSegmentPopulations[s] - 1
                    else:
                        correctedHitPMTSegmentPopulation = hitPMTSegmentPopulations[s]
                    hValue += (rawPMTSegmentPopulations[s] * math.log(1.0 - (float(correctedHitPMTSegmentPopulation) / float(rawPMTSegmentPopulations[s]))))
                hValue *= -1.0
                
                singleEnergyHValues.append(hValue)
                if hValue < singleEnergyMinHValue:
                    singleEnergyMinHValue = hValue
                if hValue > singleEnergyMaxHValue:
                    singleEnergyMaxHValue = hValue

        plotNameSingleEnergyH = parameters[parameterIndex] + "_plotSingleEnergyH_" + str(int(energy * 1000)) + "keV"
        plotSingleEnergyH = ROOT.TH1D(plotNameSingleEnergyH, plotNameSingleEnergyH, 25, (singleEnergyMinHValue * 0.9), (singleEnergyMaxHValue * 1.1))
        plotSingleEnergyH.GetXaxis().SetTitle("H Value")
        for h in singleEnergyHValues:
            plotSingleEnergyH.Fill(h)
        
        gaussFit = ROOT.TF1("gaus", "gaus", (singleEnergyMinHValue * 0.9), (singleEnergyMaxHValue * 1.1))
        plotSingleEnergyH.Fit(gaussFit, "RQ")
        meanHValues.append(gaussFit.GetParameter(1))

        plotFile.cd()
        plotSingleEnergyH.Write()

        del plotSingleEnergyH
        del gaussFit

    plotEnergyVsMeanH = ROOT.TGraph(len(energyList), array('d', energyList), array('d', meanHValues))
    plotEnergyVsMeanH.SetMarkerStyle(20)
    plotEnergyVsMeanH.SetMarkerSize(1.0)
    plotEnergyVsMeanH.SetMarkerColor(ROOT.kRed)
    plotEnergyVsMeanH.SetTitle("Mean H-Value vs. Energy")
    plotEnergyVsMeanH.GetXaxis().SetTitle("Energy, MeV")
    plotEnergyVsMeanH.GetYaxis().SetTitle("Mean H-Value")
    plotEnergyVsMeanH.SetName(parameters[parameterIndex] + "_plotEnergyVsMeanH")
    plotFile.cd()
    plotEnergyVsMeanH.Write()
	
    plotFile.Close()


##############################
# Extract the energy coefficients from the mean H-Parameter vs. energy plots, for both internal and external events
# This returns a vector of coefficients: [ 0th order coeff for internal, 1st order coeff for internal ... , 0th order coeff for external, 1st order coeff for external ... ]
def ExtractEnergyCoeffs(material):

    if (material == "lightwater_sno"):
        energies_energyCoeffs_internal = list(energies_energyCoeffs_water)
    else:
        energies_energyCoeffs_internal = list(energies_energyCoeffs_scintillator)

    energyCoefficients = []
    
    inPlotFileName = baseFileName + "PlotsForEnergyCoeffs.root"
    inPlotFile = ROOT.TFile(inPlotFileName, "READ")
	
    plotEnergyVsMeanH_internal = inPlotFile.Get(parameters[0] + "_plotEnergyVsMeanH")
    energyFit_internal = ROOT.TF1("energyFit_internal", energyFitFunction, energies_energyCoeffs_internal[0], energies_energyCoeffs_internal[-1])
    plotEnergyVsMeanH_internal.Fit(energyFit_internal, "R")
    canvasEnergyVsMeanH_internal = ROOT.TCanvas("canvasEnergyVsMeanH_internal", "canvasEnergyVsMeanH_internal", 1500, 900)
    plotEnergyVsMeanH_internal.Draw("AP")
    for parameter in range(0, numberOfEnergyCoeffs):
        energyCoefficients.append(energyFit_internal.GetParameter(parameter))
    
    plotEnergyVsMeanH_external = inPlotFile.Get(parameters[1] + "_plotEnergyVsMeanH")
    energyFit_external = ROOT.TF1("energyFit_external", energyFitFunction, energies_energyCoeffs_water[0], energies_energyCoeffs_water[-1])
    plotEnergyVsMeanH_external.Fit(energyFit_external, "R")
    canvasEnergyVsMeanH_external = ROOT.TCanvas("canvasEnergyVsMeanH_external", "canvasEnergyVsMeanH_external", 1500, 900)
    plotEnergyVsMeanH_external.Draw("AP")
    for parameter in range(0, numberOfEnergyCoeffs):
        energyCoefficients.append(energyFit_external.GetParameter(parameter))

    outPlotFileName = baseFileName + "ExtractEnergyCoeffs.root"
    outPlotFile = ROOT.TFile(outPlotFileName, "UPDATE")
    canvasEnergyVsMeanH_internal.Write()
    canvasEnergyVsMeanH_external.Write()
    outPlotFile.Close()
    
    del plotEnergyVsMeanH_internal
    del energyFit_internal
    del canvasEnergyVsMeanH_internal
    del plotEnergyVsMeanH_external
    del energyFit_external
    del canvasEnergyVsMeanH_external

    return energyCoefficients


##############################
# Plot the Radius vs. H-Factor distribution for each energy
def PlotsForRadiusCoeffs(energyCoefficients, material):

    energyList = list(energies_radiusCoeffs)
    	
    plotFileName = baseFileName + "PlotsForRadiusCoeffs.root"
    plotFile = ROOT.TFile(plotFileName, "UPDATE")

    histRadiusVsHFactor = ROOT.TH2D("histRadiusVsHFactor", "H-Factor vs. Radius over All Energies; Radius, mm; H-Factor", 155, 0.0, 9000.0, 200, 0.0, 4.0)
    histRadiusVsHFactor.SetStats(0)
    ROOT.gStyle.SetPalette(1)
    allHFactors, allRadii = [], []

    for energy in energyList:
        histNameSingleEnergyRVsHFactor = "histSingleEnergyRVsHFactor_" + str(int(energy * 1000)) + "keV"
        histSingleEnergyRVsHFactor = ROOT.TH2D(histNameSingleEnergyRVsHFactor, "H-Factor vs. Radius for a Single Energy; Radius, mm; H-Factor", 155, 0.0, 9000.0, 200, 0.0, 4.0)
        histSingleEnergyRVsHFactor.SetStats(0)
        ROOT.gStyle.SetPalette(1)
        singleEnergyHFactors, singleEnergyRadii = [], []

        for p in range (1, 6):
            fileName = "electrons_" + parameters[2] + "_" + str(int(energy * 1000)) + "keV_" + positionTypes[2] + "_part" + str(p) + ".root"

            for ds, run in rat.dsreader(fileName):
                if ds.GetEVCount() == 0:
                    continue

                trueRadius = ds.GetMC().GetMCParticle(0).GetPosition().Mag()
				
                if (trueRadius < radiusFitRange_External_Low[0]):
                    if (material == "lightwater_sno"):
                        if not (ds.GetEV(0).FitResultExists("waterPositionFit")):
                            continue
                        if not (ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).ContainsPosition()):
                            continue
                        if not (ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).ValidPosition()):
                            continue
                        recoRadius = ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).GetPosition().Mag()
                    else:
                        if not (ds.GetEV(0).FitResultExists("scintPositionFit")):
                            continue
                        if not (ds.GetEV(0).GetFitResult("scintPositionFit").GetVertex(0).ContainsPosition()):
                            continue
                        if not (ds.GetEV(0).GetFitResult("scintPositionFit").GetVertex(0).ValidPosition()):
                            continue
                        recoRadius = ds.GetEV(0).GetFitResult("scintPositionFit").GetVertex(0).GetPosition().Mag()
                else:
                    if not (ds.GetEV(0).FitResultExists("waterPositionFit")):
                        continue
                    if not (ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).ContainsPosition()):
                        continue
                    if not (ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).ValidPosition()):
                        continue
                    recoRadius = ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).GetPosition().Mag()
                    
                calibratedPMTs = ds.GetEV(0).GetCalPMTs()

                Segmentor = rat.utility().GetSegmentor()
                Segmentor.SetNumberOfDivisions(numberOfSegments)
                rawPMTSegmentIDs = Segmentor.GetSegmentIDs()
                rawPMTSegmentPopulations = Segmentor.GetSegmentPopulations()
                hitPMTSegmentPopulations = [0] * len(rawPMTSegmentPopulations)
                for j in range(0, calibratedPMTs.GetCount()):
                    hitPMTSegmentPopulations[rawPMTSegmentIDs[calibratedPMTs.GetPMT(j).GetID()]] += 1

                hValue = 0.0
                for s in range(len(rawPMTSegmentPopulations)):
                    if (hitPMTSegmentPopulations[s] >= rawPMTSegmentPopulations[s]):
                        correctedHitPMTSegmentPopulation = rawPMTSegmentPopulations[s] - 1
                    else:
                        correctedHitPMTSegmentPopulation = hitPMTSegmentPopulations[s]
                    hValue += (rawPMTSegmentPopulations[s] * math.log(1.0 - (float(correctedHitPMTSegmentPopulation) / float(rawPMTSegmentPopulations[s]))))
                hValue *= -1.0
                
                hAtCentre = 0.0
                if (recoRadius < radiusFitRange_External_Low[0]):
                    for e in range(0, numberOfEnergyCoeffs):
                        hAtCentre += (energyCoefficients[e] * math.pow(energy, e))
                else:
                    for e in range(0, numberOfEnergyCoeffs):
                        hAtCentre += (energyCoefficients[e + numberOfEnergyCoeffs] * math.pow(energy, e))
                
                hFactor = hValue / hAtCentre
                if (hFactor < 0.2) or (hFactor > 10.0):
                    continue
					
                histSingleEnergyRVsHFactor.Fill(recoRadius, hFactor)
                singleEnergyRadii.append(recoRadius)
                singleEnergyHFactors.append(hFactor)
                histRadiusVsHFactor.Fill(recoRadius, hFactor)
                allRadii.append(recoRadius)
                allHFactors.append(hFactor)               

        graphSingleEnergyRVsHFactor = ROOT.TGraph(len(singleEnergyRadii), array('d', singleEnergyRadii), array('d', singleEnergyHFactors))
        graphSingleEnergyRVsHFactor.SetMarkerStyle(20)
        graphSingleEnergyRVsHFactor.SetMarkerSize(0.5)
        graphSingleEnergyRVsHFactor.SetMarkerColor(ROOT.kRed)
        graphSingleEnergyRVsHFactor.SetTitle("H-Factor vs. Radius for a Single Energy")
        graphSingleEnergyRVsHFactor.GetXaxis().SetTitle("Radius, mm")
        graphSingleEnergyRVsHFactor.GetXaxis().SetRangeUser(0.0, 9000.0)
        graphSingleEnergyRVsHFactor.GetYaxis().SetTitle("H-Factor")
        graphSingleEnergyRVsHFactor.GetYaxis().SetRangeUser(0.0, 4.0)
        graphNameSingleEnergyRVsHFactor = "graphSingleEnergyRVsHFactor_" + str(int(energy * 1000)) + "keV"
        graphSingleEnergyRVsHFactor.SetName(graphNameSingleEnergyRVsHFactor)

        plotFile.cd()
        graphSingleEnergyRVsHFactor.Write()
        histSingleEnergyRVsHFactor.Write()

        del graphSingleEnergyRVsHFactor
        del histSingleEnergyRVsHFactor

    graphRadiusVsHFactor = ROOT.TGraph(len(allRadii), array('d', allRadii), array('d', allHFactors))
    graphRadiusVsHFactor.SetMarkerStyle(20)
    graphRadiusVsHFactor.SetMarkerSize(0.5)
    graphRadiusVsHFactor.SetMarkerColor(ROOT.kRed)
    graphRadiusVsHFactor.SetTitle("H-Factor vs. Radius over All Energies")
    graphRadiusVsHFactor.GetXaxis().SetTitle("Radius, mm")
    graphRadiusVsHFactor.GetXaxis().SetRangeUser(0.0, 9000.0)
    graphRadiusVsHFactor.GetYaxis().SetTitle("H-Factor")
    graphRadiusVsHFactor.GetYaxis().SetRangeUser(0.0, 4.0)
    graphRadiusVsHFactor.SetName("graphRadiusVsHFactor")

    plotFile.cd()
    graphRadiusVsHFactor.Write()
    histRadiusVsHFactor.Write()

    plotFile.Close()


##############################
# Extract the radius coefficients from the Radius vs. H-Factor distribution over ALL energies
def ExtractRadiusCoeffs():

    inPlotFileName = baseFileName + "PlotsForRadiusCoeffs.root"
    inPlotFile = ROOT.TFile(inPlotFileName, "READ")
    graphAllEnergiesRadiusVsHFactor = inPlotFile.Get("graphRadiusVsHFactor")
    histAllEnergiesRadiusVsHFactor = inPlotFile.Get("histRadiusVsHFactor")

    radiusFit_Internal_Low = ROOT.TF1("radiusFit_Internal_Low", radiusFitFunction_Internal_Low, radiusFitRange_Internal_Low[0], radiusFitRange_Internal_Low[1])
    radiusFit_Internal_Low.FixParameter(0, 1.0)
    graphAllEnergiesRadiusVsHFactor.Fit(radiusFit_Internal_Low, "R")

    radiusFit_Internal_Mid = ROOT.TF1("radiusFit_Internal_Mid", radiusFitFunction_Internal_Mid, radiusFitRange_Internal_Mid[0], radiusFitRange_Internal_Mid[1])
    graphAllEnergiesRadiusVsHFactor.Fit(radiusFit_Internal_Mid, "R")

    radiusFit_Internal_High = ROOT.TF1("radiusFit_Internal_High", radiusFitFunction_Internal_High, radiusFitRange_Internal_High[0], radiusFitRange_Internal_High[1])
    graphAllEnergiesRadiusVsHFactor.Fit(radiusFit_Internal_High, "R")
	
    radiusFit_External_Low = ROOT.TF1("radiusFit_External_Low", radiusFitFunction_External_Low, radiusFitRange_External_Low[0], radiusFitRange_External_Low[1])
    graphAllEnergiesRadiusVsHFactor.Fit(radiusFit_External_Low, "R")
	
    radiusFit_External_High = ROOT.TF1("radiusFit_External_High", radiusFitFunction_External_High, radiusFitRange_External_High[0], radiusFitRange_External_High[1])
    graphAllEnergiesRadiusVsHFactor.Fit(radiusFit_External_High, "R")

    radiusCoefficients = []
    for parameter in range(0, numberOfRadiusCoeffs_Internal_Low):
        radiusCoefficients.append(radiusFit_Internal_Low.GetParameter(parameter))
    for parameter in range(0, numberOfRadiusCoeffs_Internal_Mid):
        radiusCoefficients.append(radiusFit_Internal_Mid.GetParameter(parameter))
    for parameter in range(0, numberOfRadiusCoeffs_Internal_High):
        radiusCoefficients.append(radiusFit_Internal_High.GetParameter(parameter))
    for parameter in range(0, numberOfRadiusCoeffs_External_Low):
        radiusCoefficients.append(radiusFit_External_Low.GetParameter(parameter))
    for parameter in range(0, numberOfRadiusCoeffs_External_High):
        radiusCoefficients.append(radiusFit_External_High.GetParameter(parameter))

    canvasGraphRadiusVsHFactor = ROOT.TCanvas("canvasGraphRadiusVsHFactor", "canvasGraphRadiusVsHFactor", 1500, 900)
    graphAllEnergiesRadiusVsHFactor.Draw("AP")
    radiusFit_Internal_Low.Draw("L SAME")
    radiusFit_Internal_Mid.Draw("L SAME")
    radiusFit_Internal_High.Draw("L SAME")
    radiusFit_External_Low.Draw("L SAME")
    radiusFit_External_High.Draw("L SAME")
    
    canvasHistRadiusVsHFactor = ROOT.TCanvas("canvasHistRadiusVsHFactor", "canvasHistRadiusVsHFactor", 1500, 900)
    histAllEnergiesRadiusVsHFactor.Draw("COLZ")
    radiusFit_Internal_Low.Draw("L SAME")
    radiusFit_Internal_Mid.Draw("L SAME")
    radiusFit_Internal_High.Draw("L SAME")
    radiusFit_External_Low.Draw("L SAME")
    radiusFit_External_High.Draw("L SAME")
	
    outPlotFileName = baseFileName + "ExtractRadiusCoeffs.root"
    outPlotFile = ROOT.TFile(outPlotFileName, "UPDATE")
    canvasGraphRadiusVsHFactor.Write()
    canvasHistRadiusVsHFactor.Write()
    outPlotFile.Close()
    
    del radiusFit_Internal_Low
    del radiusFit_Internal_Mid
    del radiusFit_Internal_High
    del radiusFit_External_Low
    del radiusFit_External_High
    del canvasGraphRadiusVsHFactor
    del canvasHistRadiusVsHFactor

    return radiusCoefficients


##############################
# Plot the Z vs. H-Factor distribution for each energy
def PlotsForZCoeffs(energyCoefficients, radiusCoefficients, material):

    energyList = list(energies_zCoeffs)
	
    plotFileName = baseFileName + "PlotsForZCoeffs.root"
    plotFile = ROOT.TFile(plotFileName, "UPDATE")

    histZVsHFactor = ROOT.TH2D("histZVsHFactor", "H-Factor vs. Z over All Energies; Z, mm; H-Factor", 155, -9000.0, 9000.0, 150, 0.0, 1.5)
    histZVsHFactor.SetStats(0)
    ROOT.gStyle.SetPalette(1)
    allHFactors, allZ = [], []

    for energy in energyList:
        histNameSingleEnergyZVsHFactor = "histSingleEnergyZVsHFactor_" + str(int(energy * 1000)) + "keV"
        histSingleEnergyZVsHFactor = ROOT.TH2D(histNameSingleEnergyZVsHFactor, "H-Factor vs. Z for a Single Energy; Z, mm; H-Factor", 155, -9000.0, 9000.0, 150, 0.0, 1.5)
        histSingleEnergyZVsHFactor.SetStats(0)
        ROOT.gStyle.SetPalette(1)
        singleEnergyHFactors, singleEnergyZ = [], []

        for p in range (1, 6):
            fileName = "electrons_" + parameters[3] + "_" + str(int(energy * 1000)) + "keV_" + positionTypes[3] + "_part" + str(p) + ".root"

            for ds, run in rat.dsreader(fileName):
                if ds.GetEVCount() == 0:
                    continue

                trueRadius = ds.GetMC().GetMCParticle(0).GetPosition().Mag()
				
                if (trueRadius < radiusFitRange_External_Low[0]):
                    if (material == "lightwater_sno"):
                        if not (ds.GetEV(0).FitResultExists("waterPositionFit")):
                            continue
                        if not (ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).ContainsPosition()):
                            continue
                        if not (ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).ValidPosition()):
                            continue
                        recoRadius = ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).GetPosition().Mag()
                        recoZ = ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).GetPosition().Z()
                    else:
                        if not (ds.GetEV(0).FitResultExists("scintPositionFit")):
                            continue
                        if not (ds.GetEV(0).GetFitResult("scintPositionFit").GetVertex(0).ContainsPosition()):
                            continue
                        if not (ds.GetEV(0).GetFitResult("scintPositionFit").GetVertex(0).ValidPosition()):
                            continue
                        recoRadius = ds.GetEV(0).GetFitResult("scintPositionFit").GetVertex(0).GetPosition().Mag()
                        recoZ = ds.GetEV(0).GetFitResult("scintPositionFit").GetVertex(0).GetPosition().Z()
                else:
                    if not (ds.GetEV(0).FitResultExists("waterPositionFit")):
                        continue
                    if not (ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).ContainsPosition()):
                        continue
                    if not (ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).ValidPosition()):
                        continue
                    recoRadius = ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).GetPosition().Mag()
                    recoZ = ds.GetEV(0).GetFitResult("waterPositionFit").GetVertex(0).GetPosition().Z()
                    
                calibratedPMTs = ds.GetEV(0).GetCalPMTs()

                Segmentor = rat.utility().GetSegmentor()
                Segmentor.SetNumberOfDivisions(numberOfSegments)
                rawPMTSegmentIDs = Segmentor.GetSegmentIDs()
                rawPMTSegmentPopulations = Segmentor.GetSegmentPopulations()
                hitPMTSegmentPopulations = [0] * len(rawPMTSegmentPopulations)
                for j in range(0, calibratedPMTs.GetCount()):
                    hitPMTSegmentPopulations[rawPMTSegmentIDs[calibratedPMTs.GetPMT(j).GetID()]] += 1

                hValue = 0.0
                for s in range(len(rawPMTSegmentPopulations)):
                    if (hitPMTSegmentPopulations[s] >= rawPMTSegmentPopulations[s]):
                        correctedHitPMTSegmentPopulation = rawPMTSegmentPopulations[s] - 1
                    else:
                        correctedHitPMTSegmentPopulation = hitPMTSegmentPopulations[s]
                    hValue += (rawPMTSegmentPopulations[s] * math.log(1.0 - (float(correctedHitPMTSegmentPopulation) / float(rawPMTSegmentPopulations[s]))))
                hValue *= -1.0

                hAtCentre = 0.0
                if (recoRadius < radiusFitRange_External_Low[0]):
                    for e in range(0, numberOfEnergyCoeffs):
                        hAtCentre += (energyCoefficients[e] * math.pow(energy, e))
                else:
                    for e in range(0, numberOfEnergyCoeffs):
                        hAtCentre += (energyCoefficients[e + numberOfEnergyCoeffs] * math.pow(energy, e))
                
                functionOfRadius = 0.0
                if ((recoRadius >= radiusFitRange_Internal_Low[0]) and (recoRadius < radiusFitRange_Internal_Low[1])):
                    for p in range(0, numberOfRadiusCoeffs_Internal_Low):
                        functionOfRadius += (radiusCoefficients[p] * math.pow(recoRadius, p))
                elif ((recoRadius >= radiusFitRange_Internal_Mid[0]) and (recoRadius < radiusFitRange_Internal_Mid[1])):
                    for p in range(0, numberOfRadiusCoeffs_Internal_Mid):
                        functionOfRadius += (radiusCoefficients[p + numberOfRadiusCoeffs_Internal_Low] * math.pow(recoRadius, p))
                elif ((recoRadius >= radiusFitRange_Internal_High[0]) and (recoRadius < radiusFitRange_Internal_High[1])):
                    for p in range(0, numberOfRadiusCoeffs_Internal_High):
                        functionOfRadius += (radiusCoefficients[p + numberOfRadiusCoeffs_Internal_Low + numberOfRadiusCoeffs_Internal_Mid] * math.pow(recoRadius, p))
                elif ((recoRadius >= radiusFitRange_External_Low[0]) and (recoRadius < radiusFitRange_External_Low[1])):
                    for p in range(0, numberOfRadiusCoeffs_External_Low):
                        functionOfRadius += (radiusCoefficients[p + numberOfRadiusCoeffs_Internal_Low + numberOfRadiusCoeffs_Internal_Mid + numberOfRadiusCoeffs_Internal_High] * math.pow(recoRadius, p))
                elif ((recoRadius >= radiusFitRange_External_High[0]) and (recoRadius < radiusFitRange_External_High[1])):
                    for p in range(0, numberOfRadiusCoeffs_External_High):
                        functionOfRadius += (radiusCoefficients[p + numberOfRadiusCoeffs_Internal_Low + numberOfRadiusCoeffs_Internal_Mid + numberOfRadiusCoeffs_Internal_High + numberOfRadiusCoeffs_External_Low] * math.pow(recoRadius, p))
                else:
                    continue

                hFactor = hValue / (hAtCentre * functionOfRadius)
                if (hFactor < 0.2) or (hFactor > 10.0):
                    continue

                histSingleEnergyZVsHFactor.Fill(recoZ, hFactor)
                singleEnergyZ.append(recoZ)
                singleEnergyHFactors.append(hFactor)
                histZVsHFactor.Fill(recoZ, hFactor)
                allZ.append(recoZ)
                allHFactors.append(hFactor)

        graphSingleEnergyZVsHFactor = ROOT.TGraph(len(singleEnergyZ), array('d', singleEnergyZ), array('d', singleEnergyHFactors))
        graphSingleEnergyZVsHFactor.SetMarkerStyle(20)
        graphSingleEnergyZVsHFactor.SetMarkerSize(0.5)
        graphSingleEnergyZVsHFactor.SetMarkerColor(ROOT.kRed)
        graphSingleEnergyZVsHFactor.SetTitle("H-Factor vs. Z for a Single Energy")
        graphSingleEnergyZVsHFactor.GetXaxis().SetTitle("Z, mm")
        graphSingleEnergyZVsHFactor.GetXaxis().SetRangeUser(-9000.0, 9000.0)
        graphSingleEnergyZVsHFactor.GetYaxis().SetTitle("H-Factor")
        graphSingleEnergyZVsHFactor.GetYaxis().SetRangeUser(0.0, 1.5)
        graphNameSingleEnergyZVsHFactor = "graphSingleEnergyZVsHFactor_" + str(int(energy * 1000)) + "keV"
        graphSingleEnergyZVsHFactor.SetName(graphNameSingleEnergyZVsHFactor)

        plotFile.cd()
        graphSingleEnergyZVsHFactor.Write()
        histSingleEnergyZVsHFactor.Write()

        del graphSingleEnergyZVsHFactor
        del histSingleEnergyZVsHFactor

    graphZVsHFactor = ROOT.TGraph(len(allZ), array('d', allZ), array('d', allHFactors))
    graphZVsHFactor.SetMarkerStyle(20)
    graphZVsHFactor.SetMarkerSize(0.5)
    graphZVsHFactor.SetMarkerColor(ROOT.kRed)
    graphZVsHFactor.SetTitle("H-Factor vs. Z over All Energies")
    graphZVsHFactor.GetXaxis().SetTitle("Z, mm")
    graphZVsHFactor.GetXaxis().SetRangeUser(-9000.0, 9000.0)
    graphZVsHFactor.GetYaxis().SetTitle("H-Factor")
    graphZVsHFactor.GetYaxis().SetRangeUser(0.0, 1.5)
    graphZVsHFactor.SetName("graphZVsHFactor")

    plotFile.cd()
    graphZVsHFactor.Write()
    histZVsHFactor.Write()

    plotFile.Close()


##############################
# Extract the z coefficients from the Z vs. H-Factor distribution over ALL energies
def ExtractZCoeffs():

    inPlotFileName = baseFileName + "PlotsForZCoeffs.root"
    inPlotFile = ROOT.TFile(inPlotFileName, "READ")
    graphAllEnergiesZVsHFactor = inPlotFile.Get("graphZVsHFactor")
    histAllEnergiesZVsHFactor = inPlotFile.Get("histZVsHFactor")

    zFit = ROOT.TF1("zFit", zFitFunction, zFitRange[0], zFitRange[1])
    zFit.FixParameter(0, 1.0)
    graphAllEnergiesZVsHFactor.Fit(zFit, "R")

    zCoeffs = []
    for parameter in range(0, numberOfZCoeffs):
        zCoeffs.append(zFit.GetParameter(parameter))

    canvasGraphZVsHFactor = ROOT.TCanvas("canvasGraphZVsHFactor", "canvasGraphZVsHFactor", 1500, 900)
    graphAllEnergiesZVsHFactor.Draw("AP")
    zFit.Draw("L SAME")
    
    canvasHistZVsHFactor = ROOT.TCanvas("canvasHistZVsHFactor", "canvasHistZVsHFactor", 1500, 900)
    histAllEnergiesZVsHFactor.Draw("COLZ")
    zFit.Draw("L SAME")
	
    outPlotFileName = baseFileName + "ExtractZCoeffs.root"
    outPlotFile = ROOT.TFile(outPlotFileName, "UPDATE")
    canvasGraphZVsHFactor.Write()
    canvasHistZVsHFactor.Write()
    outPlotFile.Close()
    
    del zFit
    del canvasGraphZVsHFactor
    del canvasHistZVsHFactor

    return zCoeffs


##############################
