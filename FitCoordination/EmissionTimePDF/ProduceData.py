#!/usr/bin/env python
import os, sys, string
# Author P G Jones - 22/03/2012 <p.g.jones@qmul.ac.uk>
#        K Majumdar - 08/09/2014 - Cleanup of Coordinators for new DS


def ProduceRunMacros(options):

    if options.batch:
        print "Batch mode is not required for this FitCoordinator"
    
    # Load any extra .ratdb files
    extraDB = ""
    if options.loadDB:
        extraDB = "/rat/db/load " + options.loadDB

    # Load the macro
    inFile1 = open("Template_Macro.mac", "r")
    rawText1 = string.Template(inFile1.read())
    inFile1.close()
	
    outText1 = rawText1.substitute(ExtraDB = extraDB,
                                   GeoFile = options.geoFile,
                                   ScintMaterial = options.scintMaterial,
                                   Particle = options.particle)
    outFile1 = open("events_WithTracks.mac", "w")
    outFile1.write(outText1)
    outFile1.close()
	
    os.system("rat events_WithTracks.mac")
    os.remove("events_WithTracks.mac")


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the macros in Batch mode")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use - location relative to rat/data/, default = geo/snoplus.geo", default = "geo/snoplus.geo")
    parser.add_option("-l", type = "string", dest = "loadDB", help = "Load an extra .ratdb directory")
    parser.add_option("-p", type = "string", dest = "particle", help = "Particle type to use (see generator documentation for available particles), default = 'e-'", default = "e-")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = labppo_scintillator", default = "labppo_scintillator")
    (options, args) = parser.parse_args()
    ProduceRunMacros(options)

