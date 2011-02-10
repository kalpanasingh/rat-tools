////////////////////////////////////////////////////////
/// Reduces the size of a file
///
/// 09/02/11 - New File
////////////////////////////////////////////////////////

#include <iostream>
#include <vector>
#include <string>
using namespace std;

#include "FullDataManager.hh"

void
MergeFiles(
	   char* lpFile )
{
  cout << "This is untested" << endl;
  FullDataManager full;
  full.DeSerialise( lpFile );  
  full.Reduce();
  full.Serialise( lpFile );
  cout << "Finished" << endl;
}
