////////////////////////////////////////////////////////
/// Plots the fit position against the mc position and 
/// expected bias.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 01/06/11 - New File
////////////////////////////////////////////////////////

#include <FitPerformanceUtil.hh>

using namespace ROOT;

#include <string>
#include <sstream>
#include <iostream>
using namespace std;

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
