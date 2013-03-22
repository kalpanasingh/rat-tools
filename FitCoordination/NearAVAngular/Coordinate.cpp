
#include <vector>
#include <algorithm>
#include <string>
#include <iostream>
#include <fstream>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TMath.h>
#include <TH1.h>
#include <TGraph.h>
#include <TAxis.h>
#include <TF1.h>

#include <RAT/DS/MC.hh>
#include <RAT/DS/MCParticle.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/PMTCal.hh>
#include <RAT/DS/Root.hh>
#include <RAT/DS/Run.hh>

const double lowNhitsCut = 50;
const double windowWidth = 250;
const double binWidth = 0.1;
const double fraction = 0.90;
const double dipLow = 40.0;
const double dipHigh = 90.0;
const double pi = 3.14159265358979323846;

TH1D* Hist5000(char*, double, TH1D*);
double MeanRatio(char*, double);
TH1D* ErrorHist(char*, double, double, TH1D*);


void Coordination(char* infile5000, char* infile5300, char* infile5400, char* infile5500, char* infile5600, char* infile5700, char* infile5800, char* infile5900)
{
	ofstream stream0("Coordinate_Results.txt");
	stream0 << std::endl;
	
	static const int w = 12, r = 7, b = 5;
	double nhitsWindows[w] = {0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750};		// Difference between consecutive values = "windowWidth" as defined above
	double ratio5000[w];
	double radii[r] = {5300, 5400, 5500, 5600, 5700, 5800, 5900};	// This should contain the same values as the "radius" vector in Utilities.py
	double ratioBins[b] = {0.1, 0.2, 0.3, 0.4, 0.5};	//  Difference between consecutive values = "binWidth" as defined above
	
	vector<double> gradients, intercepts, negativeErrors, positiveErrors;
	
	for (int x = 0; x < w; x++)
	{
		stream0 << "Analysing Data for Nhits Window: " << nhitsWindows[x] << " to " << nhitsWindows[x] + windowWidth << std::endl;

		// Calculate the "mean-3*sigma" value for this Nhits window ... to be used later to find the ratio cut value
		stream0 << "Calculating \"Mean-3*Sigma\" Value ... ";

		TH1D *temphisto = new TH1D("temphisto", "temphisto", 100, 0.0, 0.8);
		temphisto = Hist5000(infile5000, nhitsWindows[x], temphisto);
		TF1 *gausFit = new TF1("gausFit", "gaus", 0.0, 0.8);
		temphisto->Fit("gausFit", "RQ");
		ratio5000[x] = (gausFit->GetParameter(1) - (3 * gausFit->GetParameter(2)));
		stream0 << ratio5000[x] << std::endl;
		
		delete gausFit;
		delete temphisto;

		// Calculate the linear fit parameters for this Nhits window
		stream0 << "Calculating Linear Fit Parameters ..." << std::endl;

		double *ratios = NULL;
		ratios = new double[r];
		
		ratios[0] = MeanRatio(infile5300, nhitsWindows[x]);
		ratios[1] = MeanRatio(infile5400, nhitsWindows[x]);
		ratios[2] = MeanRatio(infile5500, nhitsWindows[x]);
		ratios[3] = MeanRatio(infile5600, nhitsWindows[x]);
		ratios[4] = MeanRatio(infile5700, nhitsWindows[x]);
		ratios[5] = MeanRatio(infile5800, nhitsWindows[x]);
		ratios[6] = MeanRatio(infile5900, nhitsWindows[x]);		

		TGraph *graph = new TGraph(r, radii, ratios);
		TF1 *linearFit = new TF1("linearFit", "pol1", 5350, 6000);
		graph->Fit("linearFit", "RQ");
		
		gradients.push_back(linearFit->GetParameter(1));
		intercepts.push_back(linearFit->GetParameter(0));
		delete [] ratios;
		ratios = NULL;
		delete graph;
		delete linearFit;

		// Calculate the negative and positive errors for this Nhits window
		stream0 << "Calculating Negative and Positive Errors ..." << std::endl;

		for (int z = 0; z < b; z++)
		{
			TH1D *histo = new TH1D("histo", "histo", 140, 5300, 6000);
	
			histo = ErrorHist(infile5300, nhitsWindows[x], ratioBins[z], histo);
			histo = ErrorHist(infile5400, nhitsWindows[x], ratioBins[z], histo);
			histo = ErrorHist(infile5500, nhitsWindows[x], ratioBins[z], histo);
			histo = ErrorHist(infile5600, nhitsWindows[x], ratioBins[z], histo);
			histo = ErrorHist(infile5700, nhitsWindows[x], ratioBins[z], histo);
			histo = ErrorHist(infile5800, nhitsWindows[x], ratioBins[z], histo);
			histo = ErrorHist(infile5900, nhitsWindows[x], ratioBins[z], histo);

			double totalEvents = histo->Integral();
			
			if (totalEvents == 0)
			{
				negativeErrors.push_back(5000);
				positiveErrors.push_back(5000);
				delete histo;
				continue;
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
				
				delete histo;
				continue;
			}
		}

		stream0 << "Completed Nhits Window: " << nhitsWindows[x] << " to " << nhitsWindows[x] + windowWidth << std::endl;
		stream0 << std::endl;
	}

	// Make a linear fit to the "mean - 3*sigma" values, to find the relationship between ratio cut value and Nhits
	stream0 << "Calculating ratio cut values ... ";
	TGraph *graph = new TGraph(w, nhitsWindows, ratio5000);
	TF1 *ratioFit = new TF1("ratioFit", "pol1", 750, 3000);		// Ignore the low Nhits points, i.e. below 750 Nhits, when finding the linear fit
	graph->Fit("ratioFit", "RQ");
	double ratioGradient = ratioFit->GetParameter(1);
	double ratioIntercept = ratioFit->GetParameter(0);
	stream0 << "ratio fit gradient = " << ratioGradient << ", ratio fit intercept = " << ratioIntercept << std::endl;

	// Print coordinated values to screen in RATDB format, so that the user can just copy-paste the results into the RATDB file
	stream0 << std::endl;
	stream0 << "Please place the text below into the database file: FIT_NEAR_AV_ANGULAR.ratdb located in rat/data, replacing the existing corresponding text." << std::endl;
	stream0 << std::endl;
	stream0 << "nhits_windows: [";
	for (int a = 0; a < w; a++)
	{
		stream0 << nhitsWindows[a] << ", ";
	}
	stream0 << "]," << std::endl;
	stream0 << "nhits_cutoffs: " << lowNhitsCut << "," << std::endl;
	stream0 << "window_width: " << windowWidth << "," << std::endl;
	stream0 << "fit_gradients: [";
	for (unsigned int a = 0; a < gradients.size(); a++)
	{
		stream0 << gradients[a] << "d, ";
	}
	stream0 << "]," << std::endl;
	stream0 << "fit_intercepts: [";
	for (unsigned int a = 0; a < intercepts.size(); a++)
	{
		stream0 << intercepts[a] << "d, ";
	}
	stream0 << "]," << std::endl;
	stream0 << "ratio_cuts: [";
	for (int a = 0; a < w; a++)
	{
		double ratioCut = ((nhitsWindows[a] * ratioGradient) + ratioIntercept);
		stream0 << ratioCut << "d, ";
	}
	stream0 << "]," << std::endl;
	stream0 << "ratio_bins: [";
	for (int a = 0; a < b; a++)
	{
		stream0 << ratioBins[a] << "d, ";
	}
	stream0 << "]," << std::endl;
	stream0 << "bin_width: " << binWidth << "d," << std::endl;
	stream0 << "negative_errors: [";
	for (unsigned int a = 0; a < negativeErrors.size(); a++)
	{
		stream0 << negativeErrors[a] << "d, ";
	}
	stream0 << "]," << std::endl;
	stream0 << "positive_errors: [";
	for (unsigned int a = 0; a < positiveErrors.size(); a++)
	{
		stream0 << positiveErrors[a] << "d, ";
	}
	stream0 << "]," << std::endl;
	stream0 << std::endl;
}


