////////////////////////////////////////////////////////
/// Overlay the Aluminium NK on the same graph
///
/// 09/08/10 - New file
///////////////////////////////////////////////////////

#include "TGraph.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TLegend.h"
#include "TGaxis.h"
#include <TStyle.h>
using namespace ROOT;

#include <iostream>
using namespace std;

#include "AluNK1.hh"
#include "AluNK2.hh"
#include "AluNK3.hh"

void
DrawAluNK()
{
  gStyle->SetTitleSize( 0.06, "xyz" );
  gStyle->SetTitleOffset( 1.2, "y" );
  gStyle->SetLabelSize( 0.06, "xyz" );
  gStyle->SetTitleSize( 0.06, "xyz" );

  TGraph* AluN1 = new TGraph();
  TGraph* AluK1 = new TGraph();
  TGraph* AluN2 = new TGraph();
  TGraph* AluK2 = new TGraph();
  TGraph* AluN3 = new TGraph();
  TGraph* AluK3 = new TGraph();

  int graphPoint = 0;
  double wavelength;
  for( wavelength = 100.0; wavelength <= 800.0; wavelength += 100.0 )
    {
      double energy = 299792458 * 4.13566733e-15 * 1e9 / wavelength;
      
      AluN1->SetPoint( graphPoint, wavelength, GetAluN1( energy ) );
      AluK1->SetPoint( graphPoint, wavelength, GetAluK1( energy ) );
      AluN2->SetPoint( graphPoint, wavelength, GetAluN2( energy ) );
      AluK2->SetPoint( graphPoint, wavelength, GetAluK2( energy ) );
      AluN3->SetPoint( graphPoint, wavelength, GetAluN3( energy ) );
      AluK3->SetPoint( graphPoint, wavelength, GetAluK3( energy ) );
      graphPoint++;
    }

  const int kMSize = 1;
  const int kMStyle = 8;

  TCanvas* c1 = new TCanvas();
  c1->Divide( 2, 1 );

  c1->cd(1);
  
  //AluN1->Draw( "AL" );
  AluN1->SetMarkerSize( kMSize );
  AluN1->SetMarkerStyle( kMStyle );
  AluN3->GetXaxis()->SetTitle( "Wavelength [nm]" );
  AluN3->GetYaxis()->SetTitle( "N [a.u.]" );
  AluN3->SetTitle( "Aluminium N" );
  AluN3->GetXaxis()->SetRangeUser( 90.0, 810.0 );
  AluN3->GetYaxis()->SetRangeUser( 0.0, 3.0 );
  AluN2->SetMarkerSize( kMSize );
  AluN2->SetMarkerStyle( kMStyle );
  AluN3->SetMarkerSize( kMSize );
  AluN3->SetMarkerStyle( kMStyle );
  AluN2->SetLineColor( kRed );
  AluN3->SetLineColor( kBlue );
  //AluN2->Draw( "L" );
  AluN3->Draw( "AL" );

  TGaxis* energyAxis1 = new TGaxis( 810.0, 3.0, 90.0, 3.0, 1.53, 13.78, 510, "+" );
  energyAxis1->SetTitle( "Energy [eV]" );
  energyAxis1->SetTitleOffset( 0.4 );
  energyAxis1->SetLabelOffset( -0.02 );
  //energyAxis1->Draw();

  TLegend* legend1 = new TLegend( 0.15, 0.4, 0.35, 0.6 );
  legend1->SetHeader( "Legend" );
  legend1->AddEntry( AluN1, "SNOMAN", "L" );
  legend1->AddEntry( AluN2, "Lay", "L" );
  legend1->AddEntry( AluN3, "Data*", "L" );
  legend1->SetFillColor( kWhite );
  //legend1->Draw();

  c1->cd(2);

  //AluK1->Draw( "AL" );
  AluK1->SetMarkerSize( kMSize );
  AluK1->SetMarkerStyle( kMStyle );
  AluK3->GetXaxis()->SetTitle( "Wavelength [nm]" );
  AluK3->GetYaxis()->SetTitle( "K [a.u.]" );
  AluK3->SetTitle( "Aluminium K" );
  AluK3->GetXaxis()->SetRangeUser( 90.0, 810.0 );
  AluK3->GetYaxis()->SetRangeUser( 0.0, 9.0 );
  AluK2->SetMarkerSize( kMSize );
  AluK2->SetMarkerStyle( kMStyle );
  AluK3->SetMarkerSize( kMSize );
  AluK3->SetMarkerStyle( kMStyle );
  AluK2->SetLineColor( kRed );
  AluK3->SetLineColor( kBlue );
  //AluK2->Draw( "L" );
  AluK3->Draw( "AL" );

  TGaxis* energyAxis2 = new TGaxis( 810.0, 9.0, 90.0, 9.0, 1.53, 13.78, 510, "+" );
  energyAxis2->SetTitle( "Energy [eV]" );
  energyAxis2->SetTitleOffset( 0.4 );
  energyAxis2->SetLabelOffset( -0.02 );
  //energyAxis2->Draw();

  TLegend* legend2 = new TLegend( 0.7, 0.15, 0.9, 0.35 );
  legend2->SetHeader( "Legend" );
  legend2->AddEntry( AluK1, "SNOMAN", "L" );
  legend2->AddEntry( AluK2, "Lay", "L" );
  legend2->AddEntry( AluK3, "Data*", "L" );
  legend2->SetFillColor( kWhite );
  //legend2->Draw();

  c1->cd();
}
