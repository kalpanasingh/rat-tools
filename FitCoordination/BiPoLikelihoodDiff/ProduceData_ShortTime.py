#!/usr/bin/env python
import os, sys, string, Utilities
# Author K Majumdar - 14/03/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


def ProduceRunMacFiles(options):
    # produces and then runs the required RAT macros by sourcing a .sh file on the cluster

    if (options.isotopeAndTiming == ""):
        print "An Isotope-and-Timing option (-p) must be specified for this coordinator ... exiting"
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

    infile2 = open("Template_Submit.sh", "r")
    rawText2 = string.Template(infile2.read())
    infile2.close()
     
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
    outTextTe2 = rawText2.substitute(envronLoc = Utilities.envronLoc,
                                     currentLoc = Utilities.currentLoc,
                                     runCommand = "rat " + fileName + "_Te.mac")
    outFileTe2 = open(fileName + "_Te.sh", "w")
    outFileTe2.write(outTextTe2)
    outFileTe2.close()
    print "Running " + fileName + "_Te.mac via " + fileName + "_Te.sh and generating " + fileName + "_Te.root"
    os.system("qsub " + fileName + "_Te.sh")
    
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
    outTextBi2 = rawText2.substitute(envronLoc = Utilities.envronLoc,
                                     currentLoc = Utilities.currentLoc,
                                     runCommand = "rat " + fileName + "_Bi.mac")
    outFileBi2 = open(fileName + "_Bi.sh", "w")
    outFileBi2.write(outTextBi2)
    outFileBi2.close()
    print "Running " + fileName + "_Bi.mac via " + fileName + "_Bi.sh and generating " + fileName + "_Bi.root"
    os.system("qsub " + fileName + "_Bi.sh")
    
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
    outTextPo2 = rawText2.substitute(envronLoc = Utilities.envronLoc,
                                     currentLoc = Utilities.currentLoc,
                                     runCommand = "rat " + fileName + "_Po.mac")
    outFilePo2 = open(fileName + "_Po.sh", "w")
    outFilePo2.write(outTextPo2)
    outFilePo2.close()
    print "Running " + fileName + "_Po.mac via " + fileName + "_Po.sh and generating " + fileName + "_Po.root"
    os.system("qsub " + fileName + "_Po.sh")
    

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File - geo/[geometry file], default = snoplus.geo", default = "geo/snoplus.geo")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material, default = te_0p3_labppo_scintillator_Oct2012", default = "te_0p3_labppo_scintillator_Oct2012")
    parser.add_option("-p", type = "string", dest = "isotopeAndTiming", help = "REQUIRED Isotope ('212' or '214') and Timing ('PSD' or 'noPSD') Options separated by a '-'", default = "")
    (options, args) = parser.parse_args()
    ProduceRunMacFiles(options)
    
