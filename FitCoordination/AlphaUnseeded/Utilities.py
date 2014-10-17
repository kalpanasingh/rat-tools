#!usr/bin/env python
import ROOT, rat, math
# Secondary functions and user-defined Values for the Unseeded Classifier Coordinator
# Author K Majumdar - 11/05/2012 <Krishanu.Majumdar@physics.ox.ac.uk>
#        K Majumdar - 08/09/2014 - Cleanup of Coordinators for new DS

Energies = [5.000, 0.500]
Particles = ["alphas", "electrons"]
# the alphas must be generated with 10 times the energy of the electrons, in order to be detected with the same Nhits (this is due to alpha-quenching)

TailFracs = [0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25, 0.27, 0.29, 0.31, 0.33, 0.35, 0.37, 0.39, 0.41, 0.43, 0.45, 0.47, 0.49, 0.51]
minTimeResid = 250.0
maxTimeResid = 500.0


# Produce the overall histogram of the ratio of PMTs in the Trigger Time Tail to total PMTs in the event, for the specified rootfile
def ProduceRatioHistogram(inFileName, tailFraction):
	
    Histogram = ROOT.TH1D(inFileName, inFileName + ": Trigger Times Tail PMTs/Total PMTs in Event", 100, 0.0, 1.0)

    for ds, run in rat.dsreader(inFileName):
        if ds.GetEVCount() == 0:
            continue
        ev = ds.GetEV(0)

        tail = total = 0.0
        lowLimit = 1000.0
        highLimit = 0.0
        tempList = []

        for j in range(0, ev.GetCalPMTs().GetCount()):
            pmtTime = ev.GetCalPMTs().GetPMT(j).GetTime()
            tempList.append(pmtTime)

            if pmtTime < lowLimit and pmtTime > minTimeResid:
                lowLimit = pmtTime
            if pmtTime > highLimit and pmtTime < maxTimeResid:
                highLimit = pmtTime

        totalWidth = highLimit - lowLimit
        tailStart = highLimit - (tailFraction * totalWidth)

        for time in tempList:
            if time >= tailStart and time < highLimit:
                tail += 1.0
            if time >= lowLimit and time < highLimit:
                total += 1.0

        ratio = tail / total
        Histogram.Fill(ratio)

    return Histogram


# Calculate the Bhattacharya Coefficient: a measure of the overlap between the alpha and electron histograms (1 and 2 respectively)
def BhattacharyaCoeff(histogram1, histogram2):
	
	bhatta = 0.0
	
	for bin in range(1, histogram1.GetNbinsX()):
		sum = math.sqrt(histogram1.GetBinContent(bin) * histogram2.GetBinContent(bin))
		bhatta += sum

	return bhatta

