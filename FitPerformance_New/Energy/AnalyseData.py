#!/usr/bin/env python
import os, sys, ROOT, rat, string
import ProduceData as productionScript

energyList = productionScript.energyList
yPositionList = productionScript.yPositionList
zPositionList = productionScript.zPositionList


def AnalyseData(options):
    
    # Load any parameters for running the macros on a Batch system
    batch_params = None
    if options.batch:
        batch_params = {}
        execfile(options.batch, {}, batch_params)
	
	# Load the batch submission script template
    inFile = open("Template_Batch.sh", "r")
    rawText = string.Template(inFile.read())
    inFile.close()

    pythonRunCommand = "python -c 'import AnalyseData; AnalyseData.AnalysisFunction(\"" + options.scintMaterial + "\", \"" + options.fitterName1 + "\", \"" + options.fitterName2 + "\")'"
    
    # Run the analysis on a Batch system
    if options.batch:
        outText = rawText.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                     Ratenv = batch_params['ratenv'],
                                     Cwd = os.environ['PWD'].replace("/.", "/"),
                                     RunCommand = pythonRunCommand)
        outFile = open("AnalyseData_Energy.sh", "w")
        outFile.write(outText)
        outFile.close()

        os.system(batch_params["submit"] + " AnalyseData_Energy.sh")

    # Else run the macro locally on an interactive machine				
    else:
        os.system(pythonRunCommand)


def AnalysisFunction(material, fitter1, fitter2):

    performancePlots_Fitter1 = PerformancePlots_SingleFitter(material, fitter1, ROOT.kRed+1, ROOT.kOrange-3, ROOT.kMagenta+1)
    print "\n"
    print "***** Plots for first specified fitter complete *****"
    print "\n"
	
    if (fitter2 == ""):
        print "\n"
        print "***** No second fitter specified *****"
        OutputPlots_1Fitter(material, fitter1, performancePlots_Fitter1)
        print "\n"
        print "***** Outputting Plots complete *****"
        print "\n"
    else:
        performancePlots_Fitter2 = PerformancePlots_SingleFitter(material, fitter2, ROOT.kCyan+1, ROOT.kAzure-3, ROOT.kGreen+1)
        print "\n"
        print "***** Plots for second specified fitter complete *****"
        OutputPlots_2Fitters(material, fitter1, fitter2, performancePlots_Fitter1, performancePlots_Fitter2)
        print "\n"
        print "***** Outputting Plots complete *****"
        print "\n"
	    

