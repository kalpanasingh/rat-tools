////////////////////////////////////////////////////////
/// Plots the fit position against the mc position and 
/// expected bias.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 01/06/11 - New File
////////////////////////////////////////////////////////

#include <FitPlotsUtil.hh>

#include <TH1D.h>
#include <TChain.h>
#include <TFile.h>
#include <TPaveStats.h>
using namespace ROOT;

#include <RAT/DS/Root.hh>
#include <RAT/DS/PMTProperties.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/FitResult.hh>

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

////////////////////////////////////////////////////////
/// Correctly arrange and tile stat boxes
////////////////////////////////////////////////////////

void
ArrangeStatBox( 
			   TH1D* hHistogram,
               Int_t color,
               Int_t number )
{
  TPaveStats *sBox = (TPaveStats*)hHistogram->GetListOfFunctions()->FindObject("stats");
  hHistogram->GetListOfFunctions()->Remove( sBox );
  hHistogram->SetStats( 0 );
  sBox->SetLineColor( color );
  sBox->SetY1NDC( sBox->GetY1NDC() - number * 0.2 );
  sBox->SetY2NDC( sBox->GetY2NDC() - number * 0.2 );
  sBox->Draw();
}

////////////////////////////////////////////////////////
/// Returns a vector of fit names in the file
////////////////////////////////////////////////////////

vector<string>
GetFitNames(
			string lFile )
{
  vector<string> fitNames;

  RAT::DS::Root* rDS;
  RAT::DS::PMTProperties* rPMTList;
  TChain* tree;

  LoadRootFile( lFile, &tree, &rDS, &rPMTList );

  tree->GetEntry( 0 );

  RAT::DS::EV* rEV = rDS->GetEV(0);
  for( map<string, RAT::DS::FitResult>::iterator iTer = rEV->GetFitResultIterBegin(); iTer != rEV->GetFitResultIterEnd(); iTer++ )
	fitNames.push_back( iTer->first );

  return fitNames;
}

void
PrintFitNames(
			  string lFile )
{
  vector<string> names;
  names = GetFitNames( lFile );
  for( unsigned int uLoop = 0; uLoop < names.size(); uLoop++ )
	{
	  cout << names[uLoop] << endl;
	}
}

////////////////////////////////////////////////////////
/// Returns a shortend form of the fit name
////////////////////////////////////////////////////////

string
ShortFormName(
			  string lFit )
{
  int colonPos = lFit.find_first_of( ":" );
  return lFit.substr( 0, colonPos );
}