////////////////////////////////////////////////////////
/// Contains the raw data, orgainsed by event then by hit
/// HIT means a hit on the bucket, a PMTCal type hit is
/// called a signal.
///
///
/// 7/07/10 - New File
////////////////////////////////////////////////////////
#ifndef FullDataManager_hh
#define FullDataManager_hh

#include "HitDataMinimal.hh"
#include "EventData.hh"

#include <vector>
using namespace std;

class HitData;

class FullDataManager
{
public:
  void
  NewEvent(
	   const int eventID );
  void
  NewHit(
	 const int eventID,
	 const int trackID,
	 const int pmtID,
	 const double inTheta,
	 const double lambda,
	 const double inRadialPos,
	 const double globalTime );
  void
  NewSignal(
	    const int eventID,
	    const int trackID,
	    const int pmtID,
	    const double numPE );
  void
  NewReflection(
		const int eventID,
		const int trackID,
		const int pmtID,
		const double outTheta,
		const double globalTime );
  void
  NewPMTHit(
	    const int eventID,
	    const int trackID,
	    const int pmtID,
	    const double pmtHitZ );
  void
  NewConcHit(
	     const int eventID,
	     const int trackID,
	     const int pmtID,
	     const double concHitZ );

  vector<HitData*>
  ProduceHitData();
  vector<HitDataMinimal>
  ProduceHitDataMinimal();
  void
  Serialise(
	    const char* lpFile );
  void
  DeSerialise(
	      const char* lpFile );
  void
  Append(
	 const FullDataManager& lpNew );
  void
  Reduce();
private:
  vector<EventData> fEvents; 
};

#endif
