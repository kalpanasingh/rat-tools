////////////////////////////////////////////////////////
/// Useful functions to plot fit position against the mc 
/// position and expected bias.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 01/06/11 - New File
////////////////////////////////////////////////////////

#ifndef PlotPosition_hh
#define PlotPosition_hh

#include <TCanvas.h>

#include <string>
#include <vector>

TCanvas*
PlotPosition(
			 std::string file,
			 std::vector<std::string> fits );

#endif
