////////////////////////////////////////////////////////
/// Abstract base class for HitData extentions
///
///
/// 14/01/11 - New File
////////////////////////////////////////////////////////
#ifndef HitData_hh
#define HitData_hh

#include <string>
using namespace std;

class HitData
{
public:
  enum EOutcome { eSignal, eAbsorbed, eReflected };

  virtual HitData*
  NewClone() = 0;

  virtual void
  Signal( 
	 const double numPE ) = 0;
  virtual void
  Reflected(
	    const double outTheta,
	    const double globalTime ) = 0;
  virtual void
  ConcHitZ(
	   const double concHitZ ) = 0;
  virtual void
  PMTHitZ(
	  const double pmtHitZ ) = 0;
  virtual bool
  Check(
	const int trackID,
	const int pmtID ) = 0;
  virtual void
  Serialise(
	    ofstream& outFile ) = 0;
  virtual void
  DeSerialise(
	      ifstream& inFile ) = 0;
  virtual string
  GetIdentifier() = 0;

  // Properties
  virtual double
  GetInTheta() = 0;
  virtual double
  GetOutTheta() = 0;
  virtual double
  GetLambda() = 0;
  virtual EOutcome
  GetOutcome() = 0;
  virtual double
  GetConcHitZ() = 0;
  virtual double
  GetPMTHitZ() = 0;
  virtual double
  GetInRadialPos() = 0;
  virtual double
  GetDeltaTime() = 0;
  virtual int 
  GetPMTID() = 0;
  virtual int 
  GetTrackID() = 0;
};

#endif
