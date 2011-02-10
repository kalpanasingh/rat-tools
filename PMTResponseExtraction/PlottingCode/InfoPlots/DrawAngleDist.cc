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
MakeAngleDistGraphs(
		      vector<HitData*>& data,
		      TH1D* result,
		      const int angleMode, 
		      const double within );
void
DrawAngleDist(
		vector<char*> files,
		const int angleMode,
		const double within );

void
DrawAngleDist(
		const int angleMode = 0, // 0 is cos, 1 is radians, 2 is degrees
		const double within = 137 ) // Cut hits not within 137 mm of centre
{
  vector<char*> files;
  DrawAngleDist( files, angleMode, within );
}

void
DrawAngleDist(
		char* lpFile,
		const int angleMode = 0, // 0 is cos, 1 is radians, 2 is degrees
		const double within = 137 ) // Cut hits not within 137 mm of centre
{
  vector<char*> files; files.push_back( lpFile );
  DrawAngleDist( files, angleMode, within );
}

void
DrawAngleDist(
		char* lpFile1,
		char* lpFile2,
		const int angleMode = 0, // 0 is cos, 1 is radians, 2 is degrees
		const double within = 137 ) // Cut hits not within 137 mm of centre
{
  vector<char*> files; files.push_back( lpFile1 ); files.push_back( lpFile2 );
  DrawAngleDist( files, angleMode, within );
}

void
DrawAngleDist(
		vector<char*> files,
		const int angleMode,
		const double within )
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
	  MakeAngleDistGraphs( current, respVsAngle, angleMode, within );
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
	  MakeAngleDistGraphs( current, respVsAngle, angleMode, within );
	  results.push_back( respVsAngle );
	}
    }
  TCanvas* c1 = new TCanvas();
  c1->cd();
  c1->SetLogy();
  results[0]->GetXaxis()->SetTitle( "Angle to bucket normal" );
  results[0]->GetYaxis()->SetTitle( "Response [%]" );
  results[0]->DrawNormalized("E"); // At least 1 result
  /*
  unsigned int uLoop;
  for( uLoop = 1; uLoop < results.size(); uLoop++ )
    {
      results[uLoop]->SetLineColor( uLoop + 1 );
      results[uLoop]->DrawNormalized("SAMEE");
    }
  */
  TLegend* legend = new TLegend( 0.1, 0.60, 0.3, 0.9 );
  legend->SetFillColor( kWhite );
  legend->AddEntry( results[0], files[0], "l" );

  for( unsigned int uLoop = 1; uLoop < results.size(); uLoop++ )
    {
      legend->AddEntry( results[uLoop], files[uLoop], "l" );
      results[uLoop]->SetLineColor( uLoop + 1 );
      results[uLoop]->DrawNormalized("SAMEE");
    }
  legend->Draw();
}

void
MakeAngleDistGraphs(
		    vector<HitData*>& data,
		    TH1D* result,
		    const int angleMode,
		    const double within )
{
  TH1D* allHits = new TH1D( "allResp", "allResp", result->GetNbinsX(), result->GetXaxis()->GetXmin(), result->GetXaxis()->GetXmax() );
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
    }

  *result = *allHits;
  result->Sumw2();
}
