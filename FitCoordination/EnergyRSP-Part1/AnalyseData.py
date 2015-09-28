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

    nPhotonsTable = Utilities.NphotonsVsEnergy(material)[0]
    angularDist = Utilities.CerenkovAngularDist(material)
    rayleighProb = Utilities.RayleighAttenuationProb(material)
    pmtAngular = Utilities.PMTAngularResponse(material)

    outFileName = "AnalyseData_Output.txt"
    outFile = open(outFileName, 'w')

    outFile.write("\n\n")
    outFile.write("Please place the text below into the database file: FIT_ENERGY_RSP.ratdb located in rat/data, replacing any existing entry with the same index.")
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

    outFile.write("energies: [0.26, "),
    for energy in energies:
        outFile.write(str('%.1f' % energy) + ", ")
    outFile.write("],\n")
    outFile.write("\n")

    outFile.write("costhetaValues: ["),
    for costheta in Utilities.costhetaValues:
        outFile.write(str('%.4f' % costheta) + ", ")
    outFile.write("],\n")
    outFile.write("\n")

    outFile.write("event_dir_dot_initial_light_vec: ["),
    for uDotp in Utilities.uDotpValues:
        outFile.write(str('%.4f' % uDotp) + ", ")
    outFile.write("],\n")
    outFile.write("\n")

    outFile.write("radii: ["),
    for radius in Utilities.radialValues:
        outFile.write(str('%.4f' % radius) + ", ")
    outFile.write("],\n")
    outFile.write("\n")

    outFile.write("angularValues: ["),
    for angle in Utilities.angularValues:
        outFile.write(str('%.2f' % angle) + ", ")
    outFile.write("],\n")
    outFile.write("\n")

    outFile.write("nphotons_energy: [0.0, ")
    for nPhotons in nPhotonsTable:
        outFile.write(str('%.4f' % nPhotons) + ", ")
    outFile.write("],\n")
    outFile.write("\n")

    outFile.write("// Scale factor associated with Cerenkov angular distribution.\n")
    outFile.write("cerenkov_angular_dist: [\n"),
    lowest_energy = 0.26
    outFile.write("// Scale factors for energy = " + str(lowest_energy) + "\n")
    for costhetaIndex, costheta in enumerate(Utilities.costhetaValues):
        outFile.write(str('%.4f' % angularDist[0][costhetaIndex]) + ", ")
    outFile.seek(-1, os.SEEK_END)
    outFile.truncate()
    outFile.write("\n")
    for energyIndex, energy in enumerate(energies):
        outFile.write("// Scale factors for energy = " + str(energy) + "\n")
        for costhetaIndex, costheta in enumerate(Utilities.costhetaValues):
            outFile.write(str('%.4f' % angularDist[energyIndex][costhetaIndex]) + ", ")
        outFile.seek(-1, os.SEEK_END)
        outFile.truncate()
        outFile.write("\n")
    outFile.write("],\n")
    outFile.write("\n")

    outFile.write("// Probability that a Rayleigh scattered photon will be late.\n")
    outFile.write("rayleigh_late_prob: [\n"),
    for uDotpIndex, uDotp in enumerate(Utilities.uDotpValues):
        outFile.write("// Probability for u.p' = " + str(uDotp) + "\n")
        for radiusIndex, radius in enumerate(Utilities.radialValues):
            outFile.write(str('%.4f' % rayleighProb[uDotpIndex][radiusIndex]) + ", ")
        outFile.seek(-1, os.SEEK_END)
        outFile.truncate()
        outFile.write("\n")
    outFile.write("],\n")
    outFile.write("\n")

    outFile.write("pmt_angular_response: [")
    for response in pmtAngular:
        outFile.write(str('%.4f' % response) + ", ")
    outFile.write("],\n")
    outFile.write("\n")

    outFile.write("}\n")

    outFile.close()

    print "The coordination results have been written to \"AnalyseData_Output.txt\""


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the analysis in Batch mode")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    parser.add_option("-s", type = "string", dest = "innerAVMaterial", help = "InnerAV material to use, default = lightwater_sno", default = "lightwater_sno")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
