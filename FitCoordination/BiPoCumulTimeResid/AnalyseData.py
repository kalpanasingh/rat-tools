#!usr/bin/env python
import ROOT, rat, string, math, ProduceData, os
# Author K Majumdar - 08/09/2014 <Krishanu.Majumdar@physics.ox.ac.uk>

infileName = ProduceData.outfileName + ".root"
minTimeResid = -10.0
maxTimeResid = 400.0
fidVolLow = 0.0
fidVolHigh = 3500.0


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
                                     RunCommand = "python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.index + "\")'")
        outFile = open("AnalyseData.sh", "w")
        outFile.write(outText)
        outFile.close()
		
        os.system(batch_params["submit"] + " AnalyseData.sh")
		
    # Else run the macro locally on an interactive machine				
    else:
        os.system("python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.index + "\")'")
		

# returns the parameters for the BiPo (Cumulative Time Residuals Method) Classifier in the form of a complete RATDB entry
def AnalysisFunction(index):
    
    energyWindow = GetEnergyWindow()
    cumulTimeResids = GetCDFVector(energyWindow[0], energyWindow[1])
	
    ##############################
	
    print "\n"
    print "Please place the text below into the database file: CLASSIFIER_BIPO_CUMULTIMERESID.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "name: \"CLASSIFIER_BIPO_CUMULTIMERESID\","
    print "index: \"" + index + "\","
    print "valid_begin: [0, 0],"
    print "valid_end: [0, 0],"
    print "\n",
    print "min_time_residual: " + str(minTimeResid) + "d,"
    print "max_time_residual: " + str(maxTimeResid) + "d,"
    print "cumulative_fractions: [",
    for probability in cumulTimeResids:
        print str(probability) + "d, ",
    print "],"
    print "}"
    print "\n"


# returns a vector containing the lower and upper bounds of the energy region of interest (mean reco.energy +/- 1 sigma)
def GetEnergyWindow():
    Histogram = ROOT.TH1D("recoEnergy", "recoEnergy", 100, 0.0, 5.0)

    for ds, run in rat.dsreader(infileName):
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
	
    print "\n"
    print "Energy Window (mean reco.energy +/- 1 sigma): " + str(lowEnergy) + "MeV to " + str(highEnergy) + "MeV"
    print "\n"
    
    return energyWindow

# returns a vector containing the normalised cumulative time residuals over many events
def GetCDFVector(energyLow, energyHigh):

    numberOfBins = int(math.fabs(minTimeResid) + math.fabs(maxTimeResid))
    numberOfEvents = 0.0
    cumuHist = ROOT.TH1D("cumuHist", "cumuHist", numberOfBins, minTimeResid, maxTimeResid)
	
    effectiveVelocity = rat.utility().GetEffectiveVelocity()
    lightPath = rat.utility().GetLightPathCalculator()
    pmtInfo = rat.utility().GetPMTInfo()
		
    for ds, run in rat.dsreader(infileName):
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

        calibratedPMTs = ev.GetCalPMTs()
		
        timeResidsHist = ROOT.TH1D("timeResidsHist", "timeResidsHist", numberOfBins, minTimeResid, maxTimeResid)
        for j in range(0, calibratedPMTs.GetCount()):
            pmtPos = pmtInfo.GetPosition(calibratedPMTs.GetPMT(j).GetID())
            pmtTime = calibratedPMTs.GetPMT(j).GetTime()

            lightPath.CalcByPosition(vertPos, pmtPos)
            distInScint = lightPath.GetDistInScint()
            distInAV = lightPath.GetDistInAV()
            distInWater = lightPath.GetDistInWater()
            flightTime = effectiveVelocity.CalcByDistance(distInScint, distInAV, distInWater)
            timeResid = pmtTime - flightTime - vertTime
            timeResidsHist.Fill(timeResid)

        tempHist = ROOT.TH1D("tempHist", "tempHist", numberOfBins, minTimeResid, maxTimeResid)
        for k in range(1, timeResidsHist.GetNbinsX() + 1):
            numberOfPMTs = timeResidsHist.Integral(0, k)
            timeValue = timeResidsHist.GetBinLowEdge(k)
            tempHist.Fill(timeValue, (numberOfPMTs / calibratedPMTs.GetCount()))

        cumuHist.Add(cumuHist, tempHist, 1, 1)
        numberOfEvents += 1.0
		
        del timeResidsHist
        del tempHist

    cumuHist.Scale(1.0 / numberOfEvents)

    cumuVector = []
    for l in range(1, cumuHist.GetNbinsX() + 1):
        cumuVector.append(cumuHist.GetBinContent(l))

    return cumuVector


	
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the analysis in Batch mode")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
	
