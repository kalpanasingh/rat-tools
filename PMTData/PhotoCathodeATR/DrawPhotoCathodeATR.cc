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

#include "PCNK1.hh"
#include "PCNK2.hh"
#include "PCNK3.hh"
#include "PCThick1.hh"
#include "PCThick2.hh"
#include "PCThick3.hh"

#include <PHILCalcFunctions.hh>
#include "ATRFunctions.hh"

void
DrawPhotoCathodeATR(
		    int nkSet = 0,
		    int thickSet = 0 )
{
  const int thetaBins = 91; const double thetaLow = 0.0; const double thetaHigh = 90.0;
  const int lambdaBins = 12; const double lambdaLow = 200.0; const double lambdaHigh = 800.0;
  
  TH2D* thetaVlambdaVTPTop = new TH2D( "thetaVlambdaVTPTop", "T P Polarised, Top Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVTSTop = new TH2D( "thetaVlambdaVTSTop", "T S Polarised, Top Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVTPTS = new TH2D( "thetaVlambdaVTPTS", "T P Polarised, S-T transition Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVTSTS = new TH2D( "thetaVlambdaVTSTS", "T S Polarised, S-T transition Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVTPEq = new TH2D( "thetaVlambdaVTPEq", "T P Polarised, Equator Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVTSEq = new TH2D( "thetaVlambdaVTSEq", "T S Polarised, Equator Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVTPBot = new TH2D( "thetaVlambdaVTPBot", "T P Polarised, Bottom Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVTSBot = new TH2D( "thetaVlambdaVTSBot", "T S Polarised, Bottom Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );

  TH2D* thetaVlambdaVRPTop = new TH2D( "thetaVlambdaVRPTop", "R P Polarised, Top Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVRSTop = new TH2D( "thetaVlambdaVRSTop", "R S Polarised, Top Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVRPTS = new TH2D( "thetaVlambdaVRPTS", "R P Polarised, S-T transition Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVRSTS = new TH2D( "thetaVlambdaVRSTS", "R S Polarised, S-T transition Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVRPEq = new TH2D( "thetaVlambdaVRPEq", "R P Polarised, Equator Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVRSEq = new TH2D( "thetaVlambdaVRSEq", "R S Polarised, Equator Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVRPBot = new TH2D( "thetaVlambdaVRPBot", "R P Polarised, Bottom Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* thetaVlambdaVRSBot = new TH2D( "thetaVlambdaVRSBot", "R S Polarised, Bottom Z", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );

  double theta;
  for( theta = 0.0; theta < 91.0; theta += 1.0 )
    {
      double wavelength;
      for( wavelength = 200.0; wavelength <= 800.0; wavelength += 50.0 )
	{
	  double thetaRad = theta / 180.0 * PHIL::kPI;
	  double energy = 299792458 * 4.13566733e-15 * 1e9 / wavelength;
	  double lN1 = 1.49; // Glass
	  double lN3 = 1.0; // Vacuum
	  complex<double> lN2;
	  if( nkSet == 0 )
	    lN2 = complex<double>( GetPCN1( energy ), GetPCK1( energy ) );
	  else if( nkSet == 1 )
	    lN2 = complex<double>( GetPCN2( energy ), GetPCK2( energy ) );
	  else if( nkSet == 2 )
	    lN2 = complex<double>( GetPCN3( energy ), GetPCK3( energy ) );
	  
	  double topThick, stThick, eqThick, botThick;
	  if( thickSet == 0 )
	    {
	      topThick = GetThickness1( 73.5 ); stThick = GetThickness1( 45.0 ); eqThick = GetThickness1( 0.0 ); botThick = GetThickness1( -25.0 );
	    }
	  else if( thickSet == 1 )
	    {
	      topThick = GetThickness2( 73.5 ); stThick = GetThickness2( 45.0 ); eqThick = GetThickness2( 0.0 ); botThick = GetThickness2( -25.0 );
	    }
	  else if( thickSet == 2 )
	    {
	      topThick = GetThickness3( 73.5 ); stThick = GetThickness3( 45.0 ); eqThick = GetThickness3( 0.0 ); botThick = GetThickness3( -25.0 );
	    }
	  
	  double Rs, Rp, Ts, Tp;
	  CalculateTRThinFilm( thetaRad, lN1, lN2, lN3, energy, topThick, Ts, Tp, Rs, Rp );
	  thetaVlambdaVTPTop->Fill( theta, wavelength, Tp );
	  thetaVlambdaVTSTop->Fill( theta, wavelength, Ts );
	  thetaVlambdaVRPTop->Fill( theta, wavelength, Rp );
	  thetaVlambdaVRSTop->Fill( theta, wavelength, Rs );

	  CalculateTRThinFilm( thetaRad, lN1, lN2, lN3, energy, stThick, Ts, Tp, Rs, Rp );
	  thetaVlambdaVTPTS->Fill( theta, wavelength, Tp );
	  thetaVlambdaVTSTS->Fill( theta, wavelength, Ts );
	  thetaVlambdaVRPTS->Fill( theta, wavelength, Rp );
	  thetaVlambdaVRSTS->Fill( theta, wavelength, Rs ); 

	  CalculateTRThinFilm( thetaRad, lN1, lN2, lN3, energy, eqThick, Ts, Tp, Rs, Rp );
	  thetaVlambdaVTPEq->Fill( theta, wavelength, Tp );
	  thetaVlambdaVTSEq->Fill( theta, wavelength, Ts );
	  thetaVlambdaVRPEq->Fill( theta, wavelength, Rp );
	  thetaVlambdaVRSEq->Fill( theta, wavelength, Rs );

	  CalculateTRThinFilm( thetaRad, lN1, lN2, lN3, energy, botThick, Ts, Tp, Rs, Rp );
	  thetaVlambdaVTPBot->Fill( theta, wavelength, Tp );
	  thetaVlambdaVTSBot->Fill( theta, wavelength, Ts );
	  thetaVlambdaVRPBot->Fill( theta, wavelength, Rp );
	  thetaVlambdaVRSBot->Fill( theta, wavelength, Rs );
	}
    }
  
  gStyle->SetOptStat(0);

  gStyle->SetPalette(1);
  TCanvas* c1 = new TCanvas();
  c1->Divide( 2, 4 );

  c1->cd(1);
  thetaVlambdaVTPTop->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVTPTop->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVTPTop->GetZaxis()->SetTitle( "T [%]" );
  thetaVlambdaVTPTop->SetTitle( "P Polarised Transmission, at z=73.5mm" );
  thetaVlambdaVTPTop->Draw("COLZ");

  c1->cd(2);
  thetaVlambdaVTSTop->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVTSTop->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVTSTop->GetZaxis()->SetTitle( "T [%]" );
  thetaVlambdaVTSTop->SetTitle( "S Polarised Transmission, at z=73.5mm" );
  thetaVlambdaVTSTop->Draw("COLZ");

  c1->cd(3);
  thetaVlambdaVTPTS->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVTPTS->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVTPTS->GetZaxis()->SetTitle( "T [%]" );
  thetaVlambdaVTPTS->SetTitle( "P Polarised Transmission, at z=45.0mm" );
  thetaVlambdaVTPTS->Draw("COLZ");

  c1->cd(4);
  thetaVlambdaVTSTS->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVTSTS->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVTSTS->GetZaxis()->SetTitle( "T [%]" );
  thetaVlambdaVTSTS->SetTitle( "S Polarised Transmission, at z=45.0mm" );
  thetaVlambdaVTSTS->Draw("COLZ");

  c1->cd(5);
  thetaVlambdaVTPEq->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVTPEq->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVTPEq->GetZaxis()->SetTitle( "T [%]" );
  thetaVlambdaVTPEq->SetTitle( "P Polarised Transmission, at z=0.0mm" );
  thetaVlambdaVTPEq->Draw("COLZ");

  c1->cd(6);
  thetaVlambdaVTSEq->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVTSEq->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVTSEq->GetZaxis()->SetTitle( "T [%]" );
  thetaVlambdaVTSEq->SetTitle( "S Polarised Transmission, at z=0.0mm" );
  thetaVlambdaVTSEq->Draw("COLZ");

  c1->cd(7);
  thetaVlambdaVTPBot->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVTPBot->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVTPBot->GetZaxis()->SetTitle( "T [%]" );
  thetaVlambdaVTPBot->SetTitle( "P Polarised Transmission, at z=-25.0mm" );
  thetaVlambdaVTPBot->Draw("COLZ");

  c1->cd(8);
  thetaVlambdaVTSBot->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVTSBot->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVTSBot->GetZaxis()->SetTitle( "T [%]" );
  thetaVlambdaVTSBot->SetTitle( "S Polarised Transmission, at z=-25.0mm" );
  thetaVlambdaVTSBot->Draw("COLZ");

  c1->cd();

  TCanvas* c2 = new TCanvas();
  c2->Divide( 2, 4 );

  c2->cd(1);
  thetaVlambdaVRPTop->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVRPTop->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVRPTop->GetZaxis()->SetTitle( "R [%]" );
  thetaVlambdaVRPTop->SetTitle( "P Polarised Reflectance, at z=73.5mm" );
  thetaVlambdaVRPTop->Draw("COLZ");

  c2->cd(2);
  thetaVlambdaVRSTop->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVRSTop->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVRSTop->GetZaxis()->SetTitle( "R [%]" );
  thetaVlambdaVRSTop->SetTitle( "S Polarised Reflectance, at z=73.5mm" );
  thetaVlambdaVRSTop->Draw("COLZ");

  c2->cd(3);
  thetaVlambdaVRPTS->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVRPTS->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVRPTS->GetZaxis()->SetTitle( "R [%]" );
  thetaVlambdaVRPTS->SetTitle( "P Polarised Reflectance, at z=45.0mm" );
  thetaVlambdaVRPTS->Draw("COLZ");

  c2->cd(4);
  thetaVlambdaVRSTS->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVRSTS->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVRSTS->GetZaxis()->SetTitle( "R [%]" );
  thetaVlambdaVRSTS->SetTitle( "S Polarised Reflectance, at z=45.0mm" );
  thetaVlambdaVRSTS->Draw("COLZ");

  c2->cd(5);
  thetaVlambdaVRPEq->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVRPEq->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVRPEq->GetZaxis()->SetTitle( "R [%]" );
  thetaVlambdaVRPEq->SetTitle( "P Polarised Reflectance, at z=0.0mm" );
  thetaVlambdaVRPEq->Draw("COLZ");

  c2->cd(6);
  thetaVlambdaVRSEq->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVRSEq->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVRSEq->GetZaxis()->SetTitle( "R [%]" );
  thetaVlambdaVRSEq->SetTitle( "S Polarised Reflectance, at z=0.0mm" );
  thetaVlambdaVRSEq->Draw("COLZ");

  c2->cd(7);
  thetaVlambdaVRPBot->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVRPBot->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVRPBot->GetZaxis()->SetTitle( "R [%]" );
  thetaVlambdaVRPBot->SetTitle( "P Polarised Reflectance, at z=-25.0mm" );
  thetaVlambdaVRPBot->Draw("COLZ");

  c2->cd(8);
  thetaVlambdaVRSBot->GetXaxis()->SetTitle( "Theta [deg]" );
  thetaVlambdaVRSBot->GetYaxis()->SetTitle( "Lambda [nm]" );
  thetaVlambdaVRSBot->GetZaxis()->SetTitle( "R [%]" );
  thetaVlambdaVRSBot->SetTitle( "S Polarised Reflectance, at z=-25.0mm" );
  thetaVlambdaVRSBot->Draw("COLZ");

  c2->cd();
}
