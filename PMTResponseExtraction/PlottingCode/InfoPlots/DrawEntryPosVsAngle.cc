////////////////////////////////////////////////////////
/// Draws the Hit Position versus input angle
///
/// 15/11/10 - New File
//////////////////////////////////////////////////////// 

#include <TH2D.h>
#include <TCanvas.h>
#include <TStyle.h>
using namespace ROOT;

#include <iostream>
using namespace std;

#include "Constants.hh"

#include "Extraction.hh"
#include "HitData.hh"

void
MakeEntryPosVsAngleGraphs(
			  vector<HitData*>& data,
			  TH2D* result );
void
DrawEntryPosVsAngle(
		   vector<char*> files );

void
DrawEntryPosVsAngle()
{
  vector<char*> files;
  DrawEntryPosVsAngle( files );
}

void
DrawEntryPosVsAngle(
		   char* lpFile )
{
  vector<char*> files; files.push_back( lpFile );
  DrawEntryPosVsAngle( files );
}

void
DrawEntryPosVsAngle(
		   char* lpFile1,
		   char* lpFile2 )
{
  vector<char*> files; files.push_back( lpFile1 ); files.push_back( lpFile2 );
  DrawEntryPosVsAngle( files );
}

void
DrawEntryPosVsAngle(
		   vector<char*> files )
{
  gStyle->SetTitleSize( 0.05, "xyz" );
  gStyle->SetTitleOffset( 0.9, "y" );
  gStyle->SetLabelSize( 0.05, "xyz" );
  gStyle->SetOptStat(0);

  const int thetaBins = 90; const double thetaLow = 0.0; const double thetaHigh = 89.0;
  const int rBins = 20; const double rLow = 0.0; const double rHigh = 200.0;

  vector<TH2D*> Results;
  if( files.empty() == true ) // Load from filesFullData
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < filesFullData.size(); uLoop++ )
	{
	  TH2D* result = new TH2D( "result", files[uLoop], thetaBins, thetaLow, thetaHigh, rBins, rLow, rHigh );
	  vector<HitData*> current = filesFullData[uLoop].ProduceHitData();
	  MakeEntryPosVsAngleGraphs( current, result );
	  Results.push_back( result );
	}
    }
  else
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < files.size(); uLoop++ )
	{
	  FullDataManager fileData;
	  fileData.DeSerialise( files[uLoop] );
	  TH2D* result = new TH2D( "result", files[uLoop], thetaBins, thetaLow, thetaHigh, rBins, rLow, rHigh );
	  vector<HitData*> current = fileData.ProduceHitData();
	  MakeEntryPosVsAngleGraphs( current, result );
	  Results.push_back( result );
	}
    }
  gStyle->SetOptStat(0);

  gStyle->SetPalette(1);

  TCanvas* c1 = new TCanvas();
  c1->Divide( 1, Results.size());
  c1->cd(1);
  Results[0]->GetXaxis()->SetTitle( "Theta [deg]" );
  Results[0]->GetYaxis()->SetTitle( "R [mm]" );
  Results[0]->GetZaxis()->SetTitle( "Fraction per 10mm, 1deg bin" );
  //Results[0]->GetZaxis()->SetRangeUser( 0, 1 );
  Results[0]->DrawNormalized("COLZ");

  unsigned int uLoop;
  for( uLoop = 1; uLoop < Results.size(); uLoop++ )
    {
      c1->cd( uLoop + 1 );
      Results[uLoop]->GetXaxis()->SetTitle( "Theta [deg]" );
      Results[uLoop]->GetYaxis()->SetTitle( "R [mm]" );
      Results[uLoop]->GetZaxis()->SetTitle( "Fraction per 10mm, 1deg bin" );
      Results[uLoop]->SetLineColor( uLoop + 1 );
      //Results[uLoop]->GetZaxis()->SetRangeUser( 0, 1 );
      Results[uLoop]->DrawNormalized("COLZ");
    }
  c1->cd();

  if( Results.size() != 2 )
    return;
  TCanvas* c2 = new TCanvas();
  c2->cd();
  Results[0]->Scale( 1.0 / Results[0]->Integral() );
  Results[1]->Scale( 1.0 / Results[1]->Integral() );
  Results[0]->Add( Results[1], -1.0 );
  Results[0]->Draw("COLZ");
}

void
MakeEntryPosVsAngleGraphs(
			  vector<HitData*>& data,
			  TH2D* result )
{
  unsigned int uLoop;
  for( uLoop = 0;  uLoop < data.size(); uLoop++ )
    {
      HitData* dataHit = data[uLoop];
      double inTheta = dataHit->GetInTheta() * 180.0 / kPI;

      result->Fill( inTheta, dataHit->GetInRadialPos() );
    }

  const double numEntries = result->GetSumOfWeights();
  int iX, iY;
  for( iX = 1; iX <= result->GetNbinsX(); iX++ )
    {
      for( iY = 1; iY <= result->GetNbinsY(); iY++ )
	{
	  //cout << result->GetBinContent( iX, iY ) / numEntries << endl;
	  //  result->SetBinContent( iX, iY, result->GetBinContent( iX, iY )  / numEntries );
	}
    }
}
