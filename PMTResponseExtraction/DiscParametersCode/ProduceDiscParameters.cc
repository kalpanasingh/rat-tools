////////////////////////////////////////////////////////
/// Draws the angular response data and produces the plots.
///
/// 01/02/11 - New File
//////////////////////////////////////////////////////// 

#include <TH2D.h>
#include <TCanvas.h>
#include <TStyle.h>
#include <TLegend.h>
using namespace ROOT;

#include <iostream>
#include <sstream>
#include <fstream>
using namespace std;

#include "Constants.hh"
#include "Extraction.hh"
#include "HitData.hh"

TH2D*
MakeDiscHistogram(
		char* name,
		char* title );
void
MakeDiscGraphs(
	       vector<HitData*>& data,
	       TH2D* abs,
	       TH2D* ref,
	       const double within );
void
ProduceDiscParamters(
                     vector<char*> files,
                     char* resultFile = "",
                     char* paramsIndex = "",
                     const double within = 137.7 );
void
ProduceRATDB(
	     char* resultFile,
	     char* paramsIndex,
	     TH2D* abs,
	     TH2D* ref,
	     const double within);
string 
FormatRatD(
	   double val );
void
ProduceDiscParamters(
		     char* sourceFile,
		     char* resultFile = "",
                     char* paramsIndex = "",
                     const double within = 137.7 )
{
  vector<char*> files; files.push_back( sourceFile );
  ProduceDiscParamters( files, resultFile, paramsIndex, within );
}

void
ProduceDiscParamters(
		     vector<char*> files,
		     char* resultFile,
		     char* paramsIndex,
		     const double within )
{
  gStyle->SetTitleSize( 0.05, "xyz" );
  gStyle->SetTitleOffset( 1.2, "y" );
  gStyle->SetLabelSize( 0.05, "xyz" );
  gStyle->SetOptStat(0);

  TH2D* abs = MakeDiscHistogram( "abs", "Absorption" );
  TH2D* ref = MakeDiscHistogram( "ref", "Reflection" );
  if( filesFullData.empty() == false ) // Load from filesFullData
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < filesFullData.size(); uLoop++ )
	{
	  vector<HitData*> current = filesFullData[uLoop].ProduceHitData();
	  MakeDiscGraphs( current, abs, ref, within );
	}
    }
  else
    {
      unsigned int uLoop;
      for( uLoop = 0; uLoop < files.size(); uLoop++ )
	{
	  FullDataManager fileData;
	  fileData.DeSerialise( files[uLoop] );
	  vector<HitData*> current = fileData.ProduceHitData();
	  MakeDiscGraphs( current, abs, ref, within );
	}
    }

  if( resultFile != "" )
    ProduceRATDB( resultFile, paramsIndex, abs, ref, within );

  gStyle->SetOptStat(0);

  gStyle->SetPalette(1);

  TCanvas* c1 = new TCanvas();
  c1->Divide( 1, 2 );

  c1->cd(1);
  abs->GetXaxis()->SetTitle( "Theta [deg]" );
  abs->GetYaxis()->SetTitle( "Lambda [nm]" );
  abs->GetZaxis()->SetTitle( "Abs [%]" );
  abs->Draw("COLZ");

  c1->cd(2);
  ref->GetXaxis()->SetTitle( "Theta [deg]" );
  ref->GetYaxis()->SetTitle( "Lambda [nm]" );
  ref->GetZaxis()->SetTitle( "Ref [%]" );
  ref->Draw("COLZ");

  c1->cd();
}

TH2D*
MakeDiscHistogram(
		  char* name,
		  char* title )
{
  const int thetaBins = 90; const double thetaLow = 0.0; const double thetaHigh = 89.0;
  const int lambdaBins = 49; const double lambdaLow = 220.0; const double lambdaHigh = 710.0;
  return new TH2D( name, title, thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
}

void
MakeDiscGraphs(
               vector<HitData*>& data,
               TH2D* abs,
               TH2D* ref,
               const double within )
{
  TH2D* sig = MakeDiscHistogram( "sig", "sig" );
  TH2D* refl = MakeDiscHistogram( "refl", "refl" );
  TH2D* hits = MakeDiscHistogram( "hits", "hits" );
  sig->SetDirectory(0);
  refl->SetDirectory(0);
  hits->SetDirectory(0);

  unsigned int uLoop;
  for( uLoop = 0;  uLoop < data.size(); uLoop++ )
    {
      HitData* dataHit = data[uLoop];
      double inTheta = dataHit->GetInTheta() * 180.0 / kPI;

      if( dataHit->GetInRadialPos() > within )
        continue;

      hits->Fill( inTheta, dataHit->GetLambda() );
      if( dataHit->GetOutcome() == HitData::eSignal )
        sig->Fill( inTheta, dataHit->GetLambda() );
      else if( dataHit->GetOutcome() == HitData::eReflected )
	refl->Fill( inTheta, dataHit->GetLambda() );
    }
  abs->Divide( sig, hits );
  ref->Divide( refl, hits );
}

void
ProduceRATDB(
	     char* resultFile,
	     char* paramsIndex,
	     TH2D* abs,
	     TH2D* ref,
	     const double within )
{
  ofstream resultDB( resultFile );
  resultDB << "{" << endl << "name: \"GREY_DISC_PARAMETERS\"," << endl << "index: \"" << paramsIndex << "\"," << endl;
  resultDB << "run_range : [0, 0]," << endl << "pass : 0," << endl << "production : false,"<< endl << "comment : \"\"," << endl;
  resultDB << "travel_time: 0.25d," << endl;
  resultDB << "decay_constant: 0.25d," << endl << "bounce_spread: 0.10d," << endl << "disc_radius:" << FormatRatD( within ) << "," << endl;
  resultDB << "collection_efficiency: 1.0d," << endl;

  // Now the actual parameters
  resultDB << "absorption_probability: [";
  for( int iWave = 1; iWave <= 49; iWave++ )
    {
      for( int iTheta = 1; iTheta <= 90; iTheta++ )
	{
	  resultDB << FormatRatD( abs->GetBinContent( iTheta, iWave ) ) << ", ";
	}
    }
  resultDB << "]," << endl;
  resultDB << "reflection_probability: [";
  for( int iWave = 1; iWave <= 49; iWave++ )
    {
      for( int iTheta = 1; iTheta <= 90; iTheta++ )
	{
	  resultDB << FormatRatD( ref->GetBinContent( iTheta, iWave ) ) << ", ";
	}
    }
  resultDB << "]," << endl << "}" << endl;  
  resultDB.close();
}


///-----------------------------------------------------------------------------------------///
/// Helper method to reformat a string into ratdb double output format - Stolen from Jeanne
string 
FormatRatD(
	   double val )
{
  if( val == 0.0 )
    return string( "0.0d" );
  stringstream ss;
  ss << val;
  string sratd;
  ss >> sratd;
  /// if number is in scientific format - replace e with d, else just add a d on the end
    size_t found = sratd.find("e");
    if(found!=string::npos)
      {
	sratd.replace(sratd.find("e"),1,"d");			
      }
    else
      {
	sratd.append("d");
      }	
    return sratd;
}
