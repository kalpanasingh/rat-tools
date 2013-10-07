////////////////////////////////////////////////////////
/// Overlay the PMT Photocathode CE on the same graph
///
/// 23/07/10 - New file
///////////////////////////////////////////////////////

#include "TF1.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TLegend.h"
using namespace ROOT;

#include "CollParams1.hh"
#include "CollParams2.hh"
#include "CollParams3.hh"
#include "CollParams4.hh"
#include "CollParams5.hh"
#include "CollParams6.hh"

void
DrawCollectionEfficiencies()
{
  const double lowerBound = 5.09; // In strange units this is pmt equator cm
  const double upperBound = 12.53; // In strange units this is top of pmt front face
  const double apmt_i = 12.33; // 12.53 - 0.3
  TF1* collFunc1 = new TF1( "collFunc1", "([0] - [1] * exp( [3] * (x - [5])^4 )) * exp( [4] * (x - [5])^4 ) + [2]", lowerBound, upperBound );
  TF1* collFunc2 = new TF1( "collFunc2", "([0] - [1] * exp( [3] * (x - [5])^4 )) * exp( [4] * (x - [5])^4 ) + [2]", lowerBound, upperBound );
  TF1* collFunc3 = new TF1( "collFunc3", "([0] - [1] * exp( [3] * (x - [5])^4 )) * exp( [4] * (x - [5])^4 ) + [2]", lowerBound, upperBound );
  TF1* collFunc4 = new TF1( "collFunc4", "([0] - [1] * exp( [3] * (x - [5])^4 )) * exp( [4] * (x - [5])^4 ) + [2]", lowerBound, upperBound );
  TF1* collFunc5 = new TF1( "collFunc5", "([0] - [1] * exp( [3] * (x - [5])^4 )) * exp( [4] * (x - [5])^4 ) + [2]", lowerBound, upperBound );
  TF1* collFunc6 = new TF1( "collFunc6", "([0] - [1] * exp( [3] * (x - [5])^4 )) * exp( [4] * (x - [5])^4 ) + [2]", lowerBound, upperBound );

  collFunc1->SetParameters( a1param1, a2param1, a3param1, b1param1, b2param1, apmt_i );
  collFunc2->SetParameters( a1param2, a2param2, a3param2, b1param2, b2param2, apmt_i );
  collFunc3->SetParameters( a1param3, a2param3, a3param3, b1param3, b2param3, apmt_i );
  collFunc4->SetParameters( a1param4, a2param4, a3param4, b1param4, b2param4, apmt_i );
  collFunc5->SetParameters( a1param5, a2param5, a3param5, b1param5, b2param5, apmt_i );
  collFunc6->SetParameters( a1param6, a2param6, a3param6, b1param6, b2param6, apmt_i );

  TCanvas* c1 = new TCanvas();
  c1->cd();
  
  collFunc1->Draw();
  collFunc1->GetYaxis()->SetRangeUser( 0.5, 1.5 );
  collFunc1->GetYaxis()->SetTitle( "CE [%]" );
  collFunc1->GetXaxis()->SetTitle( " z [cm]" );
  collFunc1->SetTitle( "PC CE" );
  collFunc2->SetLineColor( kRed );
  collFunc2->Draw( "SAME" );
  collFunc3->SetLineColor( kBlue );
  collFunc3->Draw( "SAME" );
  collFunc4->SetLineColor( kGreen );
  collFunc4->Draw( "SAME" );
  collFunc5->SetLineColor( kViolet );
  collFunc5->Draw( "SAME" );
  collFunc6->SetLineColor( kGreen + 2 );
  collFunc6->Draw( "SAME" );

  TLegend* legend = new TLegend( 0.7, 0.7, 0.9, 0.9 );
  legend->SetHeader( "Legend" );
  legend->AddEntry( collFunc1, "2005 CE", "L" );
  legend->AddEntry( collFunc2, "Feb 2006 CE", "L" );
  legend->AddEntry( collFunc3, "Jan 2002 CE", "L" );
  legend->AddEntry( collFunc4, "Mar 2003 CE", "L" );
  legend->AddEntry( collFunc5, "2006 CE", "L" );
  legend->AddEntry( collFunc6, "Mar 2006 CE", "L" );
  legend->SetFillColor( kWhite );
  legend->Draw();

}
