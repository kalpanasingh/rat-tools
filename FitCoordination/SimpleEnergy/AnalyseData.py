#!/usr/bin/env python
import string, ROOT, Utilities
# Author P G Jones - 22/05/2011 <p.g.jones@qmul.ac.uk>
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
		

# returns the Nhits vs. MeV ratio, as well as the dependence near the AV
def AnalysisFunction(index):

    nhitsRadiusPlot = Utilites.ProduceNhitsRadiusGraph()
    nhitsOriginHisto = Utilities.ProduceNhitsOriginHistogram()
	
    # Fit a gaussian to the distribution of Nhits near the AV Centre
    originFit = ROOT.TF1("gaus", "gaus", 0.0, 1000.0)
    nhitsOriginHisto.Fit(originFit, "RQ")
	
    # Fit a straight line to the Nhits vs. Radius plot in the NearAV region
    nearAVFit = ROOT.TF1("linear", "pol1", 5000.0, 6000.0)
    nhitsRadiusPlot.Fit(nearAVFit, "RQ")
	
    # Print the final results
    print "\n"
    print "Please place the text below into the database file: FIT_SIMPLE_ENERGY.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "type: \"FIT_SIMPLE_ENERGY\","
    print "version: 1,"
    print "index: \"" + index + "\","
    print "run_range: [0, 0],"
    print "pass : 0,"
    print "production: false,"
    print "timestamp: \"\","
    print "comment: \"\","
    print "\n"
    print "nhit_per_mev: " + originFit.GetParameter(1) + ","
    print "nhit_intercept: " + nearAVFit.GetParameter(0) + ","
    print "nhit_gradient: " + nearAVFit.GetParameter(1) + ","
    print "}"
    print "\n"


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the analysis in Batch mode")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
