////////////////////////////////////////////////////////
/// Draws the angular response data and produces the plots.
///
/// 8/07/10 - New File
/// 19/07/10 - Split functions, new Make Graphs function
/// 14/09/10 - Rewrite
/// 15/11/10 - New Normalise versus normal incidence
/// 01/17/11 - Update for tools
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
MakeRespVsAngleGraphs(
		      vector<HitData*>& data,
		      TH1D* result,
		      const int angleMode, 
		      const double within,
		      const bool normalise );
void
DrawRespVsAngle(
		vector<char*> files,
		const int angleMode,
		const double within,
		const bool normalise );

void
DrawRespVsAngle(
		const int angleMode = 0, // 0 is cos, 1 is radians, 2 is degrees
		const double within = 137, // Cut hits not within 137 mm of centre
		const bool normalise = false ) // Scale all by normal incidence
{
  vector<char*> files;
  DrawRespVsAngle( files, angleMode, within, normalise );
}

void
DrawRespVsAngle(
		char* lpFile,
		const int angleMode = 0, // 0 is cos, 1 is radians, 2 is degrees
		const double within = 137, // Cut hits not within 137 mm of centre
		const bool normalise = false ) // Scale all by normal incidence
{
  vector<char*> files; files.push_back( lpFile );
  DrawRespVsAngle( files, angleMode, within, normalise );
}

void
DrawRespVsAngle(
		char* lpFile1,
		char* lpFile2,
		const int angleMode = 0, // 0 is cos, 1 is radians, 2 is degrees
		const double within = 137, // Cut hits not within 137 mm of centre
		const bool normalise = false ) // Scale all by normal incidence
{
  vector<char*> files; files.push_back( lpFile1 ); files.push_back( lpFile2 );
  DrawRespVsAngle( files, angleMode, within, normalise );
}

void
DrawRespVsAngle(
		vector<char*> files,
		const int angleMode,
		const double within,
		const bool normalise )
{
  gStyle->SetTitleSize( 0.05, "xyz" );
  gStyle->SetTitleOffset( 1.2, "y" );
  gStyle->SetLabelSize( 0.05, "xyz" );
  gStyle->SetOptStat(0);

  int numBins = 0; double lowBin = 0.0; double highBin = 0.0;
  if( angleMode == 0 )
    { numBins = 50; lowBin = -1.0;  highBin = -0.5; }
  else if( angleMode == 1 )
    { numBins = 50; lowBin = 0.0;  highBin = kPI / 2.0; }
  else if( angleMode == 2 )
    { numBins = 90; lowBin = 0.0;  highBin = 90.0; }
  else if( angleMode == 3 )
    { numBins = 30; lowBin = 0.0;  highBin = 90.0; }

  vector<TH1D*> results;
  if( files.empty() == true ) // Load from filesFullData
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < filesFullData.size(); uLoop++ )
	{
	  TH1D* respVsAngle = new TH1D( "hitVsAngleAll", "hitVsAngleAll", numBins, lowBin, highBin );
	  vector<HitData*> current = filesFullData[uLoop].ProduceHitData();
	  MakeRespVsAngleGraphs( current, respVsAngle, angleMode, within, normalise );
	  results.push_back( respVsAngle );
	}
    }
  else
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < files.size(); uLoop++ )
	{
	  FullDataManager fileData;
	  fileData.DeSerialise( files[uLoop] );
	  TH1D* respVsAngle = new TH1D( files[uLoop], files[uLoop], numBins, lowBin, highBin );
	  vector<HitData*> current = fileData.ProduceHitData();
	  MakeRespVsAngleGraphs( current, respVsAngle, angleMode, within, normalise );
	  results.push_back( respVsAngle );
	}
    }
  TCanvas* c1 = new TCanvas();
  c1->cd();
  results[0]->GetXaxis()->SetTitle( "Angle to bucket normal" );
  results[0]->GetYaxis()->SetTitle( "Response [%]" );
  results[0]->Draw("E"); // At least 1 result

  unsigned int uLoop;
  for( uLoop = 1; uLoop < results.size(); uLoop++ )
    {
      results[uLoop]->SetLineColor( uLoop + 1 );
      results[uLoop]->Draw("SAMEE");
    }

  TLegend* legend = new TLegend( 0.1, 0.60, 0.3, 0.9 );
  legend->SetFillColor( kWhite );
  legend->AddEntry( results[0], files[0], "l" );

  for( uLoop = 1; uLoop < results.size(); uLoop++ )
    {
      legend->AddEntry( results[uLoop], files[uLoop], "l" );
      results[uLoop]->SetLineColor( uLoop + 1 );
      results[uLoop]->Draw("SAMEE");
    }
  legend->Draw();
}

void
MakeRespVsAngleGraphs(
		      vector<HitData*>& data,
		      TH1D* result,
		      const int angleMode,
		      const double within,
		      const bool normalise )
{
  TH1D* allSignal = new TH1D( "allResp", "allResp", result->GetNbinsX(), result->GetXaxis()->GetXmin(), result->GetXaxis()->GetXmax() );
  allSignal->SetDirectory(0);
  TH1D* allHits = new TH1D( "allHits", "allHits", result->GetNbinsX(), result->GetXaxis()->GetXmin(), result->GetXaxis()->GetXmax() ); 
  allHits->SetDirectory(0);

  unsigned int uLoop;
  for( uLoop = 0;  uLoop < data.size(); uLoop++ )
    {
      HitData* dataHit = data[uLoop];
      double inTheta = 0;
      if( angleMode == 0 )
	inTheta = -cos( dataHit->GetInTheta() );
      else if( angleMode == 1 )
	inTheta = dataHit->GetInTheta();
      else if( angleMode == 2 || angleMode == 3 )
	inTheta = dataHit->GetInTheta() * 180.0 / kPI;
      
      if( dataHit->GetInRadialPos() > within )
	continue;

      allHits->Fill( inTheta, 1 );
      if( dataHit->GetOutcome() == HitData::eSignal )
	allSignal->Fill( inTheta, 1 );
    }

  cout << "Hits: " << allHits->GetSumOfWeights() << " signals: " << allSignal->GetSumOfWeights() << " ratio(s/h): " << allSignal->GetSumOfWeights() / allHits->GetSumOfWeights() << endl;

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

  if( normalise )
    {
      const double normFactor = result->GetBinContent( 1 );
      const double normError = result->GetBinError( 1 );
      int iLoop;
      for( iLoop = 1; iLoop <= allSignal->GetNbinsX(); iLoop++ )
	{
	  if( result->GetBinContent( iLoop ) == 0.0 )
	    continue;
	  const double binVal = result->GetBinContent( iLoop ) / normFactor;
	  const double errVal = sqrt( pow( result->GetBinError( iLoop ) / result->GetBinContent( iLoop ), 2 ) + pow( normError / normFactor, 2 ) ) * binVal;

	  result->SetBinContent( iLoop, binVal );
	  result->SetBinError( iLoop, errVal );
	}
    }
}
