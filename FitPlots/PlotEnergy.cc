////////////////////////////////////////////////////////
/// Plots the fit energy against the mc energy and 
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
ExtractEnergy(
              string lFile,
              string lFit,
              TH1D** hCountVRes,
              TGraph** gResVR,
              TGraph** gResVE );

TCanvas*
PlotEnergy(
           string file,
           vector<string> fits );

TCanvas*
UpdateEnergy(
             string lFile,
             string lFit, 
             TCanvas* c1,
             Int_t fitNum );

////////////////////////////////////////////////////////
/// Call-able functions
////////////////////////////////////////////////////////
TCanvas*
PlotEnergy(
           string lFile )
{
  return PlotEnergy( lFile, GetFitNames( lFile ) );
}

TCanvas*
PlotEnergy(
           string lFile,
           string lFit )
{
  vector<string> fits; fits.push_back( lFit );
  return PlotEnergy( lFile, fits );
}

TCanvas*
PlotEnergy(
           string lFile, 
           string lFit1, 
           string lFit2 )
{
  vector<string> fits; fits.push_back( lFit1 ); fits.push_back( lFit2 );
  return PlotEnergy( lFile, fits );
}

TCanvas*
PlotEnergy(
           string file,
           vector<string> fits )
{
  TCanvas* c1 = NULL;
  for( unsigned int uFit = 0; uFit < fits.size(); uFit++ )
    {
      Int_t drawNum = uFit;
      c1 = UpdateEnergy( file, fits[uFit], c1, drawNum );
      cout << "Plotted " << file << " fit: " << fits[uFit] << endl;
    }
  return c1;
}

////////////////////////////////////////////////////////
/// Adds more plots to the first plot
////////////////////////////////////////////////////////

TCanvas*
UpdateEnergy(
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
      c1->Divide( 1, 2 );
    }

  TH1D* hCountVRes;
  TGraph* gResVR;
  TGraph* gResVE;

  // First extract the data
  ExtractEnergy( lFile, lFit, &hCountVRes, &gResVR, &gResVE );
  // Don't plot empty fits...
  if( hCountVRes->GetEntries() == 0 )
    return c1;

  // Now draw the results
  TVirtualPad* cPad = NULL;
  TVirtualPad* vc1 = c1->cd(1);
  if( firstDraw )
    vc1->Divide( 2, 1 );
  cPad = vc1->cd(1);
  if( firstDraw )
    hCountVRes->Draw("E");
  else
    {
      hCountVRes->SetLineColor( fitNum + 1);
      hCountVRes->Draw("SAMES E");
    }
  vc1->Update();
  ArrangeStatBox( hCountVRes, fitNum + 1, cPad );

  vc1->cd(2);
  if( firstDraw )
    gResVE->Draw("AP");
  else
    {
      gResVE->SetMarkerColor( fitNum + 1 );
      gResVE->Draw("P");
    }

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
ExtractEnergy(
              string lFile,
              string lFit,
              TH1D** hCountVRes,
              TGraph** gResVR,
              TGraph** gResVE )
{
  // First new the histograms
  const int kBins = 200;
  const double kStartBin = -2.0; 
  const double kEndBin = 2.0;
  stringstream histoBinning;
  histoBinning << "Count per " << ( kEndBin - kStartBin ) / kBins << "MeV Bin";

  stringstream histName;
  histName << lFile << "_" << lFit << "_E";
  *hCountVRes = new TH1D( histName.str().c_str(), "#cbar Fit(E) - MC(E) #cbar", kBins, kStartBin, kEndBin );
  (*hCountVRes)->GetXaxis()->SetTitle( "#cbar Fit(E) - MC(E) #cbar [MeV]" );
  (*hCountVRes)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");

  // Now new the graphs
  *gResVR = new TGraph();
  *gResVE =  new TGraph();

  // Now extract the data
  // Load the first file
  RAT::DS::Root* rDS;
  RAT::DS::PMTProperties* rPMTList;
  TChain* tree;

  LoadRootFile( lFile, &tree, &rDS, &rPMTList );

  int graphPoint = 0;
  (*gResVE)->SetPoint( graphPoint, 0.0, 0.0 );
  graphPoint++;
  for( int iLoop = 0; iLoop < tree->GetEntries(); iLoop++ )
    {
      tree->GetEntry( iLoop );
      RAT::DS::MC *rMC = rDS->GetMC();

      TVector3 mcPos = rMC->GetMCParticle(0)->GetPos();
      double mcEnergy = rMC->GetMCParticle(0)->GetKE();
      

      for( int iEvent = 0; iEvent < rDS->GetEVCount(); iEvent++ )
        {
          if( gIgnoreRetriggers && iEvent > 0 )
            continue;

          RAT::DS::EV *rEV = rDS->GetEV( iEvent );
          if( rEV->GetFitResult( lFit ).GetValid() == false )
            continue;

          double fitEnergy;
          try
            {
              fitEnergy = rEV->GetFitResult( lFit ).GetVertex(0).GetEnergy();
            }
          catch( RAT::DS::FitVertex::NoValueError& e )
            {
              cout << lFit << " fitter has not reconstructed an energy." << endl;
              return;
            }
          catch( RAT::DS::FitResult::NoVertexError& e )
            {
              cout << lFit << " has not reconstructed a vertex." << endl;
              return;
            }
          double deltaE = fitEnergy - mcEnergy;

          (*hCountVRes)->Fill( deltaE );
          (*gResVR)->SetPoint( graphPoint, mcPos.Mag(), deltaE );
          (*gResVE)->SetPoint( graphPoint, mcEnergy, deltaE );

          graphPoint++;
        }
    }
  (*gResVR)->GetXaxis()->SetTitle( "#cbar MC(r) #cbar [mm]" );
  (*gResVR)->GetYaxis()->SetTitle( "#cbar Fit(E) - MC(E) #cbar [MeV]" );
  (*gResVR)->SetMarkerStyle( 2 );
  (*gResVE)->GetXaxis()->SetTitle( "#cbar MC(E) #cbar [MeV]" );
  (*gResVE)->GetYaxis()->SetTitle( "#cbar Fit(E) - MC(E) #cbar [MeV]" );
  (*gResVE)->SetMarkerStyle( 2 );
}

