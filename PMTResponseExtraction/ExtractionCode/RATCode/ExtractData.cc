////////////////////////////////////////////////////////
/// Extracts the raw data from the root file, and produces
/// a full filesFullData set.
///
/// 8/07/10 - New File
////////////////////////////////////////////////////////
#include <TChain.h>
#include <TFile.h>

#include <iostream>
#include <sstream>
using namespace std;

#include <RAT/DS/Root.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/MC.hh>
#include <RAT/DS/PMTProperties.hh>
#include <RAT/DS/MCTrack.hh>
#include <RAT/DS/MCTrackStep.hh>

#include "FullDataManager.hh"
#include "ExtractData.hh"
#include "Extraction.hh"

void
LoadRootFile(
	     string lFile,
	     TChain** tree,
	     RAT::DS::Root** rDS,
	     RAT::DS::PMTProperties** rPMTList );

double
invCos(
       const TVector3 a,
       const TVector3 b );

const double concA = 51.4; //mm
const double concD = 87.5; //mm

int totalNumHits;
int totalNumReflects;
int totalNumSignals;

void
ExtractData(
	    char* lpInfoFile,
	    bool saveData = false,
	    int mode = 0 ) // 0 = MC, 1 = PMTTruth, 2 = PMTCal 3 = PMTUnCal (Not in this code)
{
  filesFullData.clear();
  totalNumHits = 0;
  totalNumReflects = 0;
  totalNumSignals = 0;

  string dataLocation;
  vector<string> files;
  
  LoadSimulationInformation( lpInfoFile, dataLocation, files );
  time_t codeStart = time ( NULL );
  
  unsigned int uLoop;
  for( uLoop = 0; uLoop < files.size(); uLoop++ )
    {
      cout << files[uLoop] << endl;
      // Load the root file first
      RAT::DS::Root *rDS;
      RAT::DS::PMTProperties *rPMTList;
      TChain *tree;
      
      stringstream location;
      location << dataLocation << files[uLoop] << ".root";
      
      LoadRootFile( location.str(), &tree, &rDS, &rPMTList );

      int numMCEvents = tree->GetEntries();
      
      FullDataManager fullData;

      int iLoop2;
      for( iLoop2 = 0; iLoop2 < numMCEvents; iLoop2++ )
        {
          if( iLoop2 % 100 == 0 )
            cout << iLoop2 << " finished at " << time( NULL ) - codeStart << endl;

          tree->GetEntry( iLoop2 );
	  
	  fullData.NewEvent( iLoop2 );

	  RAT::DS::MC* rMC = rDS->GetMC();
	  ExtractTrackData( rMC, rPMTList, iLoop2, fullData );

	  ExtractSignalData( rDS, rPMTList, rMC, iLoop2, fullData, mode );
	}
      filesFullData.push_back( fullData );
      if( saveData == true )
	{
	  stringstream saveLoc;
	  saveLoc << dataLocation << files[uLoop] << ".dat";
	  fullData.Serialise( saveLoc.str().c_str() );
	}
    }   
  cout << "Absorbed: " << totalNumHits << " reflects: " << totalNumReflects << " signals: " << totalNumSignals << " hits: " << totalNumHits + totalNumReflects + totalNumSignals << endl;

}


