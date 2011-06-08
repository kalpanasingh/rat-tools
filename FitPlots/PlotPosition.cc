////////////////////////////////////////////////////////
/// Plots the fit position against the mc position and 
/// expected bias.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 01/06/11 - New File
////////////////////////////////////////////////////////

#include <FitPlotsUtil.hh>
#include <PlotPosition.hh>

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
ExtractPosition(
				string lFile,
				string lFit,
				TH1D** hCountVRes,
				TGraph** gResVR,
				TH1D** hCountVResX,
				TH1D** hCountVResY,
				TH1D** hCountVResZ,
				TGraph** gRadialBiasVR );

TCanvas*
UpdatePosition(
			   string lFile,
			   string lFit, 
			   TCanvas* c1,
			   Int_t fitNum );

////////////////////////////////////////////////////////
/// Call-able functions
////////////////////////////////////////////////////////
TCanvas*
PlotPosition(
			 string lFile )
{
  return PlotPosition( lFile, GetFitNames( lFile ) );
}

TCanvas*
PlotPosition(
			 string lFile,
			 string lFit )
{
  vector<string> fits; fits.push_back( lFit );
  return PlotPosition( lFile, fits );
}

TCanvas*
PlotPosition(
			 string lFile, 
			 string lFit1, 
			 string lFit2 )
{
  vector<string> fits; fits.push_back( lFit1 ); fits.push_back( lFit2 );
  return PlotPosition( lFile, fits );
}

TCanvas*
PlotPosition(
			 string file,
			 vector<string> fits )
{
  TCanvas* c1 = NULL;
  for( unsigned int uFit = 0; uFit < fits.size(); uFit++ )
	{
	  Int_t drawNum = uFit;
	  c1 = UpdatePosition( file, fits[uFit], c1, drawNum );
	  cout << "Plotted " << file << " fit: " << fits[uFit] << endl;
	}
  return c1;
}

////////////////////////////////////////////////////////
/// Adds more plots to the first plot
////////////////////////////////////////////////////////

TCanvas*
UpdatePosition(
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
	  c1->Divide( 2, 2 );
	}

  TH1D* hCountVRes;
  TGraph* gResVR;
  TH1D* hCountVResX;
  TH1D* hCountVResY;
  TH1D* hCountVResZ;
  TGraph* gRadialBiasVR;
  // First extract the data
  ExtractPosition( lFile, lFit, &hCountVRes, &gResVR, &hCountVResX, &hCountVResY, &hCountVResZ, &gRadialBiasVR );

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

  TVirtualPad* vc1 = c1->cd(3);
  if( firstDraw )
	vc1->Divide( 2, 1 );
  vc1->cd(1);
  if( firstDraw )
	hCountVResX->Draw("E");
  else
	{
	  hCountVResX->SetLineColor( fitNum + 1 );
	  hCountVResX->Draw("SAMES E");
	}
  c1->Update();
  ArrangeStatBox( hCountVResX, fitNum + 1, fitNum );

  vc1->cd(2);
  if( firstDraw )
	hCountVResY->Draw("E");
  else
	{
	  hCountVResY->SetLineColor( fitNum + 1 );
	  hCountVResY->Draw("SAMES E");
	}
  c1->Update();
  ArrangeStatBox( hCountVResY, fitNum + 1, fitNum );

  TVirtualPad* vc2 = c1->cd(4);
  if( firstDraw )
	vc2->Divide( 2, 1 );
  vc2->cd(1);
  if( firstDraw )
	hCountVResZ->Draw("E");
  else
	{
	  hCountVResZ->SetLineColor( fitNum + 1 );
	  hCountVResZ->Draw("SAMES E");
	}
  c1->Update();
  ArrangeStatBox( hCountVResZ, fitNum + 1, fitNum );

  vc2->cd(2);
  if( firstDraw )
	gRadialBiasVR->Draw("AP");
  else
	{
	  gRadialBiasVR->SetMarkerColor( fitNum + 1 );
	  gRadialBiasVR->Draw("P");
	}

  c1->cd();
  return c1;  
}

////////////////////////////////////////////////////////
/// Extraction from the ROOT file
////////////////////////////////////////////////////////

