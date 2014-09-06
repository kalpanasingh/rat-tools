#!usr/bin/env python
import ROOT, rat, string, math
# Author K Majumdar - 05/09/2014 <Krishanu.Majumdar@physics.ox.ac.uk>

minTimeResid = -250.0
maxTimeResid = 350.0
fidVolLow = 0.0
fidVolHigh = 3500.0


# returns the parameters for the BiPo (Log-Likelihood Difference Method) Classifier in the form of a complete RATDB entry
def AnalyseRootFiles(options):

    if (options.isotope == ""):
        print "An Isotope option (-p) must be specified for this Analysis Script: either '212' or '214' ... exiting"
        sys.exit()

    timeResidsTe = GetTimeResidsVector("130Te_NDBD.root")
    timeResidsBi = GetTimeResidsVector(options.isotope + "Bi_Beta.root")
    timeResidsPo = GetTimeResidsVector(options.isotope + "Po_Alpha.root")
    meanAlphaNhits = GetMeanNhits(options.isotope + "Po_Alpha.root")
	
    ##############################
	
    print "\n"
    print "Please place the text below into the database file: CLASSIFIER_BIPO_LIKELIHOODDIFF.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "name: \"CLASSIFIER_BIPO_LIKELIHOODDIFF\","
    print "index: \"" + options.index + "\","
    print "valid_begin: [0, 0],"
    print "valid_end: [0, 0],"
    print "\n",
    print "min_time_residual: " + str(minTimeResid) + "d,"
    print "max_time_residual: " + str(maxTimeResid) + "d,"
    print "pdf_Te: [",
    for probability in timeResidsTe:
        print str(probability) + "d, ",
    print "],"
    print "pdf_Bi: [",
    for probability in timeResidsBi:
        print str(probability) + "d, ",
    print "],"
    print "pdf_Po: [",
    for probability in timeResidsPo:
        print str(probability) + "d, ",
    print "],"
    print "meanPoAlphaNhits: " + str(meanAlphaNhits) + "d,"
    print "}"
    print "\n"


# returns a vector containing the normalised time residuals over many events
def GetTimeResidsVector(infileName):
 
    numberOfBins = int(math.fabs(minTimeResid) + math.fabs(maxTimeResid))
    numberOfPMTs = 0.0
    timeResidsHist = ROOT.TH1D("timeResidsHist", "timeResidsHist", numberOfBins, minTimeResid, maxTimeResid)
	
    effectiveVelocity = rat.utility().GetEffectiveVelocity()
    lightPath = rat.utility().GetLightPathCalculator()
    pmtInfo = rat.utility().GetPMTInfo()
		
    for ds, run in rat.dsreader(infileName):
        if ds.GetEVCount() == 0:
            continue
	    
        for j in range(0, ds.GetEVCount()):
            ev = ds.GetEV(j)

            vertPos = ev.GetFitResult("scintFitter").GetVertex(0).GetPosition()
            if (vertPos.Mag() < fidVolLow) or (vertPos.Mag() >= fidVolHigh):
                continue
            vertTime = ev.GetFitResult("scintFitter").GetVertex(0).GetTime()
		
            calibratedPMTs = ev.GetCalPMTs()

            timeResidsList = []
            for k in range(0, calibratedPMTs.GetCount()):
                pmtPos = pmtInfo.GetPosition(calibratedPMTs.GetPMT(k).GetID())
                pmtTime = calibratedPMTs.GetPMT(k).GetTime()

                lightPath.CalcByPosition(vertPos, pmtPos)
                distInScint = lightPath.GetDistInScint()
                distInAV = lightPath.GetDistInAV()
                distInWater = lightPath.GetDistInWater()
                flightTime = effectiveVelocity.CalcByDistance(distInScint, distInAV, distInWater)
                timeResid = pmtTime - flightTime - vertTime
                timeResidsList.append(timeResid)

                numberOfPMTs += 1.0

            timeResidsList.sort()

            for t in timeResidsList:
                timeResidsHist.Fill(t - timeResidsList[9])

    timeResidsHist.Scale(1.0 / numberOfPMTs)

    timeResidsVector = []
    for l in range(1, timeResidsHist.GetNbinsX() + 1):
        timeResidsVector.append(timeResidsHist.GetBinContent(l))

    return timeResidsVector

# returns the mean Nhits of a Po Alpha decay event	
def GetMeanNhits(infileName):
    Histogram = ROOT.TH1D("alphaNhits", "alphaNhits", 125, 0.0, 500.0)
	
    for ds, run in rat.dsreader(infileName):
        if ds.GetEVCount() == 0:
            continue
        ev = ds.GetEV(0)

        vertPos = ev.GetFitResult("scintFitter").GetVertex(0).GetPosition()
        if (vertPos.Mag() < fidVolLow) or (vertPos.Mag() >= fidVolHigh):
            continue
        Histogram.Fill(ev.GetCalPMTs().GetCount())

    gaussFit = ROOT.TF1("gaus", "gaus", 0.0, 500.0)
    Histogram.Fit(gaussFit, "RQ")
	
    meanNhits = gaussFit.GetParameter(1)
    return meanNhits



import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    parser.add_option("-p", type = "string", dest = "isotope", help = "REQUIRED Isotope ('212' or '214')", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
	
