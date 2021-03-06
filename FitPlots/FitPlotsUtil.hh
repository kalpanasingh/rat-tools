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
#include <TVirtualPad.h>

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
ArrangeStatBox(
               TH1D* hHistogram,
			   Int_t color,
			   TVirtualPad* pad );

std::vector<std::string>
GetFitNames( std::string lFile );

extern bool gIgnoreRetriggers;

#endif
