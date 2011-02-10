////////////////////////////////////////////////////////
/// Draws the angular response data and produces the plots.
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
MakeCalibRespVsAngleGraphs(
			   vector<HitData*>& data,
			   vector<TH1D*> resultArray,
			   const int angleMode, 
			   const double within,
			   const bool normalise );
void
DrawCalibRespVsAngle(
		vector<char*> files,
		const int angleMode,
		const double within,
		const bool normalise );
void
MakeResultVector(
		 vector<TH1D*>& resultArray,
		 const int angleMode,
		 const bool directory = true );
void
MakeRatioGraphs(
		vector< vector<TH1D*> >& respGraphs,
		vector< vector<TH1D*> >& ratioGraphs );

void
DrawCalibRespVsAngle(
		const int angleMode = 0, // 0 is cos, 1 is radians, 2 is degrees
		const double within = 137, // Cut hits not within 137 mm of centre
		const bool normalise = false ) // Scale all by normal incidence
{
  vector<char*> files;
  DrawCalibRespVsAngle( files, angleMode, within, normalise );
}

void
DrawCalibRespVsAngle(
		char* lpFile,
		const int angleMode = 0, // 0 is cos, 1 is radians, 2 is degrees
		const double within = 137, // Cut hits not within 137 mm of centre
		const bool normalise = false ) // Scale all by normal incidence
{
  vector<char*> files; files.push_back( lpFile );
  DrawCalibRespVsAngle( files, angleMode, within, normalise );
}

void
DrawCalibRespVsAngle(
		char* lpFile1,
		char* lpFile2,
		const int angleMode = 0, // 0 is cos, 1 is radians, 2 is degrees
		const double within = 137, // Cut hits not within 137 mm of centre
		const bool normalise = false ) // Scale all by normal incidence
{
  vector<char*> files; files.push_back( lpFile1 ); files.push_back( lpFile2 );
  DrawCalibRespVsAngle( files, angleMode, within, normalise );
}

