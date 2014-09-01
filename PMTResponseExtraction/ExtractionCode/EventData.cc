////////////////////////////////////////////////////////
/// Contains the event data
/// HIT means a hit on the bucket, a PMTCal type hit is
/// called a signal.
///
///
/// 7/07/10 - New File
////////////////////////////////////////////////////////
#include "HitData.hh"
#include "HitDataFull.hh"
#include "HitDataMinimal.hh"
#include "EventData.hh"

#include <iostream>
using namespace std;

EventData::~EventData()
{
  unsigned int uLoop;
  for( uLoop = 0; uLoop < fpHits.size(); uLoop++ )
    {
      delete fpHits[uLoop];
    }
}

EventData::EventData(
		     const EventData& rhs )
{
  *this = rhs;
}

EventData&
EventData::operator=(
		     const EventData& rhs )
{
  if( this == &rhs )
    return *this;

  unsigned int uLoop;
  for( uLoop = 0; uLoop < rhs.fpHits.size(); uLoop++ )
    {
      fpHits.push_back( rhs.fpHits[uLoop]->NewClone() );
    }

  return *this;
}

void
EventData::NewHit(
		  const int trackID,
		  const int pmtID,
		  const double inTheta,
		  const double lambda,
		  const double inRadialPos,
		  const double globalTime,
		  const EDataSize dataSize )
{
  //cout << "HIT " << trackID << " " << pmtID << " I " << inTheta / 3.14 * 180.0 << " L " << lambda << " R " << inRadialPos << " t " << globalTime << endl;
  int iLoop;
  for( iLoop = fpHits.size() - 1; iLoop >= 0; iLoop-- )
    {
      if( fpHits[iLoop]->Check( trackID, pmtID ) && fpHits[iLoop]->GetOutcome() != HitData::eReflected ) // May have bounced out then come back, in which case is fine
	{
	  cout << "EventData::NewHit Hit already added! " << trackID << " pmt: " << pmtID << " time: " << globalTime << " prev: " << fpHits[iLoop]->GetDeltaTime() << endl;
	  return;
	}
    }
  HitData* newHit;
  if( dataSize == eFull )
    newHit = new HitDataFull( trackID, pmtID, inTheta, lambda, inRadialPos, globalTime );
  else if( dataSize == eMinimal )
    newHit = new HitDataMinimal( trackID, pmtID, inTheta, lambda, inRadialPos, globalTime );
  fpHits.push_back( newHit );
}

void
EventData::NewSignal(
		     const int trackID,
		     const int pmtID,
		     const double numPE )
{
  //cout << "SIG " << trackID << " " << pmtID << " pe " << numPE << endl;
  int iLoop;
  for( iLoop = fpHits.size() - 1; iLoop >= 0; iLoop-- )
    {
      // Check hit is in existance
      if( fpHits[iLoop]->Check( trackID, pmtID ) && fpHits[iLoop]->GetOutcome() == HitData::eAbsorbed )
	{
	  fpHits[iLoop]->Signal( numPE );
	  return;
	}
    }
  // Fail here
  cout << "EventData::NewSignal Failed to Find hit track: " << trackID << " pmt: " << pmtID << endl;
}

void
EventData::NewReflection(
			 const int trackID,
			 const int pmtID,
			 const double outTheta,
			 const double globalTime )
{
  //cout << "REF " << trackID << " " << pmtID << " O " << outTheta / 3.14 * 180.0 << endl;
  int iLoop;
  for( iLoop = fpHits.size() - 1; iLoop >= 0; iLoop-- )
    {
      if( fpHits[iLoop]->Check( trackID, pmtID ) && fpHits[iLoop]->GetOutcome() == HitData::eAbsorbed )
	{
	  fpHits[iLoop]->Reflected( outTheta, globalTime );
	  return;
	}
    }
  // Fail here
  cout << "EventData::NewReflection Failed to Find hit track: " << trackID << " pmt: " << pmtID << endl;  
}

void
EventData::NewConcHit(
		      const int trackID,
		      const int pmtID,
		      const double concHitZ )
{
  int iLoop;
  for( iLoop = fpHits.size() - 1; iLoop >= 0; iLoop-- )
    {
      if( fpHits[iLoop]->Check( trackID, pmtID ) )
	{
	  fpHits[iLoop]->ConcHitZ( concHitZ );
	  return;
	}
    }
  // Fail here
  cout << "EventData::NewConcHit Failed to Find hit track: " << trackID << " pmt: " << pmtID << endl;  
}

void
EventData::NewPMTHit(
		     const int trackID,
		     const int pmtID,
		     const double pmtHitZ )
{
  int iLoop;
  for( iLoop = fpHits.size() - 1; iLoop >= 0; iLoop-- )
    {
      if( fpHits[iLoop]->Check( trackID, pmtID ) )
	{
	  fpHits[iLoop]->PMTHitZ( pmtHitZ );
	  return;
	}
    }
  // Fail here
  cout << "EventData::NewConcHit Failed to Find hit track: " << trackID << " pmt: " << pmtID << endl;  
}

void
EventData::ProduceHitData(
			  vector<HitData*>& fullData )
{
  unsigned int uLoop;
  for( uLoop = 0; uLoop < fpHits.size(); uLoop++ )
    {
      fullData.push_back( fpHits[uLoop] );
    }
}

void
EventData::ProduceHitDataMinimal(
				 vector<HitDataMinimal>& fullData )
{
  unsigned int uLoop;
  for( uLoop = 0; uLoop < fpHits.size(); uLoop++ )
    {
      fullData.push_back( HitDataMinimal( fpHits[uLoop] ) );
    }
}

void
EventData::Serialise(
		     ofstream& outFile )
{
  outFile << fpHits.size() << endl;
  unsigned int uLoop;
  for( uLoop = 0; uLoop < fpHits.size(); uLoop++ )
    {
      outFile << fpHits[uLoop]->GetIdentifier() << " ";
      fpHits[uLoop]->Serialise( outFile );
    }
}
 
void
EventData::DeSerialise(
		       ifstream& inFile )
{
  unsigned int numHits;
  inFile >> numHits;
  fpHits.resize( numHits );
  unsigned int uLoop;
  for( uLoop = 0; uLoop < numHits; uLoop++ )
    {
      string indentifier;
      inFile >> indentifier;
      if( indentifier == HitDataFull::Identifier() )
	fpHits[uLoop] = new HitDataFull();
      else if( indentifier == HitDataMinimal::Identifier() )
        fpHits[uLoop] = new HitDataMinimal();
      fpHits[uLoop]->DeSerialise( inFile );
    }
}

void
EventData::Reduce()
{
  unsigned int uLoop;
  for( uLoop = 0; uLoop < fpHits.size(); uLoop++ )
    {
      HitData* reduced = new HitDataMinimal( fpHits[uLoop] );
      delete fpHits[uLoop];
      fpHits[uLoop] = reduced;
    }
}
