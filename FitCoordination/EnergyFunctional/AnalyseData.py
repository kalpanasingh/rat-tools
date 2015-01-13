#!usr/bin/env python
import string, Utilities, os
# Author K Majumdar - 11/01/2015 <Krishanu.Majumdar@physics.ox.ac.uk>


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
		
    # Else run the analysis locally on an interactive machine				
    else:
        os.system("python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.index + "\", \"" + options.scintMaterial + "\")'")
		

# returns the parameters for the Functional Form of Energy Reconstruction in the form of a complete RATDB entry
def AnalysisFunction(index, material):
    
    Utilities.PlotsForEnergyCoeffs(0, material)
    Utilities.PlotsForEnergyCoeffs(1, material)
    energyCoefficients = Utilities.ExtractEnergyCoeffs(material)

    Utilities.PlotsForRadiusCoeffs(energyCoefficients, material)
    radiusCoefficients = Utilities.ExtractRadiusCoeffs()
	
    Utilities.PlotsForZCoeffs(energyCoefficients, radiusCoefficients, material)
    zCoefficients = Utilities.ExtractZCoeffs()
	
	##############################
	
    diagFileName = Utilities.baseFileName + "Output.txt"
    diagFile = open(diagFileName, "w")

    diagFile.write("\n \n")
    diagFile.write("Please place the text below into the database file: FIT_ENERGY_FUNCTIONAL.ratdb located in rat/data, replacing any existing entry with the same index.")
    diagFile.write("\n \n")
    diagFile.write("{ \n")
    diagFile.write("name: \"FIT_ENERGY_FUNCTIONAL\", \n")
    diagFile.write("index: \"" + index + "\", \n")
    diagFile.write("valid_begin: [0, 0], \n")
    diagFile.write("valid_end: [0, 0], \n")
    diagFile.write("\n")

    diagFile.write("energyCoeffs: ["),
    for coeff in energyCoefficients:
        diagFile.write(str(coeff) + ", ")
    diagFile.write("], \n")

    radiusCoeffStrings = []
    for coeff in radiusCoefficients:
        radiusCoeffStrings.append(str(coeff) + ", ")

    diagFile.write("radiusCoeffsInternalLow: ["),
    for coeff in range(0, Utilities.numberOfRadiusCoeffs_Internal_Low):
        diagFile.write(radiusCoeffStrings[coeff])
    diagFile.write("], \n")
    diagFile.write("internalMidRadiusCut: " + str(Utilities.radiusFitRange_Internal_Mid[0]) + ", \n")
    diagFile.write("radiusCoeffsInternalMid: ["),
    for coeff in range(Utilities.numberOfRadiusCoeffs_Internal_Low, (Utilities.numberOfRadiusCoeffs_Internal_Low + Utilities.numberOfRadiusCoeffs_Internal_Mid)):
        diagFile.write(radiusCoeffStrings[coeff])
    diagFile.write("], \n")	
    diagFile.write("internalHighRadiusCut: " + str(Utilities.radiusFitRange_Internal_High[0]) + ", \n")
    diagFile.write("radiusCoeffsInternalHigh: ["),
    for coeff in range((Utilities.numberOfRadiusCoeffs_Internal_Low + Utilities.numberOfRadiusCoeffs_Internal_Mid), (Utilities.numberOfRadiusCoeffs_Internal_Low + Utilities.numberOfRadiusCoeffs_Internal_Mid + Utilities.numberOfRadiusCoeffs_Internal_High)):
        diagFile.write(radiusCoeffStrings[coeff])
    diagFile.write("], \n")
    diagFile.write("externalLowRadiusCut: " + str(Utilities.radiusFitRange_External_Low[0]) + ", \n")
    diagFile.write("radiusCoeffsExternalLow: ["),
    for coeff in range((Utilities.numberOfRadiusCoeffs_Internal_Low + Utilities.numberOfRadiusCoeffs_Internal_Mid + Utilities.numberOfRadiusCoeffs_Internal_High), (Utilities.numberOfRadiusCoeffs_Internal_Low + Utilities.numberOfRadiusCoeffs_Internal_Mid + Utilities.numberOfRadiusCoeffs_Internal_High + Utilities.numberOfRadiusCoeffs_External_Low)):
        diagFile.write(radiusCoeffStrings[coeff])
    diagFile.write("], \n")		
    diagFile.write("externalHighRadiusCut: " + str(Utilities.radiusFitRange_External_High[0]) + ", \n")
    diagFile.write("radiusCoeffsExternalHigh: ["),
    for coeff in range((Utilities.numberOfRadiusCoeffs_Internal_Low + Utilities.numberOfRadiusCoeffs_Internal_Mid + Utilities.numberOfRadiusCoeffs_Internal_High + Utilities.numberOfRadiusCoeffs_External_Low), len(radiusCoeffStrings)):
        diagFile.write(radiusCoeffStrings[coeff])
    diagFile.write("], \n")
	
    diagFile.write("lowZLimit: " + str(Utilities.zFitRange[0]) + ", \n")
    diagFile.write("highZLimit: " + str(Utilities.zFitRange[1]) + ", \n")
    diagFile.write("zCoeffs: ["),
    zCoeffStrings = []
    for coeff in zCoefficients:
        diagFile.write(str(coeff) + ", ")
    diagFile.write("], \n")
	
    diagFile.write("} \n")
    diagFile.write("\n")

    diagFile.close()



import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the analysis in Batch mode")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material to use, default = labppo_scintillator", default = "labppo_scintillator")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)

