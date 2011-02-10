////////////////////////////////////////////////////////
/// Contains the event data
/// HIT means a hit on the bucket, a PMTCal type hit is
/// called a signal.
///
///
/// 7/07/10 - New File
////////////////////////////////////////////////////////
#ifndef EventData_hh
#define EventData_hh

#include <vector>
#include <fstream>
using namespace std;

#include "HitDataMinimal.hh"

class HitData;

enum EDataSize { eFull, eMinimal };

class EventData
{
public:
  EventData() {};

  EventData(
	    const EventData& rhs );

  ~EventData();

  EventData&
  operator=(
	    const EventData& rhs );

  void
  NewHit(
	 const int trackID,
	 const int pmtID,
	 const double inTheta,
	 const double lambda,
	 const double inRadialPos,
	 const double globalTime,
	 const EDataSize dataSize = eFull );
  void
  NewSignal(
	    const int trackID,
	    const int pmtID,
	    const double numPE );
  void
  NewReflection(
		const int trackID,
		const int pmtID,
		const double outTheta,
		const double globalTime  );
  void
  NewConcHit(
	     const int trackID,
	     const int pmtID,
	     const double concHitZ );
  void
  NewPMTHit(
	    const int trackID,
	    const int pmtID,
	    const double pmtHitZ );
  void
  ProduceHitData(
		 vector<HitData*>& fullData );
  void
  ProduceHitDataMinimal(
			vector<HitDataMinimal>& fullData );
  void
  Serialise(
	    ofstream& outFile );
  void
  DeSerialise(
	      ifstream& inFile );
  void
  Reduce();
private:
  vector<HitData*> fpHits; 
};


#endif
