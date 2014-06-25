#!usr/bin/env python
from array import array
import ROOT, rat, math
# Secondary functions and user-defined Values for the Functional Energy Fitter's Coordinator
# Author K Majumdar - 25/06/2014 <Krishanu.Majumdar@physics.ox.ac.uk>

##############################

# List of energies (in MeV) to coordinate the fitter over
energies = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

# List of parameters in the general formula, together with the position information used to simulate the data for each parameter
parameters = ["Alpha", "Beta", "Gamma"]
positionTypes = ["point", "plane", "fill"]
positionArgs = ["0.0 0.0 0.0", "0.0 0.0 0.0 0.0 0.0 1.0 6005", "0.0 0.0 0.0"]

# Parameters for use in submitting the macros to a batch system
envrnLoc = ""
currentLoc = ""

# Number of segments in each of phi and theta for the Segmentor (the default in the Segmentor is 10)
numberOfSegments = 10

# Base filename for the output text and root files
baseFileName = "AnalyseData_Results_"

# Information on the fit functions used to extract the parameters
# This is all included here, rather than hard-coded into the functions below, to make it easier to change the functions being used if needed
# Order is as follows: [alphaFunction, betaFunctionLowRadius, betaFunctionMidRadius, betaFunctionHighRadius, gammaFunction]
numberOfParameters = [2, 3, 4, 3, 4]
fitRangeLow = [0.0, 0.0, 2000.0, 5300.0, -6005.3]
fitRangeHigh = [energies[-1], 2000.0, 5300.0, 6005.3, 6005.3]


##############################
# Plot the H-Parameter distributions for each energy in preparation for extracting the Alpha parameters
def PlotsForAlphas():

    plotFileName = baseFileName + "PlotsForAlphas.root"
    plotFile = ROOT.TFile(plotFileName, "UPDATE")

    for energy in energies:
        singleEnergyHValues = []
        singleEnergyMaxHValue = 0.0

        for p in range (1, 6):
            fileName = "electrons_" + parameters[0] + "_" + str(int(energy * 1000)) + "keV_" + positionTypes[0] + "_part" + str(p) + ".root"

            for ds, run in rat.dsreader(fileName):
                if ds.GetEVCount() == 0:
                    continue
                calibratedPMTs = ds.GetEV(0).GetCalibratedPMTs()

                Segmentor = rat.utility().GetSegmentor()
                Segmentor.SetNumberOfDivisions(numberOfSegments)
                rawPMTSegmentIDs = Segmentor.GetSegmentIDs()
                rawPMTSegmentPopulations = Segmentor.GetSegmentPopulations()
                hitPMTSegmentPopulations = [0] * len(rawPMTSegmentPopulations)
                for j in range(0, calibratedPMTs.GetCount()):
                    hitPMTSegmentPopulations[rawPMTSegmentIDs[calibratedPMTs.GetPMT(j).GetID()]] += 1

                hValue = 0.0
                for s in range(len(rawPMTSegmentPopulations)):
                    hValue += (rawPMTSegmentPopulations[s] * math.log(1.0 - (float(hitPMTSegmentPopulations[s]) / float(rawPMTSegmentPopulations[s]))))
                hValue *= -1.0
                
                singleEnergyHValues.append(hValue)
                if hValue > singleEnergyMaxHValue:
                    singleEnergyMaxHValue = hValue

        plotNameSingleEnergyH = "plotSingleEnergyH_" + str(int(energy * 1000)) + "keV"
        plotSingleEnergyH = ROOT.TH1D(plotNameSingleEnergyH, plotNameSingleEnergyH, 100, 0.0, (singleEnergyMaxHValue * 1.1))
        plotSingleEnergyH.GetXaxis().SetTitle("H Value")
        for h in singleEnergyHValues:
            plotSingleEnergyH.Fill(h)
        
        plotFile.cd()
        plotSingleEnergyH.Write()

        del plotSingleEnergyH

    plotFile.Close()


