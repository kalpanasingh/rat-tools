////////////////////////////////////////////////////////////////////////
/// \file Geo2GDML
///
/// \brief   Entry point to the geo2gdml code
///
/// \author  Phil Jones <p.g.jones@qmul.ac.uk>
///
/// REVISION HISTORY:\n
///     2013-10-28 : P.Jones - First Revision, new file. \n
///
/// \detail  The main function is defined here.
///
////////////////////////////////////////////////////////////////////////

#include <GDMLWriter.hh>

#include <G4RunManager.hh>
#include <G4VUserPrimaryGeneratorAction.hh>
#include <G4GDMLParser.hh>

#include <RAT/Detector.hh>
#include <RAT/PhysicsList.hh>
#include <RAT/DB.hh>
#include <RAT/Log.hh>

#include <string>
#include <iostream>
#include <fstream>

using namespace std;

class User : public G4VUserPrimaryGeneratorAction
{
public:
  virtual void GeneratePrimaries(G4Event* anEvent) { } 
};

int main( int argc, char *argv[] )
{
  if( argc != 3 )
    {
      cout << "Correct usage is geo2gdml input_file.geo output_file.gdml" << endl;
      exit(0);
    }
  // Check that the .geo file exists
  ifstream geoFile( argv[1] );
  if ( !geoFile ){ 
    cout << "The file " << argv[1] << " does not exist. Check and try again." << endl; 
    exit(0);
  }
  geoFile.close();

  RAT::Log::Init( "/dev/null", RAT::Log::INFO, RAT::Log::INFO );
 
  RAT::DB* db = RAT::DB::Get();
  assert(db);
 
  const string data = getenv( "GLG4DATA" );
  assert(data != "");
  db->LoadDefaults();
  cout << "Loading geo " << argv[1] << endl;
  db->SetS( "DETECTOR", "geo_file", argv[1] );
  db->Load( data + "/snoman/MATERIALS.ratdb" );
  db->Load( data + "/snoman/OPTICS.ratdb" );

  G4RunManager* runManager = new G4RunManager;
  runManager->SetUserInitialization( new RAT::Detector() );
  runManager->SetUserInitialization( new RAT::PhysicsList() );
  runManager->SetUserAction( new User() );
  // initialize G4 kernel
  runManager->Initialize();

  cout << "Writing to " << argv[2] << endl;
  WriteGeometry( argv[2] );

  delete runManager;
}
