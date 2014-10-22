#!usr/bin/env python
import ROOT, rat, math
# Secondary functions and user-defined Values for the Seeded Classifier Coordinator
# Author K Majumdar - 14/05/2012 <Krishanu.Majumdar@physics.ox.ac.uk>
#        K Majumdar - 08/09/2014 - Cleanup of Coordinators for new DS

Energies = [5.000, 0.500]
Particles = ["alphas", "electrons"]
# the alphas must be generated with 10 times the energy of the electrons, in order to be detected with the same Nhits (this is due to alpha-quenching)

maxRadius = 5000.0
maxTimeResid = 300.0


# Produce the overall histogram of the ratio of PMTs in the Prompt Region to total PMTs in the event, for the specified rootfile
def ProduceRatioHistogram(infileName, t1, t2):
	
    Histogram = ROOT.TH1D(infileName, infileName + ": Prompt PMTs/Total PMTs in Event", 100, 0.0, 1.0)

    effectiveVelocity = rat.utility().GetEffectiveVelocity()
    lightPath = rat.utility().GetLightPathCalculator()
    pmtInfo = rat.utility().GetPMTInfo()

    for ds, run in rat.dsreader(infileName):
        if ds.GetEVCount() == 0:
            continue
        ev = ds.GetEV(0)

        vertPos = ev.GetFitResult("scintFitter").GetVertex(0).GetPosition()
        if vertPos.Mag() > maxRadius:
            continue
        vertTime = ev.GetFitResult("scintFitter").GetVertex(0).GetTime()
		
        calibratedPMTs = ev.GetCalPMTs()
        peak = total = 0.0
		
        for j in range(0, calibratedPMTs.GetCount()):
            pmtPos = pmtInfo.GetPosition(calibratedPMTs.GetPMT(j).GetID())
            pmtTime = calibratedPMTs.GetPMT(j).GetTime()

            lightPath.CalcByPosition(vertPos, pmtPos)
            distInScint = lightPath.GetDistInScint()
            distInAV = lightPath.GetDistInAV()
            distInWater = lightPath.GetDistInWater()
            flightTime = effectiveVelocity.CalcByDistance(distInScint, distInAV, distInWater)
            timeResid = pmtTime - flightTime - vertTime
			
            if timeResid > t1 and timeResid < t2:
                peak += 1.0
            if timeResid > t1 and timeResid < maxTimeResid:
                total += 1.0

        ratio = peak / total
        Histogram.Fill(ratio)

    return Histogram


# Calculate the Bhattacharya Coefficient: a measure of the overlap between the alpha and electron histograms (1 and 2 respectively)
def BhattacharyaCoeff(histogram1, histogram2):
	
	bhatta = 0.0
	
	for bin in range(1, histogram1.GetNbinsX()):
		sum = math.sqrt(histogram1.GetBinContent(bin) * histogram2.GetBinContent(bin))
		bhatta += sum

	return bhatta 

