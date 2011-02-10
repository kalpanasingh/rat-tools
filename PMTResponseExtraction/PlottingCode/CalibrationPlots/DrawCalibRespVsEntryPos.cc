////////////////////////////////////////////////////////
/// Analyses the angular response data and produces the plots.
///
/// 8/07/10 - New File
/// 19/07/10 - Split functions, new Make Graphs function
/// 14/09/10 - Split from Non calib version, only draws calib plots.
/// 22/11/10 - Added ratio calculations
/// 17/01/11 - Update to Tools
//////////////////////////////////////////////////////// 

#include <TH1D.h>
#include <TCanvas.h>
#include <TStyle.h>
#include <TLegend.h>
using namespace ROOT;

#include <iostream>
using namespace std;

#include "Extraction.hh"
#include "HitData.hh"

#include "Constants.hh"


void
MakeCalibRespVsEntryPosGraphs(
			      vector<HitData*>& data,
			      vector<TH1D*> resultArray );
void
DrawCalibRespVsEntryPos(
		   vector<char*> files );
void
MakeResultVector(
		 vector<TH1D*>& resultArray,
		 bool directory = false );
void
MakeRatioGraphs(
		vector< vector<TH1D*> >& respGraphs,
		vector< vector<TH1D*> >& ratioGraphs );

void
DrawCalibRespVsEntryPos()
{
  vector<char*> files;
  DrawCalibRespVsEntryPos( files );
}

void
DrawCalibRespVsEntryPos(
		   char* lpFile )
{
  vector<char*> files; files.push_back( lpFile );
  DrawCalibRespVsEntryPos( files );
}

void
DrawCalibRespVsEntryPos(
		   char* lpFile1,
		   char* lpFile2 )
{
  vector<char*> files; files.push_back( lpFile1 ); files.push_back( lpFile2 );
  DrawCalibRespVsEntryPos( files );
}

void
MakeResultVector(
		 vector<TH1D*>& resultArray,
		 const bool directory )
{
  resultArray.clear();
  int numBins = 200; double lowBin = 0.0; double highBin = 200.0;


  TH1D* wave1 = new TH1D( "wave1", "337nm Position Response", numBins, lowBin, highBin ); resultArray.push_back( wave1 );
  wave1->GetXaxis()->SetTitle( "Entry Position Radius [mm]");
  wave1->GetYaxis()->SetTitle( "Response per 1 mm bin [%]");
  TH1D* wave2 = new TH1D( "wave2", "365nm Position Response", numBins, lowBin, highBin ); resultArray.push_back( wave2 );
  wave2->GetXaxis()->SetTitle( "Entry Position Radius [mm]");
  wave2->GetYaxis()->SetTitle( "Response per 1 mm bin [%]");
  TH1D* wave3 = new TH1D( "wave3", "386nm Position Response", numBins, lowBin, highBin ); resultArray.push_back( wave3 );
  wave3->GetXaxis()->SetTitle( "Entry Position Radius [mm]");
  wave3->GetYaxis()->SetTitle( "Response per 1 mm bin [%]");
  TH1D* wave4 = new TH1D( "wave4", "420nm Position Response", numBins, lowBin, highBin ); resultArray.push_back( wave4 );
  wave4->GetXaxis()->SetTitle( "Entry Position Radius [mm]");
  wave4->GetYaxis()->SetTitle( "Response per 1 mm bin [%]");
  TH1D* wave5 = new TH1D( "wave5", "500nm Position Response", numBins, lowBin, highBin ); resultArray.push_back( wave5 );
  wave5->GetXaxis()->SetTitle( "Entry Position Radius [mm]");
  wave5->GetYaxis()->SetTitle( "Response per 1 mm bin [%]");
  TH1D* wave6 = new TH1D( "wave6", "620nm Position Response", numBins, lowBin, highBin ); resultArray.push_back( wave6 );
  wave6->GetXaxis()->SetTitle( "Entry Position Radius [mm]");
  wave6->GetYaxis()->SetTitle( "Response per 1 mm bin [%]");
  if( directory == false )
    {
      wave1->SetDirectory(0);
      wave2->SetDirectory(0);
      wave3->SetDirectory(0);
      wave4->SetDirectory(0);
      wave5->SetDirectory(0);
      wave6->SetDirectory(0);
    }
}

