#!usr/bin/env python
import string, Utilities
# Author K Majumdar - 10/03/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


def AnalyseRootFiles(options):
    # returns the cumulative time residuals PDF for 130Te NNBD events in the fiducial volume and energy region of interest
    
    if (options.index == ""):
        print "An Index option (-i) must be specified for this coordinator ... exiting"
        sys.exit()
    indexList = (options.index).split('-')
    material = indexList[0]
    timingProfile = indexList[1]

    if (timingProfile == "noPSD"):
        indexString = material + "_" + timingProfile
    else:
        indexString = material

    energyWindow = Utilities.GetEnergyWindow(options.index + ".root", Utilities.fidVolLow, Utilities.fidVolHigh)
    cumulTimeResids = Utilities.GetCDFVector(options.index + ".root", Utilities.fidVolLow, Utilities.fidVolHigh, energyWindow[0], energyWindow[1], Utilities.minTimeResid, Utilities.maxTimeResid)
	
    print "\n"
    print "Please place the text below into the database file: CLASSIFIER_BIPO_CUMULTIMERESID.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "name: \"CLASSIFIER_BIPO_CUMULTIMERESID\","
    print "index: \"" + indexString + "\","
    print "valid_begin: [0, 0],"
    print "valid_end: [0, 0],"
    print "\n",
    print "min_time_residual: " + str(Utilities.minTimeResid) + "d,"
    print "max_time_residual: " + str(Utilities.maxTimeResid) + "d,"
    print "cumulative_fractions: [",
    for probability in cumulTimeResids:
        print str(probability) + "d, ",
    print "],"
    print "}"
    print "\n"


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB Index, given by conecating the explicit -s and -p options from the Production Script, separated by '-'", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
	