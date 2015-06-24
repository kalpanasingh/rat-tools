#!usr/bin/env python
import string, Utilities, os
# Author K Majumdar - 11/05/2012 <Krishanu.Majumdar@physics.ox.ac.uk>
#        K Majumdar - 08/09/2014 - Cleanup of Coordinators for new DS


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
		

# returns the tail fraction value, optimised for minimum overlap between alpha and electron tail/total PMTs ratio distributions
def AnalysisFunction(index):
	
    minlap = 10**9
    minFraction = 1000.0

    for tailFraction in Utilities.TailFracs:
	
        Histogram1 = Utilities.ProduceRatioHistogram(Utilities.Particles[0] + ".root", tailFraction)
        Histogram2 = Utilities.ProduceRatioHistogram(Utilities.Particles[1] + ".root", tailFraction)
        overlap = Utilities.BhattacharyaCoeff(Histogram1, Histogram2)

        del Histogram1
        del Histogram2

        if overlap < minlap:
            minlap = overlap
            minFraction = tailFraction

    print "\n"
    print "Please place the text below into the database file: CLASSIFIER_ALPHA_UNSEEDED.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "type: \"CLASSIFIER_ALPHA_UNSEEDED\","
    print "version: 1,"
    print "index: \"" + index + "\","
    print "run_range: [0, 0],"
    print "pass : 0,"
    print "production: false,"
    print "timestamp: \"\","
    print "comment: \"\","
    print "\n",
    print "tail_fraction: " + str(minFraction) + ","
    print "pmt_Min: " + str(Utilities.minTimeResid) + ","
    print "pmt_Max: " + str(Utilities.maxTimeResid) + ","
    print "}"
    print "\n"


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the analysis in Batch mode")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
