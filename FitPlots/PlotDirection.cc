////////////////////////////////////////////////////////
/// Plots the fit direction against the x,y and z axes
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
ExtractDirection(
                 string lFile,
                 string lFit,
                 TH1D** hCountVDirX,
                 TH1D** hCountVDirY,
                 TH1D** hCountVDirZ );

TCanvas*
PlotDirection(
              string file,
              vector<string> fits );

TCanvas*
UpdateDirection(
                string lFile,
                string lFit, 
                TCanvas* c1,
                Int_t fitNum );

////////////////////////////////////////////////////////
/// Call-able functions
////////////////////////////////////////////////////////
TCanvas*
PlotDirection(
              string lFile )
{
  return PlotDirection( lFile, GetFitNames( lFile ) );
}

TCanvas*
PlotDirection(
              string lFile,
              string lFit )
{
  vector<string> fits; fits.push_back( lFit );
  return PlotDirection( lFile, fits );
}

TCanvas*
PlotDirection(
              string lFile, 
              string lFit1, 
              string lFit2 )
{
  vector<string> fits; fits.push_back( lFit1 ); fits.push_back( lFit2 );
  return PlotDirection( lFile, fits );
}

TCanvas*
PlotDirection(
              string file,
              vector<string> fits )
{
  TCanvas* c1 = NULL;
  for( unsigned int uFit = 0; uFit < fits.size(); uFit++ )
    {
      Int_t drawNum = uFit;
      c1 = UpdateDirection( file, fits[uFit], c1, drawNum );
      cout << "Plotted " << file << " fit: " << fits[uFit] << endl;
    }
  return c1;
}

////////////////////////////////////////////////////////
/// Adds more plots to the first plot
////////////////////////////////////////////////////////

TCanvas*
UpdateDirection(
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
      c1->Divide( 3, 1 );
    }

  TH1D* hCountVDirX;
  TH1D* hCountVDirY;
  TH1D* hCountVDirZ;

  // First extract the data
  ExtractDirection( lFile, lFit, &hCountVDirX, &hCountVDirY, &hCountVDirZ  );
  // Don't plot empty fits...
  if( hCountVDirX->GetEntries() == 0 )
    return c1;

  // Now draw the results
  c1->cd(1);
  if( firstDraw )
    hCountVDirX->Draw("S E");
  else
    {
      hCountVDirX->SetLineColor( fitNum + 1 );
      hCountVDirX->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVDirX, fitNum + 1, c1->cd(1) );

  c1->cd(2);
  if( firstDraw )
    hCountVDirY->Draw("S E");
  else
    {
       hCountVDirY->SetLineColor( fitNum + 1 );
       hCountVDirY->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVDirY, fitNum + 1, c1->cd(2) );

  c1->cd(3);
  if( firstDraw )
    hCountVDirZ->Draw("S E");
  else
    {
      hCountVDirZ->SetLineColor( fitNum + 1 );
      hCountVDirZ->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVDirZ, fitNum + 1, c1->cd(3) );

  c1->cd();
  return c1;  
}

////////////////////////////////////////////////////////
/// Extraction from the ROOT file
////////////////////////////////////////////////////////

void
ExtractDirection(
                 string lFile,
                 string lFit,
                 TH1D** hCountVDirX,
                 TH1D** hCountVDirY,
                 TH1D** hCountVDirZ )
{
  // First new the histograms
  const int kBins = 180;
  const double kStartBin = 0.0; 
  const double kEndBin = 180.0;
  stringstream histoBinning;
  histoBinning << "Count per " << ( kEndBin - kStartBin ) / kBins << "degree Bin";

  stringstream histName;
  histName << lFile << "_" << lFit << "_D";
  *hCountVDirX = new TH1D( histName.str().c_str(), "acos #cbar Fitted Direction #cdot x #cbar", kBins, kStartBin, kEndBin );
  (*hCountVDirX)->GetXaxis()->SetTitle( "acos #cbar Fitted Direction #cdot x #cbar [deg]" );
  (*hCountVDirX)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");

  histName << lFile << "_" << lFit << "_D";
  *hCountVDirY = new TH1D( histName.str().c_str(), "acos #cbar Fitted Direction #cdot y #cbar", kBins, kStartBin, kEndBin );
  (*hCountVDirY)->GetXaxis()->SetTitle( "acos #cbar Fitted Direction #cdot y #cbar [deg]" );
  (*hCountVDirY)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
  histName.str("");

  histName << lFile << "_" << lFit << "_D";
  *hCountVDirZ = new TH1D( histName.str().c_str(), "acos #cbar Fitted Direction #cdot z #cbar", kBins, kStartBin, kEndBin );
  (*hCountVDirZ)->GetXaxis()->SetTitle( "acos #cbar Fitted Direction #cdot z #cbar [deg]" );
  (*hCountVDirZ)->GetYaxis()->SetTitle( histoBinning.str().c_str() );
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
      TVector3 mcDirection = rMC->GetMCParticle(0)->GetMom();

      for( int iEvent = 0; iEvent < rDS->GetEVCount(); iEvent++ )
        {
          if( gIgnoreRetriggers && iEvent > 0 )
            continue;

          RAT::DS::EV *rEV = rDS->GetEV( iEvent );
          TVector3 fitDirection;
          TVector3 xAxis(1,0,0);
          TVector3 yAxis(0,1,0);
          TVector3 zAxis(0,0,1);
          try
            {
              RAT::DS::FitVertex fitVertex =rEV->GetFitResult( lFit ).GetVertex(0);
              if( fitVertex.ContainsDirection()&& fitVertex.ValidDirection() )
                fitDirection = fitVertex.GetDirection();
              else if( !fitVertex.ContainsDirection() )
                cout <<lFit <<" has not reconstructed direction." << endl;
              else if( !fitVertex.ValidDirection() )
                cout <<lFit <<": Invalid direction reconstruction." << endl;
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
         
          double deltaDX = acos( fitDirection.Dot( xAxis ) ) * 180.0 / 3.14;
          double deltaDY = acos( fitDirection.Dot( yAxis ) ) * 180.0 / 3.14;
          double deltaDZ = acos( fitDirection.Dot( zAxis ) ) * 180.0 / 3.14;

         (*hCountVDirX)->Fill( deltaDX );
         (*hCountVDirY)->Fill( deltaDY );
         (*hCountVDirZ)->Fill( deltaDZ );
        
        }
    }
 }

