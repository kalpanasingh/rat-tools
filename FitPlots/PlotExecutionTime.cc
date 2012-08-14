////////////////////////////////////////////////////////
/// Plots the execution time(s) of the fits
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
#include <TStyle.h>
#include <TLegend.h>
using namespace ROOT;

#include <string>
#include <sstream>
#include <iostream>
using namespace std;

void
ExtractExecutionTime(
                   string lFile,
                   string lFit,
				   string graphName,
                   TGraph** gExecTime );

TCanvas*
PlotExecutionTime(
                string file,
                vector<string> fits );

TCanvas*
UpdateExecutionTime(
				  string lFile,
				  string lFit, 
				  TCanvas* c1,
				  Int_t fitNum );
// Globals
double gMaxExecutionTime = 0.0;
double gMinExecutionTime = 9e99;
double gMaxNhit = 0.0;
double gMinNhit = 0.0; //Force origin

TLegend* gExecTimeLegend; // ROOT is stupid


////////////////////////////////////////////////////////
/// Call-able functions
////////////////////////////////////////////////////////

TCanvas*
PlotExecutionTime(
				string lFile )
{
  return PlotExecutionTime( lFile, GetFitNames( lFile ) );
}

TCanvas*
PlotExecutionTime(
				string lFile, 
				string lFit1 )
{
  vector<string> fits; fits.push_back( lFit1 );
  return PlotExecutionTime( lFile, fits );
}

TCanvas*
PlotExecutionTime(
				string lFile, 
				string lFit1, 
				string lFit2 )
{
  vector<string> fits; fits.push_back( lFit1 ); fits.push_back( lFit2 );
  return PlotExecutionTime( lFile, fits );
}

TCanvas*
PlotExecutionTime(
                string file,
                vector<string> fits )
{
  TCanvas* c1 = NULL;
  for( unsigned int uFit = 0; uFit < fits.size(); uFit++ )
	{
	  Int_t drawNum = uFit;
	  c1 = UpdateExecutionTime( file, fits[uFit], c1, drawNum );
	  cout << "Plotted " << file << " fit: " << fits[uFit] << endl;
	}
  gExecTimeLegend->SetFillColor( kWhite );
  gExecTimeLegend->Draw();
  gStyle->SetOptLogy(0);
  return c1;
}

////////////////////////////////////////////////////////
/// Adds more plots to the first plot
////////////////////////////////////////////////////////

TCanvas*
UpdateExecutionTime(
				  string lFile,
				  string lFit, 
				  TCanvas* c1,
				  Int_t fitNum )
{
  gStyle->SetOptLogy(1);
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
  ExtractExecutionTime( lFile, lFit, graphName.str(), &gExecTime );

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
  reinterpret_cast< TGraph* >( vc1->FindObject( lFile.c_str() ) )->GetYaxis()->SetRangeUser( gMinExecutionTime / 10.0, gMaxExecutionTime * 10.0 );

  c1->Update();

  return c1;  
}

////////////////////////////////////////////////////////
/// Extraction from the ROOT file
////////////////////////////////////////////////////////

void
ExtractExecutionTime(
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
              if( rEV->GetFitResult( lFit ).GetValid() == false )
                continue;
            }
          catch( std::runtime_error& e )
            {
              cout << lFit << " failed for event " << iEvent << ". Continuing..." << endl;
              continue;
            }
		  (*gExecTime)->SetPoint( graphPoint, rEV->GetPMTCalCount(), rEV->GetFitResult( lFit ).GetExecutionTime() );
		  
		  graphPoint++;
		}
	}
  (*gExecTime)->SetName( graphName.c_str() );
  (*gExecTime)->GetXaxis()->SetTitle( "NHits" );
  (*gExecTime)->GetYaxis()->SetTitle( "Execution Time [s]" );
  (*gExecTime)->SetMarkerStyle( 2 );

  gMaxExecutionTime = (*gExecTime)->GetHistogram()->GetMaximum() > gMaxExecutionTime ? (*gExecTime)->GetHistogram()->GetMaximum() : gMaxExecutionTime;
  gMinExecutionTime = (*gExecTime)->GetHistogram()->GetMinimum() < gMinExecutionTime ? (*gExecTime)->GetHistogram()->GetMinimum() : gMinExecutionTime;
}

