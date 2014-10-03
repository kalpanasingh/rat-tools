import ROOT, rat, sys
from numpy import arange

ParticleNames = {"212":["Bi212","Po212","Te130"],"214":["Bi214","Po214","Te130"]}
PulseDescriptions = ["wPSD","NoPSD","SeansPSD"]
ParticlePulseDict= {"Bi212":[""],"Bi214":[""],"Te130":[""],"Po212":PulseDescriptions,"Po214":PulseDescriptions}
PulseTimeConstants= {"":"",PulseDescriptions[0]:"",PulseDescriptions[1]:"-4.6d, -18d, -156d,",PulseDescriptions[2]:"-3.2d,-18d,-172d,"}
PulseTimeRatios= {"":"",PulseDescriptions[0]:"",PulseDescriptions[1]:"0.71d, 0.22d, 0.07d,",PulseDescriptions[2]:"0.61d,0.28d,0.11d,"}
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
def GetFileInfo(filename):
    energyList=[];
    nbins = (TimeRes_upperBound - TimeRes_lowerBound)/TimeRes_stepSize
    Histogram = ROOT.TH1D(filename,"",nbins,TimeRes_lowerBound,TimeRes_upperBound)
    for ds,run in rat.dsreader(filename):
        groupVelocity = rat.utility().GetGroupVelocity()
        lightPath = rat.utility().GetLightPathCalculator()
        pmtInfo = rat.utility().GetPMTInfo()
        if ds.GetEVCount() > 0:
            ev = ds.GetEV(0)
            rmc = ds.GetMC()
            mcParticle = rmc.GetMCParticle(0);
            mcPos = mcParticle.GetPosition();
            fitTime = mcParticle.GetTime()
            fitVertex = ev.GetFitResult("scintFitter").GetVertex(0)
            fitTime = fitVertex.GetTime()
            if (fitVertex.ContainsEnergy()):
                energyList.append(fitVertex.GetEnergy())
            calPMTs = ev.GetCalPMTs()
            for iPMT in range(0,calPMTs.GetCount()):
                pmt = calPMTs.GetPMT(iPMT)
                pmtPos = pmtInfo.GetPosition(pmt.GetID())
                pmtTime = pmt.GetTime()
                distInScint = ROOT.Double()
                distInAV = ROOT.Double()
                distInWater = ROOT.Double()
                lightPath.CalcByPosition(mcPos,pmtPos)
                distInScint = lightPath.GetDistInScint()
                distInAv = lightPath.GetDistInAV()
                distInWater = lightPath.GetDistInWater()
                flightTime = groupVelocity.CalcByDistance(distInScint,distInAV,distInWater)
                timeResidual = pmtTime - flightTime - fitTime
                Histogram.Fill(timeResidual)
    Histogram.Scale(1.0/Histogram.Integral())
    pdfVector = []
    for i in range(1,Histogram.GetNbinsX()):
        pdfVector.append(Histogram.GetBinContent(i))
    Histogram.Delete()
    return (pdfVector,energyList)
#Takes two lists of energies and returns a PDF of the ratio of those energies whose sum fall in or around the ROI
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
    for i in range(1,Histogram.GetNbinsX()):
        pdfVector.append(Histogram.GetBinContent(i))
    Histogram.Delete()
    return pdfVector 
#Outputs 3 pdfs in the same format as in CLASSIFIER_ALPHA_BETA_LIKELIHOOD.ratdb
def OutputFileChunk(pdfList,energyRatioPDF, options, description,f):#pdfList must be in the follwing order [Bi,Po,Te130]
    pdfNames = ["beta_probability","alpha_probability","two_beta_probability"]
    f.write("{\n")
    f.write("name: \"LIKELIHOOD_Bi"+options.particle+"_"+description+"\",\n")
    f.write("index: \""+options.scintMaterial+"\",\n")
    f.write("valid_begin: [0,0],\n")
    f.write("valid_end: [0,0],\n")
    #OUTPUT EACH TIME RESIDIUAL DISTRIBUTION  
    f.write("times: [")
    for time in arange(TimeRes_lowerBound,TimeRes_upperBound,TimeRes_stepSize):
       f.write(str(time)+"d, ")
    f.write("],\n")
    for pdfIndex,pdf in enumerate(pdfList):
        f.write(str(pdfNames[pdfIndex]) + ": [")
        for pdfIndex,pdfValue in enumerate(pdf):
            f.write(str(pdfValue)+"d, ")
        f.write("],\n")

   #OUTPUT ENERGY RATIO VALUES
    f.write("energy_ratio: [")
    for energyRatio in arange(EnergyRatio_lowerBound,EnergyRatio_upperBound,EnergyRatio_stepSize):
       f.write(str(energyRatio)+"d, ")
    f.write("],\n")
    #OUTPUT ENREGY RATIO PDF VALUES
    f.write("energy_probability: [")
    for energyRatio in energyRatioPDF:
        f.write(str(energyRatio)+"d, ")
    f.write("],\n")
    f.write("}\n")

