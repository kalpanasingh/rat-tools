////////////////////////////////////////////////////////
/// Grey Disc Parameter drawing
///
/// 21/07/10 - New file
/// 22/07/10 - TH2D draws better than TGraph2D
///////////////////////////////////////////////////////

#include "TH2D.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TStyle.h"
using namespace ROOT;

#include <iostream>
using namespace std;

#include "GreyDisc1.hh"
#include "GreyDisc2.hh"
#include "GreyDisc3.hh"
#include "GreyDisc4.hh"
#include "GreyDisc5.hh"
#include "GreyDisc6.hh"
#include "GreyDisc7.hh"
#include "GreyDisc8.hh"
#include "GreyDisc9.hh"
#include "GreyDisc10.hh"
#include "GreyDisc11.hh"
#include "GreyDisc12.hh"


void
DrawGreyDiscParameters(
		       int dataSet1,
		       int dataSet2 )
{
  gStyle->SetTitleSize( 0.05, "xyz" );
  gStyle->SetLabelSize( 0.05, "xyz" );

  TH2D** greyDiscAbs = new TH2D*[12];
  TH2D** greyDiscRef = new TH2D*[12];
  const int thetaBins = 90; const double thetaLow = 0.0; const double thetaHigh = 89.0;
  const int lambdaBins = 49; const double lambdaLow = 220.0; const double lambdaHigh = 710.0;
  
  greyDiscAbs[0] = new TH2D( "greyDisc1Abs", "1998 Data, absorption", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscRef[0] = new TH2D( "greyDisc1Ref", "1998 Data, reflection", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );  
  greyDiscAbs[1] = new TH2D( "greyDisc2Abs", "1995 Data, absorption", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscRef[1] = new TH2D( "greyDisc2Ref", "1995 Data, reflection", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscAbs[2] = new TH2D( "greyDisc3Abs", "1995 Data, absorption", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscRef[2] = new TH2D( "greyDisc3Ref", "1995 Data, reflection", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscAbs[3] = new TH2D( "greyDisc4Abs", "Apr 2001 Data, absorption", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscRef[3] = new TH2D( "greyDisc4Ref", "Apr 2001 Data, reflection", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscAbs[4] = new TH2D( "greyDisc5Abs", "Jan 2001 Data, absorption", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscRef[4] = new TH2D( "greyDisc5Ref", "Jan 2001 Data, reflection", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscAbs[5] = new TH2D( "greyDisc6Abs", "Mar 2003 Data, absorption", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscRef[5] = new TH2D( "greyDisc6Ref", "Mar 2003 Data, reflection", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscAbs[6] = new TH2D( "greyDisc7Abs", "Jan 2004 Data, absorption", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscRef[6] = new TH2D( "greyDisc7Ref", "Jan 2004 Data, reflection", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscAbs[7] = new TH2D( "greyDisc8Abs", "Nov 2004 Data, absorption", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscRef[7] = new TH2D( "greyDisc8Ref", "Nov 2004 Data, reflection", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscAbs[8] = new TH2D( "greyDisc9Abs", "Feb 2006 Data, absorption", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscRef[8] = new TH2D( "greyDisc9Ref", "Feb 2006 Data, reflection", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscAbs[9] = new TH2D( "greyDisc10Abs", "Feb 2006 Data, absorption", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscRef[9] = new TH2D( "greyDisc10Ref", "Feb 2006 Data, reflection", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscAbs[10] = new TH2D( "greyDisc11Abs", "Apr 2006 Data, absorption", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscRef[10] = new TH2D( "greyDisc11Ref", "Apr 2006 Data, reflection", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscAbs[11] = new TH2D( "greyDisc12Abs", "Sep 2006 Data, absorption", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  greyDiscRef[11] = new TH2D( "greyDisc12Ref", "Sep 2006 Data, reflection", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );

  int iLoop;
  for( iLoop = 0; iLoop < 90; iLoop++ )
    {
      int iLoop2;
      for( iLoop2 = 22; iLoop2 <= 71; iLoop2++ )
	{
	  int gdPoint = iLoop + ( iLoop2 - 22 ) * 90;

	  greyDiscAbs[0]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc1Abs[gdPoint] );
	  greyDiscRef[0]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc1Ref[gdPoint] );
	  greyDiscAbs[1]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc2Abs[gdPoint] );
          greyDiscRef[1]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc2Ref[gdPoint] );
	  greyDiscAbs[2]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc3Abs[gdPoint] );
          greyDiscRef[2]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc3Ref[gdPoint] );
	  greyDiscAbs[3]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc4Abs[gdPoint] );
          greyDiscRef[3]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc4Ref[gdPoint] );
	  greyDiscAbs[4]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc5Abs[gdPoint] );
          greyDiscRef[4]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc5Ref[gdPoint] );
	  greyDiscAbs[5]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc6Abs[gdPoint] );
          greyDiscRef[5]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc6Ref[gdPoint] );
	  greyDiscAbs[6]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc7Abs[gdPoint] );
          greyDiscRef[6]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc7Ref[gdPoint] );
	  greyDiscAbs[7]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc8Abs[gdPoint] );
          greyDiscRef[7]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc8Ref[gdPoint] );
	  greyDiscAbs[8]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc9Abs[gdPoint] );
          greyDiscRef[8]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc9Ref[gdPoint] );
	  greyDiscAbs[9]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc10Abs[gdPoint] );
          greyDiscRef[9]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc10Ref[gdPoint] );
	  greyDiscAbs[10]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc11Abs[gdPoint] );
          greyDiscRef[10]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc11Ref[gdPoint] );
	  greyDiscAbs[11]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc12Abs[gdPoint] );
          greyDiscRef[11]->Fill( (double)iLoop, (double)iLoop2 * 10.0, GreyDisc12Ref[gdPoint] );
	}
    }

  gStyle->SetOptStat(0);

  gStyle->SetPalette(1);
  TCanvas* c1 = new TCanvas();
  c1->Divide( 2, 2 );

  c1->cd(1);
  greyDiscAbs[dataSet1]->GetXaxis()->SetTitle( "Theta [deg]" );
  greyDiscAbs[dataSet1]->GetYaxis()->SetTitle( "Lambda [nm]" );
  greyDiscAbs[dataSet1]->GetZaxis()->SetTitle( "Abs [%]" );
  greyDiscAbs[dataSet1]->Draw("COLZ");

  c1->cd(2);
  greyDiscRef[dataSet1]->GetXaxis()->SetTitle( "Theta [deg]" );
  greyDiscRef[dataSet1]->GetYaxis()->SetTitle( "Lambda [nm]" );
  greyDiscRef[dataSet1]->GetZaxis()->SetTitle( "Ref [%]" );
  greyDiscRef[dataSet1]->Draw("COLZ");

  c1->cd(3);
  greyDiscAbs[dataSet2]->GetXaxis()->SetTitle( "Theta [deg]" );
  greyDiscAbs[dataSet2]->GetYaxis()->SetTitle( "Lambda [nm]" );
  greyDiscAbs[dataSet2]->GetZaxis()->SetTitle( "Abs [%]" );
  greyDiscAbs[dataSet2]->Draw("COLZ");

  c1->cd(4);
  greyDiscRef[dataSet2]->GetXaxis()->SetTitle( "Theta [deg]" );
  greyDiscRef[dataSet2]->GetYaxis()->SetTitle( "Lambda [nm]" );
  greyDiscRef[dataSet2]->GetZaxis()->SetTitle( "Ref [%]" );
  greyDiscRef[dataSet2]->Draw("COLZ");
 
  c1->cd();

  TCanvas* c2 = new TCanvas();
  c2->Divide( 1, 2 );

  c2->cd(1);
  TH2D* absDiff = new TH2D( "absDiff", "Data 1 - Data 2", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  absDiff->Add( greyDiscAbs[dataSet1], greyDiscAbs[dataSet2], 1.0, -1.0 );
  absDiff->SetEntries(1);
  absDiff->GetXaxis()->SetTitle( "Theta [deg]" );
  absDiff->GetYaxis()->SetTitle( "Lambda [nm]" );
  absDiff->GetZaxis()->SetTitle( "Ref [%]" );
  absDiff->Draw("COLZ");

  c2->cd(2);
  TH2D* refDiff = new TH2D( "refDiff", "Data 1 - Data 2", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  refDiff->Add( greyDiscRef[dataSet1], greyDiscRef[dataSet2], 1.0, -1.0 );
  refDiff->SetEntries(1);
  refDiff->GetXaxis()->SetTitle( "Theta [deg]" );
  refDiff->GetYaxis()->SetTitle( "Lambda [nm]" );
  refDiff->GetZaxis()->SetTitle( "Ref [%]" );
  refDiff->Draw("COLZ");

  c2->cd();

}