TH1D* Hist5000(char* infile, double lowNhits, TH1D* histo)
{
	TFile *f = new TFile(infile);

	TTree *eventtree = (TTree*)f->Get("T");
	RAT::DS::Root *eventds = new RAT::DS::Root();
	eventtree->SetBranchAddress("ds", &eventds);
	
	TTree *pmttree = (TTree*)f->Get("runT");
	RAT::DS::Run *pmtds = new RAT::DS::Run();
	pmttree->SetBranchAddress("run", &pmtds);
	pmttree->GetEntry();
	RAT::DS::PMTProperties *pmtProps = pmtds->GetPMTProp();
	
	for (int i = 0; i < eventtree->GetEntries(); i++)
	{
		eventtree->GetEntry(i);
		if ((eventds->GetEVCount()) == 0) continue;
		RAT::DS::EV *eventev = eventds->GetEV(0);
		if (eventev->GetPMTCalCount() < lowNhitsCut) continue;    // Ignore events with too few Nhits
		if ((eventev->GetPMTCalCount() < lowNhits) || (eventev->GetPMTCalCount() >= (lowNhits + windowWidth))) continue;
		
		TVector3 eventvector;
		for (int j = 0; j < eventev->GetPMTCalCount(); j++)
		{
			RAT::DS::PMTCal *pmt = eventev->GetPMTCal(j);
			TVector3 pmtvector = pmtProps->GetPos(pmt->GetID());
			eventvector += pmtvector;
		}
		
		double pmtcount = 0.0, total = 0.0;
		for (int k = 0; k < eventev->GetPMTCalCount(); k++)
		{
			RAT::DS::PMTCal *pmt = eventev->GetPMTCal(k);
			TVector3 pmtvector = pmtProps->GetPos(pmt->GetID());

			double angle = acos((eventvector.Dot(pmtvector)) / (eventvector.Mag() * pmtvector.Mag())) * (180 / pi);

			if ((angle >= dipLow) && (angle <= dipHigh))
			{
				pmtcount += 1.0;
			}
			total += 1.0;
		}

		double ratio = (pmtcount / total);
		histo->Fill(ratio);
	}

	f->Close();
	return histo;
}


