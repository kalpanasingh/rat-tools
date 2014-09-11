#!/usr/bin/env python
import string. ROOT, Utilities, os
# Author I T Coulter - 09/11/2012 <icoulter@hep.upenn.edu>
#        K Majumdar - 11/09/2014 - Cleanup of Coordinators for new DS


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
		

# returns the effective speed of light and other quad-fitter parameters
def AnalysisFunction(index):

    histograms = Utilities.ProducePlots()

    # Fit a straight line to the 1D Radial Bias vs. Effective Speed plot
    endRange = histograms[1].FindLastBinAbove(1.0)
    linearFit = ROOT.TF1("linearFit", "pol1", -1000.0, 1000.0)
    histograms[1].Fit(linearFit, "R")
    
    # Print the final results
    print "\n"
    print "Please place the text below into the database file: FIT_QUAD.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "name: \"QUAD_FIT\","
    print "index: \"" + index + "\","
    print "valid_begin: [0, 0],"
    print "valid_end: [0, 0],"
    print "\n",
    print "light_speed: " + str(linearFit.GetParameter(0)) + "d,    // Effective overall speed of light"
    print "num_points: 4000,    // Maximum number of points generated in quad-cloud"
    print "limit_points: 20000, // Number of attempts to generate points"
    print "calc_time: 1,        // Whether to calculate the reconstructed time"
    print "calc_errors: 1,      // Whether to compute errors on time and position"
    print "}"
    print "\n"


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the macros in Batch mode")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
    
