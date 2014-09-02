#!usr/bin/env python
import ROOT, rat, math
# Secondary functions and user-defined Values for the Seeded Classifier Coordinator
# Author K Majumdar - 14/05/2012 <Krishanu.Majumdar@physics.ox.ac.uk>


Energies = [5.000, 0.500]
Particles = ["alphas", "electrons"]
# the alphas must be generated with 10 times the energy of the electrons, in order to be detected with the same Nhits (this is due to alpha-quenching)


def ProduceRatioHistogram(filename, t1, t2):
	# produces the overall histogram of the ratio of PMTs in the Prompt Region to total PMTs in the event, for the specified rootfile
	Histogram = ROOT.TH1D(filename, filename + ": Prompt PMTs/Total PMTs in Event", 100, 0.0, 1.0)

        dsUtility = RAT.DU.Utility.Get()
        effectiveVelocity = dsUtility.GetEffectiveVelocity()
        lightPath = dsUtility.GetLightPathCalculator()
        pmtInfo = dsUtility.GetPMTInfo()

	for ds, run in rat.dsreader(filename):

		if ds.GetEVCount() == 0:
			continue
		ev = ds.GetEV(0)

		vertPos = ev.GetFitResult("scintFitter").GetVertex(0).GetPosition()
		if vertPos.Mag() > 5000:
			continue
		vertTime = ev.GetFitResult("scintFitter").GetVertex(0).GetTime()
		peak = total = 0.0
		
		for j in range(0, ev.GetCalPMTs().GetCount()):
			pmt = ev.GetCalPMTs().GetPMT(j)
			pmtPos = pmtInfo.GetPosition(pmt.GetID())
			pmtTime = pmt.GetTime()

			lightPath.CalcByPosition(vertPos, pmtPos)
                        distInScint = lightPath.GetDistInScint()
                        distInAv = lightPath.GetDistInAV()
                        distInWater = lightPath.GetDistInWater()
			flightTime = effectiveVelocity.CalcByDistance(distInScint, distInAV, distInWater)
			timeresid = pmtTime - flightTime - vertTime
			
			if timeresid > t1 and timeresid < t2:
				peak += 1.0
			if timeresid > t1 and timeresid < 300:
				total += 1.0

		ratio = peak / total
		Histogram.Fill(ratio)

	return Histogram


def BhattacharyaCoeff(histogram1, histogram2):
	# calculates the Bhattacharya Coefficient, a measure of the overlap, of the alpha and electron histograms (1 and 2 respectively)
	bhatta = 0.0
	
	for bin in range(1, histogram1.GetNbinsX()):
		sum = math.sqrt(histogram1.GetBinContent(bin) * histogram2.GetBinContent(bin))
		bhatta += sum

	return bhatta 