##############################
# Extract the Alpha parameters from the previously saved H-Parameter distributions
def ExtractAlphaParameters():

    inPlotFileName = baseFileName + "PlotsForAlphas.root"
    inPlotFile = ROOT.TFile(inPlotFileName, "READ")

    meanHValues = []

    for energy in energies:

        plotNameSingleEnergyH = "plotSingleEnergyH_" + str(int(energy * 1000)) + "keV"
        plotSingleEnergyH = inPlotFile.Get(plotNameSingleEnergyH)
        singleEnergyMaxHValue = plotSingleEnergyH.GetBinLowEdge(plotSingleEnergyH.GetNbinsX())

        gaussFit = ROOT.TF1("gaus", "gaus", 0.0, (singleEnergyMaxHValue * 1.1))
        plotSingleEnergyH.Fit(gaussFit, "RQ")
        meanHValues.append(gaussFit.GetParameter(1))
		
        del plotSingleEnergyH
        del gaussFit
		
    plotEnergyVsMeanH = ROOT.TGraph(len(energies), array('d', energies), array('d', meanHValues))
    plotEnergyVsMeanH.SetMarkerStyle(20)
    plotEnergyVsMeanH.SetMarkerSize(1.0)
    plotEnergyVsMeanH.SetMarkerColor(ROOT.kRed)
    plotEnergyVsMeanH.SetTitle("Mean H-Value vs. Energy")
    plotEnergyVsMeanH.GetXaxis().SetTitle("Energy, MeV")
    plotEnergyVsMeanH.GetYaxis().SetTitle("Mean H-Value")

    alphaFunction = "pol" + str( int(numberOfParameters[0] - 1) )
    alphaFit = ROOT.TF1(alphaFunction, alphaFunction, fitRangeLow[0], fitRangeHigh[0])
    alphaFit.FixParameter(0, 0.0)
    plotEnergyVsMeanH.Fit(alphaFit, "R")

    alphaParameters = []
    for parameter in range(0, numberOfParameters[0]):
        alphaParameters.append(alphaFit.GetParameter(parameter))

    outPlotFileName = baseFileName + "ExtractAlphas.root"
    outPlotFile = ROOT.TFile(outPlotFileName, "UPDATE")
    canvasEnergyVsMeanH = ROOT.TCanvas("canvasEnergyVsMeanH", "canvasEnergyVsMeanH", 1500, 900)
    plotEnergyVsMeanH.Draw("AP")
    outPlotFile.cd()
    canvasEnergyVsMeanH.Write()
    outPlotFile.Close()
    
    del plotEnergyVsMeanH
    del alphaFit
    del canvasEnergyVsMeanH

    return alphaParameters