void
DrawCalibRespVsEntryPos(
		   vector<char*> files )
{
  gStyle->SetTitleSize( 0.05, "xyz" );
  gStyle->SetTitleOffset( 1.2, "y" );
  gStyle->SetLabelSize( 0.05, "xyz" );
  gStyle->SetOptStat(0);

  vector< vector<TH1D*> > results;
  vector< vector<TH1D*> > ratios;
  if( files.empty() == true ) // Load from filesFullData
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < filesFullData.size(); uLoop++ )
	{
	  vector<TH1D*> resultPlots;
	  MakeResultVector( resultPlots );
	  ratios.push_back( resultPlots ); //Empty plots
	  MakeResultVector( resultPlots );
	  vector<HitData*> current = filesFullData[uLoop].ProduceHitData();
	  MakeCalibRespVsEntryPosGraphs( current, resultPlots );
	  results.push_back( resultPlots );
	}
    }
  else
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < files.size(); uLoop++ )
	{
	  FullDataManager fileData;
	  fileData.DeSerialise( files[uLoop] );

	  vector<TH1D*> resultPlots;
	  MakeResultVector( resultPlots );
	  ratios.push_back( resultPlots ); //Empty plots
	  MakeResultVector( resultPlots );
	  vector<HitData*> current = fileData.ProduceHitData();
	  MakeCalibRespVsEntryPosGraphs( current, resultPlots );
	  results.push_back( resultPlots );
	}
    }
  TLegend* legend = new TLegend( 0.7, 0.60, 0.9, 0.9 );
  legend->SetFillColor( kWhite );
  legend->AddEntry( results[0][0], "RAT", "l" );

  TCanvas* c1 = new TCanvas();
  c1->Divide( 3, 2 );
  c1->cd(1);
  results[0][0]->Draw("E"); // At least 1 result
  c1->cd(2);
  results[0][1]->Draw("E"); // At least 1 result
  c1->cd(3);
  results[0][2]->Draw("E"); // At least 1 result
  c1->cd(4);
  results[0][3]->Draw("E"); // At least 1 result
  c1->cd(5);
  results[0][4]->Draw("E"); // At least 1 result
  c1->cd(6);
  results[0][5]->Draw("E"); // At least 1 result

  unsigned int uLoop;
  for( uLoop = 1; uLoop < results.size(); uLoop++ )
    {
      legend->AddEntry( results[uLoop][0], "SNOMAN"/*files[uLoop]*/, "l" );
      c1->cd(1);
      results[uLoop][0]->SetLineColor( uLoop + 1 );
      results[uLoop][0]->Draw("SAMEE"); // At least 1 result
      c1->cd(2);
      results[uLoop][1]->SetLineColor( uLoop + 1 );
      results[uLoop][1]->Draw("SAMEE"); // At least 1 result
      c1->cd(3);
      results[uLoop][2]->SetLineColor( uLoop + 1 );
      results[uLoop][2]->Draw("SAMEE"); // At least 1 result
      c1->cd(4);
      results[uLoop][3]->SetLineColor( uLoop + 1 );
      results[uLoop][3]->Draw("SAMEE"); // At least 1 result
      c1->cd(5);
      results[uLoop][4]->SetLineColor( uLoop + 1 );
      results[uLoop][4]->Draw("SAMEE"); // At least 1 result
      c1->cd(6);
      results[uLoop][5]->SetLineColor( uLoop + 1 );
      results[uLoop][5]->Draw("SAMEE"); // At least 1 result
    }
  c1->cd(1);
  legend->Draw();
  c1->cd(2);
  legend->Draw();
  c1->cd(3);
  legend->Draw();
  c1->cd(4);
  legend->Draw();
  c1->cd(5);
  legend->Draw();
  c1->cd(6);
  legend->Draw();

  if( results.size() <= 1 )
    return;
  MakeRatioGraphs( results, ratios );
  TCanvas* c2 = new TCanvas();
  c2->Divide( 3, 2 );
  c2->cd(1);
  ratios[1][0]->SetTitle( "337nm Position Response Ratio" );
  ratios[1][0]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][0]->GetYaxis()->SetTitle( "Response ratio per 1 mm bin" );
  ratios[1][0]->Draw("E"); // At least 1 result
  c2->cd(2);
  ratios[1][1]->SetTitle( "365nm Position Response Ratio" );
  ratios[1][1]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][1]->GetYaxis()->SetTitle( "Response ratio per 1 mm bin" );
  ratios[1][1]->Draw("E"); // At least 1 result
  c2->cd(3);
  ratios[1][2]->SetTitle( "386nm Position Response Ratio" );
  ratios[1][2]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][2]->GetYaxis()->SetTitle( "Response ratio per 1 mm bin" );
  ratios[1][2]->Draw("E"); // At least 1 result
  c2->cd(4);
  ratios[1][3]->SetTitle( "420nm Position Response Ratio" );
  ratios[1][3]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][3]->GetYaxis()->SetTitle( "Response ratio per 1 mm bin" );
  ratios[1][3]->Draw("E"); // At least 1 result
  c2->cd(5);
  ratios[1][4]->SetTitle( "500nm Position Response Ratio" );
  ratios[1][4]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][4]->GetYaxis()->SetTitle( "Response ratio per 1 mm bin" );
  ratios[1][4]->Draw("E"); // At least 1 result
  c2->cd(6);
  ratios[1][5]->SetTitle( "620nm Position Response Ratio" );
  ratios[1][5]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][5]->GetYaxis()->SetTitle( "Response ratio per 1 mm bin" );
  ratios[1][5]->Draw("E"); // At least 1 result

  for( uLoop = 2; uLoop < ratios.size(); uLoop++ )
    {
      c2->cd(1);
      ratios[uLoop][0]->SetLineColor( uLoop );
      ratios[uLoop][0]->Draw("SAMEE"); // At least 1 result
      c2->cd(2);
      ratios[uLoop][1]->SetLineColor( uLoop );
      ratios[uLoop][1]->Draw("SAMEE"); // At least 1 result
      c2->cd(3);
      ratios[uLoop][2]->SetLineColor( uLoop );
      ratios[uLoop][2]->Draw("SAMEE"); // At least 1 result
      c2->cd(4);
      ratios[uLoop][3]->SetLineColor( uLoop );
      ratios[uLoop][3]->Draw("SAMEE"); // At least 1 result
      c2->cd(5);
      ratios[uLoop][4]->SetLineColor( uLoop );
      ratios[uLoop][4]->Draw("SAMEE"); // At least 1 result
      c2->cd(6);
      ratios[uLoop][5]->SetLineColor( uLoop );
      ratios[uLoop][5]->Draw("SAMEE"); // At least 1 result
    }

}

