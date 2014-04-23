#!usr/bin/env python
from array import array
import ROOT, rat, math
# Secondary functions and user-defined Values for the Functional Energy Fitter's Coordinator
# Author K Majumdar - 23/04/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


energies = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

parameters = ["Alpha", "Beta", "Gamma"]
positionTypes = ["point", "plane", "fill"]
positionArgs = ["0.0 0.0 0.0", "0.0 0.0 0.0 0.0 0.0 1.0 6005", "0.0 0.0 0.0"]

envrnLoc = ""
currentLoc = ""


# Calculate the Alpha parameters
def CalculateAlphas():
    meanHParameters = []

    for energy in energies:
        singleEnergyHParameters = []
        maxHParameter = 0.0

        for p in range (1, 6):
            fileName = "electrons_" + parameters[0] + "_" + str(int(energy * 1000)) + "keV_" + positionTypes[0] + "_part" + str(p) + ".root"

            Segmentor = rat.utility().GetSegmentor()
            rawPMTSegmentIDs = Segmentor.GetSegmentIDs()
            rawPMTSegmentPopulations = Segmentor.GetSegmentPopulations()

            for ds, run in rat.dsreader(fileName):
                if ds.GetEVCount() == 0:
                    continue
                calibratedPMTs = ds.GetEV(0).GetCalibratedPMTs()

                hitPMTSegmentPopulations = [0] * len(rawPMTSegmentPopulations)
                for j in range(0, calibratedPMTs.GetCount()):
                    hitPMTSegmentPopulations[rawPMTSegmentIDs[calibratedPMTs.GetPMT(j).GetID()]] += 1

                hParameter = 0.0
                for s in range(len(rawPMTSegmentPopulations)):
                    hParameter += (rawPMTSegmentPopulations[s] * math.log(1.0 - (float(hitPMTSegmentPopulations[s]) / float(rawPMTSegmentPopulations[s]))))
                hParameter *= -1.0
                
                singleEnergyHParameters.append(hParameter)
                if hParameter > maxHParameter:
                    maxHParameter = hParameter

        singleEnergyHPlot = ROOT.TH1D("singleEnergyHPlot", "singleEnergyHPlot", 100, 0.0, (maxHParameter * 1.1))
        for h in singleEnergyHParameters:
            singleEnergyHPlot.Fill(h)
        gaussFit = ROOT.TF1("gaus", "gaus", 0.0, (maxHParameter * 1.1))
        singleEnergyHPlot.Fit(gaussFit, "RQ")
        meanHParameters.append(gaussFit.GetParameter(1))

    hParametersVsEnergy = ROOT.TGraph(len(energies), array('d', energies), array('d', meanHParameters))
    alphaFit = ROOT.TF1("pol1", "pol1", 0, energies[-1])
    hParametersVsEnergy.Fit(alphaFit, "RQ")

    alphaParameters = []
    alphaParameters.append(alphaFit.GetParameter(0))
    alphaParameters.append(alphaFit.GetParameter(1))

    return alphaParameters


# Calculate the Beta parameters in both the Near- and Far-AV regions of the detector using the previously calculated Alpha parameters
def CalculateBetas(alphaParameters):
    totalBeta0FarAV, totalBeta1FarAV, totalBeta2FarAV, totalBeta0NearAV, totalBeta1NearAV, totalBeta2NearAV = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    for energy in energies:
        singleEnergyHFactors, singleEnergyRecoRadii = [], []
        maxRecoRadius = 0.0

        for p in range (1, 6):
            fileName = "electrons_" + parameters[1] + "_" + str(int(energy * 1000)) + "keV_" + positionTypes[1] + "_part" + str(p) + ".root"

            Segmentor = rat.utility().GetSegmentor()
            rawPMTSegmentIDs = Segmentor.GetSegmentIDs()
            rawPMTSegmentPopulations = Segmentor.GetSegmentPopulations()

            for ds, run in rat.dsreader(fileName):
                if ds.GetEVCount() == 0:
                    continue
                recoRadius = ds.GetEV(0).GetFitResult("scintFitter").GetVertex(0).GetPosition().Mag()
                calibratedPMTs = ds.GetEV(0).GetCalibratedPMTs()

                hitPMTSegmentPopulations = [0] * len(rawPMTSegmentPopulations)
                for j in range(0, calibratedPMTs.GetCount()):
                    hitPMTSegmentPopulations[rawPMTSegmentIDs[calibratedPMTs.GetPMT(j).GetID()]] += 1

                hParameter = 0.0
                for s in range(len(rawPMTSegmentPopulations)):
                    hParameter += (rawPMTSegmentPopulations[s] * math.log(1.0 - (float(hitPMTSegmentPopulations[s]) / float(rawPMTSegmentPopulations[s]))))
                hParameter *= -1.0
                
                hParameterAtCentre = alphaParameters[0] + (alphaParameters[1] * energy)
                
                hFactor = hParameter / hParameterAtCentre
                singleEnergyHFactors.append(hFactor)
                singleEnergyRecoRadii.append(recoRadius)
                if recoRadius > maxRecoRadius:
                    maxRecoRadius = recoRadius

        singleEnergyHFactorVsRadius = ROOT.TGraph(len(singleEnergyRecoRadii), array('d', singleEnergyRecoRadii), array('d', singleEnergyHFactors))
        farAVFit = ROOT.TF1("pol2", "pol2", 0.0, 5350.0)
        singleEnergyHFactorVsRadius.Fit(farAVFit, "RQ")
        totalBeta0FarAV += farAVFit.GetParameter(0)
        totalBeta1FarAV += farAVFit.GetParameter(1)
        totalBeta2FarAV += farAVFit.GetParameter(2)
        nearAVFit = ROOT.TF1("pol2", "pol2", 5350.0, maxRecoRadius)
        singleEnergyHFactorVsRadius.Fit(nearAVFit, "RQ")
        totalBeta0NearAV += nearAVFit.GetParameter(0)
        totalBeta1NearAV += nearAVFit.GetParameter(1)
        totalBeta2NearAV += nearAVFit.GetParameter(2)

    betaParameters = []
    betaParameters.append(totalBeta0FarAV / float(len(energies)))
    betaParameters.append(totalBeta1FarAV / float(len(energies)))
    betaParameters.append(totalBeta2FarAV / float(len(energies)))
    betaParameters.append(totalBeta0NearAV / float(len(energies)))
    betaParameters.append(totalBeta1NearAV / float(len(energies)))
    betaParameters.append(totalBeta2NearAV / float(len(energies)))
	
    return betaParameters


