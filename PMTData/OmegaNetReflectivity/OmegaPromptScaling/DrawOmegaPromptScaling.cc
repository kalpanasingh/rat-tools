////////////////////////////////////////////////////////
/// Draw the prompt parameters
///
/// 30/07/10 - New file
///////////////////////////////////////////////////////

#include "TH2D.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TStyle.h"
using namespace ROOT;

#include <iostream>
using namespace std;

#include "Prompt1.hh"
#include "Prompt2.hh"
#include "Prompt3.hh"
#include "Prompt4.hh"

void
DrawOmegaPromptScaling()
{
  const int thetaBins = 91; const double thetaLow = 0.0; const double thetaHigh = 90.0;
  const int lambdaBins = 48; const double lambdaLow = 230.0; const double lambdaHigh = 700.0;
  TH2D* promptScaling1 = new TH2D( "promptScaling1", "2005 Data", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* promptScaling2 = new TH2D( "promptScaling2", "Jan 2002 Data", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* promptScaling3 = new TH2D( "promptScaling3", "Mar 2003 Data", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* promptScaling4 = new TH2D( "promptScaling4", "Apr 2006 Data", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );

  double maxVal = 1.0;
  double minVal = 1.0;

  int iLoop;
  for( iLoop = 0; iLoop < 91; iLoop++ )
    {
      int iLoop2;
      for( iLoop2 = 23; iLoop2 < 71; iLoop2++ )
	{
	  int omegaPoint = iLoop + ( iLoop2 - 23 ) * 91;
	  double promptVal = normalisation1 / ( 1.0 + Prompt1[omegaPoint] * ( 1.0 - normalisation1 ) );
	  promptScaling1->Fill( (double)iLoop, (double)iLoop2 * 10.0, promptVal );

	  if( promptVal > maxVal )
	    maxVal = promptVal;
	  else if ( promptVal < minVal )
	    minVal = promptVal;

	  promptVal = normalisation2 / ( 1.0 + Prompt2[omegaPoint] * ( 1.0 - normalisation2 ) );
	  promptScaling2->Fill( (double)iLoop, (double)iLoop2 * 10.0, promptVal );

	  if( promptVal > maxVal )
	    maxVal = promptVal;
	  else if ( promptVal < minVal )
	    minVal = promptVal;

	  promptVal = normalisation3 / ( 1.0 + Prompt3[omegaPoint] * ( 1.0 - normalisation3 ) );
	  promptScaling3->Fill( (double)iLoop, (double)iLoop2 * 10.0, promptVal );

	  if( promptVal > maxVal )
	    maxVal = promptVal;
	  else if ( promptVal < minVal )
	    minVal = promptVal;

	  promptVal = normalisation4 / ( 1.0 + Prompt4[omegaPoint] * ( 1.0 - normalisation4 ) );
	  promptScaling4->Fill( (double)iLoop, (double)iLoop2 * 10.0, promptVal );

	  if( promptVal > maxVal )
	    maxVal = promptVal;
	  else if ( promptVal < minVal )
	    minVal = promptVal;
	}
    }
  gStyle->SetOptStat(0);

  gStyle->SetPalette(1);
  TCanvas* c1 = new TCanvas();
  c1->Divide( 2, 2 );

  c1->cd(1);
  promptScaling1->GetXaxis()->SetTitle( "Theta [deg]" );
  promptScaling1->GetYaxis()->SetTitle( "Lambda [nm]" );
  promptScaling1->GetZaxis()->SetTitle( "Prompt Scaling [%]" );
  promptScaling1->GetZaxis()->SetRangeUser( minVal, maxVal );
  promptScaling1->SetTitle( "2005 Data" );
  promptScaling1->Draw("COLZ");

  c1->cd(2);
  promptScaling2->GetXaxis()->SetTitle( "Theta [deg]" );
  promptScaling2->GetYaxis()->SetTitle( "Lambda [nm]" );
  promptScaling2->GetZaxis()->SetTitle( "Prompt Scaling [%]" );
  promptScaling2->GetZaxis()->SetRangeUser( minVal, maxVal );
  promptScaling2->SetTitle( "Jan 2002 Data" );
  promptScaling2->Draw("COLZ");

  c1->cd(3);
  promptScaling3->GetXaxis()->SetTitle( "Theta [deg]" );
  promptScaling3->GetYaxis()->SetTitle( "Lambda [nm]" );
  promptScaling3->GetZaxis()->SetTitle( "Prompt Scaling [%]" );
  promptScaling3->GetZaxis()->SetRangeUser( minVal, maxVal );
  promptScaling3->SetTitle( "Mar 2003 Data" );
  promptScaling3->Draw("COLZ");

  c1->cd(4);
  promptScaling4->GetXaxis()->SetTitle( "Theta [deg]" );
  promptScaling4->GetYaxis()->SetTitle( "Lambda [nm]" );
  promptScaling4->GetZaxis()->SetTitle( "Prompt Scaling [%]" );
  promptScaling4->GetZaxis()->SetRangeUser( minVal, maxVal );
  promptScaling4->SetTitle( "Apr 2006 Data" );
  promptScaling4->Draw("COLZ");
  
  c1->cd();
}
