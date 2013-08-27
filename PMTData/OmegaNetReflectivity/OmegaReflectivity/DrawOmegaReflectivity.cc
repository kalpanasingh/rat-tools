////////////////////////////////////////////////////////
/// Overlay the original and newer Omega efficiencies.
///
/// 21/07/10 - New file
/// 22/07/10 - TH2D draws better than TGraph2D
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

void
DrawOmegaReflectivity()
{
  gStyle->SetTitleSize( 0.06, "xyz" );
  gStyle->SetTitleOffset( 1.2, "y" );
  gStyle->SetLabelSize( 0.06, "xyz" );
  gStyle->SetTitleSize( 0.06, "xyz" );

  const int thetaBins = 91; const double thetaLow = 0.0; const double thetaHigh = 90.0;
  const int lambdaBins = 500; const double lambdaLow = 300.0; const double lambdaHigh = 800.0;
  TH2D* thetaVlambdaVOmega1P = new TH2D( "thetaVlambdaVOmega1P", "1994 P Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVOmega1S = new TH2D( "thetaVlambdaVOmega1S", "1994 S Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVOmega2P = new TH2D( "thetaVlambdaVOmega2P", "2003 P Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVOmega2S = new TH2D( "thetaVlambdaVOmega2S", "2003 S Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  //cout << thetaVlambdaVOmega2S->GetXaxis()->GetBinWidth( 3 ) << " " << thetaVlambdaVOmega2S->GetYaxis()->GetBinWidth( 3 ) << endl;
  int iLoop;
  for( iLoop = 0; iLoop < 91; iLoop++ )
    {
      int iLoop2;
      for( iLoop2 = 305; iLoop2 <= 800; iLoop2++ )
	{
	  int omegaPoint = iLoop + ( iLoop2 - 305 ) * 91;
	  thetaVlambdaVOmega1P->Fill( (double)iLoop, (double)iLoop2, Omega1P[omegaPoint] );
	  thetaVlambdaVOmega1S->Fill( (double)iLoop, (double)iLoop2, Omega1S[omegaPoint] );
	  thetaVlambdaVOmega2P->Fill( (double)iLoop, (double)iLoop2, Omega2P[omegaPoint] );
	  thetaVlambdaVOmega2S->Fill( (double)iLoop, (double)iLoop2, Omega2S[omegaPoint] );
	}
    }
  gStyle->SetOptStat(0);

  gStyle->SetPalette(1);
  TCanvas* c1 = new TCanvas();
  c1->Divide( 2, 1 );

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
  return;

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