##############################
# Plot the Radius vs. H-Factor distributions for each energy and over all energies in preparation for extracting the Beta parameters
def PlotsForBetas(alphaParameters):

    plotFileName = baseFileName + "PlotsForBetas.root"
    plotFile = ROOT.TFile(plotFileName, "UPDATE")

    histRadiusVsHFactor = ROOT.TH2D("histRadiusVsHFactor", "H-Factor vs. Radius over All Energies; Radius, mm; H-Factor", 155, 0.0, 6200.0, 150, 0.0, 1.5)
    histRadiusVsHFactor.SetStats(0)
    ROOT.gStyle.SetPalette(1)
    allHFactors, allRadii = [], []

    for energy in energies:
        histNameSingleEnergyRVsHFactor = "histSingleEnergyRVsHFactor_" + str(int(energy * 1000)) + "keV"
        histSingleEnergyRVsHFactor = ROOT.TH2D(histNameSingleEnergyRVsHFactor, "H-Factor vs. Radius for a Single Energy; Radius, mm; H-Factor", 155, 0.0, 6200.0, 150, 0.0, 1.5)
        histSingleEnergyRVsHFactor.SetStats(0)
        ROOT.gStyle.SetPalette(1)
        singleEnergyHFactors, singleEnergyRadii = [], []

        for p in range (1, 6):
            fileName = "electrons_" + parameters[1] + "_" + str(int(energy * 1000)) + "keV_" + positionTypes[1] + "_part" + str(p) + ".root"

            for ds, run in rat.dsreader(fileName):
                if ds.GetEVCount() == 0:
                    continue
                calibratedPMTs = ds.GetEV(0).GetCalibratedPMTs()

                radius = ds.GetMC().GetMCParticle(0).GetPosition().Mag()
                
                Segmentor = rat.utility().GetSegmentor()
                Segmentor.SetNumberOfDivisions(numberOfSegments)
                rawPMTSegmentIDs = Segmentor.GetSegmentIDs()
                rawPMTSegmentPopulations = Segmentor.GetSegmentPopulations()
                hitPMTSegmentPopulations = [0] * len(rawPMTSegmentPopulations)
                for j in range(0, calibratedPMTs.GetCount()):
                    hitPMTSegmentPopulations[rawPMTSegmentIDs[calibratedPMTs.GetPMT(j).GetID()]] += 1

                hValue = 0.0
                for s in range(len(rawPMTSegmentPopulations)):
                    hValue += (rawPMTSegmentPopulations[s] * math.log(1.0 - (float(hitPMTSegmentPopulations[s]) / float(rawPMTSegmentPopulations[s]))))
                hValue *= -1.0
                
                hAtCentre = 0.0
                for p in range(0, numberOfParameters[0]):
                    hAtCentre += (alphaParameters[p] * math.pow(energy, p))
                
                hFactor = hValue / hAtCentre

                histSingleEnergyRVsHFactor.Fill(radius, hFactor)
                singleEnergyRadii.append(radius)
                singleEnergyHFactors.append(hFactor)
                histRadiusVsHFactor.Fill(radius, hFactor)
                allRadii.append(radius)
                allHFactors.append(hFactor)

        graphSingleEnergyRVsHFactor = ROOT.TGraph(len(singleEnergyRadii), array('d', singleEnergyRadii), array('d', singleEnergyHFactors))
        graphSingleEnergyRVsHFactor.SetMarkerStyle(20)
        graphSingleEnergyRVsHFactor.SetMarkerSize(0.5)
        graphSingleEnergyRVsHFactor.SetMarkerColor(ROOT.kRed)
        graphSingleEnergyRVsHFactor.SetTitle("H-Factor vs. Radius for a Single Energy")
        graphSingleEnergyRVsHFactor.GetXaxis().SetTitle("Radius, mm")
        graphSingleEnergyRVsHFactor.GetXaxis().SetRangeUser(0.0, 6200.0)
        graphSingleEnergyRVsHFactor.GetYaxis().SetTitle("H-Factor")
        graphSingleEnergyRVsHFactor.GetYaxis().SetRangeUser(0.0, 1.5)
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
    graphRadiusVsHFactor.GetXaxis().SetRangeUser(0.0, 6200.0)
    graphRadiusVsHFactor.GetYaxis().SetTitle("H-Factor")
    graphRadiusVsHFactor.GetYaxis().SetRangeUser(0.0, 1.5)
    graphRadiusVsHFactor.SetName("graphRadiusVsHFactor")

    plotFile.cd()
    graphRadiusVsHFactor.Write()
    histRadiusVsHFactor.Write()

    plotFile.Close()


##############################
# Extract the Beta parameters from the previously saved H-Parameter distributions ("All Energies" plots only)
def ExtractBetaParameters():

    inPlotFileName = baseFileName + "PlotsForBetas.root"
    inPlotFile = ROOT.TFile(inPlotFileName, "READ")
    graphAllEnergiesRadiusVsHFactor = inPlotFile.Get("graphRadiusVsHFactor")
    histAllEnergiesRadiusVsHFactor = inPlotFile.Get("histRadiusVsHFactor")

    betaFunctionLowRadius = "pol" + str( int(numberOfParameters[1] - 1) )
    betaFitLowRadius = ROOT.TF1(betaFunctionLowRadius, betaFunctionLowRadius, fitRangeLow[1], fitRangeHigh[1])
    betaFitLowRadius.FixParameter(0, 1.0)
    graphAllEnergiesRadiusVsHFactor.Fit(betaFitLowRadius, "R")

    betaFunctionMidRadius = "pol" + str( int(numberOfParameters[2] - 1) )
    betaFitMidRadius = ROOT.TF1(betaFunctionMidRadius, betaFunctionMidRadius, fitRangeLow[2], fitRangeHigh[2])
    graphAllEnergiesRadiusVsHFactor.Fit(betaFitMidRadius, "R")

    betaFunctionHighRadius = "pol" + str( int(numberOfParameters[3] - 1) )
    betaFitHighRadius = ROOT.TF1(betaFunctionHighRadius, betaFunctionHighRadius, fitRangeLow[3], fitRangeHigh[3])
    graphAllEnergiesRadiusVsHFactor.Fit(betaFitHighRadius, "R")

    betaParameters = []
    for parameter in range(0, numberOfParameters[1]):
        betaParameters.append(betaFitLowRadius.GetParameter(parameter))
    for parameter in range(0, numberOfParameters[2]):
        betaParameters.append(betaFitMidRadius.GetParameter(parameter))
    for parameter in range(0, numberOfParameters[3]):
        betaParameters.append(betaFitHighRadius.GetParameter(parameter))

    canvasGraphRadiusVsHFactor = ROOT.TCanvas("canvasGraphRadiusVsHFactor", "canvasGraphRadiusVsHFactor", 1500, 900)
    graphAllEnergiesRadiusVsHFactor.Draw("AP")
    betaFitLowRadius.Draw("L SAME")
    betaFitMidRadius.Draw("L SAME")
    betaFitHighRadius.Draw("L SAME")
    
    canvasHistRadiusVsHFactor = ROOT.TCanvas("canvasHistRadiusVsHFactor", "canvasHistRadiusVsHFactor", 1500, 900)
    histAllEnergiesRadiusVsHFactor.Draw("COLZ")
    betaFitLowRadius.Draw("L SAME")
    betaFitMidRadius.Draw("L SAME")
    betaFitHighRadius.Draw("L SAME")
	
    outPlotFileName = baseFileName + "ExtractBetas.root"
    outPlotFile = ROOT.TFile(outPlotFileName, "UPDATE")
    canvasGraphRadiusVsHFactor.Write()
    canvasHistRadiusVsHFactor.Write()
    outPlotFile.Close()
    
    del betaFitLowRadius
    del betaFitMidRadius
    del betaFitHighRadius
    del canvasGraphRadiusVsHFactor
    del canvasHistRadiusVsHFactor

    return betaParameters


