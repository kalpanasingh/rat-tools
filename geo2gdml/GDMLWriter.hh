////////////////////////////////////////////////////////////////////
/// \class RAT::GDMLWriter
///
/// \brief  Output a GDML file containing the detector geometry
///          
/// \author R P F Stainforth <rpfs@liv.ac.uk>
///
/// REVISION HISTORY:\n
///     17 Apr 2013 : R P F Stainforth - First Revision.\n
///     2013-10-28 : P G Jones - Slight rewrite to be separate package.
///
/// \detail Output a gdml file containing the detector geometry
///         to be used by the event viewer; Snogoggles
///
////////////////////////////////////////////////////////////////////
#include <string>

void WriteGeometry( const std::string& fileName );