def PerformancePlots_SingleFitter(material, fitterName, biasColour, resolutionColour, chiSquaredColour):
		
    performancePlotsFileName = "AnalyseData_Energy_PerformancePlots_" + material + "_" + fitterName + ".root"
    performancePlotsFile = ROOT.TFile(performancePlotsFileName, "UPDATE")
        
    deltaEPlotsFileName = "AnalyseData_Energy_DeltaEPlots_" + material + "_" + fitterName + ".root"
	
    resultsTextFileName = "AnalyseData_Energy_PerformanceResults_" + material + "_" + fitterName + ".txt"
    resultsTextFile = open(resultsTextFileName, "w")
    resultsTextFile.write("energy (keV)     y (mm)     z (mm)     bias (%)     resolution (%) \n")
    resultsTextFile.close()
	
    biasPlots_FixedZ = []
    resolutionPlots_FixedZ = []
    chiSquaredPlots_FixedZ = []
    biasPlots_FixedY = []
    resolutionPlots_FixedY = []
    chiSquaredPlots_FixedY = []
	
    for energy in energyList:

        ##################################################
		##### Varying y-position, and setting z to 0 #####
        ##################################################
		
        singleEnergy_fixedZ_BiasGraph = ROOT.TGraph(len(yPositionList) - 1)
        singleEnergy_fixedZ_ResolutionGraph = ROOT.TGraph(len(yPositionList) - 1)
        singleEnergy_fixedZ_ChiSquaredGraph = ROOT.TGraph(len(yPositionList) - 1)
        
        for yIndex, yPosition in enumerate(yPositionList):
		
            zPosition = 0
            
            performanceList = SingleE_SingleY_SingleZ_SingleFitter(material, energy, yPosition, zPosition, fitterName, deltaEPlotsFileName, resultsTextFileName)
            
            singleEnergy_fixedZ_BiasGraph.SetPoint(yIndex, yPosition, performanceList[0])
            singleEnergy_fixedZ_ResolutionGraph.SetPoint(yIndex, yPosition, performanceList[1])
            singleEnergy_fixedZ_ChiSquaredGraph.SetPoint(yIndex, yPosition, performanceList[2])
		
        singleEnergy_fixedZ_BiasGraph.SetTitle(str(int(energy * 1000)) + "keV")
        singleEnergy_fixedZ_BiasGraph.GetXaxis().SetTitle("True Position Along Y-Axis, mm")
        singleEnergy_fixedZ_BiasGraph.GetXaxis().SetAxisColor(17)
        singleEnergy_fixedZ_BiasGraph.GetYaxis().SetTitle("Percentage Bias, Resolution")
        singleEnergy_fixedZ_BiasGraph.GetYaxis().SetAxisColor(17)
        singleEnergy_fixedZ_BiasGraph.GetYaxis().SetRangeUser(-25.0, 25.0)
        singleEnergy_fixedZ_BiasGraph.SetMarkerStyle(20)
        singleEnergy_fixedZ_BiasGraph.SetMarkerSize(1.0)
        singleEnergy_fixedZ_BiasGraph.SetMarkerColor(biasColour)
        singleEnergy_fixedZ_BiasGraph.SetLineColor(biasColour)
        singleEnergy_fixedZ_BiasGraph.SetName("Bias_" + str(int(energy * 1000)) + "keV_z=0mm")
        biasPlots_FixedZ.append(singleEnergy_fixedZ_BiasGraph)
        
        singleEnergy_fixedZ_ResolutionGraph.SetTitle(str(int(energy * 1000)) + "keV")
        singleEnergy_fixedZ_ResolutionGraph.GetXaxis().SetTitle("True Position Along Y-Axis, mm")
        singleEnergy_fixedZ_ResolutionGraph.GetXaxis().SetAxisColor(17)
        singleEnergy_fixedZ_ResolutionGraph.GetYaxis().SetTitle("Percentage Bias, Resolution")
        singleEnergy_fixedZ_ResolutionGraph.GetYaxis().SetAxisColor(17)
        singleEnergy_fixedZ_ResolutionGraph.GetYaxis().SetRangeUser(-25.0, 25.0)
        singleEnergy_fixedZ_ResolutionGraph.SetMarkerStyle(20)
        singleEnergy_fixedZ_ResolutionGraph.SetMarkerSize(1.0)
        singleEnergy_fixedZ_ResolutionGraph.SetMarkerColor(resolutionColour)
        singleEnergy_fixedZ_ResolutionGraph.SetLineColor(resolutionColour)
        singleEnergy_fixedZ_ResolutionGraph.SetName("Resolution_" + str(int(energy * 1000)) + "keV_z=0mm")
        resolutionPlots_FixedZ.append(singleEnergy_fixedZ_ResolutionGraph)
        
        singleEnergy_fixedZ_ChiSquaredGraph.SetTitle(str(int(energy * 1000)) + "keV")
        singleEnergy_fixedZ_ChiSquaredGraph.GetXaxis().SetTitle("True Position Along Y-Axis, mm")
        singleEnergy_fixedZ_ChiSquaredGraph.GetXaxis().SetAxisColor(17)
        singleEnergy_fixedZ_ChiSquaredGraph.GetYaxis().SetTitle("Chi-Squared Value")
        singleEnergy_fixedZ_ChiSquaredGraph.GetYaxis().SetAxisColor(17)
        singleEnergy_fixedZ_ChiSquaredGraph.GetYaxis().SetRangeUser(0.0, 120.0)
        singleEnergy_fixedZ_ChiSquaredGraph.SetMarkerStyle(20)
        singleEnergy_fixedZ_ChiSquaredGraph.SetMarkerSize(1.0)
        singleEnergy_fixedZ_ChiSquaredGraph.SetMarkerColor(chiSquaredColour)
        singleEnergy_fixedZ_ChiSquaredGraph.SetLineColor(chiSquaredColour)
        singleEnergy_fixedZ_ChiSquaredGraph.SetName("ChiSquared_" + str(int(energy * 1000)) + "keV_z=0mm")
        chiSquaredPlots_FixedZ.append(singleEnergy_fixedZ_ChiSquaredGraph)
        
        performancePlotsFile.cd()
        singleEnergy_fixedZ_BiasGraph.Write()
        singleEnergy_fixedZ_ResolutionGraph.Write()
        singleEnergy_fixedZ_ChiSquaredGraph.Write()
		
        ##################################################
		##### Varying z-position, and setting y to 0 #####
        ##################################################
		
        singleEnergy_fixedY_BiasGraph = ROOT.TGraph(len(zPositionList) - 1)
        singleEnergy_fixedY_ResolutionGraph = ROOT.TGraph(len(zPositionList) - 1)
        singleEnergy_fixedY_ChiSquaredGraph = ROOT.TGraph(len(zPositionList) - 1)
        
        for zIndex, zPosition in enumerate(zPositionList):
		
            yPosition = 0
            
            performanceList = SingleE_SingleY_SingleZ_SingleFitter(material, energy, yPosition, zPosition, fitterName, deltaEPlotsFileName, resultsTextFileName)
            
            singleEnergy_fixedY_BiasGraph.SetPoint(zIndex, zPosition, performanceList[0])
            singleEnergy_fixedY_ResolutionGraph.SetPoint(zIndex, zPosition, performanceList[1])
            singleEnergy_fixedY_ChiSquaredGraph.SetPoint(zIndex, zPosition, performanceList[2])

        singleEnergy_fixedY_BiasGraph.SetTitle(str(int(energy * 1000)))
        singleEnergy_fixedY_BiasGraph.GetXaxis().SetTitle("True Position Along Z-Axis, mm")
        singleEnergy_fixedY_BiasGraph.GetXaxis().SetAxisColor(17)
        singleEnergy_fixedY_BiasGraph.GetYaxis().SetTitle("Percentage Bias, Resolution")
        singleEnergy_fixedY_BiasGraph.GetYaxis().SetAxisColor(17)
        singleEnergy_fixedY_BiasGraph.GetYaxis().SetRangeUser(-25.0, 25.0)
        singleEnergy_fixedY_BiasGraph.SetMarkerStyle(20)
        singleEnergy_fixedY_BiasGraph.SetMarkerSize(1.0)
        singleEnergy_fixedY_BiasGraph.SetMarkerColor(biasColour)
        singleEnergy_fixedY_BiasGraph.SetLineColor(biasColour)
        singleEnergy_fixedY_BiasGraph.SetName("Bias_" + str(int(energy * 1000)) + "keV_y=0mm")
        biasPlots_FixedY.append(singleEnergy_fixedY_BiasGraph)
        
        singleEnergy_fixedY_ResolutionGraph.SetTitle(str(int(energy * 1000)))
        singleEnergy_fixedY_ResolutionGraph.GetXaxis().SetTitle("True Position Along Z-Axis, mm")
        singleEnergy_fixedY_ResolutionGraph.GetXaxis().SetAxisColor(17)
        singleEnergy_fixedY_ResolutionGraph.GetYaxis().SetTitle("Percentage Bias, Resolution")
        singleEnergy_fixedY_ResolutionGraph.GetYaxis().SetAxisColor(17)
        singleEnergy_fixedY_ResolutionGraph.GetYaxis().SetRangeUser(-25.0, 25.0)
        singleEnergy_fixedY_ResolutionGraph.SetMarkerStyle(20)
        singleEnergy_fixedY_ResolutionGraph.SetMarkerSize(1.0)
        singleEnergy_fixedY_ResolutionGraph.SetMarkerColor(resolutionColour)
        singleEnergy_fixedY_ResolutionGraph.SetLineColor(resolutionColour)
        singleEnergy_fixedY_ResolutionGraph.SetName("Resolution_" + str(int(energy * 1000)) + "keV_y=0mm")
        resolutionPlots_FixedY.append(singleEnergy_fixedY_ResolutionGraph)
		
        singleEnergy_fixedY_ChiSquaredGraph.SetTitle(str(int(energy * 1000)))
        singleEnergy_fixedY_ChiSquaredGraph.GetXaxis().SetTitle("True Position Along Z-Axis, mm")
        singleEnergy_fixedY_ChiSquaredGraph.GetXaxis().SetAxisColor(17)
        singleEnergy_fixedY_ChiSquaredGraph.GetYaxis().SetTitle("Chi-Squared Value")
        singleEnergy_fixedY_ChiSquaredGraph.GetYaxis().SetAxisColor(17)
        singleEnergy_fixedY_ChiSquaredGraph.GetYaxis().SetRangeUser(0.0, 120.0)
        singleEnergy_fixedY_ChiSquaredGraph.SetMarkerStyle(20)
        singleEnergy_fixedY_ChiSquaredGraph.SetMarkerSize(1.0)
        singleEnergy_fixedY_ChiSquaredGraph.SetMarkerColor(chiSquaredColour)
        singleEnergy_fixedY_ChiSquaredGraph.SetLineColor(chiSquaredColour)
        singleEnergy_fixedY_ChiSquaredGraph.SetName("ChiSquared_" + str(int(energy * 1000)) + "keV_y=0mm")
        chiSquaredPlots_FixedY.append(singleEnergy_fixedY_ChiSquaredGraph)

        performancePlotsFile.cd()
        singleEnergy_fixedY_BiasGraph.Write()
        singleEnergy_fixedY_ResolutionGraph.Write()
        singleEnergy_fixedY_ChiSquaredGraph.Write()

    performancePlotsFile.Close()
		
    return [biasPlots_FixedZ, resolutionPlots_FixedZ, chiSquaredPlots_FixedZ, biasPlots_FixedY, resolutionPlots_FixedY, chiSquaredPlots_FixedY]


