 ////////////////////////////////////////////////////////
/// Contains the raw data, orgainsed by event then by hit
/// HIT means a hit on the bucket, a PMTCal type hit is
/// called a signal.
///
///
/// 7/07/10 - New File
////////////////////////////////////////////////////////
#include <fstream>
#include <iostream>
using namespace std;

#include "FullDataManager.hh"
#include "HitData.hh"

void
FullDataManager::NewEvent(
			  const int eventID )
{
  if( static_cast<unsigned int>( eventID + 1 ) > fEvents.size() )
    fEvents.resize( eventID + 1 );
}

void
FullDataManager::NewHit(
			const int eventID,
			const int trackID,
			const int pmtID,
			const double inTheta,
			const double lambda,
			const double inRadialPos,
			const double globalTime )
{
  fEvents[eventID].NewHit( trackID, pmtID, inTheta, lambda, inRadialPos, globalTime );
}

void
FullDataManager::NewSignal(
			   const int eventID,
			   const int trackID,
			   const int pmtID,
			   const double numPE )
{
  fEvents[eventID].NewSignal( trackID, pmtID, numPE );
}

void
FullDataManager::NewReflection(
			       const int eventID,
			       const int trackID,
			       const int pmtID,
			       const double outTheta,
			       const double globalTime )
{
  fEvents[eventID].NewReflection( trackID, pmtID, outTheta, globalTime );
}

void
FullDataManager::NewPMTHit(
			   const int eventID,
			   const int trackID,
			   const int pmtID,
			   const double pmtHitZ )
{
  fEvents[eventID].NewPMTHit( trackID, pmtID, pmtHitZ );
}

void
FullDataManager::NewConcHit(
			   const int eventID,
			   const int trackID,
			   const int pmtID,
			   const double concHitZ )
{
  fEvents[eventID].NewConcHit( trackID, pmtID, concHitZ );
}

vector<HitData*>
FullDataManager::ProduceHitData()
{
  vector<HitData*> fullData;
  unsigned int uLoop;
  for( uLoop = 0; uLoop < fEvents.size(); uLoop++ )
    {
      fEvents[uLoop].ProduceHitData( fullData );
    }
  return fullData;
}

vector<HitDataMinimal>
FullDataManager::ProduceHitDataMinimal()
{
  vector<HitDataMinimal> fullData;
  unsigned int uLoop;
  for( uLoop = 0; uLoop < fEvents.size(); uLoop++ )
    {
      fEvents[uLoop].ProduceHitDataMinimal( fullData );
    }
  return fullData;
}

void
FullDataManager::Serialise(
			   const char* lpFile )
{
  ofstream outFile( lpFile, ios::out );//| ios::binary );
  outFile << fEvents.size() << endl;
  unsigned int uLoop;
  for( uLoop = 0; uLoop < fEvents.size(); uLoop++ )
    {
      fEvents[uLoop].Serialise( outFile );
    }
}

void
FullDataManager::DeSerialise(
			     const char* lpFile )
{
  ifstream inFile( lpFile, ios::in );//| ios::binary );
  unsigned int numEvents;
  inFile >> numEvents;
  fEvents.resize( numEvents );
  unsigned int uLoop;
  for( uLoop = 0; uLoop < numEvents; uLoop++ )
    {
      fEvents[uLoop].DeSerialise( inFile );
    }
}

void
FullDataManager::Append(
			const FullDataManager& lpNew )
{
  int startEvent = fEvents.size();
  fEvents.resize( fEvents.size() + lpNew.fEvents.size() );
  unsigned int uLoop;
  for( uLoop = 0; uLoop < lpNew.fEvents.size(); uLoop++ )
    {
      fEvents[startEvent + uLoop] = lpNew.fEvents[uLoop];
    }
}

void
FullDataManager::Reduce()
{
  unsigned int uLoop;
  for( uLoop = 0; uLoop < fEvents.size(); uLoop++ )
    {
      fEvents[uLoop].Reduce();
    }
}
