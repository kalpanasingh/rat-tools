
#include <vector>
#include <algorithm>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>

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

const double lowNhitsCut = 50;
static const int numberOfRadii = 8;
double radii[numberOfRadii] = {5000, 5300, 5400, 5500, 5600, 5700, 5800, 5900};		// This should contain the same values as the "radius" vector in ProduceData.py
static const int numberOfWindows = 12;
double nhitsWindows[numberOfWindows] = {0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750};	// Difference between consecutive values = "windowWidth" as defined below
const double windowWidth = 250;
static const int numberOfBins = 5;
double ratioBins[numberOfBins] = {0.1, 0.2, 0.3, 0.4, 0.5};	// Difference between consecutive values = "binWidth" as defined below
const double binWidth = 0.1;
const double fraction = 0.90;
const double dipLow = 40.0;
const double dipHigh = 90.0;
const double pi = 3.14159265358979323846;

double MMTSAt5000(string, double);
double MedianRatio(string, double);
TH1D* ErrorHist(string, double, double, TH1D*);


void Coordination(string index)
{
	ofstream stream0("Coordinate_Results.txt");
	stream0 << std::endl;
	
	double ratio5000[numberOfWindows];
	vector<double> gradients, intercepts, negativeErrors, positiveErrors;

	// Construct a list of filenames based on the radii
	vector<string> fileNames;
	for (int f = 0; f < numberOfRadii; f++)
	{
		std::ostringstream RadiusStream;
		RadiusStream << radii[f];
		std::string RadiusString = RadiusStream.str();
		
		std::stringstream fileNameStream;
		fileNameStream << "electrons_" << RadiusString << "mm.root";
		std::string fileNameString = fileNameStream.str();
		
		fileNames.push_back(fileNameString);
	}
	
	// For each Nhits window as defined above ...
	for (int x = 0; x < numberOfWindows; x++)
	{
		stream0 << "Analysing Data for Nhits Window: " << nhitsWindows[x] << " to " << nhitsWindows[x] + windowWidth << std::endl;

		// ... calculate the "mean - 3*sigma" ("mmts") value for this Nhits window (to be used later to find the ratio cut value)
		stream0 << "Calculating \"Mean - 3*Sigma\" Value ... ";

		ratio5000[x] = MMTSAt5000(fileNames[0], nhitsWindows[x]);
		stream0 << ratio5000[x] << std::endl;
		
		// ... calculate the linear fit parameters for this Nhits window
		stream0 << "Calculating Linear Fit Parameters ..." << std::endl;

		vector<double> radiiForGraph, ratiosForGraph;
		for (int f = 1; f < numberOfRadii; f++)
		{
			radiiForGraph.push_back(radii[f]);
			ratiosForGraph.push_back(MedianRatio(fileNames[f], nhitsWindows[x]));
		}
		
		TGraph graph (numberOfRadii - 1, &radiiForGraph[0], &ratiosForGraph[0]);
		TF1 *linearFit = new TF1("linearFit", "pol1", 5350, 6000);
		graph.Fit(linearFit, "RQ");
	
		gradients.push_back(linearFit->GetParameter(1));
		intercepts.push_back(linearFit->GetParameter(0));
		delete linearFit;
		radiiForGraph.clear();
		ratiosForGraph.clear();

		// ... calculate the negative and positive errors for this Nhits window
		stream0 << "Calculating Negative and Positive Errors ..." << std::endl;
		
		for (int z = 0; z < numberOfBins; z++)
		{
			TH1D* histo = new TH1D("histo", "histo", 140, 5300, 6000);
			for (int f = 1; f < numberOfRadii; f++)
			{
				histo = ErrorHist(fileNames[f], nhitsWindows[x], ratioBins[z], histo);
			}
			double totalEvents = histo->Integral();
			
			if (totalEvents == 0)
			{
				negativeErrors.push_back(5000);
				positiveErrors.push_back(5000);
			}
			else
			{
				int peakBin = histo->GetMaximumBin(), binNum = 1;
				double sumFraction = 0.0;
				
				while (sumFraction <= ((0.5 * (1 - fraction)) * totalEvents))
				{
					sumFraction += histo->GetBinContent(binNum);
					binNum++;
				}
				negativeErrors.push_back(histo->GetBinLowEdge(peakBin) - histo->GetBinLowEdge(binNum));
				
				while (sumFraction <= ((0.5 * (1 + fraction)) * totalEvents))
				{
					sumFraction += histo->GetBinContent(binNum);
					binNum++;
				}
				positiveErrors.push_back(histo->GetBinLowEdge(binNum) - histo->GetBinLowEdge(peakBin));
			}
			
			delete histo;
		}

		stream0 << "Completed Nhits Window: " << nhitsWindows[x] << " to " << nhitsWindows[x] + windowWidth << std::endl;
		stream0 << std::endl;
	}

	// Make a linear fit to the "mean - 3*sigma" values, to find the relationship between ratio cut value and Nhits
	stream0 << "Calculating ratio cut values ... ";
	
	TGraph graph (numberOfWindows, nhitsWindows, ratio5000);
	TF1 *ratioFit = new TF1("ratioFit", "pol1", 750, 3000);		// Ignore the low Nhits points, i.e. below 750 Nhits, when finding the linear fit
	graph.Fit(ratioFit, "RQ");
	double ratioGradient = ratioFit->GetParameter(1);
	double ratioIntercept = ratioFit->GetParameter(0);
	
	stream0 << "ratio fit gradient = " << ratioGradient << ", ratio fit intercept = " << ratioIntercept << std::endl;
	delete ratioFit;
	
	// Print coordinated values to screen in RATDB format
	stream0 << std::endl;
	stream0 << "Please place the text below into the database file: FIT_NEAR_AV_ANGULAR.ratdb located in rat/data, replacing any existing entry with the same index." << std::endl;
	stream0 << std::endl;
	stream0 << "{" << std::endl;
	stream0 << "name = \"FIT_NEAR_AV_ANGULAR\"," << std::endl;
	stream0 << "index: \"" << index << "\"," << std::endl;
	stream0 << "valid_begin : [0, 0]," << std::endl;
	stream0 << "valid_end : [0, 0]," << std::endl;
	stream0 << "nhits_windows: [";
	for (int a = 0; a < numberOfWindows; a++)
	{
		stream0 << nhitsWindows[a] << ", ";
	}
	stream0 << "]," << std::endl;
	stream0 << "nhits_cutoffs: " << lowNhitsCut << "," << std::endl;
	stream0 << "window_width: " << windowWidth << "," << std::endl;
	stream0 << "fit_gradients: [";
	for (unsigned int a = 0; a < gradients.size(); a++)
	{
		stream0 << gradients[a] << ", ";
	}
	stream0 << "]," << std::endl;
	stream0 << "fit_intercepts: [";
	for (unsigned int a = 0; a < intercepts.size(); a++)
	{
		stream0 << intercepts[a] << ", ";
	}
	stream0 << "]," << std::endl;
	stream0 << "ratio_cuts: [";
	for (int a = 0; a < numberOfWindows; a++)
	{
		double ratioCut = ((nhitsWindows[a] * ratioGradient) + ratioIntercept);
		stream0 << ratioCut << ", ";
	}
	stream0 << "]," << std::endl;
	stream0 << "ratio_bins: [";
	for (int a = 0; a < numberOfBins; a++)
	{
		stream0 << ratioBins[a] << ", ";
	}
	stream0 << "]," << std::endl;
	stream0 << "bin_width: " << binWidth << "," << std::endl;
	stream0 << "negative_errors: [";
	for (unsigned int a = 0; a < negativeErrors.size(); a++)
	{
		stream0 << negativeErrors[a] << ", ";
	}
	stream0 << "]," << std::endl;
	stream0 << "positive_errors: [";
	for (unsigned int a = 0; a < positiveErrors.size(); a++)
	{
		stream0 << positiveErrors[a] << ", ";
	}
	stream0 << "]," << std::endl;
	stream0 << "theta_error: 0.1745," << std::endl;
	stream0 << "phi_error: 0.1745," << std::endl;
	stream0 << "}" << std::endl;
	stream0 << std::endl;
}


