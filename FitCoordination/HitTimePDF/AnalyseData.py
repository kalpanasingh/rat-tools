#!/usr/bin/env python
import os, sys, string, ROOT, rat
import ProduceData as ProductionScript
# Author I T Coulter - 06/02/2013 <icoulter@hep.upenn.edu>
#        K Majumdar - 12/09/2014 - Cleanup of Coordinators for new DS


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
	
    numberOfRuns = ProductionScript.totalEvents / ProductionScript.eventsPerFile
    remainder = ProductionScript.totalEvents % ProductionScript.eventsPerFile
    if remainder != 0:
        numberOfRuns += 1

    # Run the analysis on a Batch system
    if options.batch:
        outText = rawText.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                     Ratenv = batch_params['ratenv'],
                                     Cwd = os.environ['PWD'].replace("/.", "/"),
                                     RunCommand = "python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.scintMaterial + "\", " + str(int(numberOfRuns)) + ", " + str(options.velocity) + ")'")
        outFile = open("AnalyseData.sh", "w")
        outFile.write(outText)
        outFile.close()
		
        os.system(batch_params["submit"] + " AnalyseData.sh")
		
    # Else run the macro locally on an interactive machine				
    else:
        os.system("python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.scintMaterial + "\", " + str(int(numberOfRuns)) + ", " + str(options.velocity) + ")'")


# returns the Hit Times PDF in the chosen material
def AnalysisFunction(material, numberOfRuns, velocity):
    ROOT.gROOT.ProcessLine(".L Coordinate.cpp+");
	
    if material == "lightwater_sno":
        if velocity > 0:
            raise Exception("Cannot rerun GV1D with modified velocity")
        ROOT.GetWaterPDF(material);
    else:
        ROOT.GetScintPDF(material, numberOfRuns, velocity);

    ROOT.gROOT.ProcessLine(".q");		

	
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the analysis in Batch mode")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = labppo_scintillator", default = "labppo_scintillator")
    parser.add_option("-v", type = "float", dest = "velocity", help = "Use an updated group velocity for the scintillator material, default = -999", default = -999)
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
