/// Contains the each hit raw data, but only the minimal 
/// required
/// HIT means a hit on the bucket, a PMTCal type hit is
/// called a signal.
///
///
/// 14/01/11 - New File
////////////////////////////////////////////////////////
#include "HitDataMinimal.hh"

#include <iostream>
#include <fstream>
using namespace std;

HitDataMinimal::HitDataMinimal(
			       HitData* hitData )
{
  fpmtID = hitData->GetPMTID();
  fTrackID = hitData->GetTrackID();
  fInTheta = hitData->GetInTheta();
  fLambda = hitData->GetLambda();
  fOutcome = hitData->GetOutcome();
  fInRadialPos = hitData->GetInRadialPos();
}

HitDataMinimal::HitDataMinimal( 
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
  fLambda = lambda;
  fOutcome = eAbsorbed;
  fInRadialPos = inRadialPos;
}

HitData*
HitDataMinimal::NewClone()
{
  return new HitDataMinimal( *this );
}

void
HitDataMinimal::Signal( 
		       const double numPE )
{
  fOutcome = eSignal;
}

void
HitDataMinimal::Reflected(
			  const double outTheta,
			  const double globalTime  )
{
  fOutcome = eReflected;
}

void
HitDataMinimal::ConcHitZ(
			 const double concHitZ )
{
  
}

void
HitDataMinimal::PMTHitZ(
			const double pmtHitZ )
{
  
}

bool
HitDataMinimal::Check(
		      const int trackID,
		      const int pmtID )
{
  return ( trackID == fTrackID && pmtID == fpmtID );
}

void
HitDataMinimal::Serialise(
			  ofstream& outFile )
{
  outFile << fpmtID << " " << fTrackID << " " << fInTheta << " " << fLambda << " " << fInRadialPos << " " << static_cast<int>( fOutcome ) << endl;
}

void
HitDataMinimal::DeSerialise(
			    ifstream& inFile )
{
  int tOutcome;
  inFile >> fpmtID >> fTrackID >> fInTheta >> fLambda >> fInRadialPos >> tOutcome;
  fOutcome = static_cast<EOutcome>( tOutcome );
}
