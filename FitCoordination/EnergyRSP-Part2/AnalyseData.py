#!/usr/bin/env python
import string, ROOT, Utilities, sys, os
# Author J Walker - 28/09/2015 <john.walker@liverpool.ac.uk>


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
                                     RunCommand = "python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.index + "\", \"" + options.innerAVMaterial + "\")'")
        outFile = open("AnalyseData.sh", "w")
        outFile.write(outText)
        outFile.close()

        os.system(batch_params["submit"] + " AnalyseData.sh")

    # Else run the macro locally on an interactive machine
    else:
        os.system("python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.index + "\", \"" + options.innerAVMaterial + "\")'")


# returns the Nhits vs. Position/Energy table
def AnalysisFunction(index, material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = Utilities.WaterEnergies
    else:
        energies = Utilities.ScintEnergies

    nPhotonsTable = Utilities.PredictedNCerenkovVsEnergy(material)[0]

    outFileName = "AnalyseData_Output.txt"
    outFile = open(outFileName, "w")

    outFile.write("\n \n")
    outFile.write("Please place the table below into the database file: FIT_ENERGY_LOOKUP.ratdb located in rat/data. The index the table fits into is given below.")
    outFile.write("\n\n")
    outFile.write("{\n")
    outFile.write("type: \"FIT_ENERGY_RSP\",\n")
    outFile.write("version: 1,\n")
    outFile.write("index: \"" + index + "\",\n")
    outFile.write("run_range: [0, 0],\n")
    outFile.write("pass: 0,\n")
    outFile.write("comment: \"\",\n")
    outFile.write("timestamp: \"\",\n")
    outFile.write("\n")

    outFile.write("predicted_nphotons_energy: [0.0, ")
    for nPhotons in nPhotonsTable:
        outFile.write(str('%.4f' % nPhotons) + ", ")
    outFile.write("],\n")
    outFile.write("\n")

    outFile.write("}\n")
    outFile.write("\n")

    outFile.close()


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the analysis in Batch mode")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    parser.add_option("-s", type = "string", dest = "innerAVMaterial", help = "InnerAV material to use, default = lightwater_sno", default = "lightwater_sno")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
