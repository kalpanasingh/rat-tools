////////////////////////////////////////////////////////
/// Plots the fit energy against the mc energy and 
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
ExtractDiffEnergy(
              string lFile,
              string lFit,
              TH1D** hCountVRes,
              TGraph** gResVR,
              TGraph** gResVE );

TCanvas*
PlotDiffEnergy(
           string file,
           vector<string> fits );

TCanvas*
UpdateDiffEnergy(
             string lFile,
             string lFit, 
             TCanvas* c1,
             Int_t fitNum );

////////////////////////////////////////////////////////
/// Call-able functions
////////////////////////////////////////////////////////
TCanvas*
PlotDiffEnergy(
           string lFile )
{
  return PlotDiffEnergy( lFile, GetFitNames( lFile ) );
}

TCanvas*
PlotDiffEnergy(
           string lFile,
           string lFit )
{
  vector<string> fits; fits.push_back( lFit );
  return PlotDiffEnergy( lFile, fits );
}

TCanvas*
PlotDiffEnergy(
           string lFile, 
           string lFit1, 
           string lFit2 )
{
  vector<string> fits; fits.push_back( lFit1 ); fits.push_back( lFit2 );
  return PlotDiffEnergy( lFile, fits );
}

TCanvas*
PlotDiffEnergy(
           string file,
           vector<string> fits )
{
  TCanvas* c1 = NULL;
  for( unsigned int uFit = 0; uFit < fits.size(); uFit++ )
    {
      Int_t drawNum = uFit;
      c1 = UpdateDiffEnergy( file, fits[uFit], c1, drawNum );
      cout << "Plotted " << file << " fit: " << fits[uFit] << endl;
    }
  return c1;
}

////////////////////////////////////////////////////////
/// Adds more plots to the first plot
////////////////////////////////////////////////////////

TCanvas*
UpdateDiffEnergy(
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
  ExtractDiffEnergy( lFile, lFit, &hCountVRes, &gResVR, &gResVE );
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
    hCountVRes->Draw("S E");
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
ExtractDiffEnergy(
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

  RAT::DSReader dsReader(lFile.c_str());
  RAT::DU::PMTInfo rPMTList = DS::DU::Utility::Get()->GetPMTInfo();

  int graphPoint = 0;
  (*gResVE)->SetPoint( graphPoint, 0.0, 0.0 );
  graphPoint++;

  for( size_t iEvent = 0; iEvent < dsReader.GetEventCount(); iEvent++ )
    {
      
      const RAT::DS::Root& rDS = dsReader.GetEvent( iEvent );
      const RAT::DS::MC& rMC = rDS.GetMC();
	  int npart = rMC.GetMCParticleCount();

      // assume even if multiple particles in vertex - define position by first particle
	  TVector3 mcPos = rMC.GetMCParticle(0).GetPosition();
	  double mcEnergy = 0;
	  for(int ipart=0;ipart<npart;++ipart){
        mcEnergy += rMC.GetMCParticle(ipart).GetKineticEnergy();
      }

      for( size_t iEV = 0; iEV < rDS.GetEVCount(); iEV++ )
        {
          if( gIgnoreRetriggers && iEV > 0 )
            continue;

          const RAT::DS::EV& rEV = rDS.GetEV( iEV );
          double fitEnergy;
          try
            {
              RAT::DS::FitVertex fitVertex =rEV->GetFitResult( lFit ).GetVertex(0);
              if( fitVertex.ContainsEnergy() && fitVertex.ValidEnergy() )
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
              cout << lFit << " failed for event " << iEV << ". Continuing..." << endl;
              continue;
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

