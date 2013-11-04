#!/usr/bin/env python
import os
import sys
import string
import optparse


def ProduceRunMacFile(options):
        """Produces and then runs the appropriate mac files."""
        inFile = open("Data_for_PDF.mac", "r")
        rawText = string.Template(inFile.read())
        inFile.close()
        energy = "3.0"
        if options.scintMaterial=="lightwater_sno":
            energy = "8.0"        
        outText = rawText.substitute(GeoFile = options.geoFile,
                                     ScintMaterial = options.scintMaterial,
                                     Particle = options.particle,
                                     Energy = energy
                                     )
        print outText
        outFileName = "Data_for_PDF__" + options.scintMaterial + ".mac"
        outFile = open(outFileName, "w")
        outFile.write(outText)
        outFile.close()
        rootFileName = "HitTime_%s_%d" % (options.scintMaterial, options.runNumber)
        os.system("rat -o %s -N %d %s" % (rootFileName, options.nEvents, outFileName))
        os.remove(outFileName)


if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version="%prog 1.0")
    parser.add_option("-g", type="string", dest="geoFile", help="Geometry File to use, location must be absolute or relative to target.", default="geo/snoplus.geo")
    parser.add_option("-s", type="string", dest="scintMaterial", help="Scintillator material.", default="labppo_scintillator")
    parser.add_option("-p", type="string", dest="particle", help="Particle type.", default="e-")
    parser.add_option("-r", type="int", dest="runNumber", help="Run number (if splitting jobs)", default=1)
    parser.add_option("-n", type="int", dest="nEvents", help="Number of events [100000]", default=100000)
    (options, args) = parser.parse_args()
    ProduceRunMacFile(options)