# Calculate the Gamma parameters in both the Near- and Far-Neck regions of the detector using the previously calculated Alpha and Beta parameters
# As of this version, the neck itself is NOT parametrised yet
def CalculateGammas(alphaParameters, betaParameters):
    totalGamma0FarNeck, totalGamma1FarNeck, totalGamma0NearNeck, totalGamma1NearNeck = 0.0, 0.0, 0.0, 0.0

    for energy in energies:
        singleEnergyHFactors, singleEnergyRecoZ = [], []
        
        for p in range (1, 6):
            fileName = "electrons_" + parameters[2] + "_" + str(int(energy * 1000)) + "keV_" + positionTypes[2] + "_part" + str(p) + ".root"

            Segmentor = rat.utility().GetSegmentor()
            rawPMTSegmentIDs = Segmentor.GetSegmentIDs()
            rawPMTSegmentPopulations = Segmentor.GetSegmentPopulations()

            for ds, run in rat.dsreader(fileName):
                if ds.GetEVCount() == 0:
                    continue
                recoRadius = ds.GetEV(0).GetFitResult("scintFitter").GetVertex(0).GetPosition().Mag()
                recoZ = ds.GetEV(0).GetFitResult("scintFitter").GetVertex(0).GetPosition().Z()
                calibratedPMTs = ds.GetEV(0).GetCalibratedPMTs()
				
                hitPMTSegmentPopulations = [0] * len(rawPMTSegmentPopulations)
                for j in range(0, calibratedPMTs.GetCount()):
                    hitPMTSegmentPopulations[rawPMTSegmentIDs[calibratedPMTs.GetPMT(j).GetID()]] += 1

                hParameter = 0.0
                for s in range(len(rawPMTSegmentPopulations)):
                    hParameter += (rawPMTSegmentPopulations[s] * math.log(1.0 - (float(hitPMTSegmentPopulations[s]) / float(rawPMTSegmentPopulations[s]))))
                hParameter *= -1.0
                
                hParameterAtCentre = alphaParameters[0] + (alphaParameters[1] * energy)

                functionOfRadius = 0.0
                if recoRadius <= 5350.0:
                    functionOfRadius = betaParameters[0] + (betaParameters[1] * recoRadius) + (betaParameters[2] * recoRadius * recoRadius)
                else:
                    functionOfRadius = betaParameters[3] + (betaParameters[4] * recoRadius) + (betaParameters[5] * recoRadius * recoRadius)
                
                hFactor = hParameter / (hParameterAtCentre * functionOfRadius)
                singleEnergyHFactors.append(hFactor)
                singleEnergyRecoZ.append(recoZ)

        singleEnergyHFactorVsZ = ROOT.TGraph(len(singleEnergyRecoZ), array('d', singleEnergyRecoZ), array('d', singleEnergyHFactors))
        farNeckFit = ROOT.TF1("pol1", "pol1", -6005.0, 5000.0)
        singleEnergyHFactorVsZ.Fit(farNeckFit, "RQ")
        totalGamma0FarNeck += farNeckFit.GetParameter(0)
        totalGamma1FarNeck += farNeckFit.GetParameter(1)
        nearNeckFit = ROOT.TF1("pol1", "pol1", 5000.0, 6005.0)
        singleEnergyHFactorVsZ.Fit(nearNeckFit, "RQ")
        totalGamma0NearNeck += nearNeckFit.GetParameter(0)
        totalGamma1NearNeck += nearNeckFit.GetParameter(1)

    gammaParameters = []
    gammaParameters.append(totalGamma0FarNeck / float(len(energies)))
    gammaParameters.append(totalGamma1FarNeck / float(len(energies)))
    gammaParameters.append(totalGamma0NearNeck / float(len(energies)))
    gammaParameters.append(totalGamma1NearNeck / float(len(energies)))
    
    return gammaParameters

