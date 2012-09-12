////////////////////////////////////////////////////////
/// Loads the FitPlot functions
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 01/06/11 - New File
////////////////////////////////////////////////////////

{
  gSystem->AddIncludePath(" -I$RATTOOLS/FitPlots");
  gROOT->ProcessLine(".L $RATTOOLS/FitPlots/FitPlotsUtil.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPlots/PlotPosition.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPlots/PlotDiffPosition.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPlots/PlotEnergy.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPlots/PlotDiffEnergy.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPlots/PlotTime.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPlots/PlotDiffTime.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPlots/PlotDirection.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPlots/PlotDiffDirection.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPlots/PlotExecutionTime.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/FitPlots/PlotValidity.cc+");
}
