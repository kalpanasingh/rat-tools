////////////////////////////////////////////////////////
/// Draw the reflectivity times prompt ratio i.e. Net.
/// NEEDS FIXING, as prompt angle != omega angle, prompt is angle to bucket
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

#include "Omega1.hh"
#include "Omega2.hh"
#include "Prompt1.hh"
#include "Prompt2.hh"
#include "Prompt3.hh"
#include "Prompt4.hh"

void
DrawOmegaNetReflectivity(
		      int pro1 = 0,
		      int pro2 = 3 )
{
  const int thetaBins = 91; const double thetaLow = 0.0; const double thetaHigh = 90.0;
  const int lambdaBins = 50; const double lambdaLow = 300.0; const double lambdaHigh = 800.0;
  TH2D* thetaVlambdaVOmega1P = new TH2D( "thetaVlambdaVOmega1P", "1994 P Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVOmega1S = new TH2D( "thetaVlambdaVOmega1S", "1994 S Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVOmega2P = new TH2D( "thetaVlambdaVOmega2P", "2003 P Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVOmega2S = new TH2D( "thetaVlambdaVOmega2S", "2003 S Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* promptScaling1 = new TH2D( "promptScaling1", "2005 Data", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* promptScaling2 = new TH2D( "promptScaling2", "Jan 2002 Data", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* promptScaling3 = new TH2D( "promptScaling3", "Mar 2003 Data", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* promptScaling4 = new TH2D( "promptScaling4", "Apr 2006 Data", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );

  int iLoop;
  for( iLoop = 0; iLoop < 91; iLoop++ )
    {
      int iLoop2;
      for( iLoop2 = 310; iLoop2 < 800; iLoop2+=10 )
	{
	  int omegaPoint = iLoop + ( iLoop2 - 305 ) * 91;
	  thetaVlambdaVOmega1P->Fill( (double)iLoop, (double)iLoop2, Omega1P[omegaPoint] );
	  thetaVlambdaVOmega1S->Fill( (double)iLoop, (double)iLoop2, Omega1S[omegaPoint] );
	  thetaVlambdaVOmega2P->Fill( (double)iLoop, (double)iLoop2, Omega2P[omegaPoint] );
	  thetaVlambdaVOmega2S->Fill( (double)iLoop, (double)iLoop2, Omega2S[omegaPoint] );
	}
    }
  for( iLoop = 0; iLoop < 91; iLoop++ )
    {
      int iLoop2;
      for( iLoop2 = 23; iLoop2 < 71; iLoop2++ )
	{
	  int omegaPoint = iLoop + ( iLoop2 - 23 ) * 91;
	  double promptVal = normalisation1 / ( 1.0 + Prompt1[omegaPoint] * ( 1.0 - normalisation1 ) );
	  promptScaling1->Fill( (double)iLoop, (double)iLoop2 * 10.0, promptVal );

	  promptVal = normalisation2 / ( 1.0 + Prompt2[omegaPoint] * ( 1.0 - normalisation2 ) );
	  promptScaling2->Fill( (double)iLoop, (double)iLoop2 * 10.0, promptVal );

	  promptVal = normalisation3 / ( 1.0 + Prompt3[omegaPoint] * ( 1.0 - normalisation3 ) );
	  promptScaling3->Fill( (double)iLoop, (double)iLoop2 * 10.0, promptVal );

	  promptVal = normalisation4 / ( 1.0 + Prompt4[omegaPoint] * ( 1.0 - normalisation4 ) );
	  promptScaling4->Fill( (double)iLoop, (double)iLoop2 * 10.0, promptVal );
	}
    }

  gStyle->SetOptStat(0);

  gStyle->SetPalette(1);
  TCanvas* c1 = new TCanvas();
  c1->Divide( 2, 2 );

  if( pro1 == 0 )
    {
      thetaVlambdaVOmega1P->Multiply( promptScaling1 );
      thetaVlambdaVOmega1S->Multiply( promptScaling1 );
    }
  else if( pro1 == 1 )
    {
      thetaVlambdaVOmega1P->Multiply( promptScaling2 );
      thetaVlambdaVOmega1S->Multiply( promptScaling2 );
    }
  else if( pro1 == 2 )
    {
      thetaVlambdaVOmega1P->Multiply( promptScaling3 );
      thetaVlambdaVOmega1S->Multiply( promptScaling3 );
    }
  else if( pro1 == 3 )
    {
      thetaVlambdaVOmega1P->Multiply( promptScaling4 );
      thetaVlambdaVOmega1S->Multiply( promptScaling4 );
    }

  c1->cd(1);
  thetaVlambdaVOmega1P->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVOmega1P->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVOmega1P->GetZaxis()->SetTitle( "Omega [%]" );
  thetaVlambdaVOmega1P->SetTitle( "1994 Data, P Polarised" );
  thetaVlambdaVOmega1P->Draw("COLZ");

  c1->cd(2);
  thetaVlambdaVOmega1S->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVOmega1S->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVOmega1S->GetZaxis()->SetTitle( "Omega [%]" );
  thetaVlambdaVOmega1S->SetTitle( "1994 Data, S Polarised" );
  thetaVlambdaVOmega1S->Draw("COLZ");


  if( pro2 == 0 )
    {
      thetaVlambdaVOmega2P->Multiply( promptScaling1 );
      thetaVlambdaVOmega2S->Multiply( promptScaling1 );
    }
  else if( pro2 == 1 )
    {
      thetaVlambdaVOmega2P->Multiply( promptScaling2 );
      thetaVlambdaVOmega2S->Multiply( promptScaling2 );
    }
  else if( pro2 == 2 )
    {
      thetaVlambdaVOmega2P->Multiply( promptScaling3 );
      thetaVlambdaVOmega2S->Multiply( promptScaling3 );
    }
  else if( pro2 == 3 )
    {
      thetaVlambdaVOmega2P->Multiply( promptScaling4 );
      thetaVlambdaVOmega2S->Multiply( promptScaling4 );
    }

  c1->cd(3);
  thetaVlambdaVOmega2P->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVOmega2P->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVOmega2P->GetZaxis()->SetTitle( "Omega [%]" );
  thetaVlambdaVOmega2P->SetTitle( "2003 Data, P Polarised" );
  thetaVlambdaVOmega2P->Draw("COLZ");

  c1->cd(4);
  thetaVlambdaVOmega2S->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVOmega2S->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVOmega2S->GetZaxis()->SetTitle( "Omega [%]" );
  thetaVlambdaVOmega2S->SetTitle( "2003 Data, S Polarised" );
  thetaVlambdaVOmega2S->Draw("COLZ");
  
  c1->cd();
}
