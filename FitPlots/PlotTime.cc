////////////////////////////////////////////////////////
/// Plots the fit time
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
/// J Amey <jjtamey@googlemail.com>
///
/// 23/07/12 - New File
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
            TH1D** hCountVTime );

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
    }

  TH1D* hCountVTime;

  // First extract the data
  ExtractTime( lFile, lFit, &hCountVTime );
  // Don't plot empty fits...
  if( hCountVTime->GetEntries() == 0 )
    return c1;

  // Now draw the results
  if( firstDraw )
    hCountVTime->Draw("S E");
  else
    {
      hCountVTime->SetLineColor( fitNum + 1 );
      hCountVTime->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVTime, fitNum + 1, c1 );

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
            TH1D** hCountVTime )
{
  // First new the histograms
  const int kBins = 100;
  const double kStartBin = 0.0; 
  const double kEndBin = 500.0;
  stringstream histoBinning;
  histoBinning << "Count per " << ( kEndBin - kStartBin ) / kBins << "ns Bin";

  stringstream histName;
  histName << lFile << "_" << lFit << "_T";
  *hCountVTime = new TH1D( histName.str().c_str(), " Reconstructed T ", kBins, kStartBin, kEndBin );
  (*hCountVTime)->GetXaxis()->SetTitle( " Reconstructed T [ns]" );
  (*hCountVTime)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");
  
  // Now extract the data
  // Load the first file
  RAT::DS::Root* rDS;
  RAT::DS::PMTProperties* rPMTList;
  TChain* tree;

  LoadRootFile( lFile, &tree, &rDS, &rPMTList );

  for( int iLoop = 0; iLoop < tree->GetEntries(); iLoop++ )
    {
      tree->GetEntry( iLoop );
      RAT::DS::MC *rMC = rDS->GetMC();

      TVector3 mcPos = rMC->GetMCParticle(0)->GetPos();    

      for( int iEvent = 0; iEvent < rDS->GetEVCount(); iEvent++ )
        {
          if( gIgnoreRetriggers && iEvent > 0 )
            continue;

          RAT::DS::EV *rEV = rDS->GetEV( iEvent );
          double fitTime;
          try
            {
              DS::FitVertex fitVertex =rEV->GetFitResult( lFit ).GetVertex(0);
              if( fitVertex.ContainsTime()&& fitVertex.ValidTime() )
                fitTime = fitVertex.GetTime();
              else if( !fitVetex.ContainsTime() )
                cout <<lFit <<" has not reconstructed time." << endl;
              else if( !fitVertex.ValidTime() )
                cout <<lFit <<": Invalid time reconstruction." << endl;
            }
          catch( RAT::DS::FitResult::NoVertexError& e )
            {
              cout << lFit << " has not reconstructed a vertex." << endl;
              return;
            }
          catch( std::runtime_error& e )
            {
              cout << lFit << " failed for event " << iEvent << ". Continuing..." << endl;
              continue;
            }
          
          (*hCountVTime)->Fill( fitTime );
          
        }
    }
}

