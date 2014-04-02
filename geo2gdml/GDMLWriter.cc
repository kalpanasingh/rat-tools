#include <G4GDMLParser.hh>
#include <G4LogicalVolumeStore.hh>

#include <GDMLWriter.hh>

#include <RAT/Detector.hh>

#include <string>
#include <vector>
#include <iostream>
using namespace std;

void WriteGeometry( const string& fileName )
{
  // Currently the GLG4TorusStack solid, part of all PMTs is not writable by G4GDMLParser.
  // The following code removes this GLG4TorusStack from the geometry and writes the
  // remaining 'writable' geometry to a GDML file.

  /// Find any volumes that containt _envelope (PMT Volume)
  G4LogicalVolumeStore* store = G4LogicalVolumeStore::GetInstance();
  vector<G4LogicalVolume*> pmtEnvelopes;
  for( vector<G4LogicalVolume*>::iterator iTer = store->begin(); iTer != store->end(); iTer++ )
    {
      if( (*iTer)->GetName().find( "_envelope" ) != string::npos )
        pmtEnvelopes.push_back( (*iTer) );
    }
  /// Now delete the daughters of these volumes *Evil Laughter*
  for( vector<G4LogicalVolume*>::iterator iTer = pmtEnvelopes.begin(); iTer != pmtEnvelopes.end(); iTer++ )
    {
      cout << (*iTer)->GetName() << endl;
      for( int iVol = (*iTer)->GetNoDaughters() - 1; iVol >= 0; iVol-- )
        (*iTer)->RemoveDaughter( (*iTer)->GetDaughter( iVol ) );
    }
  pmtEnvelopes.clear();
  cout << "Writing" << endl;
  /// Write the remaining geometry to a GDML(XML) formatted .gdml file.
  G4GDMLParser parser;
  parser.Write( fileName, RAT::Detector::GetWorld() );
}
