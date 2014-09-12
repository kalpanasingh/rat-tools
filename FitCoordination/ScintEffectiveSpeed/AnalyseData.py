#!/usr/bin/env python
import string, ROOT, Utilities, os
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
		

# returns the effective speeds of light in the given scintillator, water and the AV material
def AnalysisFunction(index):

    histograms = Utilities.ProducePlots()

    # Fit a straight line to the 1D Radial Bias vs. Effective Speed plot
    endRange = histograms[1].FindLastBinAbove(1.0)
    linearFit = ROOT.TF1("linearFit", "pol1", -1000.0, 1000.0)
    histograms[1].Fit(linearFit, "R")
    
    # Print the final results
    print "\n"
    print "Please place the text below into the database file: EFFECTIVE_VELOCITY.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "name: \"EFFECTIVE_VELOCITY\","
    print "index: \"" + index + "\","
    print "valid_begin: [0, 0],"
    print "valid_end: [0, 0],"
    print "\n",
    print "inner_av_velocity: " + str(linearFit.GetParameter(0)) + "d,"
    print "av_velocity: 1.93109181500140664d+02,"
    print "water_velocity: 2.17554021555098529d+02,"
    print "offset: 0.6d,"
    print "}"
    print "\n"


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the analysis in Batch mode")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
    
