#!/usr/bin/env python
import os, sys, string, Utilities
# Author K Majumdar - 12/03/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


def ProduceRunMacFiles(options):
    # produces and then runs the required RAT macro by sourcing a .sh file on the cluster
    
    if options.timingProfile == "noPSD":
        alphaLine1 = "/rat/db/set OPTICS[te_0p3_labppo_scintillator_Oct2012] SCINTWAVEFORMalpha_value1 [ -4.6d, -18d, -156d,]"
        alphaLine2 = "/rat/db/set OPTICS[te_0p3_labppo_scintillator_Oct2012] SCINTWAVEFORMalpha_value2 [ 0.71d, 0.22d, 0.07d,]"
    else:
        alphaLine1 = ""
        alphaLine2 = ""

    fileName = options.scintMaterial + "-" + options.timingProfile
    
    inFile = open("Base.mac", "r")
    rawText = string.Template(inFile.read())
    inFile.close()
    
    infile2 = open("Template_Submit.sh", "r")
    rawText2 = string.Template(infile2.read())
    infile2.close()
    
    outText = rawText.substitute(GeoFile = options.geoFile,
                                 ScintMaterial = options.scintMaterial,
                                 AlphaWaveFormLine1 = alphaLine1,
                                 AlphaWaveFormLine2 = alphaLine2,
                                 OutFileName = fileName + ".root")
    outFile = open(fileName + ".mac", "w")
    outFile.write(outText)
    outFile.close()

    outText2 = rawText2.substitute(envronLoc = Utilities.envronLoc,
                                   currentLoc = Utilities.currentLoc,
                                   runCommand = "rat " + fileName + ".mac")
    outFile2 = open(fileName + ".sh", "w")
    outFile2.write(outText2)
    outFile2.close()

    print "Running " + fileName + ".mac via " + fileName + ".sh and generating " + fileName + ".root"
    os.system("qsub " + fileName + ".sh")
            

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File - geo/[geometry file], default = snoplus.geo", default = "geo/snoplus.geo")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material, default = te_0p3_labppo_scintillator_Oct2012", default = "te_0p3_labppo_scintillator_Oct2012")
    parser.add_option("-p", type = "string", dest = "timingProfile", help = "Timing Profile, default = 'PSD' or No Pulse Shape Discrimination = 'noPSD'", default = "PSD")
    (options, args) = parser.parse_args()
    ProduceRunMacFiles(options)
    
