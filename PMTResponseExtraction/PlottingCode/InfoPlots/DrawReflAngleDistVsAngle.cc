////////////////////////////////////////////////////////
/// Analyses the angular reflection data and produces the plots.
///
/// 25/11/10 - New File
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
MakeReflAngleDistVsAngleGraphs(
		      vector<HitData*>& data,
		      vector<TH1D*> resultArray,
		      const double within );
void
DrawReflAngleDistVsAngle(
		   vector<char*> files,
		   const double within );
void
MakeReflAngleResultVector(
		 vector<TH1D*>& resultArray,
		 const bool directory = false );
void
MakeRatioGraphs(
		vector< vector<TH1D*> >& respGraphs,
		vector< vector<TH1D*> >& ratioGraphs );

void
DrawReflAngleDistVsAngle(
		   const double within = 137 ) // Cut hits not within 137 mm of centre
{
  vector<char*> files;
  DrawReflAngleDistVsAngle( files, within );
}

void
DrawReflAngleDistVsAngle(
		   char* lpFile,
		   const double within = 137 ) // Cut hits not within 137 mm of centre
{
  vector<char*> files; files.push_back( lpFile );
  DrawReflAngleDistVsAngle( files, within );
}

void
DrawReflAngleDistVsAngle(
		   char* lpFile1,
		   char* lpFile2,
		   const double within = 137 ) // Cut hits not within 137 mm of centre
{
  vector<char*> files; files.push_back( lpFile1 ); files.push_back( lpFile2 );
  DrawReflAngleDistVsAngle( files, within );
}

