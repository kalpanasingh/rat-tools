#!/usr/bin/env python
import os, sys, string

def ProduceRunMacros(options):
    
    # Load any parameters for running the macros on a Batch system
    batch_params = None
    if options.batch:
        batch_params = {}
        execfile(options.batch, {}, batch_params)

    # Load any extra .ratdb files
    extraDB = ""
    if options.loadDB:
        extraDB = "/rat/db/load " + options.loadDB

    # Load the basic macro template
    inFile1 = open("Template_Macro.mac", "r")
    rawText1 = string.Template(inFile1.read())
    inFile1.close()
	
    # Load the batch submission script template
    inFile2 = open("Template_Batch.sh", "r")
    rawText2 = string.Template(inFile2.read())
    inFile2.close()
    
    # Generate the two macros (one for alphas, one for betas)
    macros = {"NearAVANNAlphas.mac": {"generator": "gun",
                                      "vertex": "alpha 0 0 0 5.3",
                                      "hadrons": ""},
              "NearAVANNBetas.mac": {"generator": "gun2",
                                     "vertex": "e- 0 0 0 0 0.2 3.0",
                                     "hadrons": "/rat/physics_list/OmitHadronicProcesses true"}}
    for macroName, config in macros.iteritems():
        outText1 = rawText1.substitute(ExtraDB = extraDB,
                                       GeoFile = options.geoFile,
                                       ScintMaterial = options.scintMaterial,
                                       Generator = config["generator"],
                                       Vertex = config["vertex"],
                                       Hadrons = config["hadrons"])
        outFile1 = open(macroName, "w")
        outFile1.write(outText1)
        outFile1.close()
    
    # Generate 20k training, 10k cross validation entries, 5k alphas
    runs = [('training_{0}'.format(i), 'NearAVANNBetas.mac') for i in range(20)] +\
        [('crossval_{0}'.format(i), 'NearAVANNBetas.mac') for i in range(10)] +\
        [('alphas_{0}'.format(i), 'NearAVANNAlphas.mac') for i in range(5)]

    for (run, macroName) in runs:
        outName = "NearAVANN_{0}".format(run)
        if options.batch:
            # Run the macro on a Batch system
            outText2 = rawText2.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                           Ratenv = batch_params['ratenv'],
                                           Cwd = os.environ['PWD'].replace("/.", "/"),
                                           RunCommand = "rat -o " + outName + ".root " + macroName)
            outFile2 = open(outName + ".sh", "w")
            outFile2.write(outText2)
            outFile2.close()
			
            os.system( batch_params["submit"] + " " + outName +".sh" )        
				
        # Else run the macro locally on an interactive machine				
        else:
            os.system("rat -o " + outName + ".root" + macroName)


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the macros in Batch mode")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use - location relative to rat/data/, default = geo/snoplus.geo", default = "geo/snoplus.geo")
    parser.add_option("-l", type = "string", dest = "loadDB", help = "Load an extra .ratdb directory")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = labppo_scintillator", default = "labppo_scintillator")
    (options, args) = parser.parse_args()
    ProduceRunMacros(options)