def SingleE_SingleY_SingleZ_SingleFitter(material, energy, yPosition, zPosition, fitterName, deltaEPlotsFileName, resultsTextFileName):

    deltaEnergyPlotName = str( int(energy * 1000) ) + "keV_y=" + str(yPosition) + "mm_z=" + str(zPosition) + "mm"
    deltaEnergyPlot = ROOT.TH1D(deltaEnergyPlotName, deltaEnergyPlotName, 25, -25.0, 25.0)
    deltaEnergyPlot.GetXaxis().SetTitle("Percentage #DeltaE = [(fitted Energy - True Energy) / True Energy] * 100")
    deltaEnergyPlot.GetYaxis().SetTitle("No. of Events")
    
    infileName = material + "_E=" + str( int(energy * 1000) ) + "keV_y=" + str(yPosition) + "mm_z=" + str(zPosition) + "mm.root"
    
    for ds, run in rat.dsreader(infileName):
        if ds.GetEVCount() == 0:
            continue
        eventev = ds.GetEV(0)

        if not eventev.FitResultExists(fitterName):
            continue
        fittedVertex = eventev.GetFitResult(fitterName).GetVertex(0)
        if not fittedVertex.ContainsEnergy():
            continue
        if not fittedVertex.ValidEnergy():
            continue

        fittedEnergy = fittedVertex.GetEnergy()
        trueEnergy = ds.GetMC().GetMCParticle(0).GetKineticEnergy()
        deltaEnergy = fittedEnergy - trueEnergy
        deltaEnergyPlot.Fill((deltaEnergy / trueEnergy) * 100.0)

    if (deltaEnergyPlot.Integral() == 0):
        bias = -9999.0
        resolution = -9999.0
        chiSquared = -9999.0
    else:
        gaussFitEnergy = ROOT.TF1("gaussFitEnergy", "gaus", -25.0, 25.0)
        deltaEnergyPlot.Fit(gaussFitEnergy, "RQ")
		
        bias = gaussFitEnergy.GetParameter(1)
        resolution = gaussFitEnergy.GetParameter(2)
        chiSquared = gaussFitEnergy.GetChisquare()
		
        del gaussFitEnergy
	
    deltaEPlotsFile = ROOT.TFile(deltaEPlotsFileName, "UPDATE")
    deltaEnergyPlot.Write()
    deltaEPlotsFile.Close()
	
    resultsTextFile = open(resultsTextFileName, "a")
    resultsTextFile.write(str(int(energy * 1000)) + "     " + str(yPosition) + "     " + str(zPosition) + "     " + str(bias) + "     " + str(resolution) + "\n")
    resultsTextFile.close()

    del deltaEnergyPlot
    
    return [bias, resolution, chiSquared]

	
