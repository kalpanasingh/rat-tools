#!/usr/bin/env python
import os, sys, string, Utilities


def AnalyseFiles():
    # create and source the text file for ROOT-script analysis
    infile1 = open("Template_Coordinate.sh", "r")
    rawText1 = string.Template(infile1.read())
    infile1.close()
    outText1 = rawText1.substitute(ratLoc = Utilities.ratLoc,
		                           currentLoc = Utilities.currentLoc)

    outFile1 = open("Coordinate.sh", "w")
    outFile1.write(outText1)
    outFile1.close()
    os.system("source Coordinate.sh")
    os.remove("Coordinate.sh")

    # create and submit the batch script
    infile2 = open("Template_Submit.sh", "r")
    rawText2 = string.Template(infile2.read())
    infile2.close()
    outText2 = rawText2.substitute(envrnLoc = Utilities.envrnLoc,
		                           currentLoc = Utilities.currentLoc,
		                           runCommand = "./Coordinate")

    outFile2 = open("DELETE_WHEN_COMPLETE.sh", "w")
    outFile2.write(outText2)
    outFile2.close()
    os.system("qsub DELETE_WHEN_COMPLETE.sh")


if __name__ == '__main__':
	AnalyseFiles()
