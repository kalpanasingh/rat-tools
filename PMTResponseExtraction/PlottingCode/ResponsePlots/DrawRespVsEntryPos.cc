////////////////////////////////////////////////////////
/// Draws the response versus entry radius
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
MakeRespVsEntryPosGraphs(
			 vector<HitData*>& data,
			 TH1D* result );
void
DrawRespVsEntryPos(
		   vector<char*> files );

void
DrawRespVsEntryPos()
{
  vector<char*> files;
  DrawRespVsEntryPos( files );
}

void
DrawRespVsEntryPos(
		   char* lpFile )
{
  vector<char*> files; files.push_back( lpFile );
  DrawRespVsEntryPos( files );
}

void
DrawRespVsEntryPos(
		 char* lpFile1,
		 char* lpFile2 )
{
  vector<char*> files; files.push_back( lpFile1 ); files.push_back( lpFile2 );
  DrawRespVsEntryPos( files );
}

void
DrawRespVsEntryPos(
		   vector<char*> files )
{
  gStyle->SetTitleSize( 0.05, "xyz" );
  gStyle->SetTitleOffset( 1.2, "y" );
  gStyle->SetLabelSize( 0.05, "xyz" );
  gStyle->SetOptStat(0);

  int numBins = 200; double lowBin = 0.0; double highBin = 200.0;

  vector<TH1D*> results;
  if( files.empty() == true ) // Load from filesFullData
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < filesFullData.size(); uLoop++ )
	{
	  TH1D* respVsEntryPos = new TH1D( "hitVsEntryPosAll", "hitVsEntryPosAll", numBins, lowBin, highBin );
	  vector<HitData*> current = filesFullData[uLoop].ProduceHitData();
	  MakeRespVsEntryPosGraphs( current, respVsEntryPos );
	  results.push_back( respVsEntryPos );
	}
    }
  else
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < files.size(); uLoop++ )
	{
	  FullDataManager fileData;
	  fileData.DeSerialise( files[uLoop] );
	  TH1D* respVsEntryPos = new TH1D( files[uLoop], "Position Response", numBins, lowBin, highBin );
	  vector<HitData*> current = fileData.ProduceHitData();
	  MakeRespVsEntryPosGraphs( current, respVsEntryPos );
	  results.push_back( respVsEntryPos );
	}
    }
  TCanvas* c1 = new TCanvas();
  c1->cd();
  results[0]->GetXaxis()->SetTitle( "Entry Position [mm]" );
  results[0]->GetYaxis()->SetTitle( "Response per 10nm bin [%]" );
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
MakeRespVsEntryPosGraphs(
			 vector<HitData*>& data,
			 TH1D* result )
{
  TH1D* allSignal = new TH1D( "allResp", "allResp", result->GetNbinsX(), result->GetXaxis()->GetXmin(), result->GetXaxis()->GetXmax() );
  allSignal->SetDirectory(0);
  TH1D* allHits = new TH1D( "allHits", "allHits", result->GetNbinsX(), result->GetXaxis()->GetXmin(), result->GetXaxis()->GetXmax() ); 
  allHits->SetDirectory(0);

  unsigned int uLoop;
  for( uLoop = 0;  uLoop < data.size(); uLoop++ )
    {
      HitData* dataHit = data[uLoop];

      allHits->Fill( dataHit->GetInRadialPos() );
      if( dataHit->GetOutcome() == HitData::eSignal )
	allSignal->Fill( dataHit->GetInRadialPos() );
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
