#!usr/bin/env python
import string, Utilities
# Author K Majumdar - 14/03/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


def AnalyseRootFiles(options):
    # returns the time residuals PDF for 130Te NNBD, Bi Beta and Po Alpha events in the fiducial volume
    # also returns the mean Nhits for Po Alpha events
    
    if (options.index == ""):
        print "An Index option (-i) must be specified for this coordinator ... exiting"
        sys.exit()
    indexList = (options.index).split('-')
    material = indexList[0]
    isotope = indexList[1]
    timingProfile = indexList[2]

    if (timingProfile == "noPSD"):
        indexString = material + "_" + isotope + "BiPo_" + timingProfile
    else:
        indexString = material + "_" + isotope + "BiPo"

    timeResidsTe = Utilities.GetTimeResidsVector(options.index + "_Te.root", Utilities.fidVolLow, Utilities.fidVolHigh, Utilities.minTimeResid, Utilities.maxTimeResid)
    timeResidsBi = Utilities.GetTimeResidsVector(options.index + "_Bi.root", Utilities.fidVolLow, Utilities.fidVolHigh, Utilities.minTimeResid, Utilities.maxTimeResid)
    timeResidsPo = Utilities.GetTimeResidsVector(options.index + "_Po.root", Utilities.fidVolLow, Utilities.fidVolHigh, Utilities.minTimeResid, Utilities.maxTimeResid)
    meanAlphaNhits = Utilities.GetMeanNhits(options.index + "_Po.root", Utilities.fidVolLow, Utilities.fidVolHigh)

    print "\n"
    print "Please place the text below into the database file: CLASSIFIER_BIPO_LIKELIHOODDIFF.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "name: \"CLASSIFIER_BIPO_LIKELIHOODDIFF\","
    print "index: \"" + indexString + "\","
    print "valid_begin: [0, 0],"
    print "valid_end: [0, 0],"
    print "\n",
    print "min_time_residual: " + str(Utilities.minTimeResid) + "d,"
    print "max_time_residual: " + str(Utilities.maxTimeResid) + "d,"
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


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB Index, given by conecating the explicit -s and -p options from the Production Script, separated by '-'", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
	