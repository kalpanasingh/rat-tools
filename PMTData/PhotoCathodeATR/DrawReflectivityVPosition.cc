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
#include "PCThick1.hh"
#include "PCThick2.hh"
#include "PCThick3.hh"

#include <iostream>
using namespace std;

void
DrawReflectivityVPosition(
			  int nkSet = 0 )
{
  TH1D* reflVPosS1 = new TH1D( "ReflVPosS1", "Reflectivity V Position S pol", 90, -25.0, 75.0 );
  TH1D* reflVPosP1 = new TH1D( "ReflVPosP1", "Reflectivity V Position P pol", 90, -25.0, 75.0 );
  TH1D* reflVPosS2 = new TH1D( "ReflVPosS2", "Reflectivity V Position S pol", 90, -25.0, 75.0 );
  TH1D* reflVPosP2 = new TH1D( "ReflVPosP2", "Reflectivity V Position P pol", 90, -25.0, 75.0 );
  TH1D* reflVPosS3 = new TH1D( "ReflVPosS3", "Reflectivity V Position S pol", 90, -25.0, 75.0 );
  TH1D* reflVPosP3 = new TH1D( "ReflVPosP3", "Reflectivity V Position P pol", 90, -25.0, 75.0 );


  for( int iPos = 1; iPos <= 90; iPos++ )
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

      double thick;
      double thetaRad = 0.0;
      double Rs, Rp, Ts, Tp;

      double pos = reflVPosS1->GetXaxis()->GetBinCenter( iPos );
      thick = GetThickness1( pos );
      CalculateTRThinFilm( thetaRad, lN1, lN2, lN3, energy, thick, Ts, Tp, Rs, Rp );
      reflVPosS1->SetBinContent( iPos, Rs );
      reflVPosP1->SetBinContent( iPos, Rp );

      thick = GetThickness2( pos );
      CalculateTRThinFilm( thetaRad, lN1, lN2, lN3, energy, thick, Ts, Tp, Rs, Rp );
      reflVPosS2->SetBinContent( iPos, Rs );
      reflVPosP2->SetBinContent( iPos, Rp );

      thick = GetThickness3( pos );
      CalculateTRThinFilm( thetaRad, lN1, lN2, lN3, energy, thick, Ts, Tp, Rs, Rp );
      reflVPosS3->SetBinContent( iPos, Rs );
      reflVPosP3->SetBinContent( iPos, Rp );
    }

  TCanvas* c1 = new TCanvas();
  reflVPosS1->SetStats(0);
  reflVPosS1->GetXaxis()->SetTitle( "Position [nm]" );
  reflVPosS1->GetYaxis()->SetTitle( "Reflectivity [%]" );
  reflVPosS1->Draw();
  reflVPosS2->SetLineColor( kRed );
  reflVPosS2->Draw("SAME");
  reflVPosS3->SetLineColor( kBlue );
  reflVPosS3->Draw("SAME");
  

  TLegend* t1 = new TLegend( 0.7, 0.7, 0.9, 0.9 );
  t1->AddEntry( reflVPosS1, "Thick Set 1", "l" );
  t1->AddEntry( reflVPosS2, "Thick Set 2", "l" );
  t1->AddEntry( reflVPosS3, "Thick Set 3", "l" );
  t1->Draw();
}
			   
