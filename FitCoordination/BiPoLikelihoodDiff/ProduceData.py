#!/usr/bin/env python
import os, sys, string
# Author K Majumdar - 05/09/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


def ProduceRunMacros(options):
    
    if (options.isotope == ""):
        print "An Isotope option (-p) must be specified for this Production Script: either '212' or '214' ... exiting"
        sys.exit()

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
    inFile2 = open("Template_Submit.sh", "r")
    rawText2 = string.Template(inFile2.read())
    inFile2.close()
	
    ##############################
	
    outTextTe1 = rawText1.substitute(Hadrons = "/rat/physics_list/OmitHadronicProcesses true",
                                     ExtraDB = extraDB,
                                     GeoFile = options.geoFile,
                                     ScintMaterial = options.scintMaterial,
                                     FileName = "130Te_NDBD.root",
                                     Generator = "gun",
                                     Vertex = "e- 0 0 0 2.527")
    outFileTe1 = open("130Te_NDBD.mac", "w")
    outFileTe1.write(outTextTe1)
    outFileTe1.close()

    print "Running 130Te_NDBD.mac and generating 130Te_NDBD.root"
	            
    # Run the macro on a Batch system
    if options.batch:
        outTextTe2 = rawText2.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                         Ratenv = batch_params['ratenv'],
                                         Cwd = os.environ['PWD'].replace("/.", "/"),
                                         RunCommand = "rat 130Te_NDBD.mac")
        outFileTe2 = open("130Te_NDBD.sh", "w")
        outFileTe2.write(outTextTe2)
        outFileTe2.close()

        os.system(batch_params["submit"] + " 130Te_NDBD.sh")
				
    # Else run the macro locally on an interactive machine				
    else:
        os.system("rat 130Te_NDBD.mac")
        # delete the macro when running is complete
        os.remove("130Te_NDBD.mac")
		
    ##############################
	
    outfileNameBi = options.isotope + "Bi_Beta"
	
    outTextBi1 = rawText1.substitute(Hadrons = "/rat/physics_list/OmitHadronicProcesses true",
                                     ExtraDB = extraDB,
                                     GeoFile = options.geoFile,
                                     ScintMaterial = options.scintMaterial,
                                     FileName = outfileNameBi + ".root",
                                     Generator = "decay0",
                                     Vertex = "backg Bi" + options.isotope)
    outFileBi1 = open(outfileNameBi + ".mac", "w")
    outFileBi1.write(outTextBi1)
    outFileBi1.close()
	
    print "Running " + outfileNameBi + ".mac and generating " + outfileNameBi + ".root"
           
    # Run the macro on a Batch system
    if options.batch:
        outTextBi2 = rawText2.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                         Ratenv = batch_params['ratenv'],
                                         Cwd = os.environ['PWD'].replace("/.", "/"),
                                         RunCommand = "rat " + outfileNameBi + ".mac")
        outFileBi2 = open(outfileNameBi + ".sh", "w")
        outFileBi2.write(outTextBi2)
        outFileBi2.close()

        os.system(batch_params["submit"] + " " + outfileNameBi + ".sh")
				
    # Else run the macro locally on an interactive machine				
    else:
        os.system("rat " + outfileNameBi + ".mac")
        # delete the macro when running is complete
        os.remove(outfileNameBi + ".mac")
		
    ##############################
	
    outfileNamePo = options.isotope + "Po_Alpha"
	
    outTextPo1 = rawText1.substitute(Hadrons = "",
                                     ExtraDB = extraDB,
                                     GeoFile = options.geoFile,
                                     ScintMaterial = options.scintMaterial,
                                     FileName = outfileNamePo + ".root",
                                     Generator = "decay0",
                                     Vertex = "backg Po" + options.isotope)
    outFilePo1 = open(outfileNamePo + ".mac", "w")
    outFilePo1.write(outTextPo1)
    outFilePo1.close()
	
    print "Running " + outfileNamePo + ".mac and generating " + outfileNamePo + ".root"
           
    # Run the macro on a Batch system
    if options.batch:
        outTextPo2 = rawText2.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                         Ratenv = batch_params['ratenv'],
                                         Cwd = os.environ['PWD'].replace("/.", "/"),
                                         RunCommand = "rat " + outfileNamePo + ".mac")
        outFilePo2 = open(outfileNamePo + ".sh", "w")
        outFilePo2.write(outTextPo2)
        outFilePo2.close()

        os.system(batch_params["submit"] + " " + outfileNamePo + ".sh")
				
    # Else run the macro locally on an interactive machine				
    else:
        os.system("rat " + outfileNamePo + ".mac")
        # delete the macro when running is complete
        os.remove(outfileNamePo + ".mac")



import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the macros in Batch mode")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use - location relative to rat/data/, default = geo/snoplus.geo", default = "geo/snoplus.geo")
    parser.add_option("-l", type = "string", dest = "loadDB", help = "Load an extra .ratdb directory")
    parser.add_option("-p", type = "string", dest = "isotope", help = "REQUIRED Isotope ('212' or '214')", default = "")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = te_0p3_labppo_scintillator_bisMSB_Dec2013", default = "te_0p3_labppo_scintillator_bisMSB_Dec2013")
    (options, args) = parser.parse_args()
    ProduceRunMacros(options)
    
