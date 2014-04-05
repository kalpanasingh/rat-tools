#!/usr/bin/env python
import os, sys, string
# Author K Majumdar - 05/04/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


def ProduceRunMacFiles(options):
    # produces and then runs the required RAT macros, and deletes each macro once complete

    if (options.isotopeAndTiming == ""):
        print "An Isotope-and-Timing option (-p) must be specified for this coordinator, i.e. 212-PSD or 214-noPSD ... exiting"
        sys.exit()
    isotopeAndTimingList = (options.isotopeAndTiming).split('-')
    isotope = isotopeAndTimingList[0]
    timingProfile = isotopeAndTimingList[1]

    if timingProfile == "noPSD":
        alphaLine1 = "/rat/db/set OPTICS[te_0p3_labppo_scintillator_Oct2012] SCINTWAVEFORMalpha_value1 [ -4.6d, -18d, -156d,]"
        alphaLine2 = "/rat/db/set OPTICS[te_0p3_labppo_scintillator_Oct2012] SCINTWAVEFORMalpha_value2 [ 0.71d, 0.22d, 0.07d,]"
    elif timingProfile == "PSD":
        alphaLine1 = ""
        alphaLine2 = ""
    else:
        print "Invalid Timing Option set ... must be either 'PSD' or 'noPSD' ... exiting"
        sys.exit()

    fileName = options.scintMaterial + "-" + options.isotopeAndTiming
    
    inFile = open("Base.mac", "r")
    rawText = string.Template(inFile.read())
    inFile.close()
    
    outTextTe = rawText.substitute(Hadrons = "/PhysicsList/OmitHadronicProcesses true",
                                   GeoFile = options.geoFile,
                                   ScintMaterial = options.scintMaterial,
                                   AlphaWaveFormLine1 = alphaLine1,
                                   AlphaWaveFormLine2 = alphaLine2,
                                   OutFileName = fileName + "_Te.root",
                                   Generator = "/generator/add combo gun:fill:poisson",
                                   Vertex = "/generator/vtx/set e- 0 0 0 2.527")
    outFileTe = open(fileName + "_Te.mac", "w")
    outFileTe.write(outTextTe)
    outFileTe.close()
    print "Running " + fileName + "_Te.mac and generating " + fileName + "_Te.root"
    os.system("rat " + fileName + "_Te.mac")
    os.remove(fileName + "_Te.mac")

    outTextBi = rawText.substitute(Hadrons = "/PhysicsList/OmitHadronicProcesses true",
                                   GeoFile = options.geoFile,
                                   ScintMaterial = options.scintMaterial,
                                   AlphaWaveFormLine1 = alphaLine1,
                                   AlphaWaveFormLine2 = alphaLine2,
                                   OutFileName = fileName + "_Bi.root",
                                   Generator = "/generator/add combo decay0:fill:poisson",
                                   Vertex = "/generator/vtx/set backg Bi" + isotope)
    outFileBi = open(fileName + "_Bi.mac", "w")
    outFileBi.write(outTextBi)
    outFileBi.close()
    print "Running " + fileName + "_Bi.mac and generating " + fileName + "_Bi.root"
    os.system("rat " + fileName + "_Bi.mac")
    os.remove(fileName + "_Bi.mac")

    outTextPo = rawText.substitute(Hadrons = "",
                                   GeoFile = options.geoFile,
                                   ScintMaterial = options.scintMaterial,
                                   AlphaWaveFormLine1 = alphaLine1,
                                   AlphaWaveFormLine2 = alphaLine2,
                                   OutFileName = fileName + "_Po.root",
                                   Generator = "/generator/add combo decay0:fill:poisson",
                                   Vertex = "/generator/vtx/set backg Po" + isotope)
    outFilePo = open(fileName + "_Po.mac", "w")
    outFilePo.write(outTextPo)
    outFilePo.close()
    print "Running " + fileName + "_Po.mac and generating " + fileName + "_Po.root"
    os.system("rat " + fileName + "_Po.mac")
    os.remove(fileName + "_Po.mac")


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File - geo/[geometry file], default = snoplus.geo", default = "geo/snoplus.geo")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material, default = te_0p3_labppo_scintillator_Oct2012", default = "te_0p3_labppo_scintillator_Oct2012")
    parser.add_option("-p", type = "string", dest = "isotopeAndTiming", help = "REQUIRED Isotope ('212' or '214') and Timing ('PSD' or 'noPSD') Options separated by '-'", default = "")
    (options, args) = parser.parse_args()
    ProduceRunMacFiles(options)
    
