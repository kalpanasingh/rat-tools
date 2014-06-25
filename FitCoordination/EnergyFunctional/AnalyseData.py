#!usr/bin/env python
import string, Utilities
# Author K Majumdar - 25/06/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


# returns the parameters for the Functional Form of Energy Reconstruction in the form of a complete RATDB entry
def AnalyseRootFiles(options):
    
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

	##############################

    Utilities.PlotsForAlphas()
    alphaParameters = Utilities.ExtractAlphaParameters()

    alphaStringList = []
    for alpha in alphaParameters:
        alphaString = str(alpha)
        if (alphaString.find("e") == -1):
            alphaString += "d, "
        else:
            alphaString = alphaString.replace("e", "d") + ", "
        alphaStringList.append(alphaString)

    diagFile.write("alpha: ["),
    for alpha in alphaStringList:
        diagFile.write(alpha)
    diagFile.write("], \n")

	##############################

    Utilities.PlotsForBetas(alphaParameters)
    betaParameters = Utilities.ExtractBetaParameters()
	
    betaStringList = []
    for beta in betaParameters:
        betaString = str(beta)
        if (betaString.find("e") == -1):
            betaString += "d, "
        else:
            betaString = betaString.replace("e", "d") + ", "
        betaStringList.append(betaString)

    diagFile.write("betaLowRadius: ["),
    for index in range(0, Utilities.numberOfParameters[1]):
         diagFile.write(betaStringList[index])
    diagFile.write("], \n")

    diagFile.write("betaMidRadiusCut: " + str(Utilities.fitRangeHigh[1]) + "d, \n")
    diagFile.write("betaMidRadius: ["),
    for index in range(Utilities.numberOfParameters[1], (Utilities.numberOfParameters[1] + Utilities.numberOfParameters[2])):
         diagFile.write(betaStringList[index])
    diagFile.write("], \n")
    
    diagFile.write("betaHighRadiusCut: " + str(Utilities.fitRangeHigh[2]) + "d, \n")
    diagFile.write("betaHighRadius: ["),
    for index in range((Utilities.numberOfParameters[1] + Utilities.numberOfParameters[2]), len(betaStringList)):
         diagFile.write(betaStringList[index])
    diagFile.write("], \n")

	##############################

    Utilities.PlotsForGammas(alphaParameters, betaParameters)
    gammaParameters = Utilities.ExtractGammaParameters()

    gammaStringList = []
    for gamma in gammaParameters:
        gammaString = str(gamma)
        if (gammaString.find("e") == -1):
            gammaString += "d, "
        else:
            gammaString = gammaString.replace("e", "d") + ", "
        gammaStringList.append(gammaString)

    diagFile.write("gamma: ["),
    for index in range(0, Utilities.numberOfParameters[4]):
         diagFile.write(gammaStringList[index])
    diagFile.write("], \n")

	##############################

    diagFile.write("} \n")
    diagFile.write("\n")

    diagFile.close()



import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)

