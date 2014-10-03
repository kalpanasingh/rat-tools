////////////////////////////////////////////////////////
/// Useful functions for the FitPerformance
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 12/06/11 - New File
////////////////////////////////////////////////////////

#ifndef FitPerformanceUtil_hh
#define FitPerformanceUtil_hh

#include <TChain.h>

#include <string>
#include <vector>
#include <utility>

namespace RAT
{
namespace DS
{
  class Root;
  class PMTProperties;
}
}

vector< std::pair< string, string> >
PositionFiles();

vector< std::pair< string, string> >
EnergyFiles();

#endif
