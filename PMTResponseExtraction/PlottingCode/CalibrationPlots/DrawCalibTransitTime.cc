////////////////////////////////////////////////////////
/// Draws the transit time
///
/// 8/07/10 - New File
/// 19/07/10 - Split functions, new Make Graphs function
/// 14/09/10 - Split from Non calib version, only draws calib plots.
/// 22/11/10 - Added ratio calculations
/// 03/12/10 - Added normalisation 
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
MakeCalibTransitTimeGraphs(
			   vector<HitData*>& data,
			   vector<TH1D*> resultArray,
			   const double within );
void
DrawCalibTransitTime(
		vector<char*> files,
		const double within );
void
MakeTransitTimeResultVector(
			    vector<TH1D*>& resultArray,
			    const bool directory = true );
void
DrawCalibTransitTime(
		     const double within = 137 ) // Cut hits not within 137 mm of centre
{
  vector<char*> files;
  DrawCalibTransitTime( files, within );
}

void
DrawCalibTransitTime(
		     char* lpFile,
		     const double within = 137 ) // Cut hits not within 137 mm of centre
{
  vector<char*> files; files.push_back( lpFile );
  DrawCalibTransitTime( files, within );
}

void
DrawCalibTransitTime(
		     char* lpFile1,
		     char* lpFile2,
		     const double within = 137 ) // Cut hits not within 137 mm of centre
{
  vector<char*> files; files.push_back( lpFile1 ); files.push_back( lpFile2 );
  DrawCalibTransitTime( files, within );
}

void
MakeTransitTimeResultVector(
			    vector<TH1D*>& resultArray,
			    const bool directory )
{
  resultArray.clear();
  int numBins = 0; double lowBin = 0.0; double highBin = 0.0;
  numBins = 60; lowBin = -1.0;  highBin = 5.0;

  TH1D* wave1 = new TH1D( "wave1", "337nm Transit Time", numBins, lowBin, highBin ); resultArray.push_back( wave1 );
  wave1->GetXaxis()->SetTitle( "Transit Time [ns]");
  wave1->GetYaxis()->SetTitle( "Fraction per 0.1 ns bin");
  TH1D* wave2 = new TH1D( "wave2", "365nm Transit Time", numBins, lowBin, highBin ); resultArray.push_back( wave2 );
  wave2->GetXaxis()->SetTitle( "Transit Time [ns]");
  wave2->GetYaxis()->SetTitle( "Fraction per 0.1 ns bin");
  TH1D* wave3 = new TH1D( "wave3", "386nm Transit Time", numBins, lowBin, highBin ); resultArray.push_back( wave3 );
  wave3->GetXaxis()->SetTitle( "Transit Time [ns]");
  wave3->GetYaxis()->SetTitle( "Fraction per 0.1 ns bin");
  TH1D* wave4 = new TH1D( "wave4", "420nm Transit Time", numBins, lowBin, highBin ); resultArray.push_back( wave4 );
  wave4->GetXaxis()->SetTitle( "Transit Time [ns]");
  wave4->GetYaxis()->SetTitle( "Fraction per 0.1 ns bin");
  TH1D* wave5 = new TH1D( "wave5", "500nm Transit Time", numBins, lowBin, highBin ); resultArray.push_back( wave5 );
  wave5->GetXaxis()->SetTitle( "Transit Time [ns]");
  wave5->GetYaxis()->SetTitle( "Fraction per 0.1 ns bin");
  TH1D* wave6 = new TH1D( "wave6", "620nm Transit Time", numBins, lowBin, highBin ); resultArray.push_back( wave6 );
  wave6->GetXaxis()->SetTitle( "Transit Time [ns]");
  wave6->GetYaxis()->SetTitle( "Fraction per 0.1 ns bin");
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
DrawCalibTransitTime(
		     vector<char*> files,
		     const double within )
{
  gStyle->SetTitleSize( 0.05, "xyz" );
  gStyle->SetTitleOffset( 1.2, "y" );
  gStyle->SetLabelSize( 0.05, "xyz" );
  gStyle->SetOptStat(0);

  vector< vector<TH1D*> > results;
  if( files.empty() == true ) // Load from filesFullData
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < filesFullData.size(); uLoop++ )
	{
	  vector<TH1D*> resultPlots;
	  MakeTransitTimeResultVector( resultPlots );
	  vector<HitData*> current = filesFullData[uLoop].ProduceHitData();
	  MakeCalibTransitTimeGraphs( current, resultPlots, within );
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
	  MakeTransitTimeResultVector( resultPlots );
	  vector<HitData*> current = fileData.ProduceHitData();
	  MakeCalibTransitTimeGraphs( current, resultPlots, within );
	  results.push_back( resultPlots );
	}
    }
  TLegend* legend = new TLegend( 0.7, 0.60, 0.9, 0.9 );
  legend->SetFillColor( kWhite );
  legend->AddEntry( results[0][0], "RAT", "l" );

  TCanvas* c1 = new TCanvas();
  c1->Divide( 3, 2 );
  c1->cd(1);
  results[0][0]->Draw("HIST L"); // At least 1 result
  c1->cd(2);
  results[0][1]->Draw("HIST L"); // At least 1 result
  c1->cd(3);
  results[0][2]->Draw("HIST L"); // At least 1 result
  c1->cd(4);
  results[0][3]->Draw("HIST L"); // At least 1 result
  c1->cd(5);
  results[0][4]->Draw("HIST L"); // At least 1 result
  c1->cd(6);
  results[0][5]->Draw("HIST L"); // At least 1 result

  unsigned int uLoop;
  for( uLoop = 1; uLoop < results.size(); uLoop++ )
    {
      legend->AddEntry( results[uLoop][0], "SNOMAN"/*files[uLoop]*/, "l" );
      c1->cd(1);
      results[uLoop][0]->SetLineColor( uLoop + 1 );
      results[uLoop][0]->Draw("HIST SAME L"); // At least 1 result
      c1->cd(2);
      results[uLoop][1]->SetLineColor( uLoop + 1 );
      results[uLoop][1]->Draw("HIST SAME L"); // At least 1 result
      c1->cd(3);
      results[uLoop][2]->SetLineColor( uLoop + 1 );
      results[uLoop][2]->Draw("HIST SAME L"); // At least 1 result
      c1->cd(4);
      results[uLoop][3]->SetLineColor( uLoop + 1 );
      results[uLoop][3]->Draw("HIST SAME L"); // At least 1 result
      c1->cd(5);
      results[uLoop][4]->SetLineColor( uLoop + 1 );
      results[uLoop][4]->Draw("HIST SAME L"); // At least 1 result
      c1->cd(6);
      results[uLoop][5]->SetLineColor( uLoop + 1 );
      results[uLoop][5]->Draw("HIST SAME L"); // At least 1 result
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

}

