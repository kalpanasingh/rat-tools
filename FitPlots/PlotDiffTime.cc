////////////////////////////////////////////////////////
/// Plots the fit time against the mc time and 
/// expected position bias.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 01/06/11 - New File
/// 23/07/12 - Updated file and function names with "Diff"
////////////////////////////////////////////////////////

#include <FitPlotsUtil.hh>

#include <RAT/DSReader.hh>

#include <RAT/DU/PMTInfo.hh>

#include <RAT/DS/Root.hh>
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
ExtractDiffTime(
            string lFile,
            string lFit,
            TH1D** hCountVRes,
            TGraph** gResVR );

TCanvas*
PlotDiffTime(
         string file,
         vector<string> fits );

TCanvas*
UpdateDiffTime(
           string lFile,
           string lFit, 
           TCanvas* c1,
           Int_t fitNum );

////////////////////////////////////////////////////////
/// Call-able functions
////////////////////////////////////////////////////////
TCanvas*
PlotDiffTime(
         string lFile )
{
  return PlotDiffTime( lFile, GetFitNames( lFile ) );
}

TCanvas*
PlotDiffTime(
         string lFile,
         string lFit )
{
  vector<string> fits; fits.push_back( lFit );
  return PlotDiffTime( lFile, fits );
}

TCanvas*
PlotDiffTime(
         string lFile, 
         string lFit1, 
         string lFit2 )
{
  vector<string> fits; fits.push_back( lFit1 ); fits.push_back( lFit2 );
  return PlotDiffTime( lFile, fits );
}

TCanvas*
PlotDiffTime(
         string file,
         vector<string> fits )
{
  TCanvas* c1 = NULL;
  for( unsigned int uFit = 0; uFit < fits.size(); uFit++ )
    {
      Int_t drawNum = uFit;
      c1 = UpdateDiffTime( file, fits[uFit], c1, drawNum );
      cout << "Plotted " << file << " fit: " << fits[uFit] << endl;
    }
  return c1;
}

////////////////////////////////////////////////////////
/// Adds more plots to the first plot
////////////////////////////////////////////////////////

TCanvas*
UpdateDiffTime(
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
  ExtractDiffTime( lFile, lFit, &hCountVRes, &gResVR );
  // Don't plot empty fits...
  if( hCountVRes->GetEntries() == 0 )
    return c1;

  // Now draw the results
  TVirtualPad* cPad = NULL;
  cPad = c1->cd(1);
  if( firstDraw )
    hCountVRes->Draw("S E");
  else
    {
      hCountVRes->SetLineColor( fitNum + 1 );
      hCountVRes->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVRes, fitNum + 1, cPad );

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
ExtractDiffTime(
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

  RAT::DSReader dsReader(lFile.c_str());
  RAT::DU::PMTInfo rPMTList = DS::DU::Utility::Get()->GetPMTInfo();

  int graphPoint = 0;

  for( size_t iEvent = 0; iEvent < dsReader.GetEventCount(); iEvent++ )
    {

      tree->GetEntry( iEvent );
      const RAT::DS::MC& rMC = rDS.GetMC();

      TVector3 mcPos = rMC.GetMCParticle(0)->GetPosition();
      double mcTime = rMC.GetMCParticle(0)->GetTime();      

      for( size_t iEV = 0; iEV < rDS->GetEVCount(); iEV++ )
        {
          if( gIgnoreRetriggers && iEV > 0 )
            continue;

          const RAT::DS::EV& rEV = rDS.GetEV( iEV );
          double fitTime;
          try
            {
              RAT::DS::FitVertex fitVertex =rEV->GetFitResult( lFit ).GetVertex(0);
              if( fitVertex.ContainsTime()&& fitVertex.ValidTime() )
                fitTime = fitVertex.GetTime();
              else if( !fitVertex.ContainsTime() )
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
              cout << lFit << " failed for event " << iEV << ". Continuing..." << endl;
              continue;
            }
          double deltaT = fitTime - ( mcTime + 390.0 - rEV->GetGTrigTime() );

          (*hCountVRes)->Fill( deltaT );
          (*gResVR)->SetPoint( graphPoint, mcPos.Mag(), deltaT );

          graphPoint++;
        }
    }
  (*gResVR)->GetXaxis()->SetTitle( "#cbar MC(r) #cbar [mm]" );
  (*gResVR)->GetYaxis()->SetTitle( "#cbar Fit(T) - MC(T) #cbar [ns]" );
  (*gResVR)->SetMarkerStyle( 2 );
}

