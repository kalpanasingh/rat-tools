#!usr/bin/env python
import ROOT, rat, sys
from numpy import arange
# Secondary functions and user-defined Values for the AlphaBetaLikelihood Classifier Coordinator
# Author E Marzece - 13/03/2014 <marzece@sas.upenn.edu>
#        K Majumdar - 08/09/2014 - Cleanup of Coordinators for new DS

ParticleNames = {"212":["Bi212", "Po212", "Te130"], "214":["Bi214", "Po214", "Te130"]}
PulseDescriptions = ["wPSD", "NoPSD"]
ParticlePulseDict = {"Bi212":[""], "Bi214":[""], "Te130":[""], "Po212":PulseDescriptions, "Po214":PulseDescriptions}
PulseTimeConstants = {"":"", PulseDescriptions[0]:"", PulseDescriptions[1]:"-4.6d, -18d, -156d,"}
PulseTimeRatios = {"":"", PulseDescriptions[0]:"", PulseDescriptions[1]:"0.71d, 0.22d, 0.07d,"}

#These values were chosen to be around the ROI
#They loosely determine which energies are ROI-ish
LooseROI_upperBound = 2.8
LooseROI_lowerBound = 2.2
#The following define the range and step size of the TimeResidual pdfs
TimeRes_upperBound = 1000.0
TimeRes_lowerBound = -300.0
TimeRes_stepSize = 1.0;
#The following define the range and step size of the Energy Ratio pdfs
EnergyRatio_upperBound = 10.0
EnergyRatio_lowerBound =0.0
EnergyRatio_stepSize = 0.1


#Returns a normalized distribution of times residual and a list of all the energies in the file
def ProduceTimeResAndEnergyPDF(infileName):

    energyList=[];
    nbins = (TimeRes_upperBound - TimeRes_lowerBound)/TimeRes_stepSize
    Histogram = ROOT.TH1D(infileName,"",nbins,TimeRes_lowerBound,TimeRes_upperBound)

    effectiveVelocity = rat.utility().GetEffectiveVelocity()
    lightPath = rat.utility().GetLightPathCalculator()
    pmtInfo = rat.utility().GetPMTInfo()

    for ds,run in rat.dsreader(infileName):

        if ds.GetEVCount() > 0:
            
            mcParticle = ds.GetMC().GetMCParticle(0);
            mcPos = mcParticle.GetPosition();
            mcTime = mcParticle.GetTime()

            ev = ds.GetEV(0)

            if not ev.FitResultExists("scintFitter"):
                continue
            if not ev.GetFitResult("scintFitter").GetValid():
                continue
            if not ev.GetFitResult("scintFitter").GetVertex(0).ContainsPosition():
                continue

            fitVertex = ev.GetFitResult("scintFitter").GetVertex(0);
            vertPos = fitVertex.GetPosition()
            vertTime = fitVertex.GetTime()
            if (fitVertex.ContainsEnergy()):
                energyList.append(fitVertex.GetEnergy())

            calibratedPMTs = ev.GetCalPMTs()

            for iPMT in range(0, calibratedPMTs.GetCount()):
                pmtPos = pmtInfo.GetPosition(calibratedPMTs.GetPMT(iPMT).GetID())
                pmtTime = calibratedPMTs.GetPMT(iPMT).GetTime()

                lightPath.CalcByPosition(vertPos, pmtPos)
                distInScint = lightPath.GetDistInInnerAV()
                distInAV = lightPath.GetDistInAV()
                distInWater = lightPath.GetDistInWater()
                flightTime = effectiveVelocity.CalcByDistance(distInScint, distInAV, distInWater)
                timeResidual = pmtTime - flightTime - vertTime

                Histogram.Fill(timeResidual)

    Histogram.Scale(1.0 / Histogram.Integral())

    pdfVector = []
    for i in range(1, Histogram.GetNbinsX()):
        pdfVector.append(Histogram.GetBinContent(i))
    Histogram.Delete()
    return (pdfVector,energyList)

#Takes two lists of energies and returns a PDF of the ratio of the energies such
#that their sum fall in or around the ROI
def GetEnergyRatio(betaEnergiesList,alphaEnergiesList):
    pdfVector = []
    nbins = (EnergyRatio_upperBound - EnergyRatio_lowerBound)/EnergyRatio_stepSize
    Histogram = ROOT.TH1D("","",nbins,EnergyRatio_lowerBound,EnergyRatio_upperBound)
    #Loop across the 2D space of energies
    #histogram data points that haven't been used and are near the ROI
    for iBeta, betaEnergy in enumerate(betaEnergiesList):
        if(betaEnergy > 0):
            for iAlpha, alphaEnergy in enumerate(alphaEnergiesList):
                energySum = betaEnergy+alphaEnergy
                if(energySum > LooseROI_lowerBound and energySum < LooseROI_upperBound and alphaEnergy>0):
                    Histogram.Fill(betaEnergy/alphaEnergy)
                    #Now make sure that each value is only used once 
                    #This is done by changing the enegies to an unphysical sentinel value
                    betaEnergiesList[iBeta] = -1
                    alphaEnergiesList[iAlpha] = -1
    #Change the histogram into a nicer to use List
    Histogram.Scale(1.0/Histogram.Integral())
    for i in range(1,Histogram.GetNbinsX()):
        pdfVector.append(Histogram.GetBinContent(i))
    Histogram.Delete()
    return pdfVector

# Output 3 PDFs in the format that is required for the CLASSIFIER_ALPHA_BETA_LIKELIHOOD.ratdb file
# Input pdfList must be in the following order: [Bi, Po, Te130]
def OutputFileChunk(pdfList, energyRatioPDF, particle, material, description,f):

    pdfNames = ["beta_probability", "alpha_probability", "two_beta_probability"]

    f.write("{\n")
    f.write("type: \"LIKELIHOOD_Bi" + particle + "_" + description + "\",\n")
    f.write("version: 1\n")
    f.write("index: \"" + material + "\",\n")
    f.write("run_range: [0, 0],\n")
    f.write("pass: 0,\n")
    f.write("production: false,\n")
    f.write("timestamp: \"\",\n")    
    f.write("comment: \"\",\n")    
    f.write("\n")

    #OUTPUT EACH TIME RESIDIUAL DISTRIBUTION  
    f.write("times: [")
    for time in arange(TimeRes_lowerBound,TimeRes_upperBound,TimeRes_stepSize):
       f.write(str(time) + ", ")
    f.write("],\n")

    for pdfIndex, pdf in enumerate(pdfList):
        f.write(str(pdfNames[pdfIndex]) + ": [")

        for pdfIndex, pdfValue in enumerate(pdf):
            f.write(str(pdfValue) + ", ")
        f.write("],\n")

   #OUTPUT ENERGY RATIO VALUES
    f.write("energy_ratio: [")
    for energyRatio in arange(EnergyRatio_lowerBound,EnergyRatio_upperBound,EnergyRatio_stepSize):
       f.write(str(energyRatio)+", ")
    f.write("],\n")
    #OUTPUT ENREGY RATIO PDF VALUES
    f.write("energy_probability: [")
    for energyRatio in energyRatioPDF:
        f.write(str(energyRatio)+", ")
    f.write("],\n")

    f.write("}\n")

