
#include <vector>
#include <algorithm>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TMath.h>
#include <TH1.h>
#include <TGraph.h>
#include <TAxis.h>
#include <TF1.h>

#include <RAT/DU/DSReader.hh>
#include <RAT/DU/Utility.hh>
#include <RAT/DU/PMTInfo.hh>
#include <RAT/DS/Entry.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/PMT.hh>
#include <RAT/DS/MC.hh>
#include <RAT/DS/MCParticle.hh>

static const int numberOfRadii = 8;
double radii[numberOfRadii] = {5000, 5300, 5400, 5500, 5600, 5700, 5800, 5900};		// This should contain the same values as the "radius" vector in ProduceData.py
static const int numberOfNhitsWindows = 12;
double nhitsWindows[numberOfNhitsWindows] = {0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750};	// Difference between consecutive values = "nhitsWindowWidth" as defined below
const double nhitsWindowWidth = 250;
static const int numberOfRatioBins = 6;
double ratioBins[numberOfRatioBins] = {0.0, 0.1, 0.2, 0.3, 0.4, 0.5};	// Difference between consecutive values = "ratioBinWidth" as defined below
std::string ratioBinNames[numberOfRatioBins] = {"0p0", "0p1", "0p2", "0p3", "0p4", "0p5"};
const double ratioBinWidth = 0.1;
const double fraction = 0.90;
const double dipLow = 40.0;
const double dipHigh = 90.0;
const double pi = 3.14159265358979323846;
int numberOfParameters = 3;		// Number of parameters in the fit function below
const char* fitFunction = "pol2";
const char* plotsFileName = "Coordinate_DebuggingPlots.root";
const double thetaError = 0.0555;
const double phiError = 0.0655;

std::vector< std::vector<double> > CalculateMMTSValues(std::string);
std::vector< std::vector<double> > CalculateRatioVsRadiusFitsAndErrors(std::vector<std::string>);


