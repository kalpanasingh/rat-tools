#!usr/bin/env python
import string, Utilities, os
# Author K Majumdar - 08/09/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


def AnalyseRootFiles(options):

    # Load any parameters for running the macros on a Batch system
    batch_params = None
    if options.batch:
        batch_params = {}
    execfile(options.batch, {}, batch_params)
	
	# Load the batch submission script template
    inFile = open("Template_Submit.sh", "r")
    rawText = string.Template(inFile.read())
    inFile.close()
		
    # Run the analysis on a Batch system
    if options.batch:
        outText = rawText.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                     Ratenv = batch_params['ratenv'],
                                     Cwd = os.environ['PWD'].replace("/.", "/"),
                                     RunCommand = "python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.index + "\")'")
        outFile = open("AnalyseData.sh", "w")
        outFile.write(outText)
        outFile.close()
		
        os.system(batch_params["submit"] + " AnalyseData.sh")
		
    # Else run the macro locally on an interactive machine				
    else:
        os.system("python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.index + "\")'")
		

# returns the parameters for the Functional Form of Energy Reconstruction in the form of a complete RATDB entry
def AnalysisFunction(index):
    
    Utilities.PlotsForEnergyCoeffs()
    energyCoefficients = Utilities.ExtractEnergyCoeffs()

    Utilities.PlotsForRadiusCoeffs(energyCoefficients)
    radiusCoefficients = Utilities.ExtractRadiusCoeffs()
	
    Utilities.PlotsForZCoeffs(energyCoefficients, radiusCoefficients)
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
    energyCoeffStrings = []
    for coeff in energyCoefficients:
        coeffString = str(coeff)
        if (coeffString.find("e") == -1):
            coeffString += "d, "
        else:
            coeffString = coeffString.replace("e", "d") + ", "
        diagFile.write(coeffString)
    diagFile.write("], \n")

    radiusCoeffStrings = []
    for coeff in radiusCoefficients:
        coeffString = str(coeff)
        if (coeffString.find("e") == -1):
            coeffString += "d, "
        else:
            coeffString = coeffString.replace("e", "d") + ", "
        radiusCoeffStrings.append(coeffString)

    diagFile.write("radiusCoeffsLow: ["),
    for coeff in range(0, Utilities.numberOfRadiusCoeffs_Low):
        diagFile.write(radiusCoeffStrings[coeff])
    diagFile.write("], \n")
    diagFile.write("midRadiusCut: " + str(Utilities.radiusFitRange_Mid[0]) + "d, \n")
    diagFile.write("radiusCoeffsMid: ["),
    for coeff in range(Utilities.numberOfRadiusCoeffs_Low, (Utilities.numberOfRadiusCoeffs_Low + Utilities.numberOfRadiusCoeffs_Mid)):
        diagFile.write(radiusCoeffStrings[coeff])
    diagFile.write("], \n")	
    diagFile.write("highRadiusCut: " + str(Utilities.radiusFitRange_High[0]) + "d, \n")
    diagFile.write("radiusCoeffsHigh: ["),
    for coeff in range((Utilities.numberOfRadiusCoeffs_Low + Utilities.numberOfRadiusCoeffs_Mid), len(radiusCoeffStrings)):
        diagFile.write(radiusCoeffStrings[coeff])
    diagFile.write("], \n")	

    diagFile.write("zCoeffs: ["),
    zCoeffStrings = []
    for coeff in zCoefficients:
        coeffString = str(coeff)
        if (coeffString.find("e") == -1):
            coeffString += "d, "
        else:
            coeffString = coeffString.replace("e", "d") + ", "
        diagFile.write(coeffString)
    diagFile.write("], \n")
	
    diagFile.write("} \n")
    diagFile.write("\n")

    diagFile.close()



import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the macros in Batch mode")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)

