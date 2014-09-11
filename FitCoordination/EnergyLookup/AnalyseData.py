#!/usr/bin/env python
import string, ROOT, Utilities, sys, os
# Author P G Jones - 12/09/2011 <p.g.jones@qmul.ac.uk>
#        K Majumdar - 09/09/2014 - Cleanup of Coordinators for new DS


def AnalyseRootFiles(options):

    # Load any parameters for running the macros on a Batch system
    batch_params = None
    if options.batch:
        batch_params = {}
    execfile(options.batch, {}, batch_params)
	
    # Load the batch submission script template
    inFile = open("Template_Batch.sh", "r")
    rawText = string.Template(inFile.read())
    inFile.close()
		
    # Run the analysis on a Batch system
    if options.batch:
        outText = rawText.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                     Ratenv = batch_params['ratenv'],
                                     Cwd = os.environ['PWD'].replace("/.", "/"),
                                     RunCommand = "python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.index + "\", \"" + options.scintMaterial + "\")'")
        outFile = open("AnalyseData.sh", "w")
        outFile.write(outText)
        outFile.close()
		
        os.system(batch_params["submit"] + " AnalyseData.sh")
		
    # Else run the macro locally on an interactive machine				
    else:
        os.system("python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.index + "\", \"" + options.scintMaterial + "\")'")
		

# returns the Nhits vs. Position/Energy table
def AnalysisFunction(index, material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = Utilities.WaterEnergies
    else:
        energies = Utilities.ScintEnergies
	
    nHitsTable = Utilities.NhitsVsPositionEnergy(material)
	
    print "\n"
    print "Please place the text below into the database file: FIT_ENERGY_LOOKUP.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "name: \"FIT_ENERGY_LOOKUP\","
    print "index: \"" + index + "\","
    print "valid_begin: [0, 0],"
    print "valid_end: [0, 0],"
    print "\n",
    
    print "energies: [0.0d,",
    for energy in energies:
        print str(energy) + "d,",
    print "],"

    print "radii: [",
    for position in Utilities.Positions:
        print str(position) + "d,",
    print "],"

    print "nhit_energy_radius: [",
    for singlePositionNhitsTable in nHitsTable:
        print "0.0d, ",
        for nHits in singlePositionNhitsTable:
            print nHits + "d, ",
    print "],"
    
    print "}"
    print "\n"


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the macros in Batch mode")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = labppo_scintillator", default = "labppo_scintillator")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)