double MeanRatio(char *infile, double lowNhits)
{
	vector<double> ratios;

	TFile *f = new TFile(infile);
	
	TTree *eventtree = (TTree*)f->Get("T");
	RAT::DS::Root *eventds = new RAT::DS::Root();
	eventtree->SetBranchAddress("ds", &eventds);

	TTree *pmttree = (TTree*)f->Get("runT");
	RAT::DS::Run *pmtds = new RAT::DS::Run();
	pmttree->SetBranchAddress("run", &pmtds);
	pmttree->GetEntry();
	RAT::DS::PMTProperties *pmtProps = pmtds->GetPMTProp();
	
	for (int i = 0; i < eventtree->GetEntries(); i++)
	{
		eventtree->GetEntry(i);
		if ((eventds->GetEVCount()) == 0) continue;
		RAT::DS::EV *eventev = eventds->GetEV(0);
		if (eventev->GetPMTCalCount() < lowNhitsCut) continue;    // Ignore events with too few Nhits
		if ((eventev->GetPMTCalCount() < lowNhits) || (eventev->GetPMTCalCount() >= (lowNhits + windowWidth))) continue;
		
		TVector3 eventvector;
		for (int j = 0; j < eventev->GetPMTCalCount(); j++)
		{
			RAT::DS::PMTCal *pmt = eventev->GetPMTCal(j);
			TVector3 pmtvector = pmtProps->GetPos(pmt->GetID());
			eventvector += pmtvector;
		}
		
		double pmtcount = 0.0, total = 0.0;
		for (int k = 0; k < eventev->GetPMTCalCount(); k++)
		{
			RAT::DS::PMTCal *pmt = eventev->GetPMTCal(k);
			TVector3 pmtvector = pmtProps->GetPos(pmt->GetID());

			double angle = acos((eventvector.Dot(pmtvector)) / (eventvector.Mag() * pmtvector.Mag())) * (180 / pi);

			if ((angle >= dipLow) && (angle <= dipHigh))
			{
				pmtcount += 1.0;
			}
			total += 1.0;
		}

		double ratio = (pmtcount / total);
		ratios.push_back(ratio);
	}

	f->Close();
	
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


TH1D* ErrorHist(char* infile, double lowNhits, double lowRatio, TH1D* histo)
{
	TFile *f = new TFile(infile);

	TTree *eventtree = (TTree*)f->Get("T");
	RAT::DS::Root *eventds = new RAT::DS::Root();
	eventtree->SetBranchAddress("ds", &eventds);
	
	TTree *pmttree = (TTree*)f->Get("runT");
	RAT::DS::Run *pmtds = new RAT::DS::Run();
	pmttree->SetBranchAddress("run", &pmtds);
	pmttree->GetEntry();
	RAT::DS::PMTProperties *pmtProps = pmtds->GetPMTProp();
	
	for (int i = 0; i < eventtree->GetEntries(); i++)
	{
		eventtree->GetEntry(i);
		if ((eventds->GetEVCount()) == 0) continue;
		RAT::DS::EV *eventev = eventds->GetEV(0);
		if (eventev->GetPMTCalCount() < lowNhitsCut) continue;    // Ignore events with too few Nhits
		if ((eventev->GetPMTCalCount() < lowNhits) || (eventev->GetPMTCalCount() >= (lowNhits + windowWidth))) continue;
		
		TVector3 eventvector;
		for (int j = 0; j < eventev->GetPMTCalCount(); j++)
		{
			RAT::DS::PMTCal *pmt = eventev->GetPMTCal(j);
			TVector3 pmtvector = pmtProps->GetPos(pmt->GetID());
			eventvector += pmtvector;
		}
		
		double pmtcount = 0.0, total = 0.0;
		for (int k = 0; k < eventev->GetPMTCalCount(); k++)
		{
			RAT::DS::PMTCal *pmt = eventev->GetPMTCal(k);
			TVector3 pmtvector = pmtProps->GetPos(pmt->GetID());

			double angle = acos((eventvector.Dot(pmtvector)) / (eventvector.Mag() * pmtvector.Mag())) * (180 / pi);

			if ((angle >= dipLow) && (angle <= dipHigh))
			{
				pmtcount += 1.0;
			}
			total += 1.0;
		}

		double ratio = (pmtcount / total);
		if ((ratio < lowRatio) || (ratio >= (lowRatio + binWidth))) continue;

		RAT::DS::MC *eventmc = eventds->GetMC();
		RAT::DS::MCParticle *eventpart = eventmc->GetMCParticle(0);
		TVector3 MCvector = eventpart->GetPos();
		histo->Fill(MCvector.Mag());
	}

	return histo;
}


int main(int argc, char* argv[])
{
	Coordination("electrons_5000mm.root", "electrons_5300mm.root", "electrons_5400mm.root", "electrons_5500mm.root", "electrons_5600mm.root", "electrons_5700mm.root", "electrons_5800mm.root", "electrons_5900mm.root");
}
