#!/usr/bin/env python
import os, sys, string, Utilities
# Author J Walker - 28/09/2015 <john.walker@liverpool.ac.uk>


def ProduceRunMacros(options):

    # Load any parameters for running the macros on a Batch system
    batch_params = None
    if options.batch:
        batch_params = {}
        execfile(options.batch, {}, batch_params)

    # Load any extra .ratdb files
    extraDB = ""
    if options.loadDB:
        extraDB = "/rat/db/load " + options.loadDB

    # Load the basic macro template
    inFile1 = open("Template_Macro.mac", "r")
    rawText1 = string.Template(inFile1.read())
    inFile1.close()

    # Load the batch submission script template
    inFile2 = open("Template_Batch.sh", "r")
    rawText2 = string.Template(inFile2.read())
    inFile2.close()

    # Select which energies to use based on the material in the detector
    energies = []
    if options.innerAVMaterial == "lightwater_sno":
        energies = Utilities.WaterEnergies
    else:
        energies = Utilities.ScintEnergies

    # Generate the specific macro for each energy/subfile combination, with energies and number of subfiles given in Utilities.py.
    # A number of subfiles for energy = 5.0 MeV and one file for all other energies.
    energy_subfile_pairs = []
    for energy in energies:
        energy_subfile_pairs.append([energy, 0])
    for subfile in range(1, Utilities.subfiles):
        energy_subfile_pairs.append([5.0, subfile])

    for pair in energy_subfile_pairs:
        energy = pair[0]
        subfile = pair[1]

        generator = "/generator/add combo gun:fill\n" + \
                    "/generator/vtx/set " + options.particle + " 0 0 0 " + str(energy) + "\n" + \
                    "/generator/pos/set 0.0 0.0 0.0"
        outfileName = options.innerAVMaterial + "_E=" + str(int(energy * 1000)) + "keV_sf=" + str(int(subfile))

        outText1 = rawText1.substitute(ExtraDB = extraDB,
                                       GeoFile = options.geoFile,
                                       InnerAVMaterial = options.innerAVMaterial,
                                       Particle = options.particle,
                                       FileName = outfileName + ".root",
                                       Generator = generator)
        outFile1 = open(outfileName + ".mac", "w")
        outFile1.write(outText1)
        outFile1.close()

        print "Running " + outfileName + ".mac and generating " + outfileName + ".root"

        # Run the macro on a Batch system
        if options.batch:
            outText2 = rawText2.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                           Ratenv = batch_params['ratenv'],
                                           Cwd = os.environ['PWD'].replace("/.", "/"),
                                           RunCommand = "rat " + outfileName + ".mac")
            outFile2 = open(outfileName + ".sh", "w")
            outFile2.write(outText2)
            outFile2.close()

            os.system( batch_params["submit"] + " " + outfileName +".sh" )

        # Else run the macro locally on an interactive machine		
        else:
            os.system("rat " + outfileName + ".mac")
            # delete the macro when running is complete
            os.remove(outfileName + ".mac")


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the macros in Batch mode")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use - location relative to rat/data/, default = geo/snoplus.geo", default = "geo/snoplus.geo")
    parser.add_option("-l", type = "string", dest = "loadDB", help = "Load an extra .ratdb directory")
    parser.add_option("-p", type = "string", dest = "particle", help = "Particle type to use (see generator documentation for available particles), default = 'e-'", default = "e-")
    parser.add_option("-s", type = "string", dest = "innerAVMaterial", help = "InnerAV material to use, default = lightwater_sno", default = "lightwater_sno")
    (options, args) = parser.parse_args()
    ProduceRunMacros(options)