void Coordination(std::string index)
{
	std::ofstream stream0("Coordinate_Results.txt");
	stream0 << std::endl;
	
	// Step 1: construct a vector of filenames based on the radii
	std::vector<std::string> fileNamesVector;
	for (int f = 0; f < numberOfRadii; f++)
	{
		std::stringstream fileNameStream;
		fileNameStream << "electrons_" << radii[f] << "mm.root";
		std::string fileNameString = fileNameStream.str();
		
		fileNamesVector.push_back(fileNameString);
	}
	
	// Step 2: construct a vector of Nhits Window low-edges directly from the nhitsWindow array (used to construct the TGraph below)
	std::vector<double> nhitsWindowsVector;
	for (int w = 0; w < numberOfNhitsWindows; w++)
	{
		nhitsWindowsVector.push_back(nhitsWindows[w]);
	}

	// Step 3: for the 5000mm data only, calculate the "Mean - 3*Sigma" (MMTS) of each Nhits window in the Ratio value distribution - this will be used to find each window's ratio cut value
	stream0 << "Calculating \"Mean - 3*Sigma\" values ..." << std::endl;
	std::vector< std::vector<double> > MMTSValuesAt5000mm = CalculateMMTSValues(fileNamesVector[0]);
	
	// Step 4: make a linear fit to the MMTS values at higher Nhits, to find the relationship between MMTS (i.e. ratio cut) and Nhits
	stream0 << "Calculating fit to MMTS values ..." << std::endl;
	TFile plotFile (plotsFileName, "UPDATE");
	
	TGraph mmtsVsNhitsGraph ((MMTSValuesAt5000mm[0]).size(), &(MMTSValuesAt5000mm[0])[0], &(MMTSValuesAt5000mm[1])[0]);
	mmtsVsNhitsGraph.SetMarkerStyle(20);
	mmtsVsNhitsGraph.SetMarkerColor(kBlack);
	mmtsVsNhitsGraph.SetMarkerSize(0.5);
	mmtsVsNhitsGraph.GetXaxis()->SetTitle("Nhits");
	mmtsVsNhitsGraph.GetYaxis()->SetTitle("Ratio #mu - 3*#sigma");
	TF1* mmtsFit = new TF1("mmtsFit", "pol1", (MMTSValuesAt5000mm[0])[4], (MMTSValuesAt5000mm[0])[(MMTSValuesAt5000mm[0]).size() - 1]);
	mmtsVsNhitsGraph.Fit(mmtsFit, "RQ");
	
	plotFile.cd();
	mmtsVsNhitsGraph.Write();
	plotFile.Close();
	
	double fitGradient = mmtsFit->GetParameter(1);
	double fitIntercept = mmtsFit->GetParameter(0);
	delete mmtsFit;
	
	// Step 5: for the rest of the radius values, calculate the fit parameters for the Ratio vs. Radius plots as well as the positive and negative errors
	// allFitCoefficients[0] = vector of 0th radius power coefficients for the ratio vs. radius fit function (one entry for each Nhits window)
	// allFitCoefficients[1] = vector of 1st radius power coefficients for the ratio vs. radius fit function (one entry for each Nhits window)
	// allFitCoefficients[2] = vector of 2nd radius power coefficients for the ratio vs. radius fit function (one entry for each Nhits window)
	// allFitCoefficients[3] = vector of negative errors (one entry for each Nhits window / Ratio bin combination ... total = numberOfNhitsWindows * numberOfRatioBins entries)
	// allFitCoefficients[4] = vector of positive errors (one entry for each Nhits window / Ratio bin combination ... total = numberOfNhitsWindows * numberOfRatioBins entries)
	stream0 << "Populating plots of ratio vs. radius for radius > 5300mm, and calculating fit parameters and errors ..." << std::endl;
	std::vector< std::vector<double> > allFitCoefficients = CalculateRatioVsRadiusFitsAndErrors(fileNamesVector);
	
	// Print coordinated values to screen in RATDB format
	stream0 << std::endl;
	stream0 << "Please place the text below into the database file: FIT_NEAR_AV_ANGULAR.ratdb located in rat/data, replacing any existing entry with the same index." << std::endl;
	stream0 << std::endl;
	stream0 << "{" << std::endl;
	stream0 << "name: \"FIT_NEAR_AV_ANGULAR\"," << std::endl;
	stream0 << "index: \"" << index << "\"," << std::endl;
	stream0 << "valid_begin : [0, 0]," << std::endl;
	stream0 << "valid_end : [0, 0]," << std::endl;
	stream0 << "nhits_windows: [";
	for (int w = 0; w < numberOfNhitsWindows; w++)
	{
		stream0 << nhitsWindows[w] << ", ";
	}
	stream0 << "]," << std::endl;
	stream0 << "nhits_window_width: " << nhitsWindowWidth << "," << std::endl;
	for (int p = 0; p < numberOfParameters; p++)
	{
		stream0 << "fit_coefficients" << p << ": [";
		for (unsigned int c = 0; c < allFitCoefficients[p].size(); c++)
		{
			if ((allFitCoefficients[p])[c] == 0.0)
			{
				stream0 << "0.0, ";
			}
			else
			{
				stream0 << (allFitCoefficients[p])[c] << ", ";
			}
		}
		stream0 << "]," << std::endl;
	}
	stream0 << "ratio_cuts: [";
	for (int w = 0; w < numberOfNhitsWindows; w++)
	{
		double ratioCut = ((nhitsWindows[w] * fitGradient) + fitIntercept);
		stream0 << ratioCut << ", ";
	}
	stream0 << "]," << std::endl;
	stream0 << "ratio_bins: [";
	for (int b = 0; b < numberOfRatioBins; b++)
	{
		if (ratioBins[b] == 0.0)
		{
			stream0 << "0.0, ";
		}
		else
		{
			stream0 << ratioBins[b] << ", ";
		}
	}
	stream0 << "]," << std::endl;
	stream0 << "ratio_bin_width: " << ratioBinWidth << "," << std::endl;
	stream0 << std::fixed << std::setprecision(1);
	stream0 << "negative_errors: [";
	for (unsigned int n = 0; n < allFitCoefficients[numberOfParameters].size(); n++)
	{
		stream0 << (allFitCoefficients[numberOfParameters])[n] << ", ";
	}
	stream0 << "]," << std::endl;
	stream0 << "positive_errors: [";
	for (unsigned int p = 0; p < allFitCoefficients[numberOfParameters + 1].size(); p++)
	{
		stream0 << (allFitCoefficients[numberOfParameters + 1])[p] << ", ";
	}
	stream0 << "]," << std::endl;
	stream0 << std::fixed << std::setprecision(4);
	stream0 << "theta_error: " << thetaError << "," << std::endl;
	stream0 << "phi_error: " << phiError << "," << std::endl;
	stream0 << "}" << std::endl;
	stream0 << std::endl;
}


