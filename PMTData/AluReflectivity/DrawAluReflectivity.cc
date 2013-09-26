////////////////////////////////////////////////////////
/// Draw the reflectivity of the aluminium
///
/// 09/08/10 - New file
///////////////////////////////////////////////////////

#include "TH2D.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TStyle.h"
using namespace ROOT;

#include <iostream>
#include <complex>
using namespace std;

#include "AluNK1.hh"
#include "AluNK2.hh"
#include "AluNK3.hh"

#include <PHILCalcFunctions.hh>

void
GetReflectivity(
                const double lN1,
                const complex<double> lN2,
                const double theta,
                double& Rs,
                double& Rp );

void
DrawAluReflectivity(
		    bool glass = false )
{
  const int thetaBins = 91; const double thetaLow = 0.0; const double thetaHigh = 90.0;
  const int lambdaBins = 12; const double lambdaLow = 200.0; const double lambdaHigh = 800.0;
  TH2D* thetaVlambdaVReflect1P = new TH2D( "thetaVlambdaVReflect1P", "Actual SNOMAN P Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVReflect1S = new TH2D( "thetaVlambdaVReflect1S", "Actual SNOMAN S Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVReflect2P = new TH2D( "thetaVlambdaVReflect2P", "Theory SNOMAN P Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVReflect2S = new TH2D( "thetaVlambdaVReflect2S", "Theory SNOMAN S Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVReflect3P = new TH2D( "thetaVlambdaVReflect3P", "Optics0 (New RAT) P Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVReflect3S = new TH2D( "thetaVlambdaVReflect3S", "Optics0 (New RAT) S Polarised", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );

  double theta;
  for( theta = 0.0; theta < 91.0; theta += 1.0 )
    {
      double wavelength;
      for( wavelength = 200.0; wavelength <= 800.0; wavelength += 50.0 )
	{
	  double thetaRad = theta / 180.0 * PHIL::kPI;
	  double energy = 299792458 * 4.13566733e-15 * 1e9 / wavelength;
	  if( glass == true )
	    {
	      double Rs, Rp;
	      double lN1 = 1.5;
	      complex<double> lN2( GetAluN1( energy ), GetAluK1( energy ) );
	      GetReflectivity( lN1, lN2, thetaRad, Rs, Rp );
	      thetaVlambdaVReflect1P->Fill( theta, wavelength, Rp );
	      thetaVlambdaVReflect1S->Fill( theta, wavelength, Rs );

	      lN2 = complex<double>( GetAluN2( energy ), GetAluK2( energy ) );
	      GetReflectivity( lN1, lN2, thetaRad, Rs, Rp );
              thetaVlambdaVReflect2P->Fill( theta, wavelength, Rp );
              thetaVlambdaVReflect2S->Fill( theta, wavelength, Rs );
	      
	      lN1 = 1.49;
	      lN2 = complex<double>( GetAluN3( energy ), GetAluK3( energy ) );
              GetReflectivity( lN1, lN2, thetaRad, Rs, Rp );
              thetaVlambdaVReflect3P->Fill( theta, wavelength, Rp );
              thetaVlambdaVReflect3S->Fill( theta, wavelength, Rs );
	    }
	  else
	    {
	      double Rs, Rp;
              double lN1 = 1.0;
              complex<double> lN2( GetAluN1( energy ), GetAluK1( energy ) );
              GetReflectivity( lN1, lN2, thetaRad, Rs, Rp );
              thetaVlambdaVReflect1P->Fill( theta, wavelength, Rp );
              thetaVlambdaVReflect1S->Fill( theta, wavelength, Rs );

	      lN2 = complex<double>( GetAluN2( energy ), GetAluK2( energy ) );
              GetReflectivity( lN1, lN2, thetaRad, Rs, Rp );
              thetaVlambdaVReflect2P->Fill( theta, wavelength, Rp );
              thetaVlambdaVReflect2S->Fill( theta, wavelength, Rs );

              lN2 = complex<double>( GetAluN3( energy ), GetAluK3( energy ) );
              GetReflectivity( lN1, lN2, thetaRad, Rs, Rp );
              thetaVlambdaVReflect3P->Fill( theta, wavelength, Rp );
              thetaVlambdaVReflect3S->Fill( theta, wavelength, Rs );
	    }
	}
    }
  
  gStyle->SetOptStat(0);

  gStyle->SetPalette(1);
  TCanvas* c1 = new TCanvas();
  c1->Divide( 2, 3 );

  c1->cd(1);
  thetaVlambdaVReflect1P->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVReflect1P->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVReflect1P->GetZaxis()->SetTitle( "Reflect [%]" );
  thetaVlambdaVReflect1P->SetTitle( "Actual SNOMAN P Polarised" );
  thetaVlambdaVReflect1P->Draw("COLZ");

  c1->cd(2);
  thetaVlambdaVReflect1S->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVReflect1S->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVReflect1S->GetZaxis()->SetTitle( "Reflect [%]" );
  thetaVlambdaVReflect1S->SetTitle( "Actual SNOMAN S Polarised" );
  thetaVlambdaVReflect1S->Draw("COLZ");

  c1->cd(3);
  thetaVlambdaVReflect2P->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVReflect2P->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVReflect2P->GetZaxis()->SetTitle( "Reflect [%]" );
  thetaVlambdaVReflect2P->SetTitle( "Theory SNOMAN P Polarised" );
  thetaVlambdaVReflect2P->Draw("COLZ");

  c1->cd(4);
  thetaVlambdaVReflect2S->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVReflect2S->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVReflect2S->GetZaxis()->SetTitle( "Reflect [%]" );
  thetaVlambdaVReflect2S->SetTitle( "Theory SNOMAN S Polarised" );
  thetaVlambdaVReflect2S->Draw("COLZ");
  
  c1->cd(5);
  thetaVlambdaVReflect3P->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVReflect3P->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVReflect3P->GetZaxis()->SetTitle( "Reflect [%]" );
  thetaVlambdaVReflect3P->SetTitle( "Optics0 (New RAT) P Polarised" );
  thetaVlambdaVReflect3P->Draw("COLZ");

  c1->cd(6);
  thetaVlambdaVReflect3S->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVReflect3S->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVReflect3S->GetZaxis()->SetTitle( "Reflect [%]" );
  thetaVlambdaVReflect3S->SetTitle( "Optics0 (New RAT) S Polarised" );
  thetaVlambdaVReflect3S->Draw("COLZ");

  c1->cd();

  //TH1D* hp = thetaVlambdaVReflect3S->ProjectionX("",thetaVlambdaVReflect3S->GetYaxis()->FindBin(200),1);
  //hp->Draw();
}

void
GetReflectivity(
		const double lN1,
		const complex<double> lN2,
		const double theta,
		double& Rs,
		double& Rp )
{
  double cos1 = cos( theta );
  const double sin1_2 = 1.0 - cos1 * cos1;
  //const complex<double> n12 = lN1 / lN2;
  const complex<double> cos2 = sqrt( complex<double>(1.0,0.0) - ( lN1 / lN2 ) * ( lN1 / lN2 ) * sin1_2 );

  const complex<double> Ds = ( lN2 * cos2 + lN1 * cos1 );
  const complex<double> Dp = ( lN2 * cos1 + lN1 * cos2 );

  const complex<double> Rsc = ( ( lN1 * cos1 - lN2 * cos2 ) / Ds );
  const complex<double> Rpc = ( ( lN1 * cos2 - lN2 * cos1 ) / Dp );
  Rs = abs(Rsc * Rsc);
  Rp = abs(Rpc * Rpc);

  if( Rs > 1.0 || Rp > 1.0 )
    cout << Rs << " " << Rp << endl;
}
