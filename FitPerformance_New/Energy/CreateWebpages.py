#!/usr/bin/env python
import sys, string, os
import ProduceData as productionScript

energyList = productionScript.energyList
imageHeight = "450"
imageWidth = "750"


def CreateWebpages(options):

    if (options.fitterName2 == ""):
        pictureBaseName = "./EnergyPerformance/images_" + options.scintMaterial + "/" + options.fitterName1 + "_"
    else:
        pictureBaseName = "./EnergyPerformance/images_" + options.scintMaterial + "/" + options.fitterName1 + "+" + options.fitterName2 + "_"

    inFile = open("Template_Webpage.html", "r")
    rawText = string.Template(inFile.read())
    inFile.close()

    histogramLinks1 = ""
    for energy in energyList:
        biasAndResolution_fixedZ_PlotName = pictureBaseName + "biasAndResolution_E=" + str(int(energy * 1000)) + "keV_Z=0mm.png"
        biasAndResolution_fixedZ_Title = "Bias and Resolution vs. Y (Z = 0mm, E = " + str(int(energy * 1000)) + "keV)"
		
        histogramLinks1 = histogramLinks1 + "<img src=\"" + biasAndResolution_fixedZ_PlotName + "\" title=\"" + biasAndResolution_fixedZ_Title + "\" height=\"" + imageHeight + "\" width=\"" + imageWidth + "\">\n"
        
        chiSquared_fixedZ_PlotName = pictureBaseName + "chiSquared_E=" + str(int(energy * 1000)) + "keV_Z=0mm.png"
        chiSquared_fixedZ_Title = "Chi Squared of delta(E) Gaussian vs. Y (Z = 0mm, E = " + str(int(energy * 1000)) + "keV)"
		
        histogramLinks1 = histogramLinks1 + "<img src=\"" + chiSquared_fixedZ_PlotName + "\" title=\"" + chiSquared_fixedZ_Title + "\" height=\"" + imageHeight + "\" width=\"" + imageWidth + "\">\n"

    histogramLinks2 = ""
    for energy in energyList:
        biasAndResolution_fixedY_PlotName = pictureBaseName + "biasAndResolution_E=" + str(int(energy * 1000)) + "keV_Y=0mm.png"
        biasAndResolution_fixedY_Title = "Bias and Resolution vs. Z (Y = 0mm, E = " + str(int(energy * 1000)) + "keV)"
		
        histogramLinks2 = histogramLinks2 + "<img src=\"" + biasAndResolution_fixedY_PlotName + "\" title=\"" + biasAndResolution_fixedY_Title + "\" height=\"" + imageHeight + "\" width=\"" + imageWidth + "\">\n"
		
        chiSquared_fixedY_PlotName = pictureBaseName + "chiSquared_E=" + str(int(energy * 1000)) + "keV_Y=0mm.png"
        chiSquared_fixedY_Title = "Chi Squared of delta(E) Gaussian vs. Z (Y = 0mm, E = " + str(int(energy * 1000)) + "keV)"
		
        histogramLinks2 = histogramLinks2 + "<img src=\"" + chiSquared_fixedY_PlotName + "\" title=\"" + chiSquared_fixedY_Title + "\" height=\"" + imageHeight + "\" width=\"" + imageWidth + "\">\n"
	
    outText = rawText.substitute(RATVersion = options.ratVersion,
                                 Material = options.scintMaterial,
                                 HistogramLinks1 = histogramLinks1,
                                 HistogramLinks2 = histogramLinks2)
    outFileName = "./EnergyPerformance/" + options.scintMaterial + "_energyPerformance.html"
    outFile = open(outFileName, "w")
    outFile.write(outText)
    outFile.close()

	

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material, default = labppo_scintillator", default = "labppo_scintillator")
    parser.add_option("--f1", type = "string", dest = "fitterName1", help = "First Fitter to be Tested (name as specified in Template_Macro_Energy.mac)", default = "")
    parser.add_option("--f2", type = "string", dest = "fitterName2", help = "(Optional) Second Fitter to be Tested (name as specified in Template_Macro_Energy.mac)", default = "")
    parser.add_option( "-v", type = "string", dest = "ratVersion", help = "RAT Version used in simulation", default = "")
    (options, args) = parser.parse_args()
    CreateWebpages(options)

