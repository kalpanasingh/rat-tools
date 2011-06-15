////////////////////////////////////////////////////////
/// Plots the fit position against the mc position and 
/// expected bias.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 01/06/11 - New File
////////////////////////////////////////////////////////

#include <FitPerformanceUtil.hh>

#include <TChain.h>
#include <TFile.h>
using namespace ROOT;

#include <RAT/DS/Root.hh>
#include <RAT/DS/PMTProperties.hh>
#include <RAT/DS/EV.hh>

#include <string>
#include <sstream>
#include <iostream>
using namespace std;

////////////////////////////////////////////////////////
/// Load a chain of ROOTs file with RAT information in
/// and fill the information pointers
////////////////////////////////////////////////////////
void
LoadRootFile(
			 string lFile,
			 TChain** tree,
			 RAT::DS::Root** rDS,
			 RAT::DS::PMTProperties** rPMTList )
{
  (*tree) = new TChain( "T" );
  // Strip the .root part
  const int fileLen = lFile.length();
  stringstream fileWildCard;
  fileWildCard << lFile.substr( 0, fileLen - 5 ) << "*" << ".root";

  int numFiles = (*tree)->Add( fileWildCard.str().c_str() );
  cout << "Loaded " << numFiles << " files." << endl;

  *rDS = new RAT::DS::Root();

  (*tree)->SetBranchAddress( "ds", &(*rDS) );

  // Now the runT, only in the LAST file
  stringstream lastFile;
  if( numFiles > 1 )
    lastFile << lFile.substr( 0, fileLen - 5 ) << "_" << numFiles - 1 << ".root";
  else
    lastFile << lFile;
  cout << lastFile.str() << endl;
  TFile *file = new TFile( lastFile.str().c_str() );
  TTree *rRunTree = (TTree*)file->Get( "runT" );

  RAT::DS::Run *rRun = new RAT::DS::Run();

  rRunTree->SetBranchAddress( "run", &rRun );

  rRunTree->GetEntry();
  *rPMTList = rRun->GetPMTProp();
}

vector< std::pair< string, string> >
PositionFiles()
{
  vector< std::pair< string, string> > files;
  for( int pos = 0; pos < 7000; pos += 1000 )
	{
	  stringstream fileName;
	  fileName << "P" << pos << ".root";
	  stringstream eName;
	  eName << pos;
	  files.push_back( pair< string, string >( eName.str(), fileName.str() ) ); 
	}

  for( int pos = 5500; pos < 6000; pos += 100 )
    {
      stringstream fileName;
      fileName << "P" << pos << ".root";
      stringstream eName;
      eName << pos;
      files.push_back( pair< string, string >( eName.str(), fileName.str() ) );
    }
  return files;
}

vector< std::pair< string, string> >
EnergyFiles()
{
  vector< std::pair< string, string> > files;
  for( int energy = 10; energy < 55; energy += 5 )
    {
	  // No 4.5MeV files
	  if( energy == 45 )
		continue;
      stringstream fileName;
      fileName << "E" << energy << ".root";
      stringstream eName;
	  eName.setf( ios::fixed, ios::floatfield );
	  eName.precision( 1 );
      eName << ( energy / 10 );
      files.push_back( pair< string, string >( eName.str(), fileName.str() ) );
    }
  return files;
}
