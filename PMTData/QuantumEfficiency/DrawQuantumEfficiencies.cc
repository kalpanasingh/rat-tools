////////////////////////////////////////////////////////
/// Overlay the PMT Photocathode QE on the same graph
///
/// 21/07/10 - New file
///////////////////////////////////////////////////////

#include "TGraph.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TLegend.h"
#include <TStyle.h>
using namespace ROOT;

#include "PCResponse1.hh"
#include "PCResponse2.hh"
#include "PCResponse3.hh"

void
DrawQuantumEfficiencies()
{
  gStyle->SetTitleSize( 0.06, "xyz" );
  gStyle->SetTitleOffset( 1.2, "y" );
  gStyle->SetLabelSize( 0.06, "xyz" );
  gStyle->SetTitleSize( 0.06, "xyz" );

  const int numPoints = 700 - 230;
  double wavelengths[numPoints];

  int iLoop;
  for( iLoop = 0; iLoop < numPoints; iLoop++ )
    wavelengths[iLoop] = iLoop + 230;

  TGraph* response1 = new TGraph( numPoints, wavelengths, PCResponse1 );
  TGraph* response2 = new TGraph( numPoints, wavelengths, PCResponse2 );
  TGraph* response3 = new TGraph( numPoints, wavelengths, PCResponse3 );

  TCanvas* c1 = new TCanvas();
  TVirtualPad* vc1 = c1->cd();

  const int kMSize = 0;
  const int kMStyle = 2;
  
  response1->SetTitle( "Photocathode Quantum Efficiency" );
  response1->Draw( "ALP" );
  response1->SetMarkerSize( kMSize );
  response1->SetMarkerStyle( kMStyle );
  response1->GetYaxis()->SetRangeUser( 1e-4, 1e0 );
  response1->GetYaxis()->SetTitle( "QE [%]" );
  response1->GetXaxis()->SetTitle( "Wavelength [nm]" );
  response2->SetMarkerSize( kMSize );
  response2->SetMarkerStyle( kMStyle );
  response3->SetMarkerSize( kMSize );
  response3->SetMarkerStyle( kMStyle );
  response2->SetLineColor( kRed );
  response2->SetMarkerColor( kRed );
  response3->SetLineColor( kBlue );
  response3->SetMarkerColor( kBlue );
  //  response2->Draw( "LP" );
  //  response3->Draw( "LP" );
  vc1->SetLogy();
  vc1->SetGridx();
  vc1->SetGridy();

  TLegend* legend = new TLegend( 0.7, 0.7, 0.9, 0.9 );
  legend->SetHeader( "Legend" );
  legend->AddEntry( response1, "1998 QE", "LP" );
  legend->AddEntry( response2, "1994 QE", "LP" );
  legend->AddEntry( response3, "1996 QE", "LP" );
  legend->SetFillColor( kWhite );
  //  legend->Draw();

}