def OutputPlots_1Fitter(material, fitter1, performancePlots_Fitter1):

    pictureDirectory = "./EnergyPerformance/images_" + material
    if not os.path.exists(pictureDirectory):
        os.makedirs(pictureDirectory)

    combinedPlotsFileName = "AnalyseData_Energy_CombinedPlots_" + material + "_" + fitter1 + ".root"
    combinedPlotsFile = ROOT.TFile(combinedPlotsFileName, "UPDATE")
	
    for index, energy in enumerate(energyList):
	
        ##################################################
		##### Varying y-position, and setting z to 0 #####
        ##################################################
		
        combinedCanvasName1 = "biasAndResolution_E=" + str(int(energy * 1000)) + "keV_Z=0mm"
        c1 = ROOT.TCanvas(combinedCanvasName1, combinedCanvasName1, 1500, 900)
        leg1 = ROOT.TLegend(0.62, 0.12, 0.89, 0.26)
        leg1.SetTextSize(0.02)
	
        (performancePlots_Fitter1[0])[index].Draw("APL")
        leg1.AddEntry((performancePlots_Fitter1[0])[index], fitter1 + " - Bias", "p")
        (performancePlots_Fitter1[1])[index].Draw("PL")
        leg1.AddEntry((performancePlots_Fitter1[1])[index], fitter1 + " - Resolution", "p")	
        leg1.Draw("SAME")
        c1.SetGrid()

        picturePath1 = pictureDirectory + "/" + fitter1 + "_" + combinedCanvasName1 + ".png"        
        c1.Print(picturePath1, "png")
		
        combinedCanvasName2 = "chiSquared_E=" + str(int(energy * 1000)) + "keV_Z=0mm"
        c2 = ROOT.TCanvas(combinedCanvasName2, combinedCanvasName2, 1500, 900)
        leg2 = ROOT.TLegend(0.62, 0.73, 0.89, 0.87)
        leg2.SetTextSize(0.02)
	
        (performancePlots_Fitter1[2])[index].Draw("APL")
        leg2.AddEntry((performancePlots_Fitter1[2])[index], fitter1 + " - Chi Squared", "p")
        leg2.Draw("SAME")
        c2.SetGrid()

        picturePath2 = pictureDirectory + "/" + fitter1 + "_" + combinedCanvasName2 + ".png"        
        c2.Print(picturePath2, "png")
		
        combinedPlotsFile.cd()
        c1.Write()
        c2.Write()
        
        ##################################################
		##### Varying z-position, and setting y to 0 #####
        ##################################################
		
        combinedCanvasName3 = "biasAndResolution_E=" + str(int(energy * 1000)) + "keV_Y=0mm"
        c3 = ROOT.TCanvas(combinedCanvasName3, combinedCanvasName3, 1500, 900)
        leg3 = ROOT.TLegend(0.36, 0.75, 0.65, 0.89)
        leg3.SetTextSize(0.02)
	
        (performancePlots_Fitter1[3])[index].Draw("APL")
        leg3.AddEntry((performancePlots_Fitter1[3])[index], fitter1 + " - Bias", "p")
        (performancePlots_Fitter1[4])[index].Draw("PL")
        leg3.AddEntry((performancePlots_Fitter1[4])[index], fitter1 + " - Resolution", "p")	
        leg3.Draw("SAME")
        c3.SetGrid()

        picturePath3 = pictureDirectory + "/" + fitter1 + "_" + combinedCanvasName3 + ".png"        
        c3.Print(picturePath3, "png")	

        combinedCanvasName4 = "chiSquared_E=" + str(int(energy * 1000)) + "keV_Y=0mm"
        c4 = ROOT.TCanvas(combinedCanvasName4, combinedCanvasName4, 1500, 900)
        leg4 = ROOT.TLegend(0.36, 0.75, 0.65, 0.89)
        leg4.SetTextSize(0.02)
	
        (performancePlots_Fitter1[5])[index].Draw("APL")
        leg4.AddEntry((performancePlots_Fitter1[5])[index], fitter1 + " - Chi Squared", "p")
        leg4.Draw("SAME")
        c4.SetGrid()

        picturePath4 = pictureDirectory + "/" + fitter1 + "_" + combinedCanvasName4 + ".png"        
        c4.Print(picturePath4, "png")
		
        combinedPlotsFile.cd()
        c3.Write()
        c4.Write()
        
    combinedPlotsFile.Close()
	

