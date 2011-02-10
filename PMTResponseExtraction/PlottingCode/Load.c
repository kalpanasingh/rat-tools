////////////////////////////////////////////////////////
/// Loads PMT extraction functions
///
/// 12/01/11 - New File
////////////////////////////////////////////////////////

{
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/PlottingCode/CalibrationPlots/Load.c");
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/PlottingCode/ResponsePlots/Load.c");
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/PlottingCode/InfoPlots/Load.c");}
