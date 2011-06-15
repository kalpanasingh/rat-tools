////////////////////////////////////////////////////////
/// Loads the FitCharacterise functions
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 13/06/11 - New File
////////////////////////////////////////////////////////

{
  gSystem->AddIncludePath(" -I$RATTOOLS/FitPerformance");
  gROOT->ProcessLine(".L $RATTOOLS/FitPerformance/FitPerformanceUtil.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPerformance/PositionPerformance.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPerformance/TimePerformance.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPerformance/EnergyPerformance.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPerformance/ExecutionTimePerformance.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPerformance/ValidityPerformance.cc+");
}
