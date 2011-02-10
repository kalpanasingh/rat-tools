////////////////////////////////////////////////////////
/// Extracts the raw data from the root file, and produces
/// a full filesFullData set.
///
/// 8/07/10 - New File
////////////////////////////////////////////////////////
#include <TChain.h>

#include <iostream>
#include <sstream>
using namespace std;

#include "QEvent.h"
#include "QTree.h"
#include "QPMTuvw.h"
#include "QPMTxyz.h"
#include "QMCVX.h"
#include "QPMT.h"

#include "FullDataManager.hh"
#include "ExtractData.hh"
#include "Extraction.hh"

double
invCos(
       const TVector3 a,
       const TVector3 b );

const double concA = 51.4; //mm
const double concD = 87.5; //mm

QPMTuvw* gQPMTuvw;
QPMTxyz* gQPMTxyz;

int totalNumHits;
int totalNumReflects;
int totalNumSignals;

int snomanTolpmt[10000]; // Index is snoman id, value is lpmt/lcn number.
vector<int> pmtsInPanel[10000]; //Access by panel number to get vector of lpmt IDs of pmts in that panel

void
ExtractData(
	    char* lpFile,
	    bool saveData = false,
	    int mode = 0 ) // 0 = MC, 1 = PMTTruth, 2 = PMTCal 3 = PMTUnCal (Not in this code)
{
  // Clear old info lists first
  int iLoop;
  for( iLoop = 0; iLoop < 10000; iLoop++ )
    {
      snomanTolpmt[iLoop] = -1;
      pmtsInPanel[iLoop].clear();
    }

  gQPMTuvw = new QPMTuvw();
  gQPMTxyz = new QPMTxyz("read");
  FillPMTConversionList();

  filesFullData.clear();
  totalNumHits = 0;
  totalNumReflects = 0;
  totalNumSignals = 0;

  string dataLocation;
  vector<string> files;
  
  time_t codeStart = time ( NULL );
  
  cout << lpFile << endl;
  // Load the root file first
      
  TFile *file = new TFile( lpFile );
  QTree *tree = (QTree*)file->Get( "T" );
  QEvent *qEV = new QEvent();
  tree->SetEventAddress( qEV );
  
  int numMCEvents = tree->GetEntries();
  
  FullDataManager fullData;
  
  for( iLoop = 0; iLoop < numMCEvents; iLoop++ )
    {
      if( iLoop % 100 == 0 )
	cout << iLoop << " finished at " << time( NULL ) - codeStart << endl;
      
      tree->GetEntry( iLoop );
      
      fullData.NewEvent( iLoop );
      
      ExtractTrackData( qEV, iLoop, fullData );
    }
  filesFullData.push_back( fullData );
  if( saveData == true )
    {
      stringstream saveLoc;
      string lpInfoFile( lpFile );
      const int infoFileLen = lpInfoFile.length();
      const int fullPathPos = lpInfoFile.find_last_of( '/' );
      string dataLocation = lpInfoFile.substr( 0, fullPathPos + 1 );
      saveLoc << dataLocation << lpInfoFile.substr( fullPathPos + 1, infoFileLen - fullPathPos - 6 ) << ".dat";
      fullData.Serialise( saveLoc.str().c_str() );
    }

  cout << "Absorbed: " << totalNumHits << " reflects: " << totalNumReflects << " signals: " << totalNumSignals << " hits: " << totalNumHits + totalNumReflects + totalNumSignals << endl;
  delete gQPMTuvw;
  delete gQPMTxyz;
}