def OutputPlots_2Fitters(material, fitter1, fitter2, performancePlots_Fitter1, performancePlots_Fitter2):

    pictureDirectory = "./EnergyPerformance/images_" + material
    if not os.path.exists(pictureDirectory):
        os.makedirs(pictureDirectory)

    combinedPlotsFileName = "AnalyseData_Energy_CombinedPlots_" + material + "_" + fitter1 + "+" + fitter2 + ".root"
    combinedPlotsFile = ROOT.TFile(combinedPlotsFileName, "UPDATE")
	
    for index, energy in enumerate(energyList):
	
        ##################################################
		##### Varying y-position, and setting z to 0 #####
        ##################################################
		
        combinedCanvasName1 = "biasAndResolution_E=" + str(int(energy * 1000)) + "keV_Z=0mm"
        c1 = ROOT.TCanvas(combinedCanvasName1, combinedCanvasName1, 1500, 900)
        leg1 = ROOT.TLegend(0.62, 0.12, 0.89, 0.26)
        leg1.SetTextSize(0.02)
	
        (performancePlots_Fitter1[0])[index].Draw("APL")
        leg1.AddEntry((performancePlots_Fitter1[0])[index], fitter1 + " - Bias", "p")
        (performancePlots_Fitter1[1])[index].Draw("PL")
        leg1.AddEntry((performancePlots_Fitter1[1])[index], fitter1 + " - Resolution", "p")	
        (performancePlots_Fitter2[0])[index].Draw("PL")
        leg1.AddEntry((performancePlots_Fitter2[0])[index], fitter2 + " - Bias", "p")
        (performancePlots_Fitter2[1])[index].Draw("PL")
        leg1.AddEntry((performancePlots_Fitter2[1])[index], fitter2 + " - Resolution", "p")		
        leg1.Draw("SAME")
        c1.SetGrid()

        picturePath1 = pictureDirectory + "/" + fitter1 + "+" + fitter2 + "_" + combinedCanvasName1 + ".png"        
        c1.Print(picturePath1, "png")
		
        combinedCanvasName2 = "chiSquared_E=" + str(int(energy * 1000)) + "keV_Z=0mm"
        c2 = ROOT.TCanvas(combinedCanvasName2, combinedCanvasName2, 1500, 900)
        leg2 = ROOT.TLegend(0.62, 0.73, 0.89, 0.87)
        leg2.SetTextSize(0.02)
	
        (performancePlots_Fitter1[2])[index].Draw("APL")
        leg2.AddEntry((performancePlots_Fitter1[2])[index], fitter1 + " - Chi Squared", "p")
        (performancePlots_Fitter2[2])[index].Draw("PL")
        leg2.AddEntry((performancePlots_Fitter2[2])[index], fitter2 + " - Chi Squared", "p")	
        leg2.Draw("SAME")
        c2.SetGrid()

        picturePath2 = pictureDirectory + "/" + fitter1 + "+" + fitter2 + "_" + combinedCanvasName2 + ".png"        
        c2.Print(picturePath2, "png")
		
        combinedPlotsFile.cd()
        c1.Write()
        c2.Write()
        
        ##################################################
		##### Varying z-position, and setting y to 0 #####
        ##################################################
		
        combinedCanvasName3 = "biasAndResolution_E=" + str(int(energy * 1000)) + "keV_Y=0mm"
        c3 = ROOT.TCanvas(combinedCanvasName3, combinedCanvasName3, 1500, 900)
        leg3 = ROOT.TLegend(0.36, 0.75, 0.65, 0.89)
        leg3.SetTextSize(0.02)
	
        (performancePlots_Fitter1[3])[index].Draw("APL")
        leg3.AddEntry((performancePlots_Fitter1[3])[index], fitter1 + " - Bias", "p")
        (performancePlots_Fitter1[4])[index].Draw("PL")
        leg3.AddEntry((performancePlots_Fitter1[4])[index], fitter1 + " - Resolution", "p")	
        (performancePlots_Fitter2[3])[index].Draw("PL")
        leg3.AddEntry((performancePlots_Fitter2[3])[index], fitter2 + " - Bias", "p")
        (performancePlots_Fitter2[4])[index].Draw("PL")
        leg3.AddEntry((performancePlots_Fitter2[4])[index], fitter2 + " - Resolution", "p")		
        leg3.Draw("SAME")
        c3.SetGrid()

        picturePath3 = pictureDirectory + "/" + fitter1 + "+" + fitter2 + "_" + combinedCanvasName3 + ".png"        
        c3.Print(picturePath3, "png")	

        combinedCanvasName4 = "chiSquared_E=" + str(int(energy * 1000)) + "keV_Y=0mm"
        c4 = ROOT.TCanvas(combinedCanvasName4, combinedCanvasName4, 1500, 900)
        leg4 = ROOT.TLegend(0.36, 0.75, 0.65, 0.89)
        leg4.SetTextSize(0.02)
	
        (performancePlots_Fitter1[5])[index].Draw("APL")
        leg4.AddEntry((performancePlots_Fitter1[5])[index], fitter1 + " - Chi Squared", "p")
        (performancePlots_Fitter2[5])[index].Draw("PL")
        leg4.AddEntry((performancePlots_Fitter2[5])[index], fitter2 + " - Chi Squared", "p")
        leg4.Draw("SAME")
        c4.SetGrid()

        picturePath4 = pictureDirectory + "/" + fitter1 + "+" + fitter2 + "_" + combinedCanvasName4 + ".png"        
        c4.Print(picturePath4, "png")
		
        combinedPlotsFile.cd()
        c3.Write()
        c4.Write()
        
    combinedPlotsFile.Close()
	
	
	
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the analysis in Batch mode")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator Material, default = labppo_scintillator", default = "labppo_scintillator")
    parser.add_option("--f1", type = "string", dest = "fitterName1", help = "First Fitter to be Tested (name as specified in Template_Macro_Energy.mac), default = functionalForm", default = "functionalForm")
    parser.add_option("--f2", type = "string", dest = "fitterName2", help = "(Optional) Second Fitter to be Tested (name as specified in Template_Macro_Energy.mac), default = [EMPTY]", default = "")
    (options, args) = parser.parse_args()
    AnalyseData(options)