std::vector< std::vector<double> > CalculateMMTSValues(std::string infile)
{
	// Set up a vector of TH1D histograms - these are histograms of the ratio value per event, with one histogram per Nhits window
	std::vector<TH1D> ratioPlotsVector;
	for (int w = 0; w < numberOfNhitsWindows; w++)
	{
		std::stringstream plotNameStream;
		plotNameStream << "ratioValues_nhits=" << nhitsWindows[w];
		
		TH1D histogram ((plotNameStream.str()).c_str(), (plotNameStream.str()).c_str(), 100, 0.0, 0.8);
		ratioPlotsVector.push_back(histogram);
	}
	
	// Loop over the events at 5000mm, check in which window the event Nhits falls, and then save the ratio into the corresponding histogram for that window
	RAT::DU::DSReader dsReader(infile);
	const RAT::DU::PMTInfo& pmtInfo = RAT::DU::Utility::Get()->GetPMTInfo();

	for(size_t i = 0; i < dsReader.GetEntryCount(); i++) 
	{
		const RAT::DS::Entry& dsEntry = dsReader.GetEntry(i);
		if (dsEntry.GetEVCount() == 0) continue;

		const RAT::DS::CalPMTs& calibratedPMTs = dsEntry.GetEV(0).GetCalPMTs();
		double eventNhits = calibratedPMTs.GetCount();
		if (eventNhits >= (nhitsWindows[numberOfNhitsWindows - 1] + nhitsWindowWidth)) continue;
		
		int eventNhitsWindow = -1;
		for (int w = 0; w < numberOfNhitsWindows; w++)
		{
			if ((eventNhits >= nhitsWindows[w]) && (eventNhits < (nhitsWindows[w] + nhitsWindowWidth)))
			{
				eventNhitsWindow = w;
				break;
			}
		}
			
		TVector3 eventPosition;
		for (size_t j = 0; j < calibratedPMTs.GetCount(); j++)
		{
			eventPosition += pmtInfo.GetPosition(calibratedPMTs.GetPMT(j).GetID());
		}
		
		double inDipCount = 0.0, totalCount = 0.0;
		for (size_t j = 0; j < calibratedPMTs.GetCount(); j++)
		{
			const RAT::DS::PMTCal& calibratedPMT = calibratedPMTs.GetPMT(j);
			TVector3 pmtPosition = pmtInfo.GetPosition(calibratedPMT.GetID());

			double angle = acos((eventPosition.Dot(pmtPosition)) / (eventPosition.Mag() * pmtPosition.Mag())) * (180 / pi);
            
			if ((angle >= dipLow) && (angle <= dipHigh))
			{
				inDipCount += 1.0;
			}
			totalCount += 1.0;
		}

		double ratio = (inDipCount / totalCount);
		if (ratio >= (ratioBins[numberOfRatioBins - 1] + ratioBinWidth)) continue;
		
		ratioPlotsVector[eventNhitsWindow].Fill(ratio);
	}

	// For each ratio histogram, fit a gaussian distribution, extract the mean and sigma, and then save the "Mean - 3*Sigma" (MMTS) as well as the histogram
	TFile plotFile (plotsFileName, "UPDATE");
	
	std::vector<double> usedNhitsWindows, MMTSValues;
	for (int w = 0; w < numberOfNhitsWindows; w++)
	{
		if (ratioPlotsVector[w].Integral() != 0)
		{
			TF1* gaussFit = new TF1("gaussFit", "gaus", 0.0, 0.8);
			ratioPlotsVector[w].Fit(gaussFit, "RQ");

			plotFile.cd();
			ratioPlotsVector[w].Write();
		
			double mmts = (gaussFit->GetParameter(1) - (3 * gaussFit->GetParameter(2)));
			usedNhitsWindows.push_back(nhitsWindows[w]);
			MMTSValues.push_back(mmts);
		
			delete gaussFit;
		}
		else
		{
			plotFile.cd();
			ratioPlotsVector[w].Write();
		}
	}
	
	plotFile.Close();
	
	ratioPlotsVector.clear();
	
	// Return the entire structure of nhits Windows and corresponding MMTS values
	std::vector< std::vector<double> > mmtsValuesStructure;
	mmtsValuesStructure.push_back(usedNhitsWindows);
	mmtsValuesStructure.push_back(MMTSValues);	
	
	return mmtsValuesStructure;
}


