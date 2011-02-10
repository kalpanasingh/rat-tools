////////////////////////////////////////////////////////
/// Draws the reflection versus wavelength data 
/// and produces the plots.
///
/// 15/09/10 - New File
/// 17/01/11 - Update for Tools
//////////////////////////////////////////////////////// 

#include <TH1D.h>
#include <TCanvas.h>
#include <TStyle.h>
#include <TLegend.h>
using namespace ROOT;

#include <iostream>
using namespace std;

#include "Constants.hh"
#include "Extraction.hh"
#include "HitData.hh"

void
MakeReflVsLambdaGraphs(
		       vector<HitData*>& data,
		       TH1D* result,
		       const double within );
void
DrawReflVsLambda(
		 vector<char*> files,
		 const double within );

void
DrawReflVsLambda(
		 const double within = 137 ) 
{
  vector<char*> files;
  DrawReflVsLambda( files, within );
}

void
DrawReflVsLambda(
		 char* lpFile,
		 const double within = 137 ) 
{
  vector<char*> files; files.push_back( lpFile );
  DrawReflVsLambda( files, within );
}

void
DrawReflVsLambda(
		 char* lpFile1,
		 char* lpFile2,
		 const double within = 137 ) 
{
  vector<char*> files; files.push_back( lpFile1 ); files.push_back( lpFile2 );
  DrawReflVsLambda( files, within );
}

void
DrawReflVsLambda(
		 vector<char*> files,
		 const double within )
{
  gStyle->SetTitleSize( 0.05, "xyz" );
  gStyle->SetTitleOffset( 1.2, "y" );
  gStyle->SetLabelSize( 0.05, "xyz" );
  gStyle->SetOptStat(0);

  int numBins = 60; double lowBin = 200.0; double highBin = 800.0;

  vector<TH1D*> results;
  if( files.empty() == true ) // Load from filesFullData
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < filesFullData.size(); uLoop++ )
	{
	  TH1D* respVsLambda = new TH1D( "hitVsLambdaAll", "hitVsLambdaAll", numBins, lowBin, highBin );
	  vector<HitData*> current = filesFullData[uLoop].ProduceHitData();
	  MakeReflVsLambdaGraphs( current, respVsLambda, within );
	  results.push_back( respVsLambda );
	}
    }
  else
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < files.size(); uLoop++ )
	{
	  FullDataManager fileData;
	  fileData.DeSerialise( files[uLoop] );
	  TH1D* respVsLambda = new TH1D( files[uLoop], "Wavelength Reflection", numBins, lowBin, highBin );
	  vector<HitData*> current = fileData.ProduceHitData();
	  MakeReflVsLambdaGraphs( current, respVsLambda, within );
	  results.push_back( respVsLambda );
	}
    }
  TCanvas* c1 = new TCanvas();
  c1->cd();
  results[0]->GetXaxis()->SetTitle( "Wavelength [nm]" );
  results[0]->GetYaxis()->SetTitle( "Reflection per 10nm bin [%]" );
  results[0]->Draw("E"); // At least 1 result

  TLegend* legend = new TLegend( 0.1, 0.60, 0.3, 0.9 );
  legend->SetFillColor( kWhite );
  legend->AddEntry( results[0], files[0], "l" );

  unsigned int uLoop;
  for( uLoop = 1; uLoop < results.size(); uLoop++ )
    {
      legend->AddEntry( results[uLoop], files[uLoop], "l" );
      results[uLoop]->SetLineColor( uLoop + 1 );
      results[uLoop]->Draw("SAMEE");
    }
  legend->Draw();
}

void
MakeReflVsLambdaGraphs(
		      vector<HitData*>& data,
		      TH1D* result,
		      const double within ) // Cut hits not within 137 mm of centre
{
  TH1D* allSignal = new TH1D( "allRefl", "allRefl", result->GetNbinsX(), result->GetXaxis()->GetXmin(), result->GetXaxis()->GetXmax() );
  allSignal->SetDirectory(0);
  TH1D* allHits = new TH1D( "allHits", "allHits", result->GetNbinsX(), result->GetXaxis()->GetXmin(), result->GetXaxis()->GetXmax() ); 
  allHits->SetDirectory(0);

  unsigned int uLoop;
  for( uLoop = 0;  uLoop < data.size(); uLoop++ )
    {
      HitData* dataHit = data[uLoop];
      
      if( dataHit->GetInRadialPos() > within )
	continue;

      allHits->Fill( dataHit->GetLambda() );
      if( dataHit->GetOutcome() == HitData::eSignal )
	allSignal->Fill( dataHit->GetLambda() );
    }
  int iLoop;
  for( iLoop = 1; iLoop <= allSignal->GetNbinsX(); iLoop++ )
    {
      if( allHits->GetBinContent( iLoop ) > 0.0 && allSignal->GetBinContent( iLoop ) > 0.0 )
	{
	  double binVal = allSignal->GetBinContent( iLoop ) / allHits->GetBinContent( iLoop );
	  double errVal = sqrt( 1.0 / allSignal->GetBinContent( iLoop ) + 1.0 / allHits->GetBinContent( iLoop ) ) * binVal;
	  result->SetBinContent( iLoop, binVal );
	  result->SetBinError( iLoop, errVal );
	}
    }
}