##############################
# Plot the Z vs. H-Factor distributions for each energy and over all energies in preparation for extracting the Gamma parameters
def PlotsForGammas(alphaParameters, betaParameters):

    plotFileName = baseFileName + "PlotsForGammas.root"
    plotFile = ROOT.TFile(plotFileName, "UPDATE")

    histZVsHFactor = ROOT.TH2D("histZVsHFactor", "H-Factor vs. Z over All Energies; Z, mm; H-Factor", 155, -6200.0, 6200.0, 150, 0.0, 1.5)
    histZVsHFactor.SetStats(0)
    ROOT.gStyle.SetPalette(1)
    allHFactors, allZ = [], []

    for energy in energies:
        histNameSingleEnergyZVsHFactor = "histSingleEnergyZVsHFactor_" + str(int(energy * 1000)) + "keV"
        histSingleEnergyZVsHFactor = ROOT.TH2D(histNameSingleEnergyZVsHFactor, "H-Factor vs. Z for a Single Energy; Z, mm; H-Factor", 155, -6200.0, 6200.0, 150, 0.0, 1.5)
        histSingleEnergyZVsHFactor.SetStats(0)
        ROOT.gStyle.SetPalette(1)
        singleEnergyHFactors, singleEnergyZ = [], []

        for p in range (1, 6):
            fileName = "electrons_" + parameters[2] + "_" + str(int(energy * 1000)) + "keV_" + positionTypes[2] + "_part" + str(p) + ".root"

            for ds, run in rat.dsreader(fileName):
                if ds.GetEVCount() == 0:
                    continue
                calibratedPMTs = ds.GetEV(0).GetCalibratedPMTs()

                radius = ds.GetMC().GetMCParticle(0).GetPosition().Mag()
                zCoord = ds.GetMC().GetMCParticle(0).GetPosition().Z()
				
                Segmentor = rat.utility().GetSegmentor()
                Segmentor.SetNumberOfDivisions(numberOfSegments)
                rawPMTSegmentIDs = Segmentor.GetSegmentIDs()
                rawPMTSegmentPopulations = Segmentor.GetSegmentPopulations()
                hitPMTSegmentPopulations = [0] * len(rawPMTSegmentPopulations)
                for j in range(0, calibratedPMTs.GetCount()):
                    hitPMTSegmentPopulations[rawPMTSegmentIDs[calibratedPMTs.GetPMT(j).GetID()]] += 1

                hValue = 0.0
                for s in range(len(rawPMTSegmentPopulations)):
                    hValue += (rawPMTSegmentPopulations[s] * math.log(1.0 - (float(hitPMTSegmentPopulations[s]) / float(rawPMTSegmentPopulations[s]))))
                hValue *= -1.0
                
                hAtCentre = 0.0
                for p in range(0, numberOfParameters[0]):
                    hAtCentre += (alphaParameters[p] * math.pow(energy, p))
                
                functionOfRadius = 0.0
                if (radius >= fitRangeLow[1]) and (radius < fitRangeHigh[1]):
                    for p in range(0, numberOfParameters[1]):
                        functionOfRadius += (betaParameters[p] * math.pow(radius, p))
                elif ((radius >= fitRangeLow[2]) and (radius < fitRangeHigh[2])):
                    for p in range(0, numberOfParameters[2]):
                        functionOfRadius += (betaParameters[p + numberOfParameters[1]] * math.pow(radius, p))
                elif ((radius >= fitRangeLow[3]) and (radius < fitRangeHigh[3])):
                    for p in range(0, numberOfParameters[3]):
                        functionOfRadius += (betaParameters[p + numberOfParameters[1] + numberOfParameters[2]] * math.pow(radius, p))
                else:
                    continue

                hFactor = hValue / (hAtCentre * functionOfRadius)

                histSingleEnergyZVsHFactor.Fill(zCoord, hFactor)
                singleEnergyZ.append(zCoord)
                singleEnergyHFactors.append(hFactor)
                histZVsHFactor.Fill(zCoord, hFactor)
                allZ.append(zCoord)
                allHFactors.append(hFactor)

        graphSingleEnergyZVsHFactor = ROOT.TGraph(len(singleEnergyZ), array('d', singleEnergyZ), array('d', singleEnergyHFactors))
        graphSingleEnergyZVsHFactor.SetMarkerStyle(20)
        graphSingleEnergyZVsHFactor.SetMarkerSize(0.5)
        graphSingleEnergyZVsHFactor.SetMarkerColor(ROOT.kRed)
        graphSingleEnergyZVsHFactor.SetTitle("H-Factor vs. Z for a Single Energy")
        graphSingleEnergyZVsHFactor.GetXaxis().SetTitle("Z, mm")
        graphSingleEnergyZVsHFactor.GetXaxis().SetRangeUser(-6200.0, 6200.0)
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
    graphZVsHFactor.GetXaxis().SetRangeUser(-6200.0, 6200.0)
    graphZVsHFactor.GetYaxis().SetTitle("H-Factor")
    graphZVsHFactor.GetYaxis().SetRangeUser(0.0, 1.5)
    graphZVsHFactor.SetName("graphZVsHFactor")

    plotFile.cd()
    graphZVsHFactor.Write()
    histZVsHFactor.Write()

    plotFile.Close()