void
MakeCalibTransitTimeGraphs(
			   vector<HitData*>& data,
			   vector<TH1D*> resultArray,
			   const double within )
{
  vector<TH1D*> signalArray;
  MakeTransitTimeResultVector( signalArray, false );
  unsigned int uLoop;
  for( uLoop = 0; uLoop < data.size(); uLoop++ )
    {
      HitData* dataHit = data[uLoop];
      
      if( dataHit->GetInRadialPos() > within )
	continue;

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

      if( dataHit->GetOutcome() == HitData::eReflected )
	signalArray[waveNum]->Fill( dataHit->GetDeltaTime() );
    }

  for( uLoop = 0;  uLoop < signalArray.size(); uLoop++ )
    {
      const double totalSum = signalArray[uLoop]->GetSumOfWeights();
      const double totalErr = sqrt( signalArray[uLoop]->GetSumw2()->GetSum() );
	
      int iLoop;
      for( iLoop = 1; iLoop <= signalArray[uLoop]->GetNbinsX(); iLoop++ )
	{
	  if( signalArray[uLoop]->GetBinContent( iLoop ) == 0.0 )
	    continue;
	  const double binVal = signalArray[uLoop]->GetBinContent( iLoop ) / totalSum;
	  const double errVal = binVal * sqrt( 1.0/signalArray[uLoop]->GetBinContent( iLoop ) + pow( totalErr/totalSum, 2 ) );

	  resultArray[uLoop]->SetBinContent( iLoop, binVal );
	  resultArray[uLoop]->SetBinError( iLoop, errVal );
	  
	}
    }
}