void
ExtractTrackData(
		 QEvent* qEV,
		 int eventID,
		 FullDataManager& fileData )
{
  const int reflectINC = 305000; //305 for bounce 
  const int absorbINC  = 404000; //404 for absorb 
  const int signalINC  = 402000; //402 for hit
  const int discardINC = 401000; //401 for discard photon
  const int gdreflectINC = 201000; //201 for GD reflect 
  const int newPhotonINC = 301000; //301 for new photon 
  const int newTrackINC = 100000; //100 for new photon if a photon bomb

  const int refractINC  = 203000; //Method to get to ABS
  const int sReflectINC = 201000; //Method to get to ABS
  const int diffuseINC = 202000;//Method to get to ABS
  const int transINC = 204000;//Method to get to ABS

  const int pmtABS     = 4260000; 
  const int pmtRGN     = 4220000; // The final four numbers are the pmt ID
  const int h2oRGN     = 4000000;

  const int numTracks = qEV->GetnMCVXs();

  TVector3 lastDir( 0.0, 0.0, 0.0 );

  // Loop over the tracks
  int trackID = -1;
  int iLoop;
  for( iLoop = 0; iLoop < numTracks; iLoop++ )
    {
      QMCVX* qMCVX = qEV->GetMCVX( iLoop );

      const int pureINC = static_cast<int>( qMCVX->GetINC() / 1000 ) * 1000;
      const int pureIDP = qMCVX->GetIDP();
      const int pureStartRGN = static_cast<int>( qMCVX->GetRGN() / 10000 ) * 10000;
      const int pureEndRGN = static_cast<int>( qMCVX->GetRG2() / 10000 ) * 10000;
      // Photons have idp code 1
      if( pureIDP != 1 )
	continue;
      //cout << "\t" << qMCVX->GetINC() << " " << qMCVX->GetRGN() << " to " <<  qMCVX->GetRG2() << endl;

      if( pureINC == newPhotonINC || pureINC == newTrackINC ) //Cer and Bomb checks
	{
	  trackID++;
	  continue;
	}

      
      int pmtID = 0;
      if( pureStartRGN == pmtRGN )
	pmtID = ( qMCVX->GetRGN() - pmtRGN );
      else if( pureEndRGN == pmtRGN )
	pmtID = ( qMCVX->GetRG2() - pmtRGN );
      else if( pureEndRGN == pmtABS )
	pmtID = ( qMCVX->GetRG2() - pmtABS );

      TVector3 pmtPos = gQPMTxyz->GetXYZ( snomanTolpmt[pmtID] );
      TVector3 pmtDir = gQPMTuvw->GetPMTDir( snomanTolpmt[pmtID] ); //Points outwards
      pmtDir = pmtDir.Unit();

      const double lambda = 2 * 3.14 * 197.33 * 1e-6 / qMCVX->GetEnergy(); // In nm
      TVector3 trackDir( qMCVX->GetU(), qMCVX->GetV(), qMCVX->GetW() );
      trackDir = trackDir.Unit();
      TVector3 trackPos( qMCVX->GetX(), qMCVX->GetY(), qMCVX->GetZ() );
      double theta = invCos( trackDir, pmtDir );
      double time = qMCVX->GetTime();

      if( pureINC == reflectINC && pureEndRGN == pmtRGN ) 
	{
	  double thetaIn  = invCos( lastDir, pmtDir ) ;
	  double thetaOut = invCos( trackDir, -pmtDir ); 
	  fileData.NewHit( eventID, trackID, pmtID, thetaIn, lambda, 
			   GetFrontFaceHitPos( trackDir, trackPos, -pmtDir, pmtPos ),
			   time );
	  if( iLoop + 1 < numTracks )
	    time = qEV->GetMCVX( iLoop + 1 )->GetTime();
	  fileData.NewReflection( eventID, trackID, pmtID, thetaOut, time );	  
	  totalNumReflects++;
	}
      else if( ( pureINC == absorbINC || pureINC == discardINC ) && pureEndRGN == pmtRGN )
	{
	  if( lastDir.x() != trackDir.x() && lastDir.y() != trackDir.y() && lastDir.z() != trackDir.z() )
	    cout << "Abs Strange " << eventID << " " << trackID << " " << pmtID << endl;

	  fileData.NewHit( eventID, trackID, pmtID, theta, lambda, 
			   GetFrontFaceHitPos( trackDir, trackPos, -pmtDir, pmtPos ),
			   time );
	  totalNumHits++;
	}
      else if( pureINC == signalINC && pureEndRGN == pmtRGN  )
	{
	  if( lastDir.x() != trackDir.x() && lastDir.y() != trackDir.y() && lastDir.z() != trackDir.z() )
            cout << "Signal Strange " << eventID << " " << trackID << " " << pmtID << endl;

	  fileData.NewHit( eventID, trackID, pmtID, theta, lambda, 
			   GetFrontFaceHitPos( trackDir, trackPos, -pmtDir, pmtPos ),
			   time );
	  fileData.NewSignal( eventID, trackID, pmtID, 1.0 );
	  totalNumSignals++;
	}
      //else if( ( pureINC == refractINC || pureINC == sReflectINC || pureINC == diffuseINC || pureINC == transINC ) && pureStartRGN == h2oRGN && pureEndRGN == pmtABS ) // As included in RAT, copy in SNOMAN
	  // int panelID = ( qMCVX->GetRGN() - h2oRGN );
// 	  int pmtID = FindNearestPMT( panelID, trackPos );
// 	  pmtPos = gQPMTxyz->GetXYZ( snomanTolpmt[pmtID] );
// 	  pmtDir = gQPMTuvw->GetPMTDir( snomanTolpmt[pmtID] ); //Points outwards
// 	  pmtDir = pmtDir.Unit();
// 	  theta = acos( trackDir.Dot( pmtDir ) );
// 	  fileData.NewHit( eventID, trackID, pmtID, theta, lambda, 
// 			   GetFrontFaceHitPos( trackDir, trackPos, -pmtDir, pmtPos ),
// 			   time );
      else if( pureINC == absorbINC && pureEndRGN == pmtABS )
	{ 
	  // Remember it refracts into the ABS before being absorbed, thus must use last dir i.e. in water direction
	  double thetaIn  = invCos( lastDir, pmtDir );
	  fileData.NewHit( eventID, trackID, pmtID, thetaIn, lambda, 
			   GetFrontFaceHitPos( trackDir, trackPos, -pmtDir, pmtPos ),
			   time );
	  totalNumHits++;
	}
      else if( pureEndRGN == h2oRGN ) //Will always record last direction before hitting the pmt
	lastDir = trackDir;
    }
}

