extern vector<FullDataManager> filesFullData;////////////////////////////////////////////////////////
/// Extracts the raw data from the root file, and produces
/// a full filesFullData set.
///
/// 8/07/10 - New File
////////////////////////////////////////////////////////
#ifndef ExtractData_hh
#define ExtractData_hh

#include <vector>
using namespace std;

#include "FullDataManager.hh"

namespace RAT
{
namespace DS
{
  class MC;
  class Root;
  class PMTProperties;
}
}

void
ExtractTrackData(
                 const RAT::DS::MC& rMC,
                 const int eventID,
                 FullDataManager& fileData );
void
ExtractSignalData(
                  const RAT::DS::Entry& rDS,
                  const RAT::DS::MC& rMC,
                  const int eventID,
                  FullDataManager& fileData,
                  int mode );
double
GetFrontFaceHitPos(
		   const TVector3 trackDir,
		   const TVector3 trackPos,
		   const TVector3 pmtDir, //This should be corrected s.t. it points towards the centre
		   const TVector3 pmtPos ); //Uncorrected position of conc front face


#endif
