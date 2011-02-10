////////////////////////////////////////////////////////
/// Merges two or more FullDataManager files
///
/// 27/09/10 - New File
////////////////////////////////////////////////////////

#include <iostream>
#include <vector>
#include <string>
using namespace std;

#include "FullDataManager.hh"

void
MergeFiles(
          vector<char*> inFiles,
          char* lpOutFile );

void
MergeFiles(
	  vector<string> inFiles,
	  string outFile );

void
MergeFiles(
	  char* lpInFile1,
	  char* lpInFile2,
	  char* lpOutFile )
{
  vector<char*> inFiles; inFiles.push_back( lpInFile1 ); inFiles.push_back( lpInFile2 );
  MergeFiles( inFiles, lpOutFile );
}

void
MergeFiles(
	  vector<char*> inFiles,
	  char* lpOutFile )
{
  cout << "Merging" << endl;
  if( inFiles.size() < 2 )
    cout << "More files needed to merge" << endl;

  FullDataManager fullMerged;
  fullMerged.DeSerialise( inFiles[0] );  

  unsigned int uLoop;
  for( uLoop = 1; uLoop < inFiles.size(); uLoop++ )
    {
      cout << inFiles[uLoop] << " ";
      FullDataManager newFile;
      newFile.DeSerialise( inFiles[uLoop] );
      fullMerged.Append( newFile );
    }
  fullMerged.Serialise( lpOutFile );
  cout << "to " << lpOutFile << " Finished Merge" << endl;
}

void
MergeFiles(
          vector<string> inFiles,
          string outFile )
{
  cout << "Merging" << endl;
  if( inFiles.size() < 2 )
    cout << "More files needed to merge" << endl;

  FullDataManager fullMerged;
  fullMerged.DeSerialise( inFiles[0].c_str() );

  unsigned int uLoop;
  for( uLoop = 1; uLoop < inFiles.size(); uLoop++ )
    {
      cout << inFiles[uLoop] << " ";
      FullDataManager newFile;
      newFile.DeSerialise( inFiles[uLoop].c_str() );
      fullMerged.Append( newFile );
    }
  fullMerged.Serialise( outFile.c_str() );
  cout << "to " << outFile << " Finished Merge" << endl;
}