void
ExtractTrackData(
		 RAT::DS::MC* rMC,
		 RAT::DS::PMTProperties* rPMTList,
		 int eventID,
		 FullDataManager& fileData )
{
  const string envelopeVolumeName( "innerPMT_env" ); //Equivalent to PMT envelope volume
  const string panelVolumeName( "innerPMT_panel" ); //If panel builder then this surrounds env.
  const string h2oVolumeName( "h2o" ); //If pmt builder then this surrounds env.
  const string pmtVolumeName( "innerPMT_pmt" ); //Actually the pmt
  const string concVolumeName( "innerPMT_concentrator" ); //The concentrator
  const string gdVolumeOutName( "GDOut" ); //Exiting the Grey Disc
  const int numTracks = rMC->GetMCTrackCount();

  // Loop over the tracks
  int iLoop;
  for( iLoop = 0; iLoop < numTracks; iLoop++ )
    {
      stringstream trackHist;
      bool printTrack = false;

      RAT::DS::MCTrack *rMCTrack = rMC->GetMCTrack( iLoop );
      const int trackID = rMCTrack->GetTrackID();
      trackHist << trackID << endl;;
      // Photons have pdg code 0
      if( rMCTrack->GetPDGCode() != 0 )
	continue;
      
      const int numTrackSteps = rMCTrack->GetMCTrackStepCount();

      // Loop over the track steps
      int iLoop2;
      for( iLoop2 = 0; iLoop2 < numTrackSteps; iLoop2++ )
	{
	  RAT::DS::MCTrackStep *rMCTrackStep = rMCTrack->GetMCTrackStep( iLoop2 );

	  trackHist << "\t" << rMCTrackStep->GetStartVolume() << " to " << rMCTrackStep->GetEndVolume() << endl;

	  size_t envStart = rMCTrackStep->GetStartVolume().find( envelopeVolumeName );
	  size_t panStart = rMCTrackStep->GetStartVolume().find( panelVolumeName );
	  size_t h2oStart = rMCTrackStep->GetStartVolume().find( h2oVolumeName );
	  size_t envEnd = rMCTrackStep->GetEndVolume().find( envelopeVolumeName );
	  size_t panEnd = rMCTrackStep->GetEndVolume().find( panelVolumeName );
	  size_t h2oEnd = rMCTrackStep->GetEndVolume().find( h2oVolumeName );
	  size_t gdEnd = rMCTrackStep->GetEndVolume().find( gdVolumeOutName );

	  if( ( panStart != string::npos || h2oStart != string::npos ) && envEnd != string::npos ) // Hit on a PMT
	    {
	      int pmtID = atoi( rMCTrackStep->GetEndVolume().substr( 12 ).c_str() ); // Leave only the PMT ID number
	      const TVector3 pmtDirection = rPMTList->GetDir( pmtID ).Unit();
	      const TVector3 trackDirection = rMCTrackStep->GetMom().Unit();
	      double theta = invCos( trackDirection, pmtDirection ); // NOTE - sign And Stupid PMTProperties convention
	      double lambda = 2 * 3.14 * 197.33 * 1e-6 / rMCTrackStep->GetKE(); // In nm

	      if( theta / 3.14 * 180.0 > 40 )
		printTrack = true;

	      // Not interested in trigger signals thus ignore 
	      fileData.NewHit( eventID, trackID, pmtID, theta, lambda, 
			       GetFrontFaceHitPos( trackDirection, rMCTrackStep->GetEndPos(), -pmtDirection, rPMTList->GetPos( pmtID ) ),
			       rMCTrackStep->GetGlobalTime() );
	      totalNumHits++;
	    }
	  else if( envStart != string::npos && ( panEnd != string::npos || h2oEnd != string::npos || gdEnd != string::npos ) ) // Reflected from a PMT
	    {
	      int pmtID = atoi( rMCTrackStep->GetStartVolume().substr( 12 ).c_str() ); // Leave only the PMT ID number
	      const TVector3 pmtDirection = rPMTList->GetDir( pmtID ).Unit();
	      const TVector3 trackDirection = rMCTrackStep->GetMom().Unit();
	      double theta = invCos( trackDirection, -pmtDirection ); // NOTE - sign And Stupid PMTProperties convention

	      if( trackDirection.Dot( -pmtDirection ) == 1.0 ) 
		theta = 0.0;

	      fileData.NewReflection( eventID, trackID, pmtID, theta, rMCTrackStep->GetGlobalTime() );
	      totalNumReflects++;
	    }

	  size_t pmtEnd = rMCTrackStep->GetEndVolume().find( pmtVolumeName );
	  size_t concEnd = rMCTrackStep->GetEndVolume().find( concVolumeName );
	  if( envStart != string::npos && pmtEnd != string::npos ) // Hit pmt
	    {
	      int pmtID = atoi( rMCTrackStep->GetStartVolume().substr( 12 ).c_str() );
	      const TVector3 pmtDirection = rPMTList->GetDir( pmtID ).Unit();
	      const TVector3 pmtPosition = rPMTList->GetPos( pmtID );
	      const TVector3 trackPosition = rMCTrackStep->GetEndPos();
	      const double hitPosZ = 130.0 - ( trackPosition - pmtPosition ).Dot( pmtDirection );
	      
	      fileData.NewPMTHit( eventID, trackID, pmtID, hitPosZ );
	    }
	  else if( envStart != string::npos && concEnd != string::npos ) // Hit conc
	    {
	      int pmtID = atoi( rMCTrackStep->GetStartVolume().substr( 12 ).c_str() );
	      const TVector3 pmtDirection = rPMTList->GetDir( pmtID ).Unit();
	      const TVector3 pmtPosition = rPMTList->GetPos( pmtID );
	      const TVector3 trackPosition = rMCTrackStep->GetEndPos();
	      const double hitPosZ = 130.0 - ( trackPosition - pmtPosition ).Dot( pmtDirection );

	      fileData.NewConcHit( eventID, trackID, pmtID, hitPosZ );
	    }
	}
      printTrack = false; // PHIL
      if( printTrack )
	cout << trackHist.str() << endl;
    }
}

