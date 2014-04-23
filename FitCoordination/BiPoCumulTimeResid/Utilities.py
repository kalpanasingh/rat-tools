#!usr/bin/env python
import ROOT, rat, math
# Secondary functions and user-defined Values for the BiPoCumulTimeResid Coordinator
# Author K Majumdar - 23/04/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


envronLoc = ""
currentLoc = ""

minTimeResid = -10.0
maxTimeResid = 400.0
fidVolLow = 0.0
fidVolHigh = 3500.0


def GetEnergyWindow(filename, fidVolLow, fidVolHigh):
	# returns a vector containing the lower and upper bounds of the energy region of interest (mean reco.energy -/+ 1 sigma)
	Histogram = ROOT.TH1D("recoEnergy", "recoEnergy", 100, 0.0, 5.0)

	for ds, run in rat.dsreader(filename):
	    if ds.GetEVCount() == 0:
	        continue
	    ev = ds.GetEV(0)

	    vertPos = ev.GetFitResult("scintFitter").GetVertex(0).GetPosition()
	    if (vertPos.Mag() < fidVolLow) or (vertPos.Mag() >= fidVolHigh):
	        continue
	    vertEnergy = ev.GetFitResult("scintFitter").GetVertex(0).GetEnergy()
	    Histogram.Fill(vertEnergy)

	gaussFit = ROOT.TF1("gaus", "gaus", 0.0, 5.0)
	Histogram.Fit(gaussFit, "RQ")
	lowEnergy = gaussFit.GetParameter(1) - gaussFit.GetParameter(2)
	highEnergy = gaussFit.GetParameter(1) + gaussFit.GetParameter(2)

	energyWindow = [lowEnergy, highEnergy]
	return energyWindow


def GetCDFVector(filename, fidVolLow, fidVolHigh, energyLow, energyHigh, minTimeResid, maxTimeResid):
	# returns a vector containing the normalised cumulative time residuals over many events

	numbOfBins = int(math.fabs(minTimeResid) + math.fabs(maxTimeResid))
	numEvents = 0.0
	cumuHist = ROOT.TH1D("cumuHist", "cumuHist", numbOfBins, minTimeResid, maxTimeResid)
	
	for ds, run in rat.dsreader(filename):
	    groupVelocity = rat.utility().GetGroupVelocity()
	    lightPath = rat.utility().GetLightPath()
	    pmtInfo = rat.utility().GetPMTInfo()
	
	    if ds.GetEVCount() == 0:
	        continue
	    ev = ds.GetEV(0)

	    vertPos = ev.GetFitResult("scintFitter").GetVertex(0).GetPosition()
	    if (vertPos.Mag() < fidVolLow) or (vertPos.Mag() >= fidVolHigh):
	        continue
	    vertEnergy = ev.GetFitResult("scintFitter").GetVertex(0).GetEnergy()
	    if (vertEnergy < energyLow) or (vertEnergy >= energyHigh):
	        continue
	    vertTime = ev.GetFitResult("scintFitter").GetVertex(0).GetTime()

        calibratedPMTs = ev.GetCalibratedPMTs()
		
	    timeResidsHist = ROOT.TH1D("timeResidsHist", "timeResidsHist", numbOfBins, minTimeResid, maxTimeResid)
	    for j in range(0, calibratedPMTs.GetCount()):
	        pmt = calibratedPMTs.GetPMT(j)
	        pmtPos = pmtInfo.GetPosition(pmt.GetID())
	        pmtTime = pmt.GetTime()

	        distInScint = ROOT.Double()
	        distInAV = ROOT.Double()
	        distInWater = ROOT.Double()
	        lightPath.CalcByPosition(vertPos, pmtPos, distInScint, distInAV, distInWater)
	        flightTime = groupVelocity.CalcByDistance(distInScint, distInAV, distInWater)
	        timeResid = pmtTime - flightTime - vertTime
	        timeResidsHist.Fill(timeResid)

	    tempHist = ROOT.TH1D("tempHist", "tempHist", numbOfBins, minTimeResid, maxTimeResid)
	    for k in range(1, timeResidsHist.GetNbinsX() + 1):
	        numPMTs = timeResidsHist.Integral(0, k)
	        timeVal = timeResidsHist.GetBinLowEdge(k)
	        tempHist.Fill(timeVal, (numPMTs / calibratedPMTs.GetCount()))

	    cumuHist.Add(cumuHist, tempHist, 1, 1)
	    numEvents += 1.0

	cumuHist.Scale(1.0 / numEvents)

	cumuVector = []
	for l in range(1, cumuHist.GetNbinsX() + 1):
	    cumuVector.append(cumuHist.GetBinContent(l))

	return cumuVector

