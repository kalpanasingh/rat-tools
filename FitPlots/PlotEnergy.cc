////////////////////////////////////////////////////////
/// Plots the fitted energy
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

ExtractEnergy(
              string lFile,
              string lFit,
              TH1D** hCountVEnergy,
              TGraph** gEnergyVR );

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
      c1->Divide( 2, 1 );
    }

  TH1D* hCountVEnergy;
  TGraph* gEnergyVR;

  // First extract the data
  ExtractEnergy( lFile, lFit, &hCountVEnergy, &gEnergyVR );
  // Don't plot empty fits...
  if( hCountVEnergy->GetEntries() == 0 )
    return c1;

  // Now draw the results
  c1->cd(1);
  if( firstDraw )
    hCountVEnergy->Draw("S E");
  else
    {
      hCountVEnergy->SetLineColor( fitNum + 1);
      hCountVEnergy->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVEnergy, fitNum + 1, c1->cd(1) );

  c1->cd(2);
  if( firstDraw )
    gEnergyVR->Draw("AP");
  else
    {
      gEnergyVR->SetMarkerColor( fitNum + 1 );
      gEnergyVR->Draw("P");
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
              TH1D** hCountVEnergy,
              TGraph** gEnergyVR )
{
  // First new the histograms
  const int kBins = 200;
  const double kStartBin = 0.0; 
  const double kEndBin = 20.0;
  stringstream histoBinning;
  histoBinning << "Count per " << ( kEndBin - kStartBin ) / kBins << "MeV Bin";

  stringstream histName;
  histName << lFile << "_" << lFit << "_E";
  *hCountVEnergy = new TH1D( histName.str().c_str(), " Reconstructed E ", kBins, kStartBin, kEndBin );
  (*hCountVEnergy)->GetXaxis()->SetTitle( " Reconstructed E [MeV]" );
  (*hCountVEnergy)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");

  // Now new the graphs
  *gEnergyVR = new TGraph();
  
  // Now extract the data
  // Load the first file
  RAT::DS::Root* rDS;
  RAT::DS::PMTProperties* rPMTList;
  TChain* tree;

  LoadRootFile( lFile, &tree, &rDS, &rPMTList );

  int graphPoint = 1;
  
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
          double fitEnergy;
          try
            {
              RAT::DS::FitVertex fitVertex =rEV->GetFitResult( lFit ).GetVertex(0);
              if( fitVertex.ContainsEnergy()&& fitVertex.ValidEnergy() )
                fitEnergy = fitVertex.GetEnergy();
              else if( !fitVertex.ContainsEnergy() )
                cout <<lFit <<" has not reconstructed energy." << endl;
              else if( !fitVertex.ValidEnergy() )
                cout <<lFit <<": Invalid energy reconstruction." << endl;
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
         
          (*hCountVEnergy)->Fill( fitEnergy );
          (*gEnergyVR)->SetPoint( graphPoint, mcPos.Mag(), fitEnergy );
         
          graphPoint++;
        }
    }
  (*gEnergyVR)->GetXaxis()->SetTitle( "MC r [mm]" );
  (*gEnergyVR)->GetYaxis()->SetTitle( "Reconstructed E [MeV]" );
  (*gEnergyVR)->SetMarkerStyle( 2 ); 
}

