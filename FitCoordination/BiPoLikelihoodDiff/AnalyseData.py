#!usr/bin/env python
import ROOT, rat, string, math, os, sys
# Author K Majumdar - 08/09/2014 <Krishanu.Majumdar@physics.ox.ac.uk>

minTimeResid = -200.0
maxTimeResid = 300.0
fidVolLow = 0.0
fidVolHigh = 3500.0
triggerWindowStartTime = -180.0
triggerWindowEndTime = 220.0


def AnalyseRootFiles(options):

    # Load any parameters for running the macros on a Batch system
    batch_params = None
    if options.batch:
        batch_params = {}
        execfile(options.batch, {}, batch_params)
	
	# Load the batch submission script template
    inFile = open("Template_Batch.sh", "r")
    rawText = string.Template(inFile.read())
    inFile.close()
		
    # Run the analysis on a Batch system
    if options.batch:
        outText = rawText.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                     Ratenv = batch_params['ratenv'],
                                     Cwd = os.environ['PWD'].replace("/.", "/"),
                                     RunCommand = "python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.index + "\", \"" + options.isotope + "\")'")
        outFile = open("AnalyseData.sh", "w")
        outFile.write(outText)
        outFile.close()
		
        os.system(batch_params["submit"] + " AnalyseData.sh")
		
    # Else run the macro locally on an interactive machine				
    else:
        os.system("python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.index + "\", \"" + options.isotope + "\")'")
		

# returns the parameters for the BiPo (Log-Likelihood Difference Method) Classifier in the form of a complete RATDB entry
def AnalysisFunction(index, isotope):

    if (isotope == ""):
        print "An Isotope option (-p) must be specified for this Analysis Script: either '212' or '214' ... exiting"
        sys.exit()

    numberOfBins = int(math.fabs(minTimeResid) + math.fabs(maxTimeResid))

    times = []
    for currentTime in range(int(minTimeResid), int(maxTimeResid)):
        times.append(currentTime)
    
    timeResidsTe = GetTimeResidsVector("Te130_NDBD.root", numberOfBins)
    timeResidsBi = GetTimeResidsVector("Bi_Beta" + isotope + ".root", numberOfBins)
    timeResidsPo = GetTimeResidsVector("Po_Alpha" + isotope + ".root", numberOfBins)
    meanAlphaNhits = GetMeanNhits("Po_Alpha" + isotope + ".root")
	
    ##############################

    # For BiPoLikelihoodDiff RATDB index is a combination of material and mass number
    index = index + "_" + isotope + "BiPo"
	
    print "\n"
    print "Please place the text below into the database file: CLASSIFIER_BIPO_LIKELIHOODDIFF.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "type: \"CLASSIFIER_BIPO_LIKELIHOODDIFF\","
    print "version: 1,"
    print "index: \"" + index + "\","
    print "run_range: [0, 0],"
    print "pass : 0,"
    print "production: false,"
    print "timestamp: \"\","
    print "comment: \"\","
    print "\n",
    print "times: [",
    for time in times:
        print str(float(time)) + ", ",
    print "],"
    print "pdf_Te: [",
    for probability in timeResidsTe:
        print str(probability) + ", ",
    print "],"
    print "pdf_Bi: [",
    for probability in timeResidsBi:
        print str(probability) + ", ",
    print "],"
    print "pdf_Po: [",
    for probability in timeResidsPo:
        print str(probability) + ", ",
    print "],"
    print "meanPoAlphaNhits: " + str(meanAlphaNhits) + ","
    print "triggerWindowStartTime: " + str(float(triggerWindowStartTime)) + ","
    print "triggerWindowEndTime: " + str(float(triggerWindowEndTime)) + ","
    print "}"
    print "\n"


# returns a vector containing the normalised time residuals over many events
def GetTimeResidsVector(infileName, numberOfBins):
 
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

            if not ev.FitResultExists("scintFitter"):
                continue
            if not ev.GetFitResult("scintFitter").GetValid():
                continue
            if not ev.GetFitResult("scintFitter").GetVertex(0).ContainsPosition():
                continue
            vertPos = ev.GetFitResult("scintFitter").GetVertex(0).GetPosition()
            

            if (vertPos.Mag() < fidVolLow) or (vertPos.Mag() >= fidVolHigh):
                continue
            vertTime = ev.GetFitResult("scintFitter").GetVertex(0).GetTime()
		
            calibratedPMTs = ev.GetCalPMTs()
            if (calibratedPMTs.GetCount() < 10):
                continue

            timeResidsList = []
            for k in range(0, calibratedPMTs.GetCount()):
                pmtPos = pmtInfo.GetPosition(calibratedPMTs.GetPMT(k).GetID())
                pmtTime = calibratedPMTs.GetPMT(k).GetTime()

                lightPath.CalcByPosition(vertPos, pmtPos)
                distInInnerAV = lightPath.GetDistInInnerAV()
                distInAV = lightPath.GetDistInAV()
                distInWater = lightPath.GetDistInWater()
                flightTime = effectiveVelocity.CalcByDistance(distInInnerAV, distInAV, distInWater)
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

        if not ev.FitResultExists("scintFitter"):
            continue
        if not ev.GetFitResult("scintFitter").GetValid():
            continue
        if not ev.GetFitResult("scintFitter").GetVertex(0).ContainsPosition():
            continue

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
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the analysis in Batch mode")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    parser.add_option("-p", type = "string", dest = "isotope", help = "REQUIRED Isotope ('212' or '214')", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
	