##############################
# Extract the Gamma parameters from the previously saved H-Parameter distributions ("All Energies" plots only)
def ExtractGammaParameters():

    inPlotFileName = baseFileName + "PlotsForGammas.root"
    inPlotFile = ROOT.TFile(inPlotFileName, "READ")
    graphAllEnergiesZVsHFactor = inPlotFile.Get("graphZVsHFactor")
    histAllEnergiesZVsHFactor = inPlotFile.Get("histZVsHFactor")

    gammaFunction = "pol" + str( int(numberOfParameters[4] - 1) )
    gammaFit = ROOT.TF1(gammaFunction, gammaFunction, fitRangeLow[4], fitRangeHigh[4])
    gammaFit.FixParameter(0, 1.0)
    graphAllEnergiesZVsHFactor.Fit(gammaFit, "R")

    gammaParameters = []
    for parameter in range(0, numberOfParameters[4]):
        gammaParameters.append(gammaFit.GetParameter(parameter))

    canvasGraphZVsHFactor = ROOT.TCanvas("canvasGraphZVsHFactor", "canvasGraphZVsHFactor", 1500, 900)
    graphAllEnergiesZVsHFactor.Draw("AP")
    gammaFit.Draw("L SAME")
    
    canvasHistZVsHFactor = ROOT.TCanvas("canvasHistZVsHFactor", "canvasHistZVsHFactor", 1500, 900)
    histAllEnergiesZVsHFactor.Draw("COLZ")
    gammaFit.Draw("L SAME")
	
    outPlotFileName = baseFileName + "ExtractGammas.root"
    outPlotFile = ROOT.TFile(outPlotFileName, "UPDATE")
    canvasGraphZVsHFactor.Write()
    canvasHistZVsHFactor.Write()
    outPlotFile.Close()
    
    del gammaFit
    del canvasGraphZVsHFactor
    del canvasHistZVsHFactor

    return gammaParameters


##############################
