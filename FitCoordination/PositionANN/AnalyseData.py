#!/usr/bin/env python
import os, sys, string, ROOT, rat
from ROOT import RAT


def CreateRootTrees(options):

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
    for time in options.times:
        for angle in options.angles:
            output_suffix = "_t_{0}_a_{1}".format(time, angle)
            command = "python -c 'import AnalyseData; AnalyseData.RunCreateTree({0}, {1})'".format(time, angle)
            if options.batch:
                outText = rawText.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                             Ratenv = batch_params['ratenv'],
                                             Cwd = os.environ['PWD'].replace("/.", "/"),
                                             RunCommand = command)
                scriptName = "AnalyseData_{0}.sh".format(output_suffix)
                outFile = open(scriptName, "w")
                outFile.write(outText)
                outFile.close()
        		
                os.system(batch_params["submit"] + " " + scriptName)
        		
            # Else run the macro locally on an interactive machine				
            else:
                os.system(command)


# Fills trees in files for the given number of angle and time bins
def RunCreateTree(time, angle):
    ROOT.gROOT.ProcessLine(".L FillTree.cc+")
    # Run for each of training, crossval, alphas
    ROOT.FillTree("NearAVANN_training_*.root", "training_tree_{0}_{1}.root".format(time, angle), time, angle)
    ROOT.FillTree("NearAVANN_crossval_*.root", "crossval_tree_{0}_{1}.root".format(time, angle), time, angle)
    ROOT.FillTree("NearAVANN_alphas_*.root", "alphas_tree_{0}_{1}.root".format(time, angle), time, angle)
    ROOT.gROOT.ProcessLine(".q")


import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", type = str, dest = "batch", help = "Run the analysis in Batch mode")
    parser.add_argument("-i", type = str, dest = "index", help = "RATDB index to place result.", default = "")
    parser.add_argument("-t", type = int, dest = "times", help = "Timing bins", nargs = "+", default = [20])
    parser.add_argument("-a", type = int, dest = "angles", help = "Angular bins", nargs = "+", default = [20])
    (args) = parser.parse_args()
    CreateRootTrees(args)
