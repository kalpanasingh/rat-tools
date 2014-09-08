#!usr/bin/env python
import Utilities, os
# Author E Marzece - 13/03/2014 <marzece@sas.upenn.edu>
#        K Majumdar - 08/09/2014 - Cleanup of Coordinators for new DS


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
                                     RunCommand = "python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.particle + "\", \"" + options.scintMaterial + "\")'")
        outFile = open("AnalyseData.sh", "w")
        outFile.write(outText)
        outFile.close()
		
        os.system(batch_params["submit"] + " AnalyseData.sh")
		
    # Else run the macro locally on an interactive machine				
    else:
        os.system("python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.particle + "\", \"" + options.scintMaterial + "\")'")
		

def AnalysisFunction(particle, material):

    pdfs = {}
    particleNames = Utilities.ParticleNames[particle]
	
    for particleIndex, particle in enumerate(particleNames):
	
        for pulseIndex, pulseDescription in enumerate(Utilities.ParticlePulseDict[particle]):
		
            infileName = particle + pulseDescription
            pdfs[infileName] = Utilities.ProduceTimeResidualPDF(infileName + ".root")
			
    outfileName = "AlphaBetaOutput" + particle + ".txt"
    print "The relevant PDFs for the AlphaBetaClassifier have been output to:  " + str(outfileName) 
    print "Please replace any existing entry that has the same index in the database file: ALPHA_BETA_CLASSIFIER.ratdb located in rat/data with the text found in this textfile"

    f = open(outfileName, 'w')
    for pulseIndex, pulseDescription in enumerate(Utilities.ParticlePulseDict[particleNames[1]]):
        Utilities.OutputFileChunk([pdfs[particleNames[0]], pdfs[particleNames[1] + pulseDescription], pdfs[particleNames[2]]], particle, material, pulseDescription, f)
    f.close()
	
	
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the macros in Batch mode")
    parser.add_option("-p", type = "string", dest = "particle", help = "Desired Isotope - either 212 or 214", default = "")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = labppo_scintillator", default = "labppo_scintillator")
    (options, args) = parser.parse_args()
    if options.particle == "212" or options.particle == "214": 
        AnalyseRootFiles(options)
    else:
        print "You must specify if you want to generate PDFs for Bi212 or Bi214.  This can be done by adding the option -p IsotopeNumber to your command."
		
