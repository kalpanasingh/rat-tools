////////////////////////////////////////////////////////
/// Plots the fit position
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
/// J Amey <jjtamey@googlemail.com>
///
/// 23/07/12 - New File
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
                TH1D** hCountVR,
                TH1D** hCountVX,
                TH1D** hCountVY,
                TH1D** hCountVZ );

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
      c1->Divide( 1, 2 );
    }

  TH1D* hCountVR;
  TH1D* hCountVX;
  TH1D* hCountVY;
  TH1D* hCountVZ;
  // First extract the data
  ExtractPosition( lFile, lFit, &hCountVR, &hCountVX, &hCountVY, &hCountVZ );
  // Don't plot empty fits...
  if( hCountVR->GetEntries() == 0 )
    return c1;

  // Now draw the results
  TVirtualPad* cPad = NULL;
  cPad = c1->cd(1);
  if( firstDraw )
    hCountVR->Draw("S E");
  else
    {
      hCountVR->SetLineColor( fitNum + 1 );
      hCountVR->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVR, fitNum + 1, cPad );

  TVirtualPad* vc1 = c1->cd(2);
  if( firstDraw )
    vc1->Divide( 3, 1 );
  cPad = vc1->cd(1);
  if( firstDraw )
    hCountVX->Draw("E");
  else
    {
      hCountVX->SetLineColor( fitNum + 1 );
      hCountVX->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVX, fitNum + 1, cPad );

  cPad = vc1->cd(2);
  if( firstDraw )
    hCountVY->Draw("S E");
  else
    {
      hCountVY->SetLineColor( fitNum + 1 );
      hCountVY->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVY, fitNum + 1, cPad );

  cPad = vc1->cd(3);
   if( firstDraw )
    hCountVZ->Draw("S E");
  else
    {
      hCountVZ->SetLineColor( fitNum + 1 );
      hCountVZ->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVZ, fitNum + 1, cPad );

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
                TH1D** hCountVR,
                TH1D** hCountVX,
                TH1D** hCountVY,
                TH1D** hCountVZ )
{
  // First new the histograms
  const int kBins = 200;
  const double kStartBin = -9000.0; 
  const double kEndBin = 9000.0;
  stringstream histoBinning;
  histoBinning << "Count per " << ( kEndBin - kStartBin ) / kBins << "mm Bin";

  stringstream histName;
  histName << lFile << "_" << lFit << "_R";
  *hCountVR = new TH1D( histName.str().c_str(), " Reconstructed r ", kBins, 0.0, kEndBin );
  (*hCountVR)->GetXaxis()->SetTitle( " Reconstructed r [mm]" );
  (*hCountVR)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");

  histName << lFile << "_" << lFit << "_X";
  *hCountVX = new TH1D( histName.str().c_str(), " Reconstructed x ", kBins, kStartBin, kEndBin );
  (*hCountVX)->GetXaxis()->SetTitle( " Reconstructed x [mm]" );
  (*hCountVX)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");

  histName << lFile << "_" << lFit << "_Y";
  *hCountVY = new TH1D( histName.str().c_str(), " Reconstructed y ", kBins, kStartBin, kEndBin );
  (*hCountVY)->GetXaxis()->SetTitle( " Reconstructed y [mm]" );
  (*hCountVY)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");

  histName << lFile << "_" << lFit << "_Z";
  *hCountVZ = new TH1D( histName.str().c_str(), " Reconstructed z ", kBins, kStartBin, kEndBin );
  (*hCountVZ)->GetXaxis()->SetTitle( " Reconstructed z [mm]" );
  (*hCountVZ)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
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
          if( gIgnoreRetriggers && iEvent > 0 )
            continue;

          RAT::DS::EV *rEV = rDS->GetEV( iEvent );
          TVector3 fitPos;
          try
            {
              DS::FitVertex fitVertex =rEV->GetFitResult( lFit ).GetVertex(0);
              if( fitVertex.ContainsPosition()&& fitVertex.ValidPosition() )
                fitPos = fitVertex.GetPosition();
              else if( !fitVetex.ContainsPosition() )
                cout <<lFit <<" has not reconstructed position." << endl;
              else if( !fitVertex.ValidPosition() )
                cout <<lFit <<": Invalid position reconstruction." << endl;
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
          
          (*hCountVR)->Fill( fitPos.Mag() );
          (*hCountVX)->Fill( fitPos.x() );
          (*hCountVY)->Fill( fitPos.y() );
          (*hCountVZ)->Fill( fitPos.z() );

        }
    }
}

