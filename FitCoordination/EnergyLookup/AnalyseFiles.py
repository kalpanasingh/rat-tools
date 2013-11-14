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
    EnergyLookupUtil.SetMaterial(options.scintMaterial)

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
    
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version="%prog 1.0")
    parser.add_option("-i", type="string", dest="index", help="RATDB index to place result.", default="")
    parser.add_option("-s", type="string", dest="scintMaterial", help="Scintillator material.", default="labppo_scintillator")
    parser.add_option("-e", type="string", dest="energies", help="Energies (accepts comma delimited list)",
                      action="callback", callback=EnergyLookupUtil.parse_list_arg)
    parser.add_option("-x", type="string", dest="positions", help="Positions (accepts comma delimited list)",
                      action="callback", callback=EnergyLookupUtil.parse_list_arg)
    (options, args) = parser.parse_args()
    AnalyseFiles(options)
                    
