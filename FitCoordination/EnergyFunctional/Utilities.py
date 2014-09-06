#!usr/bin/env python
from array import array
import ROOT, rat, math
# Secondary functions and user-defined Values for the Functional Energy Fitter's Coordinator
# Author K Majumdar - 04/09/2014 <Krishanu.Majumdar@physics.ox.ac.uk>

##############################

# List of energies (in MeV) to coordinate the fitter over
energies = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

# List of parameters in the general formula, together with the position information used to simulate the data for each parameter
parameters = ["EnergyCoeffs", "RadiusCoeffs", "ZCoeffs"]
positionTypes = ["point", "plane", "fill"]
positionArgs = ["0.0 0.0 0.0", "0.0 0.0 0.0 0.0 0.0 1.0 6005", "0.0 0.0 0.0"]

# Number of segments in each of phi and theta for the Segmentor (the default in the Segmentor is 10)
numberOfSegments = 10

# Base filename for the output text and root files
baseFileName = "AnalyseData_Results_"

# Information on the fit functions used to extract the parameters
# This is all included here, rather than hard-coded into the functions below, to make it easier to change the functions being used if needed
numberOfEnergyCoeffs = 2
energyFitFunction = "[0]+([1]*x)"
energyFitRange = [0.0, energies[-1]]
numberOfRadiusCoeffs_Low = 3
radiusFitFunction_Low = "[0]+([1]*x)+([2]*x*x)"
radiusFitRange_Low = [0.0, 2000.0]
numberOfRadiusCoeffs_Mid = 4
radiusFitFunction_Mid = "[0]+([1]*x)+([2]*x*x)+([3]*x*x*x)"
radiusFitRange_Mid = [2000.0, 5300.0]
numberOfRadiusCoeffs_High = 3
radiusFitFunction_High = "[0]+([1]*x)+([2]*x*x)"
radiusFitRange_High = [5300.0, 6005.3]
numberOfZCoeffs = 4
zFitFunction = "[0]+([1]*x)+([2]*x*x)+([3]*x*x*x)"
zFitRange = [-6005.3, 6005.3]


##############################
# Plot the H-Parameter distributions for each energy and the mean H-Parameter vs. energy
def PlotsForEnergyCoeffs():

    plotFileName = baseFileName + "PlotsForEnergyCoeffs.root"
    plotFile = ROOT.TFile(plotFileName, "UPDATE")

    meanHValues = []

    for energy in energies:
        singleEnergyHValues = []
        singleEnergyMaxHValue = 0.0

        for p in range (1, 6):
            fileName = "electrons_" + parameters[0] + "_" + str(int(energy * 1000)) + "keV_" + positionTypes[0] + "_part" + str(p) + ".root"

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
        
        gaussFit = ROOT.TF1("gaus", "gaus", 0.0, (singleEnergyMaxHValue * 1.1))
        plotSingleEnergyH.Fit(gaussFit, "RQ")
        meanHValues.append(gaussFit.GetParameter(1))

        plotFile.cd()
        plotSingleEnergyH.Write()

        del plotSingleEnergyH
        del gaussFit

    plotEnergyVsMeanH = ROOT.TGraph(len(energies), array('d', energies), array('d', meanHValues))
    plotEnergyVsMeanH.SetMarkerStyle(20)
    plotEnergyVsMeanH.SetMarkerSize(1.0)
    plotEnergyVsMeanH.SetMarkerColor(ROOT.kRed)
    plotEnergyVsMeanH.SetTitle("Mean H-Value vs. Energy")
    plotEnergyVsMeanH.GetXaxis().SetTitle("Energy, MeV")
    plotEnergyVsMeanH.GetYaxis().SetTitle("Mean H-Value")
    plotEnergyVsMeanH.SetName("plotEnergyVsMeanH")
    plotFile.cd()
    plotEnergyVsMeanH.Write()
	
    plotFile.Close()


##############################
# Extract the energy coefficients from the previously saved mean H-Parameter vs. energy distribution
def ExtractEnergyCoeffs():

    inPlotFileName = baseFileName + "PlotsForEnergyCoeffs.root"
    inPlotFile = ROOT.TFile(inPlotFileName, "READ")
    plotEnergyVsMeanH = inPlotFile.Get("plotEnergyVsMeanH")
    
    energyFit = ROOT.TF1("energyFit", energyFitFunction, energyFitRange[0], energyFitRange[1])
    energyFit.FixParameter(0, 0.0)
    plotEnergyVsMeanH.Fit(energyFit, "R")

    energyCoefficients = []
    for parameter in range(0, numberOfEnergyCoeffs):
        energyCoefficients.append(energyFit.GetParameter(parameter))

    outPlotFileName = baseFileName + "ExtractEnergyCoeffs.root"
    outPlotFile = ROOT.TFile(outPlotFileName, "UPDATE")
    canvasEnergyVsMeanH = ROOT.TCanvas("canvasEnergyVsMeanH", "canvasEnergyVsMeanH", 1500, 900)
    plotEnergyVsMeanH.Draw("AP")
    outPlotFile.cd()
    canvasEnergyVsMeanH.Write()
    outPlotFile.Close()
    
    del plotEnergyVsMeanH
    del energyFit
    del canvasEnergyVsMeanH

    return energyCoefficients


