#!/usr/bin/env python
import os
import sys
import string
import EnergyLookupUtil
# Author P G Jones - 12/09/2011 <p.jones22@physics.ox.ac.uk>

def ProduceRunFiles(options):
    # Load the raw Base file
    inFile = open("Base.mac", "r")
    rawText = string.Template(inFile.read())
    inFile.close()
    
    # Setup arrays for positions and energies
    if options.energies:
        EnergyLookupUtil.SetEnergies(options.energies)
    if options.positions:
        EnergyLookupUtil.SetPositions(options.positions)
    EnergyLookupUtil.SetMaterial(options.scintMaterial)

    for pos in EnergyLookupUtil.PosSet:
        for energy in EnergyLookupUtil.EnergySet:
            # Set the generator text first
            generator = "/generator/add combo gun:point\n" + \
                "/generator/vtx/set " + options.particle + " 0 0 0 " + str(energy) + "\n" + \
                "/generator/pos/set 0 %.0f 0" % pos 
            # Create the correct file
            outFileName = EnergyLookupUtil.GetFileName(pos, energy)
            outText = rawText.substitute(Generator = generator,
                                         GeoFile = options.geoFile,
                                         ScintMaterial = options.scintMaterial,
                                         OutFileName = outFileName + ".root") # Note upper/lower case first letter...
            outFile = open(outFileName + ".mac", "w")
            outFile.write(outText)
            outFile.close()
            # Now run it
            print "Running " + outFileName
            os.system("rat " + outFileName + ".mac")
            # Now delete the temporary mac file
            os.remove(outFileName + ".mac")


import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage = "usage: %prog [options] target", version="%prog 1.0")
    parser.add_argument("-g", type=str, dest="geoFile", help="Geometry File to use, location must be absolute or relative to target.",
                      default="geo/snoplus.geo")
    parser.add_argument("-s", type=str, dest="scintMaterial", help="Scintillator material.", default="labppo_scintillator")
    parser.add_argument("-p", type=str, dest="particle", help="Particle type.", default="e-")
    parser.add_argument("-e", type=float, dest="energies", help="Energies (accepts a list)", default=None, nargs="+")
    parser.add_argument("-x", type=float, dest="positions", help="Positions (accepts a list)", default=None, nargs="+")
    args = parser.parse_args()
    ProduceRunFiles(args)
