#!usr/bin/env python
import ROOT, rat, math
# Secondary functions and user-defined Values for the BiPoLikelihoodDiff Coordinator
# Author K Majumdar - 05/04/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


envronLoc = ""
currentLoc = ""

minTimeResid = -250.0
maxTimeResid = 350.0
fidVolLow = 0.0
fidVolHigh = 3500.0


def GetTimeResidsVector(filename, fidVolLow, fidVolHigh, minTimeResid, maxTimeResid):
    # returns a vector containing the normalised time residuals over many events

    numbOfBins = int(math.fabs(minTimeResid) + math.fabs(maxTimeResid))
    numbOfPMTs = 0.0
    timeResidsHist = ROOT.TH1D("timeResidsHist", "timeResidsHist", numbOfBins, minTimeResid, maxTimeResid)
	
    for ds, run in rat.dsreader(filename):
	    groupVelocity = rat.utility().GetGroupVelocity()
	    lightPath = rat.utility().GetLightPath()
	    pmtInfo = rat.utility().GetPMTInfo()
	
        if ds.GetEVCount() == 0:
            continue
	    
        for j in range(0, ds.GetEVCount()):
            ev = ds.GetEV(j)

            vertPos = ev.GetFitResult("scintFitter").GetVertex(0).GetPosition()
            if (vertPos.Mag() < fidVolLow) or (vertPos.Mag() >= fidVolHigh):
                continue
            vertTime = ev.GetFitResult("scintFitter").GetVertex(0).GetTime()
		
            calibratedPMTs = ev.GetCalibratedPMTs()

            timeResidsList = []
            for k in range(0, calibratedPMTs.GetCount()):
                pmt = calibratedPMTs.GetPMT(k)
                pmtPos = pmtInfo.GetPosition(pmt.GetID())
                pmtTime = pmt.GetTime()

                distInScint = ROOT.Double()
                distInAV = ROOT.Double()
                distInWater = ROOT.Double()
                lightPath.CalcByPosition(vertPos, pmtPos, distInScint, distInAV, distInWater)
                flightTime = groupVelocity.CalcByDistance(distInScint, distInAV, distInWater)
                timeResid = pmtTime - flightTime - vertTime
                timeResidsList.append(timeResid)

                numbOfPMTs += 1.0

            timeResidsList.sort()

            for t in timeResidsList:
                timeResidsHist.Fill(t - timeResidsList[9])

    timeResidsHist.Scale(1.0 / numbOfPMTs)

    timeResidsVector = []
    for l in range(1, timeResidsHist.GetNbinsX() + 1):
        timeResidsVector.append(timeResidsHist.GetBinContent(l))

    return timeResidsVector


def GetMeanNhits(filename, fidVolLow, fidVolHigh):
    # returns the mean Nhits of a Po Alpha decay event

    nhitsHist = ROOT.TH1D("nhitsHist", "nhitsHist", 125, 0.0, 500.0)
	
    for ds, run in rat.dsreader(filename):
        if ds.GetEVCount() == 0:
            continue
        ev = ds.GetEV(0)

        vertPos = ev.GetFitResult("scintFitter").GetVertex(0).GetPosition()
        if (vertPos.Mag() < fidVolLow) or (vertPos.Mag() >= fidVolHigh):
            continue
		
        nhitsHist.Fill(ev.GetCalibratedPMTs().GetCount())

    gaussFit = ROOT.TF1("gaus", "gaus", 0.0, 500.0)
    nhitsHist.Fit(gaussFit, "RQ")
	
    meanNhits = gaussFit.GetParameter(1)
    return meanNhits
