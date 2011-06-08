////////////////////////////////////////////////////////
/// Useful functions for the FitPlots
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 01/06/11 - New File
////////////////////////////////////////////////////////

#ifndef FitPlotsUtil_hh
#define FitPlotsUtil_hh

#include <TChain.h>
#include <TH1D.h>

#include <string>
#include <vector>

namespace RAT
{
namespace DS
{
  class Root;
  class PMTProperties;
}
}

void
LoadRootFile(
			 std::string lFile,
			 TChain** tree,
			 RAT::DS::Root** rDS,
			 RAT::DS::PMTProperties** rPMTList );

void
ArrangeStatBox(
               TH1D* hHistogram,
			   Int_t color,
			   Int_t number );


std::vector<std::string>
GetFitNames(
			std::string lFile );

std::string
ShortFormName(
			  std::string lFit );

#endif
