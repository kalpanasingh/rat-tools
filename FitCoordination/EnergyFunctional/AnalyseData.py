#!usr/bin/env python
import string, Utilities
# Author K Majumdar - 04/09/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


# returns the parameters for the Functional Form of Energy Reconstruction in the form of a complete RATDB entry
def AnalyseRootFiles(options):
    
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
    diagFile.write("index: \"" + options.index + "\", \n")
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
    for index in range(0, Utilities.numberOfRadiusCoeffs_Low):
        diagFile.write(radiusCoeffStrings[index])
    diagFile.write("], \n")
    diagFile.write("midRadiusCut: " + str(Utilities.radiusFitRange_Mid[0]) + "d, \n")
    diagFile.write("radiusCoeffsMid: ["),
    for index in range(Utilities.numberOfRadiusCoeffs_Low, (Utilities.numberOfRadiusCoeffs_Low + Utilities.numberOfRadiusCoeffs_Mid)):
        diagFile.write(radiusCoeffStrings[index])
    diagFile.write("], \n")	
    diagFile.write("highRadiusCut: " + str(Utilities.radiusFitRange_High[0]) + "d, \n")
    diagFile.write("radiusCoeffsHigh: ["),
    for index in range((Utilities.numberOfRadiusCoeffs_Low + Utilities.numberOfRadiusCoeffs_Mid), len(radiusCoeffStrings)):
        diagFile.write(radiusCoeffStrings[index])
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
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)

