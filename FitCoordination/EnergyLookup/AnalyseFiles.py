#!/usr/bin/env python
# Returns the nhitpermev in ratdb format
# Author P G Jones - 13/09/2011 <p.jones22@physics.ox.ac.uk>
import string
import ROOT
import EnergyLookupUtil
import sys

def AnalyseFiles(options):

    if options.energies:
        EnergyLookupUtil.SetEnergies(options.energies)
    if options.positions:
        EnergyLookupUtil.SetPositions(options.positions)

    nhitPerMeVtable = EnergyLookupUtil.NhitPerMeVPosEnergy()
    print "{\nname: \"FIT_ENERGY_LOOKUP\","
    print "index: \"%s\"," % options.index
    print "valid_begin : [0, 0],\nvalid_end : [0, 0],"
    
    print "energies: [0.0d,",
    for energy in EnergyLookupUtil.EnergySet:
        outText = "%f" % energy
        outText = ToRATDB(outText)
        sys.stdout.write(outText)
    print "],"

    print "radii: [",
    for pos in EnergyLookupUtil.PosSet:
        outText = "%f" % pos
        outText = ToRATDB(outText)
        sys.stdout.write(outText)
    print "],"

    print "nhit_energy_radius: [",
    for energyList in nhitPerMeVtable:
        sys.stdout.write("0.0d, ")
        for nhit in energyList:
            outText = "%e" % nhit
            outText = ToRATDB(outText)
            sys.stdout.write(outText)
    print "],"
    print "}"
    return

def ToRATDB(inText):
    outText = ""
    if(inText.find("e") != -1):
        outText = outText + inText.replace("e", "d") + ", "
    else:
        outText = outText + inText + "d, "
    return outText
    
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage = "usage: %prog [options] target", version="%prog 1.0")
    parser.add_argument("-i", type=str, dest="index", help="RATDB index to place result.", default="")
    parser.add_argument("-e", type=float, dest="energies", help="Energies (accepts a list)", default=None, nargs="+")
    parser.add_argument("-x", type=float, dest="positions", help="Positions (accepts a list)", default=None, nargs="+")
    args = parser.parse_args()
    AnalyseFiles(args)
                    