void
MakeReflAngleResultVector(
			  vector<TH1D*>& resultArray,
			  const bool directory )
{
  resultArray.clear();
  int numBins = 0; double lowBin = 0.0; double highBin = 0.0;
  numBins = 90; lowBin = 0.0;  highBin = 90.0;

  TH1D* wave1 = new TH1D( "wave1", "0-10 Degree Refl Dist", numBins, lowBin, highBin ); resultArray.push_back( wave1 );
  wave1->GetXaxis()->SetTitle( "Reflected Angle [degree]");
  wave1->GetYaxis()->SetTitle( "Fraction per degree bin [%]");
  TH1D* wave2 = new TH1D( "wave2", "10-20 Degree Refl Dist", numBins, lowBin, highBin ); resultArray.push_back( wave2 );
  wave2->GetXaxis()->SetTitle( "Reflected Angle [degree]");
  wave2->GetYaxis()->SetTitle( "Fraction per degree bin [%]");
  TH1D* wave3 = new TH1D( "wave3", "20-30 Degree Refl Dist", numBins, lowBin, highBin ); resultArray.push_back( wave3 );
  wave3->GetXaxis()->SetTitle( "Reflected Angle [degree]");
  wave3->GetYaxis()->SetTitle( "Fraction per degree bin [%]");
  TH1D* wave4 = new TH1D( "wave4", "30-40 Degree Refl Dist", numBins, lowBin, highBin ); resultArray.push_back( wave4 );
  wave4->GetXaxis()->SetTitle( "Reflected Angle [degree]");
  wave4->GetYaxis()->SetTitle( "Fraction per degree bin [%]");
  TH1D* wave5 = new TH1D( "wave5", "40-50 Degree Refl Dist", numBins, lowBin, highBin ); resultArray.push_back( wave5 );
  wave5->GetXaxis()->SetTitle( "Reflected Angle [degree]");
  wave5->GetYaxis()->SetTitle( "Fraction per degree bin [%]");
  TH1D* wave6 = new TH1D( "wave6", ">50 Degree Refl Dist", numBins, lowBin, highBin ); resultArray.push_back( wave6 );
  wave6->GetXaxis()->SetTitle( "Reflected Angle [degree]");
  wave6->GetYaxis()->SetTitle( "Fraction per degree bin [%]");
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
DrawReflAngleDistVsAngle(
			 vector<char*> files,
			 const double within )
{
  gStyle->SetTitleSize( 0.05, "xyz" );
  gStyle->SetTitleOffset( 1.6, "y" );
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
	  MakeReflAngleResultVector( resultPlots );
	  ratios.push_back( resultPlots ); //Empty plots
	  MakeReflAngleResultVector( resultPlots );
	  vector<HitData*> current = filesFullData[uLoop].ProduceHitData();
	  MakeReflAngleDistVsAngleGraphs( current, resultPlots, within );
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
	  MakeReflAngleResultVector( resultPlots );
	  ratios.push_back( resultPlots ); //Empty plots
	  MakeReflAngleResultVector( resultPlots );
	  vector<HitData*> current = fileData.ProduceHitData();
	  MakeReflAngleDistVsAngleGraphs( current, resultPlots, within );
	  results.push_back( resultPlots );
	}
    }
  TLegend* legend = new TLegend( 0.7, 0.9, 0.3, 0.9 );
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
  ratios[1][0]->SetTitle( "Angular Reflection Distribution Ratio" );
  ratios[1][0]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][0]->GetYaxis()->SetTitle( "Reflection Distribution ratio per degree bin" );
  ratios[1][0]->Draw("E"); // At least 1 result
  c2->cd(2);
  ratios[1][1]->SetTitle( "Angular Reflection Distribution Ratio" );
  ratios[1][1]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][1]->GetYaxis()->SetTitle( "Reflection Distribution ratio per degree bin" );
  ratios[1][1]->Draw("E"); // At least 1 result
  c2->cd(3);
  ratios[1][2]->SetTitle( "Angular Reflection Distribution Ratio" );
  ratios[1][2]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][2]->GetYaxis()->SetTitle( "Reflection Distribution ratio per degree bin" );
  ratios[1][2]->Draw("E"); // At least 1 result
  c2->cd(4);
  ratios[1][3]->SetTitle( "Angular Reflection Distribution Ratio" );
  ratios[1][3]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][3]->GetYaxis()->SetTitle( "Reflection Distribution ratio per degree bin" );
  ratios[1][3]->Draw("E"); // At least 1 result
  c2->cd(5);
  ratios[1][4]->SetTitle( "Angular Reflection Distribution Ratio" );
  ratios[1][4]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][4]->GetYaxis()->SetTitle( "Reflection Distribution ratio per degree bin" );
  ratios[1][4]->Draw("E"); // At least 1 result
  c2->cd(6);
  ratios[1][5]->SetTitle( "Angular Reflection Distribution Ratio" );
  ratios[1][5]->GetYaxis()->SetRangeUser( 0.8, 1.2 );
  ratios[1][5]->GetYaxis()->SetTitle( "Reflection Response ratio per degree bin" );
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
MakeReflAngleDistVsAngleGraphs(
		      vector<HitData*>& data,
		      vector<TH1D*> resultArray,
		      const double within ) 
{
  vector<TH1D*> signalArray;
  MakeReflAngleResultVector( signalArray, false );

  unsigned int uLoop;
  for( uLoop = 0; uLoop < data.size(); uLoop++ )
    {
      HitData* dataHit = data[uLoop];
      double inTheta = dataHit->GetInTheta() * 180.0 / kPI;
      double outTheta = dataHit->GetOutTheta() * 180.0 / kPI;
      
      if( dataHit->GetInRadialPos() > within )
	continue;

      int waveNum = -1;
      if( inTheta < 10.0 )
	waveNum = 0;
      else if( inTheta < 20.0 )
	waveNum = 1;
      else if( inTheta < 30.0 )
	waveNum = 2;
      else if( inTheta < 40.0 )
	waveNum = 3;
      else if( inTheta < 50.0 )
	waveNum = 4;
      else if( inTheta > 50.0 )
	waveNum = 5;
      if( waveNum == -1 )
	continue;

      if( dataHit->GetOutcome() == HitData::eReflected )
	signalArray[waveNum]->Fill( outTheta );
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

