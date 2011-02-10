////////////////////////////////////////////////////////
/// Functions of use in ExtractData, shared in RAT and SNOMAN
///
/// 29/09/10 - Checked File
////////////////////////////////////////////////////////

#include "Extraction.hh"

#include <fstream>
#include <iostream>
#include <sstream>
using namespace std;

vector<FullDataManager> filesFullData;
 
////////////////////////////////////////////////////////
/// Allow multiple root files to be analysed, hence parse a file with 
/// each root file on a different line, with the first line being the
/// path of all files. OR load a single root file.
////////////////////////////////////////////////////////
void
LoadSimulationInformation(
			  string lpInfoFile,
			  string& dataLocation,
			  vector<string>& files )
{
  const string rootStr(".root");
  const string datStr(".dat");
  const int infoFileLen = lpInfoFile.length();

  if( lpInfoFile.substr( infoFileLen - 5 ) == rootStr )
    {
      const int fullPathPos = lpInfoFile.find_last_of( '/' );
      dataLocation = lpInfoFile.substr( 0, fullPathPos + 1 );
      files.push_back( lpInfoFile.substr( fullPathPos + 1, infoFileLen - fullPathPos - 6 ) ); 
    }
  else if(lpInfoFile.substr( infoFileLen - 4 ) == datStr )
    {
      ifstream infoFile( lpInfoFile.c_str() );
      infoFile >> dataLocation;
      while( !infoFile.eof() )
	{
	  string fileName; 
	  infoFile >> fileName;
	  if( fileName[0] != '#' && fileName.size() > 1 ) // Do not parse commented lines
	    files.push_back( fileName );
	}
    }
}
