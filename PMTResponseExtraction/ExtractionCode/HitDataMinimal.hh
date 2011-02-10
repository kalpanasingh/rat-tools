////////////////////////////////////////////////////////
/// Contains the each hit raw data, but only the minimal 
/// required
/// HIT means a hit on the bucket, a PMTCal type hit is
/// called a signal.
///
///
/// 14/01/11 - New File
////////////////////////////////////////////////////////
#ifndef HitDataMinimal_hh
#define HitDataMinimal_hh

#include "HitData.hh"

class HitDataMinimal : public HitData
{
public:

  HitDataMinimal() {};

  HitDataMinimal(
		 HitData* hitData );

  HitDataMinimal( 
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
  Identifier() { return string("m"); };
  // Properties
  double
  GetInTheta() { return fInTheta; };
  double
  GetOutTheta() { return 0.0; };
  double
  GetLambda() { return fLambda; };
  EOutcome
  GetOutcome() { return fOutcome; };
  double
  GetConcHitZ() { return 0.0; };
  double
  GetPMTHitZ() { return 0.0; };
  double
  GetInRadialPos() { return fInRadialPos; };
  double
  GetDeltaTime() { return 0.0; };
  int 
  GetPMTID() { return fpmtID; };
  int 
  GetTrackID() { return fTrackID; };

private:
  float fInTheta;
  float fLambda;
  float fInRadialPos; // Radial position on entry to bucket
  EOutcome fOutcome;
  unsigned short int fpmtID;
  unsigned int fTrackID;
};

#endif
