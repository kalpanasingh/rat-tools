#!/usr/bin/env python
import os, sys, string, Utilities
# Author J Walker - 23/04/2015 <john.walker@liverpool.ac.uk>


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
    fitter = ""
    scale_factor_energy = 0.0
    subfiles = 0
    if options.innerAVMaterial == "lightwater_sno":
        energies = Utilities.WaterEnergies
        fitter = "# quadFitter\n" + \
            "/rat/proc fitter\n" + \
            "/rat/procset method \"quad\"\n" + \
            "/rat/procset name \"seedResult\"\n" + \
            "\n" + \
            "# simpleDirection\n" + \
            "/rat/proc fitter\n" + \
            "/rat/procset method \"simpleDirection\"\n" + \
            "/rat/procset seed \"seedResult\"\n" + \
            "/rat/procset name \"waterResult\"\n" + \
            "\n" + \
            "# positionTimeLikelihood\n" + \
            "/rat/proc fitter\n" + \
            "/rat/procset method \"positionTimeLikelihood\"\n" + \
            "/rat/procset optimiser \"metaDriveCorrectSeed-powell\"\n" + \
            "/rat/procset pdf \"gv1d-lightwater-sno\"\n" + \
            "/rat/procset seed \"waterResult\"\n" + \
            "/rat/procset selector \"modeCut\"\n" + \
            "/rat/procset name \"waterResult\"\n" + \
            "\n" + \
            "# positionTimeDirectionLikelihood\n" + \
            "/rat/proc fitter\n" + \
            "/rat/procset method \"positionTimeDirectionLikelihood\"\n" + \
            "/rat/procset optimiser \"simulatedAnnealing\"\n" + \
            "/rat/procset pdf \"positionDirectionPDF\"\n" + \
            "/rat/procset seed \"waterResult\"\n" + \
            "/rat/procset selector \"modeCut\"\n" + \
            "/rat/procset name \"waterResult\"\n" + \
            "\n" + \
            "# energyPromptLookup\n" + \
            "/rat/proc fitter\n" + \
            "/rat/procset method \"energyPromptLookup\"\n" + \
            "/rat/procset seed \"waterResult\"\n" + \
            "/rat/procset name \"waterResult\"\n" + \
            "\n" + \
            "# energyRSP\n" + \
            "/rat/proc fitter\n" + \
            "/rat/procset method \"energyRSP\"\n" + \
            "/rat/procset seed \"waterResult\"\n" + \
            "/rat/procset name \"waterResult\"\n"
        scale_factor_energy = 5.0
        subfiles = Utilities.WaterSubfiles
    else:
        energies = Utilities.ScintEnergies
        fitter = "scintFitter"
        scale_factor_energy = 2.5
        subfiles = Utilities.ScintSubfiles

    # Generate the specific macro for each energy/position combination, with energies and positions given in the Utilities tables.
    # For each position with energy = 5.0 MeV and each energy with position = 0.0 mm.
    energy_position_subfile = []
    for energy in energies:
        energy_position_subfile.append([energy, 0.0, 0])
    for position in Utilities.Positions:
        if position == 0.0:
            for sf in range(1, subfiles):
                energy_position_subfile.append([scale_factor_energy, position, sf])
        else:
            for sf in range(0, subfiles):
                energy_position_subfile.append([scale_factor_energy, position, sf])

    for eps in energy_position_subfile:
        energy = eps[0]
        position = eps[1]
        subfile = eps[2]

        generator = "/generator/add combo gun:fillshell\n" + \
                    "/generator/vtx/set " + options.particle + " 0 0 0 " + str(energy) + "\n" + \
                    "/generator/pos/set 0.0 0.0 0.0 " + str(position) + " " + str(position) + " inner_av,av,cavity"
        outfileName = options.innerAVMaterial + "_P=" + str(int(position)) + "mm_E=" + str(int(energy * 1000)) + "keV_sf=" + str(int(subfile))

        outText1 = rawText1.substitute(ExtraDB = extraDB,
                                       GeoFile = options.geoFile,
                                       InnerAVMaterial = options.innerAVMaterial,
                                       Fitter = fitter,
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