void
ExtractPosition(
				string lFile,
				string lFit,
				TH1D** hCountVRes,
				TGraph** gResVR,
				TH1D** hCountVResX,
				TH1D** hCountVResY,
				TH1D** hCountVResZ,
				TGraph** gRadialBiasVR )
{
  // First new the histograms
  const int kBins = 20;
  const double kStartBin = -750.0; 
  const double kEndBin = 750.0;
  stringstream histoBinning;
  histoBinning << "Count per " << ( kEndBin - kStartBin ) / kBins << "mm Bin";

  stringstream histName;
  histName << lFile << "_" << lFit << "_R";
  *hCountVRes = new TH1D( histName.str().c_str(), "#cbar Fit(r) - MC(r) #cbar", kBins, 0.0, 2.0 * kEndBin );
  (*hCountVRes)->GetXaxis()->SetTitle( "#cbar Fit(r) - MC(r) #cbar [mm]" );
  (*hCountVRes)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");

  histName << lFile << "_" << lFit << "_X";
  *hCountVResX = new TH1D( histName.str().c_str(), "Fit(x) - MC(x)", kBins, kStartBin, kEndBin );
  (*hCountVResX)->GetXaxis()->SetTitle( "Fit(x) - MC(x) [mm]" );
  (*hCountVResX)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");

  histName << lFile << "_" << lFit << "_Y";
  *hCountVResY = new TH1D( histName.str().c_str(), "Fit(y) - MC(y)", kBins, kStartBin, kEndBin );
  (*hCountVResY)->GetXaxis()->SetTitle( "Fit(y) - MC(y) [mm]" );
  (*hCountVResY)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");

  histName << lFile << "_" << lFit << "_Z";
  *hCountVResZ = new TH1D( histName.str().c_str(), "Fit(z) - MC(z)", kBins, kStartBin, kEndBin );
  (*hCountVResZ)->GetXaxis()->SetTitle( "Fit(z) - MC(z) [mm]" );
  (*hCountVResZ)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");

  // Now new the graphs
  *gResVR = new TGraph();
  *gRadialBiasVR =  new TGraph();

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
	    
      /*Produce a average position (unweighted ?? )
      for( int iLoop2 = 1; iLoop2 < numMCParticles; iLoop2++ )
		{
		  cout << "Warn, pileup: averaging position" << endl;
		  RAT::DS::MCParticle *rMCParticle =  rMC->GetMCParticle( iLoop2 );
		  mcPos = mcPos + rMCParticle->GetPos();
		}
      mcPos = mcPos * ( 1.0 / numMCParticles );
	  */
      for( int iEvent = 0; iEvent < rDS->GetEVCount(); iEvent++ )
		{
		  RAT::DS::EV *rEV = rDS->GetEV( iEvent );
		  if( rEV->GetFitResult( lFit ).GetValid() == false )
			continue;

		  TVector3 fitPos;
		  try
			{
			  fitPos = rEV->GetFitResult( lFit ).GetVertex(0).GetPosition();
			}
		  catch( RAT::DS::FitVertex::NoValueError& e )
			{
			  cout << "Position has not been fit." << endl;
			  return;
			}
		  TVector3 deltaR = fitPos - mcPos;

		  (*hCountVRes)->Fill( deltaR.Mag() );
		  (*gResVR)->SetPoint( graphPoint, mcPos.Mag(), deltaR.Mag() );
		  (*hCountVResX)->Fill( fitPos.x() - mcPos.x() );
		  (*hCountVResY)->Fill( fitPos.y() - mcPos.y() );
		  (*hCountVResZ)->Fill( fitPos.z() - mcPos.z() );
		  (*gRadialBiasVR)->SetPoint( graphPoint, mcPos.Mag(), deltaR.Dot( mcPos.Unit() ) );

		  graphPoint++;
		}
	}
  (*gResVR)->GetXaxis()->SetTitle( "#cbar MC(r) #cbar [mm]" );
  (*gResVR)->GetYaxis()->SetTitle( "#cbar Fit(r) - MC(r) #cbar [mm]" );
  (*gResVR)->SetMarkerStyle( 2 );
  (*gRadialBiasVR)->GetXaxis()->SetTitle( "#cbar MC(r) #cbar [mm]" );
  (*gRadialBiasVR)->GetYaxis()->SetTitle( "Radial Bias (fit - mc) [mm]" );// (Fit(r) - MC(r)) #cdot ( MC(r) )/(#cbar MC(r)#cbar) [mm]" );
  (*gRadialBiasVR)->SetMarkerStyle( 2 );
}