##############################
# Plot the Radius vs. H-Factor distributions for each energy and over all energies
def PlotsForRadiusCoeffs(energyCoefficients):

    plotFileName = baseFileName + "PlotsForRadiusCoeffs.root"
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
                calibratedPMTs = ds.GetEV(0).GetCalPMTs()

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
                for p in range(0, numberOfEnergyCoeffs):
                    hAtCentre += (energyCoefficients[p] * math.pow(energy, p))
                
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
# Extract the radius coefficients from the previously saved all-energies Radius vs. H-Factor distribution
def ExtractRadiusCoeffs():

    inPlotFileName = baseFileName + "PlotsForRadiusCoeffs.root"
    inPlotFile = ROOT.TFile(inPlotFileName, "READ")
    graphAllEnergiesRadiusVsHFactor = inPlotFile.Get("graphRadiusVsHFactor")
    histAllEnergiesRadiusVsHFactor = inPlotFile.Get("histRadiusVsHFactor")

    radiusFitLow = ROOT.TF1("radiusFitLow", radiusFitFunction_Low, radiusFitRange_Low[0], radiusFitRange_Low[1])
    radiusFitLow.FixParameter(0, 1.0)
    graphAllEnergiesRadiusVsHFactor.Fit(radiusFitLow, "R")

    radiusFitMid = ROOT.TF1("radiusFitMid", radiusFitFunction_Mid, radiusFitRange_Mid[0], radiusFitRange_Mid[1])
    graphAllEnergiesRadiusVsHFactor.Fit(radiusFitMid, "R")

    radiusFitHigh = ROOT.TF1("radiusFitHigh", radiusFitFunction_High, radiusFitRange_High[0], radiusFitRange_High[1])
    graphAllEnergiesRadiusVsHFactor.Fit(radiusFitHigh, "R")

    radiusCoefficients = []
    for parameter in range(0, numberOfRadiusCoeffs_Low):
        radiusCoefficients.append(radiusFitLow.GetParameter(parameter))
    for parameter in range(0, numberOfRadiusCoeffs_Mid):
        radiusCoefficients.append(radiusFitMid.GetParameter(parameter))
    for parameter in range(0, numberOfRadiusCoeffs_High):
        radiusCoefficients.append(radiusFitHigh.GetParameter(parameter))

    canvasGraphRadiusVsHFactor = ROOT.TCanvas("canvasGraphRadiusVsHFactor", "canvasGraphRadiusVsHFactor", 1500, 900)
    graphAllEnergiesRadiusVsHFactor.Draw("AP")
    radiusFitLow.Draw("L SAME")
    radiusFitMid.Draw("L SAME")
    radiusFitHigh.Draw("L SAME")
    
    canvasHistRadiusVsHFactor = ROOT.TCanvas("canvasHistRadiusVsHFactor", "canvasHistRadiusVsHFactor", 1500, 900)
    histAllEnergiesRadiusVsHFactor.Draw("COLZ")
    radiusFitLow.Draw("L SAME")
    radiusFitMid.Draw("L SAME")
    radiusFitHigh.Draw("L SAME")
	
    outPlotFileName = baseFileName + "ExtractRadiusCoeffs.root"
    outPlotFile = ROOT.TFile(outPlotFileName, "UPDATE")
    canvasGraphRadiusVsHFactor.Write()
    canvasHistRadiusVsHFactor.Write()
    outPlotFile.Close()
    
    del radiusFitLow
    del radiusFitMid
    del radiusFitHigh
    del canvasGraphRadiusVsHFactor
    del canvasHistRadiusVsHFactor

    return radiusCoefficients


##############################
# Plot the Z vs. H-Factor distributions for each energy and over all energies
def PlotsForZCoeffs(energyCoefficients, radiusCoefficients):

    plotFileName = baseFileName + "PlotsForZCoeffs.root"
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
                calibratedPMTs = ds.GetEV(0).GetCalPMTs()

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
                for p in range(0, numberOfEnergyCoeffs):
                    hAtCentre += (energyCoefficients[p] * math.pow(energy, p))
                
                functionOfRadius = 0.0
                if ((radius >= radiusFitRange_Low[0]) and (radius < radiusFitRange_Low[1])):
                    for p in range(0, numberOfRadiusCoeffs_Low):
                        functionOfRadius += (radiusCoefficients[p] * math.pow(radius, p))
                elif ((radius >= radiusFitRange_Mid[0]) and (radius < radiusFitRange_Mid[1])):
                    for p in range(0, numberOfRadiusCoeffs_Mid):
                        functionOfRadius += (radiusCoefficients[p + numberOfRadiusCoeffs_Low] * math.pow(radius, p))
                elif ((radius >= radiusFitRange_High[0]) and (radius < radiusFitRange_High[1])):
                    for p in range(0, numberOfRadiusCoeffs_High):
                        functionOfRadius += (radiusCoefficients[p + numberOfRadiusCoeffs_Low + numberOfRadiusCoeffs_Mid] * math.pow(radius, p))
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
# Extract the Gamma parameters from the previously saved all-energies Z vs. H-Factor distribution
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
