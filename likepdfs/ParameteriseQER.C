/*-----------------------------------------------------------------------
This is a simple root macro that fits the total charge distributions to 
determine a parameterisation for the mean and sigma as a function of position 
and true energy for use in the FitLike likelihood fit for event energy.

The total charge distribution fits well to a Gaussian and it appears that 
the mean and sigma follow quadratic trends in E and R. 

The method is to take the histograms from files, extract the generated energy and 
position from the last two bins of the file (hardcoded in the processor that created them). 
Rebin and refit the histograms. 
Take the mean and sigma of the fitted gaussians and parameterise them in terms 
of energy and position. 
Afterwards, check that gaussians with the parameterised mean and sigma fit 
well to the original data histograms (plot and extract chisquared).

Make plots 
C1: Q distributions with fitted gaussians with different panels showing different radii
C2: Q distributions with fitted gaussians with different panels showing different energies
Cg: Graphs of fitted means and sigmas against energy and radius
C3: Gaussians with parameterised mean and sigma shown against histograms with different panels showing different radii

Note that the fit should work for any set of E and R histograms, but for nicely formatted plots (and correct labels) 
it expects R = 0, 1, 2, 3, 4, 5 m and E = 0.5, 1.0, 1.5...5.5 MeV

To run, open root, and type:
> .L ParameteriseQER.C
> Param()
-----------------------------------------------------------------------*/
// Root includes
#include "TROOT.h"
#include "TFile.h"
#include "TF1.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TMinuit.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TStyle.h"
#include "TLatex.h"

// C++ includes
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
using std::cout;
using std::endl;

int nTot;	// total number of histograms read in
const int MAX(100);	// upper limit
float Ecount[MAX];
float Vcount[MAX];
float mean[MAX];
float sigma[MAX];

double calcMean(double *E, double *V, double *par){
	// Define the mean with 9 parameters (quadratic with both Energy, E,  and radius, V)
	double A = par[0]+par[1]*V[0] + par[2]*pow(V[0],2);
	double B = par[3]+par[4]*V[0] + par[5]*pow(V[0],2);
	double C = par[6]+par[7]*V[0] + par[8]*pow(V[0],2);
	double mean = A + B*E[0] + C*pow(E[0],2);
	return mean;
}

void meanFCN(Int_t &npar, Double_t *gin, Double_t &f, Double_t *par, Int_t iflag)
{
	// This is the function MINUIT minimises when fitting the parameterisation of the means
    double temp;
    temp = gin[0]*iflag;		// Use the input parameters we don't need to stop complaints
    double chisq = 0;
    double mymean;
	double myE[1], myV[1];
    for(int iC=0; iC<nTot; ++iC){
		myE[0] = Ecount[iC];
		myV[0] = Vcount[iC];
        mymean = calcMean(myE,myV,par);
        chisq += pow((mean[iC]-mymean),2)/mymean;               
    }
    f = chisq;	
}

double calcSigma(double *E, double *V, double *par){
	// Define the sigma with 9 parameters (quadratic with both Energy, E,  and radius, V)
	double A = par[0]+par[1]*V[0] + par[2]*pow(V[0],2);
	double B = par[3]+par[4]*V[0] + par[5]*pow(V[0],2);
	double C = par[6]+par[7]*V[0] + par[8]*pow(V[0],2);
	double sigma = A + B*E[0] + C*pow(E[0],2);
	return sigma;
}

void sigmaFCN(Int_t &npar, Double_t *gin, Double_t &f, Double_t *par, Int_t iflag)
{
	// This is the function MINUIT minimises when fitting the parameterisation of the sigmas
    double temp;
    temp = gin[0]*iflag;		// Use the input parameters we don't need to stop complaints
    double chisq = 0;
    double mysigma;
	double myE[1], myV[1];
    for(int iC=0; iC<nTot; ++iC){
		myE[0] = Ecount[iC];
		myV[0] = Vcount[iC];
        mysigma = calcSigma(myE,myV,par);
        chisq += pow((sigma[iC]-mysigma),2)/mysigma;               
    }
    f = chisq;	
}