std::vector< std::vector<double> > CalculateRatioVsRadiusFitsAndErrors(std::vector<std::string> fileNamesVector)
{
	// Set up a vector of vectors for each of the Ratios and Radii, where there is one vector for each Nhits window
	// Set up a vector of TH1D's for calculating the positive and negative errors, one TH1D for each Nhits Window / Radio Bin combination (= numberOfNhitsWindows * numberOfRatioBins)
	std::vector< std::vector<double> > radiiAllNhitsWindows, ratiosAllNhitsWindows;
	std::vector<TH1D> mcRadiusPlots;	
	for (int w = 0; w < numberOfNhitsWindows; w++)
	{
		std::vector<double> radiiSingleNhitsWindow, ratiosSingleNhitsWindow;
		radiiAllNhitsWindows.push_back(radiiSingleNhitsWindow);
		ratiosAllNhitsWindows.push_back(ratiosSingleNhitsWindow);
		
		for (int b = 0; b < numberOfRatioBins; b++)
		{
			std::stringstream plotNameStream;
			plotNameStream << "mcRadius_nhits=" << nhitsWindows[w] << "_ratio=" << ratioBinNames[b];
		
			TH1D histogram ((plotNameStream.str()).c_str(), (plotNameStream.str()).c_str(), 140, 5300, 6000);
			mcRadiusPlots.push_back(histogram);
		}
	}
	
	// For each radius that is > 5000mm, get the Nhits and check in which Nhits window it falls, calculate the ratio and check in which ratio bin it falls
	// Based on these, fill the corresponding vectors and histograms with the radius and ratio values
	for (unsigned int f = 1; f < fileNamesVector.size(); f++)
	{
		RAT::DU::DSReader dsReader(fileNamesVector[f]);
		const RAT::DU::PMTInfo& pmtInfo = RAT::DU::Utility::Get()->GetPMTInfo();

		for(size_t i = 0; i < dsReader.GetEntryCount(); i++) 
		{
			const RAT::DS::Entry& dsEntry = dsReader.GetEntry(i);
			if (dsEntry.GetEVCount() == 0) continue;

			const RAT::DS::CalPMTs& calibratedPMTs = dsEntry.GetEV(0).GetCalPMTs();
			double eventNhits = calibratedPMTs.GetCount();
			if (eventNhits >= (nhitsWindows[numberOfNhitsWindows - 1] + nhitsWindowWidth)) continue;
		
			int eventNhitsWindow = -1;
			for (int w = 0; w < numberOfNhitsWindows; w++)
			{
				if ((eventNhits >= nhitsWindows[w]) && (eventNhits < (nhitsWindows[w] + nhitsWindowWidth)))
				{
					eventNhitsWindow = w;
					break;
				}
			}
			
			TVector3 eventPosition;
			for (size_t j = 0; j < calibratedPMTs.GetCount(); j++)
			{
				eventPosition += pmtInfo.GetPosition(calibratedPMTs.GetPMT(j).GetID());
			}
			
			double inDipCount = 0.0, totalCount = 0.0;
			for (size_t j = 0; j < calibratedPMTs.GetCount(); j++)
			{
				const RAT::DS::PMTCal& calibratedPMT = calibratedPMTs.GetPMT(j);
				TVector3 pmtPosition = pmtInfo.GetPosition(calibratedPMT.GetID());

				double angle = acos((eventPosition.Dot(pmtPosition)) / (eventPosition.Mag() * pmtPosition.Mag())) * (180 / pi);
				
				if ((angle >= dipLow) && (angle <= dipHigh))
				{
					inDipCount += 1.0;
				}
				totalCount += 1.0;
			}

			double ratio = (inDipCount / totalCount);
			if (ratio >= (ratioBins[numberOfRatioBins - 1] + ratioBinWidth)) continue;
			
			int eventRatioBin = -1;
			for (int b = 0; b < numberOfRatioBins; b++)
			{
				if ((ratio >= ratioBins[b]) && (ratio < (ratioBins[b] + ratioBinWidth)))
				{
					eventRatioBin = b;
					break;
				}
			}
			
			double mcRadius = dsEntry.GetMC().GetMCParticle(0).GetPosition().Mag();
		
			radiiAllNhitsWindows[eventNhitsWindow].push_back(mcRadius);
			ratiosAllNhitsWindows[eventNhitsWindow].push_back(ratio);
			mcRadiusPlots[(numberOfRatioBins * eventNhitsWindow) + eventRatioBin].Fill(mcRadius);
		}
	}
	
	// For each Nhits window, create a TGraph of ratio vs. radius, and fit the given function to the distribution
	TFile plotFile (plotsFileName, "UPDATE");
	
	std::vector< std::vector<double> > allFitCoefficients;
	for (int p = 0; p < numberOfParameters; p++)
	{
		std::vector<double> singlePowerCoefficients;
		allFitCoefficients.push_back(singlePowerCoefficients);
	}
	
	for (int w = 0; w < numberOfNhitsWindows; w++)
	{
		if ((radiiAllNhitsWindows[w]).size() != 0)
		{
			std::stringstream graphNameStream;
			graphNameStream << "ratioVsRadius_nhits=" << nhitsWindows[w];
			
			TGraph graph ((radiiAllNhitsWindows[w]).size(), &(radiiAllNhitsWindows[w])[0], &(ratiosAllNhitsWindows[w])[0]);
			graph.SetName((graphNameStream.str()).c_str());
			graph.SetTitle("Ratio Value as a Function of the MC Radius");
			graph.GetXaxis()->SetTitle("MC Radius, mm");
			graph.GetXaxis()->SetAxisColor(17);
			graph.GetYaxis()->SetTitle("Ratio");
			graph.GetYaxis()->SetAxisColor(17);
			graph.GetYaxis()->SetRangeUser(0.0, 0.8);
			graph.SetMarkerStyle(20);
			graph.SetMarkerSize(0.5);
			
			TF1* ratioRadiusFit = new TF1("ratioRadiusFit", fitFunction, 5350, 6005);
			graph.Fit(ratioRadiusFit, "RQ");
			
			plotFile.cd();
			graph.Write();
			
			for (int p = 0; p < numberOfParameters; p++)
			{
				allFitCoefficients[p].push_back(ratioRadiusFit->GetParameter(p));
			}
			
			delete ratioRadiusFit;
		}
		else
		{
			for (int p = 0; p < numberOfParameters; p++)
			{
				allFitCoefficients[p].push_back(0.0);
			}
		}
	}
	
	// For each of the mcRadius plots (one for each Nhits Window / Radio Bin combination), calculate and save the positive and negative errors
	std::vector<double> negativeErrors, positiveErrors;
	
	for (unsigned int h = 0; h < mcRadiusPlots.size(); h++)
	{
		if (mcRadiusPlots[h].Integral() == 0)
		{
			negativeErrors.push_back(5000);
			positiveErrors.push_back(5000);
		}
		else
		{
			int peakBin = mcRadiusPlots[h].GetMaximumBin(), binNum = 1;
			double sumFraction = 0.0;
			
			while (sumFraction <= ((0.5 * (1 - fraction)) * mcRadiusPlots[h].Integral()))
			{
				sumFraction += mcRadiusPlots[h].GetBinContent(binNum);
				binNum++;
			}
			negativeErrors.push_back(mcRadiusPlots[h].GetBinLowEdge(peakBin) - mcRadiusPlots[h].GetBinLowEdge(binNum));
			
			while (sumFraction <= ((0.5 * (1 + fraction)) * mcRadiusPlots[h].Integral()))
			{
				sumFraction += mcRadiusPlots[h].GetBinContent(binNum);
				binNum++;
			}
			positiveErrors.push_back(mcRadiusPlots[h].GetBinLowEdge(binNum) - mcRadiusPlots[h].GetBinLowEdge(peakBin));
		}
		
		plotFile.cd();
		mcRadiusPlots[h].Write();
	}
	
	plotFile.Close();
	
	allFitCoefficients.push_back(negativeErrors);
	allFitCoefficients.push_back(positiveErrors);
	
	radiiAllNhitsWindows.clear();
	ratiosAllNhitsWindows.clear();
	mcRadiusPlots.clear();
	
	// Return the entire set of fit parameters and errors, with the following structure:
	// allFitCoefficients[0] = vector of 0th radius power coefficients for the ratio vs. radius fit function (one entry for each Nhits window)
	// allFitCoefficients[1] = vector of 1st radius power coefficients for the ratio vs. radius fit function (one entry for each Nhits window)
	// allFitCoefficients[2] = vector of 2nd radius power coefficients for the ratio vs. radius fit function (one entry for each Nhits window)
	// allFitCoefficients[3] = vector of negative errors (one entry for each Nhits window / Ratio bin combination ... total = numberOfNhitsWindows * numberOfRatioBins entries)
	// allFitCoefficients[4] = vector of positive errors (one entry for each Nhits window / Ratio bin combination ... total = numberOfNhitsWindows * numberOfRatioBins entries)
	return allFitCoefficients;
}


