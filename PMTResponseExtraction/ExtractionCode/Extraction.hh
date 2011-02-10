////////////////////////////////////////////////////////
/// Shared common header file for the ExtractData function
///
/// 12/01/11 - New File
////////////////////////////////////////////////////////
#ifndef Extraction_hh
#define Extraction_hh

#include "FullDataManager.hh"

#include <vector>
using namespace std;

extern vector<FullDataManager> filesFullData;

// void
// ExtractData(
// 	    char* lpInfoFile,
// 	    bool saveData = false,
// 	    int mode = 0 ); // 0 = MC, 1 = PMTTruth, 2 = PMTCal 3 = PMTUnCal (Not in this code)

void
LoadSimulationInformation(
			  string lpInfoFile,
			  string& dataLocation,
			  vector<string>& files );

#endif
