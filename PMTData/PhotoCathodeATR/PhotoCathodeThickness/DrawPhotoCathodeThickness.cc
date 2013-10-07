////////////////////////////////////////////////////////
/// Overlay the PMT Photocathode thickness on the same graph
///
/// 05/08/10 - New file
///////////////////////////////////////////////////////

#include "TGraph.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TLegend.h"
#include <TStyle.h>
using namespace ROOT;

#include <iostream>
using namespace std;

#include "PCThick1.hh"
#include "PCThick2.hh"
#include "PCThick3.hh"

void
DrawPhotoCathodeThickness()
{
  gStyle->SetTitleSize( 0.06, "xyz" );
  gStyle->SetTitleOffset( 1.2, "y" );
  gStyle->SetLabelSize( 0.06, "xyz" );
  gStyle->SetTitleSize( 0.06, "xyz" );

  TGraph* pcThickness1 = new TGraph();
  TGraph* pcThickness2 = new TGraph();
  TGraph* pcThickness3 = new TGraph();

  int graphPoint = 0;
  double zPos;
  cout << "Thickness" << endl;
  for( zPos = -25.0; zPos < 76.0; zPos += 5.0 )
    {
      pcThickness1->SetPoint( graphPoint, zPos, GetThickness1( zPos ) );
      pcThickness2->SetPoint( graphPoint, zPos, GetThickness2( zPos ) );
      pcThickness3->SetPoint( graphPoint, zPos, GetThickness3( zPos ) );
      graphPoint++;
    }
  for( zPos = 75.0; zPos >= -26.0; zPos -= 5.0 )
    {
      cout << GetThickness3( zPos )*1e-6 << ", ";
    }
  cout << endl;
  TCanvas* c1 = new TCanvas();

  const int kMSize = 1;
  const int kMStyle = 8;
  
  //pcThickness1->Draw( "AL" );
  pcThickness1->SetMarkerSize( kMSize );
  pcThickness1->SetMarkerStyle( kMStyle );
  pcThickness2->GetXaxis()->SetTitle( "z [mm]" );
  pcThickness2->GetYaxis()->SetTitle( "Thickness [nm]" );
  pcThickness2->SetTitle( "Photocathode Thickness" );
  pcThickness2->SetMarkerSize( kMSize );
  pcThickness2->SetMarkerStyle( kMStyle );
  pcThickness3->SetMarkerSize( kMSize );
  pcThickness3->SetMarkerStyle( kMStyle );
  pcThickness2->SetLineColor( kRed );
  pcThickness3->SetLineColor( kBlue );
  pcThickness2->Draw( "AL" );
  //pcThickness3->Draw( "L" );

  TLegend* legend = new TLegend( 0.1, 0.7, 0.3, 0.9 );
  legend->SetHeader( "Legend" );
  legend->AddEntry( pcThickness1, "Lay", "L" );
  legend->AddEntry( pcThickness2, "Optics6b", "L" );
  //legend->AddEntry( pcThickness3, "Theorectical", "L" );
  legend->SetFillColor( kWhite );
  //legend->Draw();

}
