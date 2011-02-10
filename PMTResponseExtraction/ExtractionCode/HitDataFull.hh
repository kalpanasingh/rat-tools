////////////////////////////////////////////////////////
/// Contains the each hit raw data
/// HIT means a hit on the bucket, a PMTCal type hit is
/// called a signal.
///
///
/// 7/07/10 - New File
////////////////////////////////////////////////////////
#ifndef HitDataFull_hh
#define HitDataFull_hh

#include "HitData.hh"

class HitDataFull : public HitData
{
public:

  HitDataFull() {};

  HitDataFull( 
	      const int trackID,
	      const int pmtID,
	      const double inTheta,
	      const double lambda,
	      const double inRadialPos,
	      const double globalTime );

  HitData*
  NewClone();

  void
  Signal( 
	 const double numPE );
  void
  Reflected(
	    const double outTheta,
	    const double globalTime );
  void
  ConcHitZ(
	   const double concHitZ );
  void
  PMTHitZ(
	  const double pmtHitZ );
  bool
  Check(
	const int trackID,
	const int pmtID );
  void
  Serialise(
	    ofstream& outFile );
  void
  DeSerialise(
	      ifstream& inFile );
  string
  GetIdentifier() { return Identifier(); };
  static string 
  Identifier() { return string("f"); };
  // Properties
  double
  GetInTheta() { return fInTheta; };
  double
  GetOutTheta() { return fOutTheta; };
  double
  GetLambda() { return fLambda; };
  EOutcome
  GetOutcome() { return fOutcome; };
  double
  GetConcHitZ() { return fConcHitZ; };
  double
  GetPMTHitZ() { return fPMTHitZ; };
  double
  GetInRadialPos() { return fInRadialPos; };
  double
  GetDeltaTime() { return fDeltaTime; };
  int 
  GetPMTID() { return fpmtID; };
  int 
  GetTrackID() { return fTrackID; };

private:
  float fInTheta;
  float fOutTheta;
  float fLambda;
  float fNumPE;
  float fConcHitZ;
  float fPMTHitZ;
  float fInRadialPos; // Radial position on entry to bucket
  float fDeltaTime;
  EOutcome fOutcome;
  unsigned short int fpmtID;
  unsigned int fTrackID;
};

#endif
