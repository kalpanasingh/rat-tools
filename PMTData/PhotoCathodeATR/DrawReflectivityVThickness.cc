////////////////////////////////////////////////////////
/// Draw the reflectivity of the photocathode as a function
/// of the thickness
///
/// 27/02/11 - New file
////////////////////////////////////////////////////////

#include "ATRFunctions.hh"

#include "TH1D.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TStyle.h"
#include "TLegend.h"
using namespace ROOT;

#include "PCNK1.hh"
#include "PCNK2.hh"
#include "PCNK3.hh"

#include <iostream>
using namespace std;

void
DrawReflectivityVThickness(
			   int nkSet = 0 )
{
  TH1D* reflVThickS = new TH1D( "ReflVThickS", "Reflectivity V Thickness S pol", 30, 1, 31.0 );
  TH1D* reflVThickP = new TH1D( "ReflVThickP", "Reflectivity V Thickness P pol", 30, 1, 31.0 );

  for( int iThick = 1; iThick <= 31; iThick++ )
    {
      double energy = 299792458 * 4.13566733e-15 * 1e9 / 500.0;
      double lN1 = 1.49; // Glass
      double lN3 = 1.0; // Vacuum
      complex<double> lN2;
      if( nkSet == 0 )
	lN2 = complex<double>( GetPCN1( energy ), GetPCK1( energy ) );
      else if( nkSet == 1 )
	lN2 = complex<double>( GetPCN2( energy ), GetPCK2( energy ) );
      else if( nkSet == 2 )
	lN2 = complex<double>( GetPCN3( energy ), GetPCK3( energy ) );

      double thetaRad = 0.0;
      double thick = reflVThickS->GetXaxis()->GetBinCenter( iThick );
      double Rs, Rp, Ts, Tp;
      CalculateTRThinFilm( thetaRad, lN1, lN2, lN3, energy, thick, Ts, Tp, Rs, Rp );

      reflVThickS->SetBinContent( iThick, Rs );
      reflVThickP->SetBinContent( iThick, Rp );
    }

  TCanvas* c1 = new TCanvas();
  reflVThickS->SetStats(0);
  reflVThickS->GetXaxis()->SetTitle( "Thickness [nm]" );
  reflVThickS->GetYaxis()->SetTitle( "Reflectivity [%]" );
  reflVThickS->Draw();
  reflVThickP->SetStats(0);
  reflVThickP->SetLineColor( kRed );
  reflVThickP->Draw("SAME");

  TLegend* t1 = new TLegend( 0.7, 0.7, 0.9, 0.9 );
  t1->AddEntry( reflVThickS, "S Polarised", "l" );
  t1->AddEntry( reflVThickP, "P Polarised", "l" );
  t1->Draw();
}
			   