void
MakeResultVector(
		 vector<TH1D*>& resultArray,
		 const int angleMode,
		 const bool directory )
{
  resultArray.clear();
  int numBins = 0; double lowBin = 0.0; double highBin = 0.0;
  if( angleMode == 0 )
    { numBins = 50; lowBin = -1.0;  highBin = -0.5; }
  else if( angleMode == 1 )
    { numBins = 50; lowBin = 0.0;  highBin = kPI / 2.0; }
  else if( angleMode == 2 )
    { numBins = 90; lowBin = 0.0;  highBin = 90.0; }
  else if( angleMode == 3 )
    { numBins = 30; lowBin = 0.0;  highBin = 90.0; }

  TH1D* wave1 = new TH1D( "wave1", "337nm Angular Response", numBins, lowBin, highBin ); resultArray.push_back( wave1 );
  wave1->GetXaxis()->SetTitle( "Angle [degree]");
  wave1->GetYaxis()->SetTitle( "Response per 1 degree bin [%]");
  TH1D* wave2 = new TH1D( "wave2", "365nm Angular Response", numBins, lowBin, highBin ); resultArray.push_back( wave2 );
  wave2->GetXaxis()->SetTitle( "Angle [degree]");
  wave2->GetYaxis()->SetTitle( "Response per 1 degree bin [%]");
  TH1D* wave3 = new TH1D( "wave3", "386nm Angular Response", numBins, lowBin, highBin ); resultArray.push_back( wave3 );
  wave3->GetXaxis()->SetTitle( "Angle [degree]");
  wave3->GetYaxis()->SetTitle( "Response per 1 degree bin [%]");
  TH1D* wave4 = new TH1D( "wave4", "420nm Angular Response", numBins, lowBin, highBin ); resultArray.push_back( wave4 );
  wave4->GetXaxis()->SetTitle( "Angle [degree]");
  wave4->GetYaxis()->SetTitle( "Response per 1 degree bin [%]");
  TH1D* wave5 = new TH1D( "wave5", "500nm Angular Response", numBins, lowBin, highBin ); resultArray.push_back( wave5 );
  wave5->GetXaxis()->SetTitle( "Angle [degree]");
  wave5->GetYaxis()->SetTitle( "Response per 1 degree bin [%]");
  TH1D* wave6 = new TH1D( "wave6", "620nm Angular Response", numBins, lowBin, highBin ); resultArray.push_back( wave6 );
  wave6->GetXaxis()->SetTitle( "Angle [degree]");
  wave6->GetYaxis()->SetTitle( "Response per 1 degree bin [%]");
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
DrawCalibRespVsAngle(
		vector<char*> files,
		const int angleMode,
		const double within,
		const bool normalise )
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
	  MakeResultVector( resultPlots, angleMode );
	  ratios.push_back( resultPlots ); //Empty plots
	  MakeResultVector( resultPlots, angleMode );
	  vector<HitData*> current = filesFullData[uLoop].ProduceHitData();
	  MakeCalibRespVsAngleGraphs( current, resultPlots, angleMode, within, normalise );
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
	  MakeResultVector( resultPlots, angleMode );
	  ratios.push_back( resultPlots ); //Empty plots
	  MakeResultVector( resultPlots, angleMode );
	  vector<HitData*> current = fileData.ProduceHitData();
	  MakeCalibRespVsAngleGraphs( current, resultPlots, angleMode, within, normalise );
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
  ratios[1][0]->SetTitle( "337nm Angular Response Ratio" );
  ratios[1][0]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][0]->GetYaxis()->SetTitle( "Response ratio per 1 degree bin" );
  ratios[1][0]->Draw("E"); // At least 1 result
  c2->cd(2);
  ratios[1][1]->SetTitle( "365nm Angular Response Ratio" );
  ratios[1][1]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][1]->GetYaxis()->SetTitle( "Response ratio per 1 degree bin" );
  ratios[1][1]->Draw("E"); // At least 1 result
  c2->cd(3);
  ratios[1][2]->SetTitle( "386nm Angular Response Ratio" );
  ratios[1][2]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][2]->GetYaxis()->SetTitle( "Response ratio per 1 degree bin" );
  ratios[1][2]->Draw("E"); // At least 1 result
  c2->cd(4);
  ratios[1][3]->SetTitle( "420nm Angular Response Ratio" );
  ratios[1][3]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][3]->GetYaxis()->SetTitle( "Response ratio per 1 degree bin" );
  ratios[1][3]->Draw("E"); // At least 1 result
  c2->cd(5);
  ratios[1][4]->SetTitle( "500nm Angular Response Ratio" );
  ratios[1][4]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][4]->GetYaxis()->SetTitle( "Response ratio per 1 degree bin" );
  ratios[1][4]->Draw("E"); // At least 1 result
  c2->cd(6);
  ratios[1][5]->SetTitle( "620nm Angular Response Ratio" );
  ratios[1][5]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][5]->GetYaxis()->SetTitle( "Response ratio per 1 degree bin" );
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
MakeCalibRespVsAngleGraphs(
			   vector<HitData*>& data,
			   vector<TH1D*> resultArray,
			   const int angleMode,
			   const double within,
			   const bool normalise ) 
{
  vector<TH1D*> signalArray;
  MakeResultVector( signalArray, angleMode, false );
  vector<TH1D*> hitArray;
  MakeResultVector( hitArray, angleMode, false );
  unsigned int uLoop;
  for( uLoop = 0; uLoop < data.size(); uLoop++ )
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

      hitArray[waveNum]->Fill( inTheta );
      if( dataHit->GetOutcome() == HitData::eSignal )
	signalArray[waveNum]->Fill( inTheta );
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

  if( normalise )
    { 
      for( uLoop = 0;  uLoop < signalArray.size(); uLoop++ )
	{
	  const double normFactor = resultArray[uLoop]->GetBinContent( 1 );
	  const double normError = resultArray[uLoop]->GetBinError( 1 );
	  int iLoop;
	  for( iLoop = 1; iLoop <= resultArray[uLoop]->GetNbinsX(); iLoop++ )
	    {
	      if( resultArray[uLoop]->GetBinContent( iLoop ) == 0.0 )
		continue;
	      const double binVal = resultArray[uLoop]->GetBinContent( iLoop ) / normFactor;
	      const double errVal = sqrt( pow( resultArray[uLoop]->GetBinError( iLoop ) / resultArray[uLoop]->GetBinContent( iLoop ), 2 ) + pow( normError / normFactor, 2 ) ) * binVal;
	      
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

