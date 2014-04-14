#!usr/bin/env python
import ROOT, rat, math
# Secondary functions and user-defined Values for the Unseeded Classifier Coordinator
# Author K Majumdar - 11/05/2012 <Krishanu.Majumdar@physics.ox.ac.uk>


Energies = [5.000, 0.500]
Particles = ["alphas", "electrons"]
# the alphas must be generated with 10 times the energy of the electrons, in order to be detected with the same Nhits (this is due to alpha-quenching)
TailFracs = [0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25, 0.27, 0.29, 0.31, 0.33, 0.35, 0.37, 0.39, 0.41, 0.43, 0.45, 0.47, 0.49, 0.51]


def ProduceRatioHistogram(filename, tailfrac):
	# produces the overall histogram of the ratio of PMTs in the Trigger Time Tail to total PMTs in the event, for the specified rootfile
	Histogram = ROOT.TH1D(filename, filename + ": Trigger Times Tail PMTs/Total PMTs in Event", 100, 0.0, 1.0)

	for ds, run in rat.dsreader(filename):
		if ds.GetEVCount() == 0:
			continue
		ev = ds.GetEV(0)

		tail = total = 0.0
		lowlimit, highlimit = 1000.0, 0.0
		temp = []

		for j in range(0, ev.GetCalibratedPMTs.GetCount()):
			pmtTime = ev.GetCalibratedPMTsGetPMT(j).GetTime()
			temp.append(pmtTime)

			if pmtTime < lowlimit and pmtTime > 250:
				lowlimit = pmtTime
			if pmtTime > highlimit and pmtTime < 500:
				highlimit = pmtTime

		totalwidth = highlimit - lowlimit
		tailstart = highlimit - (tailfrac * totalwidth)

		for time in temp:
			if time >= tailstart and time < highlimit:
				tail += 1.0
			if time >= lowlimit and time < highlimit:
				total += 1.0

		ratio = tail / total
		Histogram.Fill(ratio)

	return Histogram


def BhattacharyaCoeff(histogram1, histogram2):
	# calculates the Bhattacharya Coefficient, a measure of the overlap, of the alpha and electron histograms (1 and 2 respectively)
	bhatta = 0.0
	
	for bin in range(1, histogram1.GetNbinsX()):
		sum = math.sqrt(histogram1.GetBinContent(bin) * histogram2.GetBinContent(bin))
		bhatta += sum

	return bhatta 