double MMTSAt5000(string infile, double lowNhits)
{
	TH1D Histogram("Histogram", "Histogram", 100, 0.0, 0.8);
	
	RAT::DU::DSReader dsReader(infile);
	const RAT::DU::PMTInfo& pmtInfo = RAT::DU::Utility::Get()->GetPMTInfo();

	for(size_t i = 0; i < dsReader.GetEntryCount(); i++) 
	{
		const RAT::DS::Entry& dsEntry = dsReader.GetEntry(i);
		if (dsEntry.GetEVCount() == 0) continue;

		const RAT::DS::EV& triggeredEvent = dsEntry.GetEV(0);
		const RAT::DS::CalPMTs& calibratedPMTs = triggeredEvent.GetCalPMTs();
		if (calibratedPMTs.GetCount() < lowNhitsCut) continue;
		if ((calibratedPMTs.GetCount() < lowNhits) || (calibratedPMTs.GetCount() >= (lowNhits + windowWidth))) continue;
		
		TVector3 eventPosition;
		for (size_t j = 0; j < calibratedPMTs.GetNormalCount(); j++)
		{
			eventPosition += pmtInfo.GetPosition(calibratedPMTs.GetPMT(j).GetID());
		}
		
		double inDipCount = 0.0, totalCount = 0.0;
		for (size_t j = 0; j < calibratedPMTs.GetNormalCount(); j++)
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
		Histogram.Fill(ratio);
	}

	TF1 *gaussFit = new TF1("gaus", "gaus", 0.0, 0.8);
	Histogram.Fit(gaussFit, "RQ");
	
	double mmts = (gaussFit->GetParameter(1) - (3 * gaussFit->GetParameter(2)));
	return mmts;		
}

