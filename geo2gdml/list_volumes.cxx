#include <string>
#include <sstream>

void list_volumes( const char* geo_file ){

  // Load the ROOT geometry libraries
  gSystem->Load( "libGeom" );

  // Import the geometry file into the working session
  TGeoManager::Import( geo_file );

  // String stream for 'const char*' --> 'string' conversion
  // of the filename
  stringstream fileStrStream;
  string fileName;

  // char buffer for the output file name
  char buffer[64];
  
  // Feed the string stream the input filename
  fileStrStream << geo_file;

  // Regurgitate input filename into string
  fileStrStream >> fileName;

  // Parse the file extension off of the string
  string fN = fileName.substr(0, fileName.find_last_of("."));

  // Create the outfile name buffer
  strcpy( buffer, fN.c_str() );
  strcat( buffer, "_volume_list.txt" );
  
  // The empty file which will be filled with the output
  ofstream volList;
  volList.open( buffer );
  volList << "Volume ID" << ", Volume Name" << "\n";

  // Array of all the TGeoVolumes loaded into the session
  TObjArray* vols = gGeoManager->GetListOfUVolumes();

  // Loop over all volumes and write their ID's and names
  // to the output file
  for (int k=0; k < vols->GetEntries(); k++){

    // Obtain the k-th volume pointer name
    char* volpName = gGeoManager->GetVolume(k)->GetPointerName();

    // Parse the pointer name into just the volume name
    stringstream pName;
    pName << volpName;
    string volName;
    pName >> volName;
    string vN = volName.substr(1, volName.find_first_of("_") -1);

    // Write the volume and ID and name to file
    volList << k << ", " << vN.c_str() << "\n";
  }
  
  // Close the file
  volList.close();   
}
