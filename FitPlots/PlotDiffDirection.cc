////////////////////////////////////////////////////////
/// Plots the fit direction against the mc direction and 
/// expected position bias.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
/// J Amey <jjtamey@googlemail.com>
///
/// 01/06/11 - New File
/// 23/07/12 - Updated file and function names with "Diff"
///          - fixed bug:  mcDirection must be made a unit vector 
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
ExtractDiffDirection(
                 string lFile,
                 string lFit,
                 TH1D** hCountVRes,
                 TGraph** gResVR );

TCanvas*
PlotDiffDirection(
              string file,
              vector<string> fits );

TCanvas*
UpdateDiffDirection(
                string lFile,
                string lFit, 
                TCanvas* c1,
                Int_t fitNum );

////////////////////////////////////////////////////////
/// Call-able functions
////////////////////////////////////////////////////////
TCanvas*
PlotDiffDirection(
              string lFile )
{
  return PlotDiffDirection( lFile, GetFitNames( lFile ) );
}

TCanvas*
PlotDiffDirection(
              string lFile,
              string lFit )
{
  vector<string> fits; fits.push_back( lFit );
  return PlotDiffDirection( lFile, fits );
}

TCanvas*
PlotDiffDirection(
              string lFile, 
              string lFit1, 
              string lFit2 )
{
  vector<string> fits; fits.push_back( lFit1 ); fits.push_back( lFit2 );
  return PlotDiffDirection( lFile, fits );
}

TCanvas*
PlotDiffDirection(
              string file,
              vector<string> fits )
{
  TCanvas* c1 = NULL;
  for( unsigned int uFit = 0; uFit < fits.size(); uFit++ )
    {
      Int_t drawNum = uFit;
      c1 = UpdateDiffDirection( file, fits[uFit], c1, drawNum );
      cout << "Plotted " << file << " fit: " << fits[uFit] << endl;
    }
  return c1;
}

////////////////////////////////////////////////////////
/// Adds more plots to the first plot
////////////////////////////////////////////////////////

TCanvas*
UpdateDiffDirection(
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
  ExtractDiffDirection( lFile, lFit, &hCountVRes, &gResVR );
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
  c1->Update();

  c1->cd();
  return c1;  
}

////////////////////////////////////////////////////////
/// Extraction from the ROOT file
////////////////////////////////////////////////////////

void
ExtractDiffDirection(
                 string lFile,
                 string lFit,
                 TH1D** hCountVRes,
                 TGraph** gResVR )
{
  // First new the histograms
  const int kBins = 180;
  const double kStartBin = 0.0; 
  const double kEndBin = 180.0;
  stringstream histoBinning;
  histoBinning << "Count per " << ( kEndBin - kStartBin ) / kBins << "degree Bin";

  stringstream histName;
  histName << lFile << "_" << lFit << "_D";
  *hCountVRes = new TH1D( histName.str().c_str(), "acos #cbar Fit(T) #cdot MC(T) #cbar", kBins, kStartBin, kEndBin );
  (*hCountVRes)->GetXaxis()->SetTitle( "acos #cbar Fit(T) #cdot  MC(T) #cbar [deg]" );
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
  graphPoint++;
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
          try
            {
              DS::FitVertex fitVertex = rEV->GetFitResult( lFit ).GetVertex(0);
              if( fitVertex.ContainsDirection() && fitVertex.ValidDirection() )
                fitDirection = fitVertex.GetDirection();
              else if( !fitVetex.ContainsDirection() )
                cout << lFit << " has not reconstructed direction." << endl;
              else if( !fitVertex.ValidDirection() )
                cout << lFit << ": Invalid direction reconstruction." << endl;
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

          //fitDirection is already a unit vector. mcDirection is not a unit vector.
          double deltaD = acos( fitDirection.Dot( mcDirection.Unit() ) ) * 180.0 / 3.14; 
         
          (*hCountVRes)->Fill( deltaD );
          (*gResVR)->SetPoint( graphPoint, mcPos.Mag(), deltaD );

          graphPoint++;
        }
    }
  (*gResVR)->GetXaxis()->SetTitle( "#cbar MC(r) #cbar [mm]" );
  (*gResVR)->GetYaxis()->SetTitle( "acos #cbar Fit(D) #cdot MC(D) #cbar [deg]" );
  (*gResVR)->SetMarkerStyle( 2 );
}