double MedianRatio(string infile, double lowNhits)
{
	vector<double> ratios;

	RAT::DU::DSReader dsReader(infile);
	const RAT::DU::PMTInfo& pmtInfo = RAT::DU::Utility::Get()->GetPMTInfo();

	for(size_t i = 0; i < dsReader.GetEntryCount(); i++) 
	{
		const RAT::DS::Entry& dsEntry = dsReader.GetEntry(i);
		if (dsEntry.GetEVCount() == 0) continue;

		const RAT::DS::EV& triggeredEvent = dsEntry.GetEV(0);
		const RAT::DS::CalPMTs& calibratedPMTs = triggeredEvent.GetCalPMTs();
		if (calibratedPMTs.GetCount() < lowNhitsCut) continue;
		if ((calibratedPMTs.GetCount() < lowNhits) || (calibratedPMTs.GetCount() >= (lowNhits + windowWidth))) continue;
	
		TVector3 eventPosition;
		for (size_t j = 0; j < calibratedPMTs.GetNormalCount(); j++)
		{
			eventPosition += pmtInfo.GetPosition(calibratedPMTs.GetPMT(j).GetID());
		}
		
		double inDipCount = 0.0, totalCount = 0.0;
		for (size_t j = 0; j < calibratedPMTs.GetNormalCount(); j++)
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
		ratios.push_back(ratio);
	}

	sort(ratios.begin(), ratios.end());
	int s = ratios.size();
		
	if ((s % 2) == 0)
    {
		return ((ratios[s / 2] + ratios[(s / 2) - 1]) / 2);
	}
	else
	{
		double midIndex = ((s / 2) - 0.5);
		int u = (int)midIndex;
		return ratios[u];
	}
}

TH1D* ErrorHist(string infile, double lowNhits, double lowRatio, TH1D* histo)
{
	RAT::DU::DSReader dsReader(infile);
	const RAT::DU::PMTInfo& pmtInfo = RAT::DU::Utility::Get()->GetPMTInfo();

	for(size_t i = 0; i < dsReader.GetEntryCount(); i++) 
	{
		const RAT::DS::Entry& dsEntry = dsReader.GetEntry(i);
		if (dsEntry.GetEVCount() == 0) continue;

		const RAT::DS::EV& triggeredEvent = dsEntry.GetEV(0);
		const RAT::DS::CalPMTs& calibratedPMTs = triggeredEvent.GetCalPMTs();
		if (calibratedPMTs.GetCount() < lowNhitsCut) continue;
		if ((calibratedPMTs.GetCount() < lowNhits) || (calibratedPMTs.GetCount() >= (lowNhits + windowWidth))) continue;
	
		TVector3 eventPosition;
		for (size_t j = 0; j < calibratedPMTs.GetNormalCount(); j++)
		{
			eventPosition += pmtInfo.GetPosition(calibratedPMTs.GetPMT(j).GetID());
		}
		
		double inDipCount = 0.0, totalCount = 0.0;
		for (size_t j = 0; j < calibratedPMTs.GetNormalCount(); j++)
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
		if ((ratio < lowRatio) || (ratio >= (lowRatio + binWidth))) continue;
      
		const RAT::DS::MC& mcEvent = dsEntry.GetMC();
		const RAT::DS::MCParticle& mcParticle = mcEvent.GetMCParticle(0);
		TVector3 mcPosition = mcParticle.GetPosition();
		histo->Fill(mcPosition.Mag());
	}

	return histo;
}

