#!/usr/bin/env python
import os
import sys
import string
import optparse
import HitTimePDFUtil


def ProduceRunMacFile(options):
    """Produces and then runs the appropriate mac files."""

    batch_params = None
    if options.batch:
        batch_params = {}
	execfile( options.batch, {}, batch_params )

    inFile = open("Data_for_PDF.mac", "r")
    rawText = string.Template(inFile.read())
    inFile.close()

    inFile = open( "batch.sh", "r" )
    rawScriptText = string.Template( inFile.read() )
    inFile.close()

    energy = "3.0"
    if options.scintMaterial=="lightwater_sno":
        energy = "8.0"

    extraDB = ""
    if options.loaddb:
	    extraDB = "/rat/db/load %s" % options.loaddb

    outText = rawText.substitute(GeoFile = options.geoFile,
				 ScintMaterial = options.scintMaterial,
				 Particle = options.particle,
				 Energy = energy,
				 ExtraDB = extraDB
				 )

    outFileName = "Data_for_PDF__" + options.scintMaterial + ".mac"
    outFile = open(outFileName, "w")
    outFile.write(outText)
    outFile.close()

    if options.batch:

        numberOfRuns = HitTimePDFUtil.totalEvents / HitTimePDFUtil.batchEventsPerFile
	remainder = HitTimePDFUtil.totalEvents % HitTimePDFUtil.batchEventsPerFile
	if remainder != 0:
            numberOfRuns += 1

        for run in range(numberOfRuns):
	    rootFileName = "HitTime_%s_%d" % (options.scintMaterial, run+1)
            outText = rawScriptText.substitute( Preamble = "\n".join(s for s in batch_params['preamble']),
                                                Cwd = os.environ['PWD'].replace("/.", "/"),
                                                Macro = outFileName,
                                                Ratenv = batch_params['ratenv'],
						Output = rootFileName,
						Nevents = str(HitTimePDFUtil.batchEventsPerFile)
						)
            outScriptName = "HitTime_%s_%d.sh" % (options.scintMaterial, run+1)
            outScript = open( outScriptName, "w" )
            outScript.write( outText )
            outScript.close()

	    os.system( batch_params["submit"] + " " + outScriptName )

    else:
        rootFileName = "HitTime_%s_0" % (options.scintMaterial)
	os.system("rat -o %s -N %d %s" % (rootFileName, HitTimePDFUtil.totalEvents, outFileName))
	os.remove(outFileName)


if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version="%prog 1.0")
    parser.add_option("-g", type="string", dest="geoFile", help="Geometry File to use, location must be absolute or relative to target.", default="geo/snoplus.geo")
    parser.add_option("-s", type="string", dest="scintMaterial", help="Scintillator material.", default="labppo_scintillator")
    parser.add_option("-p", type="string", dest="particle", help="Particle type.", default="e-")
    parser.add_option("-b", type="string", dest="batch", help="Run in batch mode" )
    parser.add_option("-l", type="string", dest="loaddb", help="Load an extra DB directory")
    (options, args) = parser.parse_args()
    ProduceRunMacFile(options)
