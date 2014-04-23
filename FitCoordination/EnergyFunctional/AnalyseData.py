#!usr/bin/env python
import string, Utilities
# Author K Majumdar - 23/04/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


# returns the parameters for the Functional Form of Energy Reconstruction in the form of a complete RATDB entry
def AnalyseRootFiles(options):
    
    alphaParameters = Utilities.CalculateAlphas()
    alphaStringList = []
    for alpha in alphaParameters:
        alphaString = str(alpha)
        if (alphaString.find("e") == -1):
            alphaString += "d,"
        else:
            alphaString = alphaString.replace("e", "d") + ","
        alphaStringList.append(alphaString)

    betaParameters = Utilities.CalculateBetas(alphaParameters)
    betaStringList = []
    for beta in betaParameters:
        betaString = str(beta)
        if (betaString.find("e") == -1):
            betaString += "d,"
        else:
            betaString = betaString.replace("e", "d") + ","
        betaStringList.append(betaString)

    gammaParameters = Utilities.CalculateGammas(alphaParameters, betaParameters)
    gammaStringList = []
    for gamma in gammaParameters:
        gammaString = str(gamma)
        if (gammaString.find("e") == -1):
            gammaString += "d,"
        else:
            gammaString = gammaString.replace("e", "d") + ","
        gammaStringList.append(gammaString)

    print "\n"
    print "Please place the text below into the database file: FIT_ENERGY_FUNCTIONAL.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "name: \"FIT_ENERGY_FUNCTIONAL\","
    print "index: \"" + options.index + "\","
    print "valid_begin: [0, 0],"
    print "valid_end: [0, 0],"
    print "\n",
    print "alpha0: " + alphaStringList[0]
    print "alpha1: " + alphaStringList[1]
    print "beta0FarAV: " + betaStringList[0]
    print "beta1FarAV: " + betaStringList[1]
    print "beta2FarAV: " + betaStringList[2]
    print "beta0NearAV: " + betaStringList[3]
    print "beta1NearAV: " + betaStringList[4]
    print "beta2NearAV: " + betaStringList[5]
    print "gamma0FarNeck: " + gammaStringList[0]
    print "gamma1FarNeck: " + gammaStringList[1]
    print "gamma0NearNeck: " + gammaStringList[2]
    print "gamma1NearNeck: " + gammaStringList[3]
    print "}"
    print "\n"


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)

