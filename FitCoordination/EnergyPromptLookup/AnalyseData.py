#!/usr/bin/env python
import string, ROOT, Utilities, sys, os
# Author J Walker - 23/04/2015 <john.walker@liverpool.ac.uk>


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


# returns the parameters for the Energy Prompt Lookup fitter in the form of a RATDB entry
def AnalysisFunction(index, material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = Utilities.WaterEnergies
    else:
        energies = Utilities.ScintEnergies

    nHitsTable = Utilities.PromptNhitsVsEnergy(material)
    scaleFactor = Utilities.PositionDirectionScaleFactor(material)

    outFileName = "AnalyseData_Output.txt"
    outFile = open(outFileName, "w")

    outFile.write("\n \n")
    outFile.write("Please place the text below into the database file: FIT_ENERGY_PROMPT_LOOKUP.ratdb located in rat/data, replacing any existing entry with the same index.")
    outFile.write("\n \n")
    outFile.write("{ \n")
    outFile.write("name: \"FIT_ENERGY_PROMPT_LOOKUP\", \n")
    outFile.write("index: \"" + index + "\", \n")
    outFile.write("valid_begin: [0, 0], \n")
    outFile.write("valid_end: [0, 0], \n")
    outFile.write("\n")
    outFile.write("// Values for position and direction scaling. Scaling coefficient adjusts\n")
    outFile.write("// the prompt Nhits of an event according to the radial position of the\n")
    outFile.write("// event and the costheta angle of the direction from the position vector.\n")
    outFile.write("// Prompt Nhits are divided by the scaling factor.\n")
    outFile.write("\n")
    outFile.write("// number of radial bins\n")
    outFile.write("r_bins: " + str('%.1f' % len(Utilities.Positions)) + ",\n")
    outFile.write("// number of angular bins\n")
    outFile.write("costheta_bins: " + str('%.1f' % Utilities.uDotrBins) + ",\n")
    outFile.write("// maximum radius\n")
    outFile.write("r_max: " + str('%.1f' % Utilities.Positions[-1]) + ",\n")
    outFile.write("\n")

    outFile.write("// Scaling factor corresponding to radius and costheta value. \n")
    outFile.write("scaling_factor: [ \n"),
    for uDotrBin in range(0,Utilities.uDotrBins):
        outFile.write("// Coefficients for " + str('%.2f' % Utilities.uDotrLimitValues[uDotrBin]) + " < CosTheta < " + str('%.2f' % Utilities.uDotrLimitValues[uDotrBin+1]) + "\n")
        for positionIndex, position in enumerate(Utilities.Positions):
            outFile.write(str('%.4f' % scaleFactor[uDotrBin][positionIndex]) + ", ")
        outFile.write("\n")
    outFile.write("], \n")
    outFile.write("\n \n")

    outFile.write("// Values to map between adjusted prompt Nhits and corresponding MeV energy.\n")
    outFile.write("\n")
    outFile.write("mev_values: [0.0, 0.26, "),
    for energy in energies:
        outFile.write(str('%.1f' % energy) + ", ")
    outFile.write("], \n")
    outFile.write("\n")

    outFile.write("nhit_values: [0.0, 0.0, ")
    for nHits in nHitsTable:
        outFile.write(str('%.4f' % nHits) + ", ")
    outFile.write("], \n")
    outFile.write("\n")

    outFile.write("} \n")
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
