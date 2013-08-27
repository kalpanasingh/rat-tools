////////////////////////////////////////////////////////
/// Overlay the response and timing scans and an average on the same plot
///
/// 09/05/13 - New file
///////////////////////////////////////////////////////

#include <TGraph.h>
#include <TCanvas.h>
#include <TAxis.h>
#include <TLegend.h>
#include <TStyle.h>
using namespace ROOT;

#include <Scan0.hh>
#include <Scan135.hh>
#include <Scan180.hh>
#include <Scan225.hh>
#include <Scan270.hh>
#include <Scan315.hh>
#include <Scan45.hh>
#include <Scan90.hh>

void
DrawScansAndAverage()
{
  gStyle->SetTitleSize( 0.06, "xyz" );
  gStyle->SetTitleOffset( 1.2, "y" );
  gStyle->SetLabelSize( 0.06, "xyz" );
  gStyle->SetTitleSize( 0.06, "xyz" );

  TGraph* gResponse0 = new TGraph( numValues0, radius0, response0 );
  TGraph* gResponse135 = new TGraph( numValues135, radius135, response135 );
  TGraph* gResponse180 = new TGraph( numValues180, radius180, response180 );
  TGraph* gResponse225 = new TGraph( numValues225, radius225, response225 );
  TGraph* gResponse270 = new TGraph( numValues270, radius270, response270 );
  TGraph* gResponse315 = new TGraph( numValues315, radius315, response315 );
  TGraph* gResponse45 = new TGraph( numValues45, radius45, response45 );
  TGraph* gResponse90 = new TGraph( numValues90, radius90, response90 );
  TGraph* gResponseAverage = new TGraph();

  TGraph* gTiming0 = new TGraph( numValues0, radius0, timing0 );
  TGraph* gTiming135 = new TGraph( numValues135, radius135, timing135 );
  TGraph* gTiming180 = new TGraph( numValues180, radius180, timing180 );
  TGraph* gTiming225 = new TGraph( numValues225, radius225, timing225 );
  TGraph* gTiming270 = new TGraph( numValues270, radius270, timing270 );
  TGraph* gTiming315 = new TGraph( numValues315, radius315, timing315 );
  TGraph* gTiming45 = new TGraph( numValues45, radius45, timing45 );
  TGraph* gTiming90 = new TGraph( numValues90, radius90, timing90 );
  TGraph* gTimingAverage = new TGraph();

  int graphPoint = 0;
  for( double radius = 0.0; radius < 105.0; radius+=5.0 )
    {
      const double averageResponse = ( gResponse0->Eval( radius ) + gResponse135->Eval( radius ) + gResponse180->Eval( radius ) + gResponse225->Eval( radius ) + gResponse270->Eval( radius ) + gResponse315->Eval( radius ) + gResponse45->Eval( radius ) + gResponse90->Eval( radius ) ) / 8.0;
      const double averageTiming = ( gTiming0->Eval( radius ) + gTiming135->Eval( radius ) + gTiming180->Eval( radius ) + gTiming225->Eval( radius ) + gTiming270->Eval( radius ) + gTiming315->Eval( radius ) + gTiming45->Eval( radius ) + gTiming90->Eval( radius ) ) / 8.0;
      gResponseAverage->SetPoint( graphPoint, radius, averageResponse );
      gTimingAverage->SetPoint( graphPoint++, radius, averageTiming );
    }

    
  const int kMSize = 0;
  const int kMStyle = 2;
  TCanvas* c1 = new TCanvas();
  {
    TVirtualPad* vc1 = c1->cd();
    
    gResponse0->SetTitle( "Averaged response" );
    gResponse0->SetMarkerSize( kMSize );
    gResponse0->SetMarkerStyle( kMStyle );
    gResponse0->GetYaxis()->SetRangeUser( 0.7, 1.2 );
    gResponse0->GetYaxis()->SetTitle( "Relative response" );
    gResponse0->GetXaxis()->SetTitle( "Radius [mm]" );
    gResponse0->Draw( "ALP" );
    gResponse135->SetMarkerSize( kMSize ); gResponse135->SetMarkerStyle( kMStyle ); gResponse135->Draw( "LP" );
    gResponse180->SetMarkerSize( kMSize ); gResponse180->SetMarkerStyle( kMStyle ); gResponse180->Draw( "LP" );
    gResponse225->SetMarkerSize( kMSize ); gResponse225->SetMarkerStyle( kMStyle ); gResponse225->Draw( "LP" );
    gResponse270->SetMarkerSize( kMSize ); gResponse270->SetMarkerStyle( kMStyle ); gResponse270->Draw( "LP" );
    gResponse315->SetMarkerSize( kMSize ); gResponse315->SetMarkerStyle( kMStyle ); gResponse315->Draw( "LP" );
    gResponse45->SetMarkerSize( kMSize ); gResponse45->SetMarkerStyle( kMStyle ); gResponse45->Draw( "LP" );
    gResponse90->SetMarkerSize( kMSize ); gResponse90->SetMarkerStyle( kMStyle ); gResponse90->Draw( "LP" );
    gResponseAverage->SetLineColor( kRed ); gResponseAverage->SetMarkerSize( kMSize ); gResponseAverage->SetMarkerStyle( kMStyle ); gResponseAverage->Draw( "LP" );
    vc1->SetGridx();
    vc1->SetGridy();
    
    TLegend* legend = new TLegend( 0.7, 0.7, 0.9, 0.9 );
    legend->SetHeader( "Legend" );
    legend->AddEntry( gResponse0, "0", "LP" );
    legend->AddEntry( gResponse135, "135", "LP" );
    legend->AddEntry( gResponse180, "180", "LP" );
    legend->AddEntry( gResponse225, "225", "LP" );
    legend->AddEntry( gResponse270, "270", "LP" );
    legend->AddEntry( gResponse315, "315", "LP" );
    legend->AddEntry( gResponse45, "45", "LP" );
    legend->AddEntry( gResponse90, "90", "LP" );
    
    legend->SetFillColor( kWhite );
    legend->Draw();
  }
  TCanvas* c2 = new TCanvas();
  {
    TVirtualPad* vc2 = c2->cd();
    
    gTiming0->SetTitle( "Averaged timing" );
    gTiming0->SetMarkerSize( kMSize );
    gTiming0->SetMarkerStyle( kMStyle );
    gTiming0->GetYaxis()->SetRangeUser( -1.0, 1.5 );
    gTiming0->GetYaxis()->SetTitle( "Relative timing" );
    gTiming0->GetXaxis()->SetTitle( "Radius [mm]" );
    gTiming0->Draw( "ALP" );
    gTiming135->SetMarkerSize( kMSize ); gTiming135->SetMarkerStyle( kMStyle ); gTiming135->Draw( "LP" );
    gTiming180->SetMarkerSize( kMSize ); gTiming180->SetMarkerStyle( kMStyle ); gTiming180->Draw( "LP" );
    gTiming225->SetMarkerSize( kMSize ); gTiming225->SetMarkerStyle( kMStyle ); gTiming225->Draw( "LP" );
    gTiming270->SetMarkerSize( kMSize ); gTiming270->SetMarkerStyle( kMStyle ); gTiming270->Draw( "LP" );
    gTiming315->SetMarkerSize( kMSize ); gTiming315->SetMarkerStyle( kMStyle ); gTiming315->Draw( "LP" );
    gTiming45->SetMarkerSize( kMSize ); gTiming45->SetMarkerStyle( kMStyle ); gTiming45->Draw( "LP" );
    gTiming90->SetMarkerSize( kMSize ); gTiming90->SetMarkerStyle( kMStyle ); gTiming90->Draw( "LP" );
    gTimingAverage->SetLineColor( kRed ); gTimingAverage->SetMarkerSize( kMSize ); gTimingAverage->SetMarkerStyle( kMStyle ); gTimingAverage->Draw( "LP" );
    vc2->SetGridx();
    vc2->SetGridy();
    
    TLegend* legend = new TLegend( 0.7, 0.7, 0.9, 0.9 );
    legend->SetHeader( "Legend" );
    legend->AddEntry( gTiming0, "0", "LP" );
    legend->AddEntry( gTiming135, "135", "LP" );
    legend->AddEntry( gTiming180, "180", "LP" );
    legend->AddEntry( gTiming225, "225", "LP" );
    legend->AddEntry( gTiming270, "270", "LP" );
    legend->AddEntry( gTiming315, "315", "LP" );
    legend->AddEntry( gTiming45, "45", "LP" );
    legend->AddEntry( gTiming90, "90", "LP" );
    
    legend->SetFillColor( kWhite );
    legend->Draw();
  }
}
