////////////////////////////////////////////////////////
/// Plots the fit position against the mc position and 
/// expected bias.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 11/06/11 - New File
/// 23/07/12 - Updated file name and function names with "Diff"
////////////////////////////////////////////////////////

#include <FitPlotsUtil.hh>
#include <PlotDiffPosition.hh>

#include <RAT/DU/DSReader.hh>

#include <RAT/DS/Entry.hh>
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
ExtractDiffPosition(
                string lFile,
                string lFit,
                TH1D** hCountVRes,
                TGraph** gResVR,
                TH1D** hCountVResX,
                TH1D** hCountVResY,
                TH1D** hCountVResZ,
                TGraph** gRadialBiasVR );

TCanvas*
UpdateDiffPosition(
               string lFile,
               string lFit, 
               TCanvas* c1,
               Int_t fitNum );

////////////////////////////////////////////////////////
/// Call-able functions
////////////////////////////////////////////////////////
TCanvas*
PlotDiffPosition(
             string lFile )
{
  return PlotDiffPosition( lFile, GetFitNames( lFile ) );
}

TCanvas*
PlotDiffPosition(
             string lFile,
             string lFit )
{
  vector<string> fits; fits.push_back( lFit );
  return PlotDiffPosition( lFile, fits );
}

TCanvas*
PlotDiffPosition(
             string lFile, 
             string lFit1, 
             string lFit2 )
{
  vector<string> fits; fits.push_back( lFit1 ); fits.push_back( lFit2 );
  return PlotDiffPosition( lFile, fits );
}

TCanvas*
PlotDiffPosition(
             string file,
             vector<string> fits )
{
  TCanvas* c1 = NULL;
  for( unsigned int uFit = 0; uFit < fits.size(); uFit++ )
    {
      Int_t drawNum = uFit;
      c1 = UpdateDiffPosition( file, fits[uFit], c1, drawNum );
      cout << "Plotted " << file << " fit: " << fits[uFit] << endl;
    }
  return c1;
}

////////////////////////////////////////////////////////
/// Adds more plots to the first plot
////////////////////////////////////////////////////////

TCanvas*
UpdateDiffPosition(
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
  ExtractDiffPosition( lFile, lFit, &hCountVRes, &gResVR, &hCountVResX, &hCountVResY, &hCountVResZ, &gRadialBiasVR );
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

  cPad = c1->cd(2);
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
  cPad = vc1->cd(1);
  if( firstDraw )
    hCountVResX->Draw("S E");
  else
    {
      hCountVResX->SetLineColor( fitNum + 1 );
      hCountVResX->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVResX, fitNum + 1, cPad );

  cPad = vc1->cd(2);
  if( firstDraw )
    hCountVResY->Draw("S E");
  else
    {
      hCountVResY->SetLineColor( fitNum + 1 );
      hCountVResY->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVResY, fitNum + 1, cPad );

  TVirtualPad* vc2 = c1->cd(4);
  if( firstDraw )
    vc2->Divide( 2, 1 );
  cPad = vc2->cd(1);
  if( firstDraw )
    hCountVResZ->Draw("S E");
  else
    {
      hCountVResZ->SetLineColor( fitNum + 1 );
      hCountVResZ->Draw("SAMES E");
    }
  c1->Update();
  ArrangeStatBox( hCountVResZ, fitNum + 1, cPad );

  cPad = vc2->cd(2);
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
ExtractDiffPosition(
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

  RAT::DU::DSReader dsReader(lFile.c_str());

  int graphPoint = 0;

  for( size_t iEntry = 0; iEntry < dsReader.GetEntryCount(); iEntry++ )
    {

      const RAT::DS::Entry& rDS = dsReader.GetEntry( iEntry );
      const RAT::DS::MC& rMC = rDS.GetMC();

      TVector3 mcPos = rMC->GetMCParticle(0)->GetPosition();
        
      /*Produce a average position (unweighted ?? )
      for( int iEvent2 = 1; iEvent2 < numMCParticles; iEvent2++ )
        {
          cout << "Warn, pileup: averaging position" << endl;
          RAT::DS::MCParticle& rMCParticle =  rMC.GetMCParticle( iEvent2 );
          mcPos = mcPos + rMCParticle->GetPos();
        }
      mcPos = mcPos * ( 1.0 / numMCParticles );
      */
      for( size_t iEV = 0; iEV < rDS.GetEVCount(); iEV++ )
        {
          if( gIgnoreRetriggers && iEV > 0 )
            continue;

          const RAT::DS::EV& rEV = rDS.GetEV( iEV );
          TVector3 fitPos;
          try
            {
              RAT::DS::FitVertex fitVertex =rEV->GetFitResult( lFit ).GetVertex(0);
              if( fitVertex.ContainsPosition()&& fitVertex.ValidPosition() )
                fitPos = fitVertex.GetPosition();
              else if( !fitVertex.ContainsPosition() )
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
              cout << lFit << " failed for event " << iEV << ". Continuing..." << endl;
              continue;
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

