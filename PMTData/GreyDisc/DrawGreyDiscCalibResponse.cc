////////////////////////////////////////////////////////
/// Grey disc response at the calibration wavelengths drawing
///
/// 11/10/10 - New file
///////////////////////////////////////////////////////

#include "TH1D.h"
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

#include <PHILCalcFunctions.hh>

void
DrawGreyDiscCalibResponse(
			  int dataSet,
			  const int angleMode = 0, // 0 is cos, 1 is radians, 2 is degrees
			  const double pmt_coll_eff = 0.55 ) // SNOMAN Version of this
{
  int numBins = 0; double lowBin = 0.0; double highBin = 0.0;
  if( angleMode == 0 )
    { numBins = 50; lowBin = -1.0;  highBin = -0.5; }
  else if( angleMode == 1 )
    { numBins = 50; lowBin = 0.0;  highBin = PHIL::kPI / 2.0; }
  else if( angleMode == 2 )
    { numBins = 90; lowBin = 0.0;  highBin = 90.0; }

  TH1D* wave1 = new TH1D( "337", "337", numBins, lowBin, highBin );
  TH1D* wave2 = new TH1D( "365", "365", numBins, lowBin, highBin );
  TH1D* wave3 = new TH1D( "386", "386", numBins, lowBin, highBin );
  TH1D* wave4 = new TH1D( "420", "420", numBins, lowBin, highBin );
  TH1D* wave5 = new TH1D( "500", "500", numBins, lowBin, highBin );
  TH1D* wave6 = new TH1D( "620", "620", numBins, lowBin, highBin );
  
  int iTheta;
  for( iTheta = 0; iTheta < 90; iTheta++ )
    {
      const int point1 = iTheta + ( 34 - 22 ) * 90; // 33.7 -> 34
      const int point2 = iTheta + ( 36 - 22 ) * 90; // 36.5 ->36
      const int point3 = iTheta + ( 39 - 22 ) * 90; // 38.6 -> 39
      const int point4 = iTheta + ( 42 - 22 ) * 90; // 42.0 -> 42
      const int point5 = iTheta + ( 50 - 22 ) * 90; // 50.0 -> 50
      const int point6 = iTheta + ( 62 - 22 ) * 90; // 62.0 -> 62

      double resp1 = pmt_coll_eff / 0.55;
      double resp2 = pmt_coll_eff / 0.55;
      double resp3 = pmt_coll_eff / 0.55;
      double resp4 = pmt_coll_eff / 0.55;
      double resp5 = pmt_coll_eff / 0.55;
      double resp6 = pmt_coll_eff / 0.55;

      switch( dataSet )
	{
	case 0:
	  resp1 *= GreyDisc1Abs[point1];
	  resp2 *= GreyDisc1Abs[point2];
	  resp3 *= GreyDisc1Abs[point3];
	  resp4 *= GreyDisc1Abs[point4];
	  resp5 *= GreyDisc1Abs[point5];
	  resp6 *= GreyDisc1Abs[point6];
	  break;
	case 1:
	  resp1 *= GreyDisc2Abs[point1];
	  resp2 *= GreyDisc2Abs[point2];
	  resp3 *= GreyDisc2Abs[point3];
	  resp4 *= GreyDisc2Abs[point4];
	  resp5 *= GreyDisc2Abs[point5];
	  resp6 *= GreyDisc2Abs[point6];
	  break;
	case 2:
	  resp1 *= GreyDisc3Abs[point1];
	  resp2 *= GreyDisc3Abs[point2];
	  resp3 *= GreyDisc3Abs[point3];
	  resp4 *= GreyDisc3Abs[point4];
	  resp5 *= GreyDisc3Abs[point5];
	  resp6 *= GreyDisc3Abs[point6];
	  break;
	case 3:
	  resp1 *= GreyDisc4Abs[point1];
	  resp2 *= GreyDisc4Abs[point2];
	  resp3 *= GreyDisc4Abs[point3];
	  resp4 *= GreyDisc4Abs[point4];
	  resp5 *= GreyDisc4Abs[point5];
	  resp6 *= GreyDisc4Abs[point6];
	  break;
	case 4:
	  resp1 *= GreyDisc5Abs[point1];
	  resp2 *= GreyDisc5Abs[point2];
	  resp3 *= GreyDisc5Abs[point3];
	  resp4 *= GreyDisc5Abs[point4];
	  resp5 *= GreyDisc5Abs[point5];
	  resp6 *= GreyDisc5Abs[point6];
	  break;
	case 5:
	  resp1 *= GreyDisc6Abs[point1];
	  resp2 *= GreyDisc6Abs[point2];
	  resp3 *= GreyDisc6Abs[point3];
	  resp4 *= GreyDisc6Abs[point4];
	  resp5 *= GreyDisc6Abs[point5];
	  resp6 *= GreyDisc6Abs[point6];
	  break;
	case 6:
	  resp1 *= GreyDisc7Abs[point1];
	  resp2 *= GreyDisc7Abs[point2];
	  resp3 *= GreyDisc7Abs[point3];
	  resp4 *= GreyDisc7Abs[point4];
	  resp5 *= GreyDisc7Abs[point5];
	  resp6 *= GreyDisc7Abs[point6];
	  break;
	case 7:
	  resp1 *= GreyDisc8Abs[point1];
	  resp2 *= GreyDisc8Abs[point2];
	  resp3 *= GreyDisc8Abs[point3];
	  resp4 *= GreyDisc8Abs[point4];
	  resp5 *= GreyDisc8Abs[point5];
	  resp6 *= GreyDisc8Abs[point6];
	  break;
	case 8:
	  resp1 *= GreyDisc9Abs[point1];
	  resp2 *= GreyDisc9Abs[point2];
	  resp3 *= GreyDisc9Abs[point3];
	  resp4 *= GreyDisc9Abs[point4];
	  resp5 *= GreyDisc9Abs[point5];
	  resp6 *= GreyDisc9Abs[point6];
	  break;
	case 9:
	  resp1 *= GreyDisc10Abs[point1];
	  resp2 *= GreyDisc10Abs[point2];
	  resp3 *= GreyDisc10Abs[point3];
	  resp4 *= GreyDisc10Abs[point4];
	  resp5 *= GreyDisc10Abs[point5];
	  resp6 *= GreyDisc10Abs[point6];
	  break;
	case 10:
	  resp1 *= GreyDisc11Abs[point1];
	  resp2 *= GreyDisc11Abs[point2];
	  resp3 *= GreyDisc11Abs[point3];
	  resp4 *= GreyDisc11Abs[point4];
	  resp5 *= GreyDisc11Abs[point5];
	  resp6 *= GreyDisc11Abs[point6];
	  break;
	case 11:
	  resp1 *= GreyDisc12Abs[point1];
	  resp2 *= GreyDisc12Abs[point2];
	  resp3 *= GreyDisc12Abs[point3];
	  resp4 *= GreyDisc12Abs[point4];
	  resp5 *= GreyDisc12Abs[point5];
	  resp6 *= GreyDisc12Abs[point6];
	  break;
	}
      double angle;
      if( angleMode == 0 )
	angle = cos( iTheta );
      else if ( angleMode == 1 )
	angle = iTheta / 180.0 * PHIL::kPI;
      else 
	angle = iTheta;
      
      wave1->Fill( angle, resp1 );
      wave2->Fill( angle, resp2 );
      wave3->Fill( angle, resp3 );
      wave4->Fill( angle, resp4 );
      wave5->Fill( angle, resp5 );
      wave6->Fill( angle, resp6 );
    }

  TCanvas* c1 = new TCanvas();
  c1->Divide( 3, 2 );
  c1->cd(1);
  wave1->Draw(); 
  c1->cd(2);
  wave2->Draw(); 
  c1->cd(3);
  wave3->Draw(); 
  c1->cd(4);
  wave4->Draw(); 
  c1->cd(5);
  wave5->Draw(); 
  c1->cd(6);
  wave6->Draw(); 
}