double
GetFrontFaceHitPos(
		   const TVector3 trackDir,
		   const TVector3 trackPos,
		   const TVector3 pmtDir, //This should be corrected s.t. it points towards the centre
		   const TVector3 pmtPos ) //Uncorrected position of conc front face
{
  const double alpha = pmtDir.Dot( pmtPos - trackPos ) / pmtDir.Dot( trackDir );
  const TVector3 planePos = trackPos + alpha * trackDir;
  return ( planePos - pmtPos ).Mag() * 10.0; // From cm to mm
}

void
FillPMTConversionList()
{
  int iLoop;
  for( iLoop = 0; iLoop < 10000; iLoop++ )
    {
      if( gQPMTxyz->IsInvalidPMT( iLoop ) || !gPMTxyz->IsNormalPMT( iLoop ) )
	continue;
      int snomanNo = gQPMTxyz->GetSnomanNo( iLoop );
      int panelNo = gQPMTxyz->GetPanel( iLoop );
      if( snomanNo > 0 )
	{
	  snomanTolpmt[snomanNo] = iLoop;
	  pmtsInPanel[panelNo].push_back( iLoop );
	}
    }
}

int
FindNearestPMT( 
	       int panelID, 
	       TVector3 trackPos )
{
  double nearDist2 = 1e9;
  int lpmt = -1;
  unsigned int uLoop;
  for( uLoop = 0; uLoop < pmtsInPanel[panelID].size(); uLoop++ )
    {
      TVector3 pmtPos = gQPMTxyz->GetXYZ( pmtsInPanel[panelID][uLoop] );
      double localDist2 = ( trackPos - pmtPos ).Mag2();
      if( localDist2 < nearDist2 )
	{
	  lpmt = pmtsInPanel[panelID][uLoop];
	  nearDist2 = localDist2;
	} 
    }
  //cout << sqrt(nearDist2) << " " << lpmt << endl;
  return gQPMTxyz->GetSnomanNo( lpmt );
}

double
invCos(
       const TVector3 a,
       const TVector3 b )
{
  double cosTheta = a.Dot( b );
  if( cosTheta >= 1.0 )
    cosTheta = 1.0;
  else if( cosTheta <= -1.0 )
    cosTheta = -1.0;
  double theta = acos( cosTheta );
  if( isnan( theta ) )
    {
      cout << "invCos nan error " << cosTheta << endl;
      theta = 0.0;
    }
  return theta;
}

