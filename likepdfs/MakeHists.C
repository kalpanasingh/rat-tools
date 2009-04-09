/*-----------------------------------------------------------------------
/// This program allows the user to create and view the PDFs that would be generated 
/// and used in the RAT FitLikePos processor. The number of bins and binning are specified
/// via the FIT_LIKE.ratdb file in rat.

/// To run
/// To run, open root, and type:
/// > .L MakeHists.C
/// > MakeHists()
-----------------------------------------------------------------------*/

// Root includes
#include "TROOT.h"
#include "TFile.h"
#include "TNtuple.h"
#include "TH1D.h"
#include "TCanvas.h"

// C++ includes
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
using std::cout;
using std::endl;

void MakeHists(char* fileName = "FitLikePDFNtuple.root")
{
	// open input file and get the ntuple
	TFile fileIn(fileName);							  
	TNtuple *flntp = (TNtuple*)fileIn.Get("PDFntuple");
	
	const int nQBins = 6;
	const int nVertexBins = 6;
	const int nAngleBins = 10;
	
	// create the histograms
	TH1D *hists[nQBins][nVertexBins][nAngleBins];
	const int nbins = 73;
	double fbins[74] = {-20.,-4,-3,-2,-1.,0.,
					 	1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.,12.,13.,14.,15.,16.,17.,18.,19.,20.,
						25.,30.,35.,40.,45.,50.,
						55.,60.,65.,70.,75.,80.,85.,90.,95.,100.,
						105.,110.,115.,120.,125.,130.,135.,140.,145.,150.,
						155.,160.,165.,170.,175.,180.,185.,190.,195.,200.,
						205.,210.,215.,220.,225.,230.,235.,240.,245.,250.,
						300.,350.};
	
	for(int iQ=0; iQ<nQBins; ++iQ){
		for(int iV=0; iV<nVertexBins; ++iV){
			for(int iS=0; iS<nAngleBins; ++iS){
				hists[iQ][iV][iS] = new TH1D(Form("T_Q%d_V%d_S%d",iQ,iV,iS),"",nbins,fbins);				
				hists[iQ][iV][iS]->SetDirectory(0);
			}//iS loop
		}//iV loop
	}//iQ loop	

	// now fill them
	int nen = flntp->GetEntries();
	cout << "There are " << nen << " entries " << endl;
	int step = nen/10;	
	for(int in=0; in<nen; ++in){
		if((in%step)==0)cout << "processed " << in << endl;
		flntp->GetEntry(in);
		float *vals = flntp->GetArgs();
		int nQ = int(vals[0]);
		int nV = int(vals[1]);
		int nS = int(vals[2]);
		double tres = double(vals[3]);
		hists[nQ][nV][nS]->Fill(tres);
	}
	
	// now normalise them
	for(int iQ=0; iQ<nQBins; ++iQ){
		for(int iV=0; iV<nVertexBins; ++iV){
			for(int iS=0; iS<nAngleBins; ++iS){
				double nEn = double(hists[iQ][iV][iS]->GetEntries());
				if(nEn>0){
					for(int iB=0; iB < nbins; ++iB){
						double wid = hists[iQ][iV][iS]->GetBinWidth(iB);
						double newval =hists[iQ][iV][iS]->GetBinContent(iB)/(wid*nEn);
						hists[iQ][iV][iS]->SetBinContent(iB,newval);
					}
				}else{
					cout << "Histogram " << hists[iQ][iV][iS]->GetName() << " has 0 entries " << endl;
				}
			}
		}	
	}//iX	
	
	// Now draw them
	TCanvas *Can[6];
	for(int iQ=0; iQ<nQBins; ++iQ){
		Can[iQ] = new TCanvas(Form("Can%d",iQ));
		Can[iQ]->Divide(3,2);
		for(int iV=0; iV<nVertexBins; ++iV){
			Can[iQ]->cd(iV+1);
			hists[iQ][iV][0]->SetLineColor(kOrange);
			hists[iQ][iV][0]->Draw();
			if(iV>0){
				for(int iS=1; iS<nAngleBins; ++iS){			
					cout << iQ << " " << iV << " " << iS << endl;	
					hists[iQ][iV][iS]->SetLineColor(kOrange+iS);
					hists[iQ][iV][iS]->Draw("same");
				}
			}
		}		
	}	
				  
}
