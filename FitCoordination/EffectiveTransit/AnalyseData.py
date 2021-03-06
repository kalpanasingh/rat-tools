#!/usr/bin/env python
import os, string, ROOT, Utilities
# Author P G Jones - 22/05/2011 <p.g.jones@qmul.ac.uk>
#        K Majumdar - 10/09/2014 - Cleanup of Coordinators for new DS


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
		

# returns the Transit Time
def AnalysisFunction(index):

    histograms = Utilities.ProducePlots()

    # Fit a straight line to the Prompt Time histogram
    endRange = histograms[1].FindLastBinAbove(1.0)
    linearFit = ROOT.TF1("linearFit", "pol1", 0.0, 10000.0)
    histograms[1].Fit(linearFit, "R")

    # Print the final results
    print "\n"
    print "Please place the text below into the database file: FIT_EFFECTIVE_TRANSIT.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "type: \"FIT_EFFECTIVE_TRANSIT\","
    print "version: 1,"
    print "index: \"" + index + "\","
    print "run_range: [0, 0],"
    print "pass : 0,"
    print "production: false,"
    print "timestamp: \"\","
    print "comment: \"\","
    print "\n",
    print "Intercept: " + linearFit.GetParameter(0) + ","
    print "Speed: " + float(1.0 / linearFit.GetParameter(1)) + ","
    print "}"
    print "\n"


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the analysis in Batch mode")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
    
