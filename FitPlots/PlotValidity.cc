////////////////////////////////////////////////////////
/// Plots the validity of the fits
///
/// P G Jones <p.g.jones@qmul.ac.uk>
///
/// 11/04/12 - New File
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
#include <TStyle.h>
#include <TLegend.h>
using namespace ROOT;

#include <string>
#include <sstream>
#include <iostream>
using namespace std;

void
ExtractValidity(
                   string lFile,
                   string lFit,
				   string graphName,
                   TGraph** gExecTime );

TCanvas*
PlotValidity(
                string file,
                vector<string> fits );

TCanvas*
UpdateValidity(
				  string lFile,
				  string lFit, 
				  TCanvas* c1,
				  Int_t fitNum );
// Globals
double gMaxNhit = 0.0;
double gMinNhit = 0.0; //Force origin

TLegend* gExecTimeLegend; // ROOT is stupid


////////////////////////////////////////////////////////
/// Call-able functions
////////////////////////////////////////////////////////

TCanvas*
PlotValidity(
             string lFile )
{
  return PlotValidity( lFile, GetFitNames( lFile ) );
}

TCanvas*
PlotValidity(
             string lFile, 
             string lFit1 )
{
  vector<string> fits; fits.push_back( lFit1 );
  return PlotValidity( lFile, fits );
}

TCanvas*
PlotValidity(
             string lFile, 
             string lFit1, 
             string lFit2 )
{
  vector<string> fits; fits.push_back( lFit1 ); fits.push_back( lFit2 );
  return PlotValidity( lFile, fits );
}

TCanvas*
PlotValidity(
             string file,
             vector<string> fits )
{
  TCanvas* c1 = NULL;
  for( unsigned int uFit = 0; uFit < fits.size(); uFit++ )
	{
	  Int_t drawNum = uFit;
	  c1 = UpdateValidity( file, fits[uFit], c1, drawNum );
	  cout << "Plotted " << file << " fit: " << fits[uFit] << endl;
	}
  gExecTimeLegend->SetFillColor( kWhite );
  gExecTimeLegend->Draw();
  return c1;
}

////////////////////////////////////////////////////////
/// Adds more plots to the first plot
////////////////////////////////////////////////////////

TCanvas*
UpdateValidity(
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
	  gExecTimeLegend = new TLegend( 0.1, 0.7, 0.3, 0.9 );
	}

  TGraph* gExecTime;
  // First extract the data
  stringstream graphName;
  if( firstDraw )
	graphName << lFile;
  else
	graphName << lFile << "_" << lFit;
  ExtractValidity( lFile, lFit, graphName.str(), &gExecTime );

  TVirtualPad* vc1 = c1->cd(1);
  // Now draw the results
  if( firstDraw )
	gExecTime->Draw("AP");
  else
	{
	  gExecTime->SetMarkerColor( fitNum + 1 );
	  gExecTime->Draw("P");
	}
  gExecTimeLegend->AddEntry( gExecTime, lFit.c_str(), "P" );
  reinterpret_cast< TGraph* >( vc1->FindObject( lFile.c_str() ) )->GetYaxis()->SetRangeUser( 0.0, 1.0 );

  c1->Update();

  return c1;  
}

////////////////////////////////////////////////////////
/// Extraction from the ROOT file
////////////////////////////////////////////////////////

void
ExtractValidity(
                string lFile,
                string lFit,
                string graphName,
                TGraph** gExecTime )
{
  // Now new the graphs
  *gExecTime = new TGraph();

  // Now extract the data
  // Load the first file
  RAT::DS::Root* rDS;
  RAT::DS::PMTProperties* rPMTList;
  TChain* tree;

  LoadRootFile( lFile, &tree, &rDS, &rPMTList );

  int graphPoint = 0;
  double validEvents, totalEvents;
  validEvents = totalEvents = 0.0;
  for( int iLoop = 0; iLoop < tree->GetEntries(); iLoop++ )
    {
      tree->GetEntry( iLoop );

      for( int iEvent = 0; iEvent < rDS->GetEVCount(); iEvent++ )
		{
          if( gIgnoreRetriggers && iEvent > 0 )
            continue;

		  RAT::DS::EV *rEV = rDS->GetEV(0);
          try
            {
              totalEvents += 1.0;
              const int valid = rEV->GetFitResult( lFit ).GetValid();
              (*gExecTime)->SetPoint( graphPoint, rEV->GetPMTCalCount(), valid );
              validEvents += valid;
              graphPoint++;
            }
          catch( std::runtime_error& e )
            {
              cout << lFit << " failed for event " << iEvent << ". Continuing..." << endl;
              continue;
            }
		}
	}
  cout << lFile << " " << lFit << " " << validEvents / totalEvents << endl;
  (*gExecTime)->SetName( graphName.c_str() );
  (*gExecTime)->GetXaxis()->SetTitle( "NHits" );
  (*gExecTime)->GetYaxis()->SetTitle( "Validity" );
  (*gExecTime)->SetMarkerStyle( 2 );

}