void Param(char* filelist = "files_energy.txt", bool verbose = false){
	// This function does the bulk of the work. The input is the name of the file containing 
	// the list of histogram files. User can also change to more verbose output from fits.
	int count = 0;

	// Plot the charge histograms
	gStyle->SetOptStat(0);
	gStyle->SetOptTitle(0);
	TCanvas *C1 = new TCanvas("C1");	// each pad for a different radius
	C1->Divide(2,3);
	TCanvas *C3 = new TCanvas("C3");	// each pad for a different energy
	C3->Divide(2,3);
	TH2F *space = new TH2F("space","",1,0,120000,1,0,30);
	TLatex *lat1[6];
	for(int i=0;i<6;++i){
		lat1[i] = new TLatex(90000,25,Form("V = %d m", i));
		C1->cd(i+1);
		space->Draw();
		lat1[i]->Draw();
		C3->cd(i+1);
		space->Draw();
		lat1[i]->Draw();
	}
	TCanvas *C2 = new TCanvas("C2");
	C2->Divide(2,6);
	TLatex *lat2[11];
	for(int i=0;i<11;++i){
		float E = 0.5*(i+1);
		lat2[i] = new TLatex(90000,25,Form("E = %f2.1 MeV", E));
		C2->cd(i+1);
		space->Draw();
		lat2[i]->Draw();
	}
	TCanvas *Ctemp = new TCanvas("Ctemp");		// temporary canvas for fits

	// Need to refit
	TH1F *h[MAX];		// store histograms obtained from files
	TF1 *f1[MAX];		// gaussian fit to data
	TF1 *f2[MAX];		// gaussian with parameterised mean and sigma - test results
	
	// load up info from all the files in the list
	ifstream fin;
	fin.open(filelist);
	char histname[500];
	fin >> histname;
	do{
		TFile *f = new TFile(histname);
		// store and rename the histogram
		h[count] = (TH1F*)f->Get("Qdist");
		h[count]->SetName(Form("Qdist%d",count));
		// store energy
		Ecount[count] = h[count]->GetBinContent(1002);
		// and radius
		Vcount[count] = h[count]->GetBinContent(1001)/1000.;
		// just to decide where to plot things..
		int pos = int(Vcount[count]);
		int eng = int(Ecount[count]/0.5);
		int eng2 = eng;
		if(eng>=10)eng2 = eng+1;
		// choose range for the fit (based on ~18000ADC counts / MeV)
		float min = (Ecount[count]-1)*18000;
		float max = (Ecount[count]+1)*18000;
		f1[count] = new TF1(Form("Qfit%d",count),"gaus",min,max);
		f2[count] = new TF1(Form("Qfit%d",count),"gaus",min,max);
		f1[count]->SetParameters(Ecount[count]*18000,6000);
		f1[count]->SetLineColor(pos+1);
		f1[count]->SetLineWidth(1);

		Ctemp->cd();
		// need to rebin histogram so that fit has sufficient information
		h[count]->Fit(f1[count],"QR");
		mean[count] = f1[count]->GetParameter(1);
		sigma[count] = f1[count]->GetParameter(2);
		if(verbose){
			cout << histname << " " << count << " " << Ecount[count] << " " <<  Vcount[count]
			 << " " << mean[count] << " " << sigma[count] << endl;
		}
		C1->cd(pos+1);
		h[count]->SetLineColor(pos+1);
		h[count]->Draw("histsame");
		f1[count]->Draw("same");
		C2->cd(eng);
		h[count]->Draw("histsame");
		f1[count]->Draw("same");

		// done - get next histogram
		count++;
		fin >> histname;
	}while(fin.good());
	
	nTot = count;
	cout << "Read in " << nTot << " Files " << endl;
	
	// Make some plots
	TCanvas *Cg = new TCanvas("Cg");
	Cg->Divide(2,2);
	Cg->cd(1);
	TGraph *gEmeanTot = new TGraph(nTot, Ecount, mean);
	gEmeanTot->GetXaxis()->SetTitle("Energy (MeV)");
	gEmeanTot->GetYaxis()->SetTitle("mean Qtot (ADC counts)");
	gEmeanTot->SetMarkerStyle(2);
	gEmeanTot->Draw("AP");
	Cg->cd(2);
	TGraph *gEsigTot = new TGraph(nTot, Ecount, sigma);
	gEsigTot->GetXaxis()->SetTitle("Energy (MeV)");
	gEsigTot->GetYaxis()->SetTitle("Qtot sigma (ADC counts)");
	gEsigTot->SetMarkerStyle(2);
	gEsigTot->Draw("AP");
	Cg->cd(3);
	TGraph *gVmeanTot = new TGraph(nTot, Vcount, mean);
	gVmeanTot->GetXaxis()->SetTitle("Radial postision (m)");
	gVmeanTot->GetYaxis()->SetTitle("mean Qtot (ADC counts)");
	gVmeanTot->SetMarkerStyle(2);
	gVmeanTot->Draw("AP");
	Cg->cd(4);
	TGraph *gVsigTot = new TGraph(nTot, Vcount, sigma);
	gVsigTot->GetXaxis()->SetTitle("Radial position (m)");
	gVsigTot->GetYaxis()->SetTitle("Qtot sigma (ADC counts)");
	gVsigTot->SetMarkerStyle(2);
	gVsigTot->Draw("AP");	
	
	
	// Now try for a 2D fit to the mean
	const int npar(9);
	TMinuit minmean(npar);	
	minmean.SetFCN(meanFCN);
	if(!verbose) minmean.SetPrintLevel(-1);
	int ierflg =0;
	double arglist[10];
	minmean.mnparm(0,"A",-200,10,0,0,ierflg);
	minmean.mnparm(1,"B",5.,0.1,0,0,ierflg);
	minmean.mnparm(2,"C",1.,0.1,0,0,ierflg);
	minmean.mnparm(3,"D",18000.,1.0,0,0,ierflg);
	minmean.mnparm(4,"E",0.02,0.1,0,0,ierflg);
	minmean.mnparm(5,"F",0.,0.1,0,0,ierflg);
	minmean.mnparm(6,"G",150.,0.1,0,0,ierflg);
	minmean.mnparm(7,"H",-0.1,0.1,0,0,ierflg);
	minmean.mnparm(8,"I",0.1,0.1,0,0,ierflg);

	
	arglist[0] = 150000;
	arglist[1] = 1.;
	minmean.mnexcm("MIGRAD",arglist,2,ierflg);
	
	// Now check the fit values
	double meanparams[npar], meanerr[npar];
	cout << "Fit to means: "<< endl;
    for(int iP=0; iP<npar; ++iP){
        minmean.GetParameter(iP,meanparams[iP], meanerr[iP]);
 		cout << "Param " << iP << " = " << meanparams[iP] << " +/- " << meanerr[iP] << endl;
	}
	cout << "Chisquared = " << minmean.fAmin << " per " << minmean.GetNumFreePars() << 
	        " parameters " << endl;
	
	if(verbose){
		// How well does the fit do?
		cout << "Compare means: Fit cf Param " << endl;
		double myE[1], myV[1];
		for(int iC=0; iC<nTot; ++iC){
			myE[0] = Ecount[iC];
			myV[0] = Vcount[iC];
			float temp = calcMean(myE, myV, meanparams);
			if(verbose){
				 cout << "E = " << myE[0] << " V = " << myV[0] << " : " 
			           << mean[iC] << " cf " << temp << endl;
			}		   
		}
	}
	
	// Now try for a 2D fit to the sigma
	const int npar2(9);
	TMinuit minsigma(npar2);	
	minsigma.SetFCN(sigmaFCN);
	if(!verbose) minsigma.SetPrintLevel(-1);
	ierflg =0;
	minsigma.mnparm(0,"A",450,10,0,0,ierflg);
	minsigma.mnparm(1,"B",0.005,0.1,0,0,ierflg);
	minsigma.mnparm(2,"C",0.,0.1,0,0,ierflg);
	minsigma.mnparm(3,"D",500,1.0,0,0,ierflg);
	minsigma.mnparm(4,"E",0.0,0.1,0,0,ierflg);
	minsigma.mnparm(5,"F",0.,0.1,0,0,ierflg);
	minsigma.mnparm(6,"G",-20,0.1,0,0,ierflg);
	minsigma.mnparm(7,"H",0.,0.1,0,0,ierflg);
	minsigma.mnparm(8,"I",0.,0.1,0,0,ierflg);	
	arglist[0] = 150000;
	arglist[1] = 1.;
	minsigma.mnexcm("MIGRAD",arglist,2,ierflg);
	
	// Now check the fit values
	double sigmaparams[npar2], sigmaerr[npar2];
	cout << "Fit to sigmas: " << endl;
	for(int iP=0; iP<npar2; ++iP){
	  minsigma.GetParameter(iP,sigmaparams[iP], sigmaerr[iP]);
 		cout << "Param " << iP << " = " << sigmaparams[iP] << " +/- " << sigmaerr[iP] << endl;
	}
	cout << "Chisquared = " << minsigma.fAmin << " per " << minsigma.GetNumFreePars() << 
	        " parameters " << endl;

	if(verbose){
		// How well does the fit do?
		cout << "Compare sigmas: Fit cf Param " << endl;
		double myE[1], myV[1];
		for(int iC=0; iC<nTot; ++iC){
			myE[0] = Ecount[iC];
			myV[0] = Vcount[iC];
			float temp = calcSigma(myE, myV, sigmaparams);
			cout << "E = " << myE[0] << " V = " << myV[0] << " : " << sigma[iC] << " cf " << temp << endl;
		}
	}
	
	// Now lets do a check of the parameterised gaussians against the data histograms
	float max_chidof = 0;
	for(int i=0; i<nTot; ++i){
		float amp = f1[i]->GetParameter(0);
		double myE[1], myV[1];
		myE[0] = Ecount[i];
		myV[0] = Vcount[i];
		float mean = calcMean(myE, myV, meanparams);
		float sigma = calcMean(myE, myV, sigmaparams);
		int pos = int(Vcount[i]);
		f2[i]->SetLineWidth(1);
		f2[i]->SetParameters(amp,mean,sigma);
		// Now we fix the mean and sigma to the parameterised values, only allow the 
		// amplitude to float
		f2[i]->FixParameter(1,mean);
		f2[i]->FixParameter(2,sigma);
		Ctemp->cd();
		h[i]->Fit(f2[i],"QR");
		float chidof = f2[i]->GetChisquare()/f2[i]->GetNDF();
		if(chidof>max_chidof)max_chidof = chidof;
		if(verbose){
			cout << "E = " << Ecount[i] << ", V = " << Vcount[i] << ", chisq/DoF = " <<
				chidof << endl;
		}
		C3->cd(pos+1);
		h[i]->Draw("histsame");		
		f2[i]->Draw("same");		
	}
	cout << "Maximum chi-squared/DoF = " << max_chidof << endl;
	
	// And output in the format required for RATDB input
	cout << "charge_prob_pmean : [ ";
    for(int iP=0; iP<npar; ++iP){
		cout << meanparams[iP] << "d, "; 
	}
	cout << " ]," << endl;
	cout << "charge_prob_psigma : [ ";
	for(int iP=0; iP<npar; ++iP){
		cout << sigmaparams[iP] << "d, "; 
	}
	cout << " ]," << endl;
	
	delete Ctemp;
}