void
ExtractSignalData(
		  RAT::DS::Root* rDS,
		  RAT::DS::PMTProperties* rPMTList,
		  RAT::DS::MC* rMC,
		  int eventID,
		  FullDataManager& fileData,
		  int mode )
{
  if( mode == 0 )
    {
      int numPMTHits = rMC->GetMCPMTCount();
      
      int iLoop;
      for( iLoop = 0; iLoop < numPMTHits; iLoop++ )
        {
          RAT::DS::MCPMT *rMCPMT = rMC->GetMCPMT( iLoop );
          int numPMTPhotons = rMCPMT->GetMCPhotonCount();
          int pmtID = rMCPMT->GetPMTID();
          
          // Not interested in trigger signals thus ignore 
          if( pmtID == 9190 )
            continue;
          
          //Loop over the photons
          int iLoop2;
          for( iLoop2 = 0; iLoop2 < numPMTPhotons; iLoop2++ )
            {
              RAT::DS::MCPhoton *rMCPhoton = rMCPMT->GetMCPhoton( iLoop2 );
              if( rMCPhoton->GetIsNoise() )
                continue;
              int trackID = rMCPhoton->GetTrackID();
              double numPE = rMCPhoton->GetCharge();
              
              fileData.NewSignal( eventID, trackID, pmtID, numPE );
              totalNumSignals++;
            }
        }
    }
}

double
GetFrontFaceHitPos(
		   const TVector3 trackDir,
		   const TVector3 trackPos,
		   const TVector3 pmtDir, //This should be corrected s.t. it points towards the centre
		   const TVector3 pmtPos ) //Uncorrected position of conc front face
{
  TVector3 corPMTPos = pmtPos; 
  const double alpha = pmtDir.Dot( corPMTPos - trackPos ) / pmtDir.Dot( trackDir );
  const TVector3 planePos = trackPos + alpha * trackDir;

  return ( planePos - pmtPos ).Mag();
}

double
invCos(
       const TVector3 a,
       const TVector3 b )
{
  double cosTheta = a.Dot( b );
  if( cosTheta >= 1.0 )
    cosTheta = 1.0;
  else if( cosTheta <= -1.0 )
    cosTheta = -1.0;
  double theta = acos( cosTheta );
  if( isnan( theta ) )
    {
      cout << "invCos nan error " << cosTheta << endl;
      theta = 0.0;
    }
  return theta;
}

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
