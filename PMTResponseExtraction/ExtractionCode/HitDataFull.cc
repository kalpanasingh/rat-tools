 ////////////////////////////////////////////////////////
/// Contains the each hit raw data
/// HIT means a hit on the bucket, a PMTCal type hit is
/// called a signal.
///
///
/// 7/07/10 - New File
////////////////////////////////////////////////////////
#include "HitDataFull.hh"

#include <iostream>
#include <fstream>
using namespace std;

HitDataFull::HitDataFull( 
			 const int trackID,
			 const int pmtID,
			 const double inTheta,
			 const double lambda,
			 const double inRadialPos,
			 const double globalTime )
{
  const unsigned short int max = 0;
  if( fTrackID > ~max )
    cout << "Too many tracks..." << endl;
  fpmtID = static_cast<unsigned short int>( pmtID );
  fTrackID = static_cast<unsigned int>( trackID );
  fInTheta = static_cast<float>( inTheta );
  fOutTheta = -1.0;
  fLambda = lambda;
  fNumPE = -1.0;
  fOutcome = eAbsorbed;
  fConcHitZ = -400.0;
  fPMTHitZ = -400.0;
  fInRadialPos = inRadialPos;
  fDeltaTime = globalTime;
}

HitData*
HitDataFull::NewClone()
{
  return new HitDataFull( *this );
}

void
HitDataFull::Signal( 
		    const double numPE )
{
  fNumPE = numPE;
  fOutcome = eSignal;
}

void
HitDataFull::Reflected(
		       const double outTheta,
		       const double globalTime  )
{
  fOutTheta = outTheta;
  fOutcome = eReflected;
  fDeltaTime = globalTime - fDeltaTime;
}

void
HitDataFull::ConcHitZ(
		      const double concHitZ )
{
  if( fConcHitZ == -400.0 )
    fConcHitZ = concHitZ;
}

void
HitDataFull::PMTHitZ(
		     const double pmtHitZ )
{
  if( fPMTHitZ == -400.0 )
    fPMTHitZ = pmtHitZ;
}

bool
HitDataFull::Check(
		   const int trackID,
		   const int pmtID )
{
  return ( trackID == fTrackID && pmtID == fpmtID );
}

void
HitDataFull::Serialise(
		       ofstream& outFile )
{
  outFile << fpmtID << " " << fTrackID << " " << fInTheta << " " << fOutTheta << " " << fLambda << " " 
	  << fNumPE << " " << fPMTHitZ << " " << fConcHitZ << " " << fInRadialPos << " " << fDeltaTime << " " 
	  << static_cast<int>( fOutcome ) << endl;
}

void
HitDataFull::DeSerialise(
			 ifstream& inFile )
{
  int tOutcome;
  inFile >> fpmtID >> fTrackID >> fInTheta >> fOutTheta >> fLambda >> fNumPE >> fPMTHitZ >> fConcHitZ >> fInRadialPos >> fDeltaTime >> tOutcome;
  fOutcome = static_cast<EOutcome>( tOutcome );
}
