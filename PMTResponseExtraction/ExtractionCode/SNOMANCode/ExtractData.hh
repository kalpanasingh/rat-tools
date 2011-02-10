////////////////////////////////////////////////////////
/// Extracts the raw data from the root file, and produces
/// a full filesFullData set.
///
/// 26/09/10 - New File
////////////////////////////////////////////////////////
#ifndef ExtractDataSNOMAN_hh
#define ExtractDataSNOMAN_hh

#include <vector>
using namespace std;

#include "FullDataManager.hh"

namespace RAT
{
namespace DS
{
  class MC;
  class QTree;
  class QEvent;
}
}

void
ExtractTrackData(
		 QEvent* qEV,
		 int eventID,
		 FullDataManager& fileData );
double
GetFrontFaceHitPos(
		   const TVector3 trackDir,
		   const TVector3 trackPos,
		   const TVector3 pmtDir, //This should be corrected s.t. it points towards the centre
		   const TVector3 pmtPos ); //Uncorrected position of conc front face
void
FillPMTConversionList();

int
FindNearestPMT( 
	       int panelID, 
	       TVector3 trackPos );

#endif