void
MakeCalibRespVsEntryPosGraphs(
			      vector<HitData*>& data,
			      vector<TH1D*> resultArray )
{
  vector<TH1D*> signalArray;
  MakeResultVector( signalArray, false );
  vector<TH1D*> hitArray;
  MakeResultVector( hitArray, false );
  unsigned int uLoop;
  for( uLoop = 0; uLoop < data.size(); uLoop++ )
    {
      HitData* dataHit = data[uLoop];
      
      int waveNum = -1;
      if( fabs( dataHit->GetLambda() - wavelength1 ) < waveWidth )
	waveNum = 0;
      else if( fabs( dataHit->GetLambda() - wavelength2 ) < waveWidth )
	waveNum = 1;
      else if( fabs( dataHit->GetLambda() - wavelength3 ) < waveWidth )
	waveNum = 2;
      else if( fabs( dataHit->GetLambda() - wavelength4 ) < waveWidth )
	waveNum = 3;
      else if( fabs( dataHit->GetLambda() - wavelength5 ) < waveWidth )
	waveNum = 4;
      else if( fabs( dataHit->GetLambda() - wavelength6 ) < waveWidth )
	waveNum = 5;
      if( waveNum == -1 )
	continue;

      hitArray[waveNum]->Fill( dataHit->GetInRadialPos() );
      if( dataHit->GetOutcome() == HitData::eSignal )
	signalArray[waveNum]->Fill( dataHit->GetInRadialPos() );
    }

  for( uLoop = 0;  uLoop < signalArray.size(); uLoop++ )
    {
      cout << uLoop << " hits: " << hitArray[uLoop]->GetSumOfWeights() << " signals: " << signalArray[uLoop]->GetSumOfWeights() << " ratio(s/h): " << signalArray[uLoop]->GetSumOfWeights() / hitArray[uLoop]->GetSumOfWeights() << " +/- " << sqrt( 1.0 / signalArray[uLoop]->GetSumOfWeights() + 1.0 / hitArray[uLoop]->GetSumOfWeights() ) * signalArray[uLoop]->GetSumOfWeights() / hitArray[uLoop]->GetSumOfWeights() << endl;
      int iLoop;
      for( iLoop = 1; iLoop <= signalArray[uLoop]->GetNbinsX(); iLoop++ )
	{
	  if( hitArray[uLoop]->GetBinContent( iLoop ) > 0.0 && signalArray[uLoop]->GetBinContent( iLoop ) > 0.0 )
	    {
	      double binVal = signalArray[uLoop]->GetBinContent( iLoop ) / hitArray[uLoop]->GetBinContent( iLoop );
	      double errVal = sqrt( 1.0 / signalArray[uLoop]->GetBinContent( iLoop ) + 1.0 / hitArray[uLoop]->GetBinContent( iLoop ) ) * binVal;
	      resultArray[uLoop]->SetBinContent( iLoop, binVal );
	      resultArray[uLoop]->SetBinError( iLoop, errVal );
	    }
	}
    }
}

void
MakeRatioGraphs(
		vector< vector<TH1D*> >& respGraphs,
		vector< vector<TH1D*> >& ratioGraphs )
{
  unsigned int uLoop;
  for( uLoop = 0; uLoop < respGraphs.size(); uLoop++ )
    {
      ratioGraphs[uLoop][0]->Divide( respGraphs[uLoop][0], respGraphs[0][0] );
      ratioGraphs[uLoop][1]->Divide( respGraphs[uLoop][1], respGraphs[0][1] );
      ratioGraphs[uLoop][2]->Divide( respGraphs[uLoop][2], respGraphs[0][2] );
      ratioGraphs[uLoop][3]->Divide( respGraphs[uLoop][3], respGraphs[0][3] );
      ratioGraphs[uLoop][4]->Divide( respGraphs[uLoop][4], respGraphs[0][4] );
      ratioGraphs[uLoop][5]->Divide( respGraphs[uLoop][5], respGraphs[0][5] );
    }
}

