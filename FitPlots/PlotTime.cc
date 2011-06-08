////////////////////////////////////////////////////////
/// Plots the fit time against the mc time and 
/// expected position bias.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 01/06/11 - New File
////////////////////////////////////////////////////////

#include <FitPlotsUtil.hh>

#include <RAT/DS/Root.hh>
#include <RAT/DS/PMTProperties.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/FitResult.hh>
#include <RAT/DS/FitVertex.hh>

#include <TH1D.h>
#include <TGraph.h>
#include <TCanvas.h>
#include <TChain.h>
#include <TFile.h>
#include <TPaveStats.h>
using namespace ROOT;

#include <string>
#include <sstream>
#include <iostream>
using namespace std;

void
ExtractTime(
			string lFile,
			string lFit,
			TH1D** hCountVRes,
			TGraph** gResVR );

TCanvas*
PlotTime(
		 string file,
		 vector<string> fits );

TCanvas*
UpdateTime(
		   string lFile,
		   string lFit, 
		   TCanvas* c1,
		   Int_t fitNum );

////////////////////////////////////////////////////////
/// Call-able functions
////////////////////////////////////////////////////////
TCanvas*
PlotTime(
		 string lFile )
{
  return PlotTime( lFile, GetFitNames( lFile ) );
}

TCanvas*
PlotTime(
		 string lFile,
		 string lFit )
{
  vector<string> fits; fits.push_back( lFit );
  return PlotTime( lFile, fits );
}

TCanvas*
PlotTime(
		 string lFile, 
		 string lFit1, 
		 string lFit2 )
{
  vector<string> fits; fits.push_back( lFit1 ); fits.push_back( lFit2 );
  return PlotTime( lFile, fits );
}

TCanvas*
PlotTime(
		 string file,
		 vector<string> fits )
{
  TCanvas* c1 = NULL;
  for( unsigned int uFit = 0; uFit < fits.size(); uFit++ )
	{
	  Int_t drawNum = uFit;
	  c1 = UpdateTime( file, fits[uFit], c1, drawNum );
	  cout << "Plotted " << file << " fit: " << fits[uFit] << endl;
	}
  return c1;
}

////////////////////////////////////////////////////////
/// Adds more plots to the first plot
////////////////////////////////////////////////////////

TCanvas*
UpdateTime(
		   string lFile,
		   string lFit, 
		   TCanvas* c1,
		   Int_t fitNum )
{
  bool firstDraw = false;
  if( c1 == NULL )
	{
	  firstDraw = true;
	  c1 = new TCanvas();
	  c1->Divide( 2, 1 );
	}

  TH1D* hCountVRes;
  TGraph* gResVR;

  // First extract the data
  ExtractTime( lFile, lFit, &hCountVRes, &gResVR );

  // Now draw the results
  c1->cd(1);
  if( firstDraw )
	hCountVRes->Draw("E");
  else
	{
	  hCountVRes->SetLineColor( fitNum + 1);
	  hCountVRes->Draw("SAMES E");
	}
  c1->Update();
  ArrangeStatBox( hCountVRes, fitNum + 1, fitNum );

  c1->cd(2);
  if( firstDraw )
	gResVR->Draw("AP");
  else
	{
	  gResVR->SetMarkerColor( fitNum + 1 );
	  gResVR->Draw("P");
	}

  c1->cd();
  return c1;  
}

////////////////////////////////////////////////////////
/// Extraction from the ROOT file
////////////////////////////////////////////////////////

void
ExtractTime(
			string lFile,
			string lFit,
			TH1D** hCountVRes,
			TGraph** gResVR )
{
  // First new the histograms
  const int kBins = 100;
  const double kStartBin = -50.0; 
  const double kEndBin = 50.0;
  stringstream histoBinning;
  histoBinning << "Count per " << ( kEndBin - kStartBin ) / kBins << "ns Bin";

  stringstream histName;
  histName << lFile << "_" << lFit << "_T";
  *hCountVRes = new TH1D( histName.str().c_str(), "#cbar Fit(T) - MC(T) #cbar", kBins, kStartBin, kEndBin );
  (*hCountVRes)->GetXaxis()->SetTitle( "#cbar Fit(T) - MC(T) #cbar [ns]" );
  (*hCountVRes)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");

  // Now new the graphs
  *gResVR = new TGraph();
  
  // Now extract the data
  // Load the first file
  RAT::DS::Root* rDS;
  RAT::DS::PMTProperties* rPMTList;
  TChain* tree;

  LoadRootFile( lFile, &tree, &rDS, &rPMTList );

  int graphPoint = 0;
  for( int iLoop = 0; iLoop < tree->GetEntries(); iLoop++ )
    {
      tree->GetEntry( iLoop );
	  RAT::DS::MC *rMC = rDS->GetMC();

      TVector3 mcPos = rMC->GetMCParticle(0)->GetPos();
	  double mcTime = rMC->GetMCParticle(0)->GetTime();	  

      for( int iEvent = 0; iEvent < rDS->GetEVCount(); iEvent++ )
		{
		  RAT::DS::EV *rEV = rDS->GetEV( iEvent );
		  if( rEV->GetFitResult( lFit ).GetValid() == false )
			continue;

		  double fitTime;
		  try
			{
			  fitTime = rEV->GetFitResult( lFit ).GetVertex(0).GetTime();
			}
		  catch( RAT::DS::FitVertex::NoValueError& e )
			{
			  cout << "Time has not been fit." << endl;
			  return;
			}
		  double deltaT = fitTime - mcTime;

		  (*hCountVRes)->Fill( deltaT );
		  (*gResVR)->SetPoint( graphPoint, mcPos.Mag(), deltaT );

		  graphPoint++;
		}
	}
  (*gResVR)->GetXaxis()->SetTitle( "#cbar MC(r) #cbar [mm]" );
  (*gResVR)->GetYaxis()->SetTitle( "#cbar Fit(T) - MC(T) #cbar [ns]" );
  (*gResVR)->SetMarkerStyle( 2 );
}

