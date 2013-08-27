////////////////////////////////////////////////////////
/// Overlay the Photocathode NK on the same graph
///
/// 10/08/10 - New file, from the Alu version
///////////////////////////////////////////////////////

#include "TGraph.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TLegend.h"
#include "TGaxis.h"
#include "TStyle.h"
using namespace ROOT;

#include <iostream>
using namespace std;

#include "PCNK1.hh"
#include "PCNK2.hh"
#include "PCNK3.hh"
#include "PCNK4.hh"

void
DrawPhotoCathodeNK()
{
  gStyle->SetTitleSize( 0.06, "xyz" );
  gStyle->SetTitleOffset( 1.2, "y" );
  gStyle->SetLabelSize( 0.06, "xyz" );
  gStyle->SetTitleSize( 0.06, "xyz" );

  TGraph* PCN1 = new TGraph();
  TGraph* PCK1 = new TGraph();
  TGraph* PCN2 = new TGraph();
  TGraph* PCK2 = new TGraph();
  TGraph* PCN3 = new TGraph();
  TGraph* PCK3 = new TGraph();
  TGraph* PCN4 = new TGraph();
  TGraph* PCK4 = new TGraph();

  int graphPoint = 0;
  double wavelength;
  for( wavelength = 100.0; wavelength <= 800.0; wavelength += 20.0 )
    {
      double energy = 299792458 * 4.13566733e-15 * 1e9 / wavelength;
      
      PCN1->SetPoint( graphPoint, wavelength, GetPCN1( energy ) );
      PCK1->SetPoint( graphPoint, wavelength, GetPCK1( energy ) );
      PCN2->SetPoint( graphPoint, wavelength, GetPCN2( energy ) );
      PCK2->SetPoint( graphPoint, wavelength, GetPCK2( energy ) );
      PCN3->SetPoint( graphPoint, wavelength, GetPCN3( energy ) );
      PCK3->SetPoint( graphPoint, wavelength, GetPCK3( energy ) );      
      PCN4->SetPoint( graphPoint, wavelength, GetPCN4( energy ) );
      PCK4->SetPoint( graphPoint, wavelength, GetPCK4( energy ) );
      graphPoint++;
      cout << wavelength << "\t" << GetPCN1( energy ) << "\t" << GetPCK1( energy ) << endl;
    }

  const int kMSize = 1;
  const int kMStyle = 8;

  TCanvas* c1 = new TCanvas();
  c1->Divide( 2, 1 );

  c1->cd(1);
  
  PCN1->Draw( "AL" );
  PCN1->SetMarkerSize( kMSize );
  PCN1->SetMarkerStyle( kMStyle );
  PCN1->GetXaxis()->SetTitle( "Wavelength [nm]" );
  PCN1->GetYaxis()->SetTitle( "N [a.u.]" );
  PCN1->SetTitle( "PhotoCathode N" );
  PCN1->GetXaxis()->SetRangeUser( 90.0, 810.0 );
  PCN1->GetYaxis()->SetRangeUser( 0.0, 4.0 );
  PCN2->SetMarkerSize( kMSize );
  PCN2->SetMarkerStyle( kMStyle );
  PCN3->SetMarkerSize( kMSize );
  PCN3->SetMarkerStyle( kMStyle );
  PCN2->SetLineColor( kRed );
  PCN3->SetLineColor( kBlue );
  //  PCN2->Draw( "L" );
  PCN3->Draw( "L" );
  PCN4->SetLineColor( kGreen + 3 );
  PCN4->Draw( "L" );

  TGaxis* energyAxis1 = new TGaxis( 810.0, 4.0, 90.0, 4.0, 1.53, 13.78, 510, "+" );
  energyAxis1->SetTitle( "Energy [eV]" );
  energyAxis1->SetTitleOffset( 0.4 );
  energyAxis1->SetLabelOffset( -0.02 );
  //energyAxis1->Draw();

  TLegend* legend1 = new TLegend( 0.45, 0.15, 0.9, 0.3 );
  legend1->SetHeader( "Legend" );
  legend1->AddEntry( PCN1, "Lay", "L" );
  //legend1->AddEntry( PCN2, "Optics0, RAT attempt", "L" );
  legend1->AddEntry( PCN3, "D.Motta & S. Schonert", "L" );  
  legend1->AddEntry( PCN4, "Lay Interpolated", "L" );
  legend1->SetFillColor( kWhite );
  legend1->Draw();

  c1->cd(2);

  PCK1->Draw( "AL" );
  PCK1->SetMarkerSize( kMSize );
  PCK1->SetMarkerStyle( kMStyle );
  PCK1->GetXaxis()->SetTitle( "Wavelength [nm]" );
  PCK1->GetYaxis()->SetTitle( "K [a.u.]" );
  PCK1->SetTitle( "PhotoCathode K" );
  PCN1->GetXaxis()->SetRangeUser( 90.0, 810.0 );
  PCK1->GetYaxis()->SetRangeUser( 0.0, 3.0 );
  PCK2->SetMarkerSize( kMSize );
  PCK2->SetMarkerStyle( kMStyle );
  PCK3->SetMarkerSize( kMSize );
  PCK3->SetMarkerStyle( kMStyle );
  PCK2->SetLineColor( kRed );
  PCK3->SetLineColor( kBlue );
  //PCK2->Draw( "L" );
  PCK3->Draw( "L" );
  PCK4->SetLineColor( kGreen + 3 );
  PCK4->Draw( "L" );

  TGaxis* energyAxis2 = new TGaxis( 810.0, 4.0, 90.0, 4.0, 1.53, 13.78, 510, "+" );
  energyAxis2->SetTitle( "Energy [eV]" );
  energyAxis2->SetTitleOffset( 0.4 );
  energyAxis2->SetLabelOffset( -0.02 );
  //energyAxis2->Draw();

  TLegend* legend2 = new TLegend( 0.45, 0.65, 0.9, 0.8 );
  legend2->SetHeader( "Legend" );
  legend2->AddEntry( PCK1, "Lay", "L" );
  //legend2->AddEntry( PCK2, "Optics0, RAT attempt", "L" );
  legend2->AddEntry( PCK3, "D.Motta &\n S. Schonert", "L" );
  legend2->AddEntry( PCK4, "Lay Interpolated", "L" );
  legend2->SetFillColor( kWhite );
  legend2->Draw();

  c1->cd();
}
