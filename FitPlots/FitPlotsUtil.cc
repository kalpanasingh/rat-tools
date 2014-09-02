////////////////////////////////////////////////////////
/// Plots the fit position against the mc position and 
/// expected bias.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 01/06/11 - New File
////////////////////////////////////////////////////////

#include <FitPlotsUtil.hh>

#include <TH1D.h>
#include <TChain.h>
#include <TFile.h>
#include <TPaveStats.h>
#include <TVirtualPad.h>
using namespace ROOT;

#include <RAT/DSReader.hh>

#include <RAT/DS/Root.hh>

#include <string>
#include <sstream>
#include <iostream>
using namespace std;

bool gIgnoreRetriggers = false; // Global variable used to ignore retriggered (low nhit tail) events

////////////////////////////////////////////////////////
/// Correctly arrange and tile stat boxes
////////////////////////////////////////////////////////

void
ArrangeStatBox( 
               TH1D* hHistogram,
               Int_t color,
               TVirtualPad* pad )
{
  // First Get the number of exisiting stat boxes
  int numStats = 0;
  TIter next( pad->GetListOfPrimitives() );
  while( TObject *obj = next() ) 
    if( obj->GetName() == string( "stats" ) )
      numStats++;

  TPaveStats *sBox = (TPaveStats*)hHistogram->GetListOfFunctions()->FindObject("stats");
  hHistogram->GetListOfFunctions()->Remove( sBox );
  hHistogram->SetStats( 0 );
  sBox->SetLineColor( color );
  sBox->SetY1NDC( sBox->GetY1NDC() - numStats * 0.2 );
  sBox->SetY2NDC( sBox->GetY2NDC() - numStats * 0.2 );
  sBox->Draw();
}

////////////////////////////////////////////////////////
/// Returns a vector of fit names in the file
////////////////////////////////////////////////////////

GetFitNames( string lFile )
{

  RAT::DU::DSReader dsReader( lFile );

  int iEntry = 0;
  const RAT::DS::Entry& dsEntry = dsReader.GetEntry( iEntry );
  while( dsEntry.GetEVCount() == 0 )
    dsEntry = dsReader.GetEntry( ++iEntry );

  vector<string> fitNames = dsEntry.GetEV( 0 ).GetFitNames();
  
  return fitNames;
}

