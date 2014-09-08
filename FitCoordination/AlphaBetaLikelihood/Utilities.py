#!usr/bin/env python
import ROOT, rat, sys
# Secondary functions and user-defined Values for the AlphaBetaLikelihood Classifier Coordinator
# Author E Marzece - 13/03/2014 <marzece@sas.upenn.edu>
#        K Majumdar - 08/09/2014 - Cleanup of Coordinators for new DS

ParticleNames = {"212":["Bi212", "Po212", "Te130"], "214":["Bi214", "Po214", "Te130"]}
PulseDescriptions = ["wPSD", "NoPSD", "SeansPSD"]
ParticlePulseDict = {"Bi212":[""], "Bi214":[""], "Te130":[""], "Po212":PulseDescriptions, "Po214":PulseDescriptions}
PulseTimeConstants = {"":"", PulseDescriptions[0]:"", PulseDescriptions[1]:"-4.6d, -18d, -156d,", PulseDescriptions[2]:"-3.2d,-18d,-172d,"}
PulseTimeRatios = {"":"", PulseDescriptions[0]:"", PulseDescriptions[1]:"0.71d, 0.22d, 0.07d,", PulseDescriptions[2]:"0.61d,0.28d,0.11d,"}


# Create a normalized time residual PDF for a given rootfile
def ProduceTimeResidualPDF(infileName):

    Histogram = ROOT.TH1D(infileName, "", 1400, -300, 1000)

    effectiveVelocity = rat.utility().GetEffectiveVelocity()
    lightPath = rat.utility().GetLightPathCalculator()
    pmtInfo = rat.utility().GetPMTInfo()
		
    for ds,run in rat.dsreader(infileName):

        if ds.GetEVCount() > 0:
            
            mcParticle = ds.GetMC().GetMCParticle(0);
            mcPos = mcParticle.GetPosition();
            mcTime = mcParticle.GetTime()
			
            ev = ds.GetEV(0)
            vertPos = ev.GetFitResult("scintFitter").GetVertex(0).GetPosition()
            vertTime = ev.GetFitResult("scintFitter").GetVertex(0).GetTime()

            calibratedPMTs = ev.GetCalPMTs()

            for iPMT in range(0, calibratedPMTs.GetCount()):
                pmtPos = pmtInfo.GetPosition(calibratedPMTs.GetPMT(iPMT).GetID())
                pmtTime = calibratedPMTs.GetPMT(iPMT).GetTime()
				
                lightPath.CalcByPosition(vertPos, pmtPos)
                distInScint = lightPath.GetDistInScint()
                distInAV = lightPath.GetDistInAV()
                distInWater = lightPath.GetDistInWater()
                flightTime = effectiveVelocity.CalcByDistance(distInScint, distInAV, distInWater)
                timeResidual = pmtTime - flightTime - vertTime
				
                Histogram.Fill(timeResidual)
				
    Histogram.Scale(1.0 / Histogram.Integral())

    pdfVector = []
    for i in range(1, Histogram.GetNbinsX()):
        pdfVector.append(Histogram.GetBinContent(i))
		
    return pdfVector
	

# Output 3 PDFs in the format that is required for the CLASSIFIER_ALPHA_BETA_LIKELIHOOD.ratdb file
# Input pdfList must be in the following order: [Bi, Po, Te130]
def OutputFileChunk(pdfList, particle, material, description, f):

    pdfNames = ["beta_probability", "alpha_probability", "two_beta_probability"]

    f.write("{\n")
    f.write("name: \"LIKELIHOOD_Bi" + particle + "_" + description + "\",\n")
    f.write("index: \"" + material + "\",\n")
    f.write("valid_begin: [0, 0],\n")
    f.write("valid_end: [0, 0],\n")
    f.write("\n")
	
    f.write("times: [")
    for time in range(-300, 1000):
       f.write(str(time) + "d, ")
    f.write("],\n")

    for pdfIndex, pdf in enumerate(pdfList):
        f.write(str(pdfNames[pdfIndex]) + ": [")

        for pdfIndex, pdfValue in enumerate(pdf):
            f.write(str(pdfValue) + "d, ")
        f.write("],\n")

    f.write("}\n")

