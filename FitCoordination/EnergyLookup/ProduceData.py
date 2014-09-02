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

    # load any batch options
    batch_params = None
    if options.batch:
        batch_params = {}
        execfile( options.batch, {}, batch_params )

    inFile = open( "batch.sh", "r" )
    rawScriptText = string.Template( inFile.read() )
    inFile.close()

    extraDB = ""
    if options.loadDB:
        extraDB = "/rat/db/load " + options.loadDB
    
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
                                         OutFileName = outFileName + ".root",
                                         ExtraDB = extraDB) # Note upper/lower case first letter...
            outFile = open(outFileName + ".mac", "w")
            outFile.write(outText)
            outFile.close()

            print "Running " + outFileName

            if options.batch:
                # run the macro on a batch system 
                outText = rawScriptText.substitute( Preamble = "\n".join(s for s in batch_params['preamble']),
                                                    Cwd = os.environ['PWD'].replace("/.", "/"),
                                                    Macro = outFileName + ".mac",
                                                    Ratenv = batch_params['ratenv'] )
                outFile = open(outFileName + ".sh", "w")
                outFile.write(outText)
                outFile.close()
                os.system( batch_params["submit"] + " " + outFileName + ".sh" )

            else:
                # run the macro locally
                os.system("rat " + outFileName + ".mac")
                # Now delete the temporary mac file
                os.remove(outFileName + ".mac")


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version="%prog 1.0")
    parser.add_option("-g", type="string", dest="geoFile", help="Geometry File to use, location must be absolute or relative to target.",
                      default="geo/snoplus.geo")
    parser.add_option("-s", type="string", dest="scintMaterial", help="Scintillator material.", default="labppo_scintillator")
    parser.add_option("-p", type="string", dest="particle", help="Particle type.", default="e-")
    parser.add_option("-e", type="string", dest="energies", help="Energies (accepts a list)",
                      action="callback", callback=EnergyLookupUtil.parse_list_arg)
    parser.add_option("-x", type="string", dest="positions", help="Positions (accepts a list)",
                      action="callback", callback=EnergyLookupUtil.parse_list_arg)
    parser.add_option("-b", type="string", dest="batch", help="Run in batch mode" )
    parser.add_option("-l", type="string", dest="loadDB", help="Load an extra DB directory")
    (options, args) = parser.parse_args()
    ProduceRunFiles(options)
